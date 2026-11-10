#!/usr/bin/env python3
"""Screenshot each built slide widget (notebooks/slide-<name>.html) at its
initial slider values as the PDF poster media/posters/slide-<name>.png.

Usage: python3 scripts/render-widget-posters.py [<rendered-notebooks-dir>] [--only NAME ...]
       (default public/notebooks; build first with make -j site)
Requires Playwright's Python package and Chromium.
The frame has the aspect of the deck's widget area, 257 mm x 150 mm.
"""
import argparse
import shutil
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 970, round(970 * 150 / 257)


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rendered", type=Path, nargs="?", default=ROOT / "public/notebooks")
    parser.add_argument("--chrome", default=shutil.which("chromium"), help="Chromium executable")
    parser.add_argument("--only", nargs="+", metavar="NAME", help="widget names without slide- (default: all)")
    args = parser.parse_args()
    # Observable JS does not start from file:// URLs.
    handler = partial(Quiet, directory=str(args.rendered.resolve()))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    names = sorted(p.stem for p in (ROOT / "notebooks").glob("slide-*.html")
                   if not args.only or p.stem.removeprefix("slide-") in args.only)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=args.chrome, headless=True,
                                              args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=3)
        for name in names:
            page.goto(f"http://127.0.0.1:{server.server_port}/{name}.html")
            page.wait_for_selector("svg[class^=plot], canvas", timeout=60000)
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready")
            # Simulations run on: give their running averages time to settle.
            page.wait_for_timeout(20000)
            out = ROOT / "media/posters" / f"{name}.png"
            page.screenshot(path=str(out))
            print(f"Poster written: {out.relative_to(ROOT)}")
        browser.close()
    server.shutdown()


if __name__ == "__main__":
    main()
