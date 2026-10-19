#!/usr/bin/env python3
"""Stage registered animations into the site and build their player pages.

site/media receives animations.json, the posters and each registered MP4 at
exactly its mp4_sha256 revision (local render cache first, else the hosted
stream_url), so the presenter can stage it offline. Every registered animation
needs a captioned Skript figure (theme `animation`); its stable page
site/animations/<slug>.html shows the full-window video with that caption.
"""
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def stage_video(slug, record, media):
    """Copy or download the registered revision; refuse any other bytes."""
    expected = record["mp4_sha256"]
    target = media / (slug + ".mp4")
    cache = Path(os.environ.get("MEDIA_DIR", ROOT / ".cache/animations"))
    for path in (target, cache / (slug + ".mp4"), ROOT / ".cache/present-media" / (expected + ".mp4")):
        if path.is_file() and sha(path) == expected:
            if path.resolve() != target.resolve():
                shutil.copyfile(path, target)
            return
    saved = ROOT / ".cache/present-media" / (expected + ".mp4")
    saved.parent.mkdir(parents=True, exist_ok=True)
    temp = saved.with_suffix(".part")
    print("Downloading registered animation:", slug, flush=True)
    with urlopen(record["stream_url"], timeout=120) as source, temp.open("wb") as out:
        shutil.copyfileobj(source, out)
    if sha(temp) != expected:
        temp.unlink()
        raise ValueError("Checksum mismatch for registered animation: " + slug)
    temp.replace(saved)
    shutil.copyfile(saved, target)


def player_markup(figure):
    start = figure.index('<div class="animation-player">')
    depth = 0
    for tag in re.finditer(r'</?div\b[^>]*>', figure[start:]):
        depth += -1 if tag.group(0).startswith('</') else 1
        if depth == 0:
            return figure[start:start + tag.end()]
    raise ValueError("Unclosed animation player")


def prepare(site):
    media = site / "media"
    media.mkdir(parents=True, exist_ok=True)
    register = ROOT / "media/animations.json"
    shutil.copyfile(register, media / "animations.json")
    records = json.loads(register.read_text())["animations"]
    for slug, record in records.items():
        shutil.copyfile(ROOT / record["poster"], media / (slug + ".png"))
        stage_video(slug, record, media)
    players = site / "animations"
    players.mkdir(exist_ok=True)
    for name in ("animation-player.js", "animation-player.css"):
        shutil.copyfile(ROOT / "src" / name, site / name)
    by_source = {urlsplit(r["stream_url"]).path: slug for slug, r in records.items()}
    found = {}
    for page in sorted(site.rglob("*.html")):
        if page.parent == players:
            continue
        content = page.read_text()
        figures = re.findall(r'<figure\b[^>]*class="animation-figure"[^>]*>.*?</figure>', content, re.S)
        for figure in figures:
            source = re.search(r'<video\b[^>]*src="([^"]+)"', figure)
            if source:
                slug = by_source[urlsplit(html.unescape(source.group(1))).path]
                found[slug] = (figure, page.relative_to(site).as_posix())
        if figures and "animation-player.js" not in content:
            prefix = "../" * (len(page.relative_to(site).parts) - 1)
            content = content.replace("</head>", f'<link rel="stylesheet" href="{prefix}animation-player.css">\n</head>', 1)
            content = content.replace("</body>", f'<script defer src="{prefix}animation-player.js"></script>\n</body>', 1)
            page.write_text(content)
    missing = sorted(set(records) - set(found))
    if missing:
        raise ValueError("No captioned Skript animation figure for: " + ", ".join(missing))
    for slug, (figure, chapter) in found.items():
        video = player_markup(figure)
        caption = re.search(r'<figcaption\b[^>]*>.*?</figcaption>', figure, re.S).group(0)
        title = slug.replace("-", " ").capitalize()
        (players / (slug + ".html")).write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — Fusion Physics animation</title>
<link rel="stylesheet" href="../animation-player.css"></head>
<body class="animation-presentation"><main><figure style="margin:0">
{video}<div class="animation-information"><h1>{html.escape(title)}</h1>{caption}
<p><a href="../{chapter}">Return to the Skript chapter</a> · Original animation: Christopher Albert, CC BY 4.0.</p></div>
</figure></main><script defer src="../animation-player.js"></script></body></html>
''')
    print("Animation pages:", len(found))


if __name__ == "__main__":
    prepare(Path(sys.argv[1]))
