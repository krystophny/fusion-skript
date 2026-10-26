#!/usr/bin/env python3
"""Stage registered animations into the site and build their player pages.

site/media receives animations.json, the posters and each registered MP4 at
exactly its mp4_sha256 revision (local render cache first, else the hosted
stream_url), so the presenter can stage it offline. A registered animation
needs no script chapter: its record names the Manim scene source that
scripts/render-animations.sh renders, a title and a caption, and its stable
page site/animations/<slug>.html shows the full-window video with that caption.
"""
import hashlib
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
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


def rendered_slugs():
    """Slugs that scripts/render-animations.sh renders from repository scenes."""
    result = subprocess.run(["bash", str(ROOT / "scripts/render-animations.sh"), "--slugs"],
                            capture_output=True, text=True, check=True)
    return set(result.stdout.split())


def check_provenance(slug, record, scenes):
    for key in ("source", "title", "caption", "description", "poster", "mp4_sha256", "stream_url"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError(f"Registered animation {slug} lacks {key}")
    if slug not in scenes or not (ROOT / record["source"]).is_file():
        raise ValueError("Registered animation has no repository scene: " + slug)


def player_page(slug, record):
    e = html.escape
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(record["title"])} — Fusion Physics animation</title>
<link rel="stylesheet" href="../animation-player.css"></head>
<body class="animation-presentation"><main><figure style="margin:0">
<div class="animation-player"><video class="animation-video" aria-label="{e(record["description"])}" controls loop muted playsinline preload="metadata" src="{e(record["stream_url"])}" poster="../media/{slug}.png" width="960">{e(record["description"])}</video><div class="animation-controls" hidden><input type="range" class="animation-seek" min="0" max="100" step="0.1" value="0" aria-label="Animation position"> <button type="button" class="animation-fullscreen" aria-label="Full screen"></button></div><p class="animation-status" role="status"></p></div><div class="animation-information"><h1>{e(record["title"])}</h1><figcaption>{e(record["caption"])}</figcaption>
<p><a href="../present/">Lecture slides</a> · Original animation: Christopher Albert, CC BY 4.0.</p></div>
</figure></main><script defer src="../animation-player.js"></script></body></html>
'''


def prepare(site):
    media = site / "media"
    media.mkdir(parents=True, exist_ok=True)
    register = ROOT / "media/animations.json"
    shutil.copyfile(register, media / "animations.json")
    records = json.loads(register.read_text())["animations"]
    scenes = rendered_slugs()
    for slug, record in records.items():
        check_provenance(slug, record, scenes)
        shutil.copyfile(ROOT / record["poster"], media / (slug + ".png"))
        stage_video(slug, record, media)
    players = site / "animations"
    players.mkdir(exist_ok=True)
    for name in ("animation-player.js", "animation-player.css"):
        shutil.copyfile(ROOT / "src" / name, site / name)
    for slug, record in records.items():
        (players / (slug + ".html")).write_text(player_page(slug, record))
    print("Animation pages:", len(records))


if __name__ == "__main__":
    prepare(Path(sys.argv[1]))
