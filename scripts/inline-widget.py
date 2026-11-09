#!/usr/bin/env python3
"""Make a slide widget (notebooks/slide-*.html) one self-contained file.

Relative references in quotes ("./x.js", "./data/y.json") inside module
scripts, linked stylesheets and CSS url() become data: URLs, recursively for
imported JavaScript and CSS, so the page runs offline in the presenter and in
Slopshell's sandboxed widget frame. Only files inside the repository are
inlined; other references are left unchanged. Slopshell does the same when it
serves an .html widget.
"""
import base64
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIME = {".js": "text/javascript", ".mjs": "text/javascript", ".json": "application/json",
        ".csv": "text/csv", ".css": "text/css", ".otf": "font/otf", ".ttf": "font/ttf",
        ".woff": "font/woff", ".woff2": "font/woff2", ".svg": "image/svg+xml",
        ".png": "image/png", ".jpg": "image/jpeg", ".txt": "text/plain"}
QUOTED = re.compile(r"""(["'])(\.\.?/[^"'\s]+)\1""")
CSS_URL = re.compile(r"""url\((["']?)([^"')]+)\1\)""")
LINK = re.compile(r"""<link\s+rel=["']stylesheet["']\s+href=["']([^"']+)["']\s*/?>""")
SCRIPT = re.compile(r"""(<script\s+type=["']module["']>)(.*?)(</script>)""", re.S)


def target(base, ref):
    path = (base / ref).resolve()
    if ROOT not in path.parents or not path.is_file() or path.suffix not in MIME:
        return None
    return path


def data_url(path):
    if path.suffix in (".js", ".mjs"):
        body = js(path.read_text(), path.parent).encode()
    elif path.suffix == ".css":
        body = css(path.read_text(), path.parent).encode()
    else:
        body = path.read_bytes()
    return f"data:{MIME[path.suffix]};base64,{base64.b64encode(body).decode()}"


def js(text, base):
    def swap(m):
        path = target(base, m.group(2))
        return m.group(0) if path is None else f'{m.group(1)}{data_url(path)}{m.group(1)}'
    return QUOTED.sub(swap, text)


def css(text, base):
    def swap(m):
        if m.group(2).startswith(("data:", "http:", "https:")):
            return m.group(0)
        path = target(base, m.group(2))
        return m.group(0) if path is None else f'url("{data_url(path)}")'
    return CSS_URL.sub(swap, text)


def inline(page):
    text, base = page.read_text(), page.parent

    def link(m):
        path = target(base, m.group(1))
        return m.group(0) if path is None else f"<style>\n{css(path.read_text(), path.parent)}</style>"
    text = LINK.sub(link, text)
    return SCRIPT.sub(lambda m: m.group(1) + js(m.group(2), base) + m.group(3), text)


if __name__ == "__main__":
    source, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(inline(source))
