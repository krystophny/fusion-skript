#!/usr/bin/env python3
"""Open the rendered notebooks in headless Chromium and check that every OJS cell runs.

Requires Playwright's Python package and Chromium; an optional local gate like
check-present-browser.py. Each page must load without console errors or OJS
error cells and must show its reference numbers. Full-page screenshots are
written below .cache/notebook-review/.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import sys
import tempfile
from threading import Thread

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[1]
EXPECT = {
    "reactivity": ["1.136 × 10-22", "30.9 keV", "40.6 keV", "13.5 keV"],
    "lawson": ["2.743 × 1021 keV s m⁻³ at 13.5 keV", "2.915 × 1021 keV s m⁻³ at 14.2 keV"],
    "impurities": ["0.926", "0.857", "6.40"],
    "scaling": ["3.57 s", "3.60", "0.77", "0.61"],
}


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main():
    shots = REPO / ".cache/notebook-review"
    shots.mkdir(parents=True, exist_ok=True)
    failures = []
    with tempfile.TemporaryDirectory(prefix="fusion-notebooks-") as tmp:
        (Path(tmp) / "fusion-skript").symlink_to(REPO / "public", target_is_directory=True)
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=tmp))
        Thread(target=server.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{server.server_port}/fusion-skript/notebooks/"
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(executable_path=shutil.which("chromium"),
                                            headless=True, args=["--no-sandbox"])
                for name, needles in EXPECT.items():
                    if not (REPO / f"public/notebooks/{name}.html").is_file():
                        print(f"{name}: FAIL; not rendered")
                        failures.append(name)
                        continue
                    page = browser.new_page(viewport={"width": 1100, "height": 900})
                    errors = []
                    page.on("console", lambda m, e=errors: e.append(m.text)
                            if m.type == "error" and not m.text.startswith("Failed to load resource") else None)
                    page.on("pageerror", lambda exc, e=errors: e.append(str(exc)))
                    page.on("response", lambda r, e=errors: e.append(f"HTTP {r.status} {r.url}")
                            if r.status >= 400 else None)
                    page.goto(base + name + ".html", wait_until="networkidle")
                    page.wait_for_timeout(2500)
                    bad = page.locator(".observablehq--error").count()
                    text = page.inner_text("main")
                    missing = [n for n in needles if n not in text]
                    page.screenshot(path=str(shots / f"{name}.png"), full_page=True)
                    status = "ok" if not (errors or bad or missing) else "FAIL"
                    print(f"{name}: {status}; console errors {len(errors)}, OJS error cells {bad}, "
                          f"missing {missing}")
                    for e in errors[:5]:
                        print("   ", e[:300])
                    if status != "ok":
                        failures.append(name)
                    page.close()
                browser.close()
        finally:
            server.shutdown()
    print("screenshots:", shots)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
