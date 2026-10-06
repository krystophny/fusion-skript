#!/usr/bin/env python3
"""Build the unchanged Plasma presenter UI for any Typst course.

Numbered slides/*.typ become present/<stem>/ SVG pages and manifest.json.
Every page should contain one <present-page> metadata dictionary; missing
metadata is a local static/light fallback, rejected with --strict-metadata.
All page/PDF/media URLs carry a SHA-256 revision (?v=...). Media must already
exist locally in public/; no remote downloads are made. decks.json owns the
course/author. The web manifest and service-worker cache are course-specific.
"""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import quote, unquote, urlsplit
import xml.etree.ElementTree as ET


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def revision(path, relative):
    return quote(relative, safe="/.-_") + "?v=" + digest(path)


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def command(root, operation, *args):
    cmd = ["typst", operation, "--root", str(root), "--ignore-system-fonts"]
    if (root / "fonts").is_dir():
        cmd += ["--font-path", str(root / "fonts")]
    return subprocess.check_output(cmd + list(args), text=True)


def stage_media(value, metadata, site, deck):
    """Copy a local staged file, including local equivalents of slug URLs."""
    url = urlsplit(value)
    if url.scheme or url.netloc:
        slug = metadata.get("slug")
        if not slug or not re.fullmatch(r"[\w-]+", slug):
            raise ValueError("Remote media requires a local registered slug: " + value)
        source = site / "media" / (slug + Path(url.path).suffix)
    else:
        source = site / unquote(url.path).lstrip("/")
    source = source.resolve()
    if not source.is_relative_to(site.resolve()) or not source.is_file():
        raise ValueError("Media must exist inside the site directory: " + value)
    name = digest(source) + source.suffix.lower()
    dest = deck / "media" / name
    dest.parent.mkdir(exist_ok=True)
    shutil.copyfile(source, dest)
    return revision(dest, "media/" + name)


def build(args):
    root = args.root.resolve()
    site = (args.site_dir or root / "public").resolve()
    site.mkdir(parents=True, exist_ok=True)
    templates = root / "src/present"
    outline = json.loads((root / "slides/build/script-outline.json").read_text())
    sources = sorted(p for p in (root / "slides").glob("*.typ")
                     if re.match(r"^\d+-", p.stem))
    if not sources:
        raise ValueError("No numbered lecture decks found")
    prefix = re.sub(r"[^a-z0-9]+", "-", args.course.lower()).strip("-")
    if not prefix:
        raise ValueError("Course name needs at least one letter or digit")
    replacements = {"__COURSE__": args.course, "__COURSE_SHORT__": args.short_name,
                    "__AUTHOR__": args.author, "__CACHE_PREFIX__": prefix}
    with tempfile.TemporaryDirectory(prefix=".present-", dir=site) as tmp:
        output = Path(tmp) / "present"
        shutil.copytree(templates, output)
        for name in ("index.html", "deck.html"):
            text = (output / name).read_text()
            for key, value in replacements.items():
                text = text.replace(key, html.escape(value, quote=True))
            (output / name).write_text(text)
        sw = (output / "sw.js").read_text().replace("__CACHE_PREFIX__", prefix)
        (output / "sw.js").write_text(sw)
        manifest = json.loads((output / "manifest.webmanifest").read_text())
        manifest.update(name=args.course, short_name=args.short_name)
        write_json(output / "manifest.webmanifest", manifest)
        decks = []
        for source in sources:
            stem = source.stem
            chapter = int(stem.split("-", 1)[0])
            info = next((c for c in outline["chapters"] if c["number"] == chapter), None)
            if info is None:
                raise ValueError("Deck has no corresponding script chapter: " + stem)
            deck = output / stem
            deck.mkdir()
            shutil.copyfile(output / "deck.html", deck / "index.html")
            command(root, "compile", "--format", "svg", str(source), str(deck / "page-{0p}.svg"))
            records = json.loads(command(root, "eval", "--in", str(source),
                "query(<present-page>).map(m => (page: m.location().page(), value: m.value))"))
            files = sorted(deck.glob("page-*.svg"), key=lambda p: int(p.stem.split("-")[-1]))
            if not files:
                raise ValueError("No SVG pages produced: " + stem)
            per_page = {}
            for record in records:
                number = record["page"]
                if number in per_page or not 1 <= number <= len(files):
                    raise ValueError("Duplicate or out-of-range page metadata: " + stem)
                per_page[number] = record["value"]
            missing = sorted(set(range(1, len(files) + 1)) - set(per_page))
            if missing:
                message = f"{stem}: metadata missing on {len(missing)}/{len(files)} pages"
                if args.strict_metadata:
                    raise ValueError(message)
                print("WARNING: " + message + "; static/light fallback until designer integration")
            pages = []
            for number, svg in enumerate(files, 1):
                meta = per_page.get(number, {"kind": "static", "background": "light"})
                if meta.get("kind") not in ("static", "animation"):
                    raise ValueError("Unknown page kind")
                if meta.get("background") not in ("light", "dark"):
                    raise ValueError("Unknown page background")
                page = {"src": revision(svg, svg.name), "kind": meta["kind"],
                        "background": meta["background"]}
                if page["kind"] == "animation":
                    if not isinstance(meta.get("video"), str):
                        raise ValueError("Animation page needs a video")
                    page["video"] = stage_media(meta["video"], meta, site, deck)
                    page["poster"] = (stage_media(meta["poster"], meta, site, deck)
                                      if meta.get("poster") else page["src"])
                    page["loop"] = meta.get("loop", True)
                pages.append(page)
            pdf = site / "slides" / (stem + ".pdf")
            shutil.copyfile(pdf, deck / "deck.pdf")
            svg_root = ET.parse(files[0]).getroot()
            width = float(svg_root.attrib["width"].removesuffix("pt"))
            height = float(svg_root.attrib["height"].removesuffix("pt"))
            data = {"stem": stem, "chapter": chapter, "title": info["title"],
                    "course": args.course, "author": args.author, "aspect": width / height,
                    "pdf": revision(deck / "deck.pdf", "deck.pdf"), "pages": pages}
            write_json(deck / "manifest.json", data)
            decks.append({"stem": stem, "chapter": chapter, "title": info["title"],
                          "pages": len(pages), "cover": stem + "/" + pages[0]["src"]})
        write_json(output / "decks.json", {"course": args.course, "author": args.author, "decks": decks})
        (output / "deck.html").unlink()
        target = site / "present"
        backup = Path(tmp) / "previous"
        if target.exists():
            os.replace(target, backup)
        try:
            os.replace(output, target)
        except BaseException:
            if backup.exists():
                os.replace(backup, target)
            raise
        print(f"Presenter: {len(decks)} deck(s), {sum(d['pages'] for d in decks)} SVG pages → {target}")


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--site-dir", type=Path)
    p.add_argument("--course", required=True)
    p.add_argument("--short-name", required=True)
    p.add_argument("--author", default="Christopher Albert")
    p.add_argument("--strict-metadata", action="store_true")
    return p


if __name__ == "__main__":
    build(parser().parse_args())
