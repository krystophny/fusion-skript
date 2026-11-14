#!/usr/bin/env python3
"""Open the disruption widget in headless Chromium and check that MILCA runs.

Like check-notebooks-browser.py an optional local gate. The page must load
without console errors, run the WebAssembly model for every device and
scenario, report a disruption for the default density ramp and animate the
cross-section. Screenshots go below .cache/notebook-review/.
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


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main():
    shots = REPO / ".cache/notebook-review"
    shots.mkdir(parents=True, exist_ok=True)
    errors = []
    with tempfile.TemporaryDirectory(prefix="fusion-disruption-") as tmp:
        (Path(tmp) / "fusion-skript").symlink_to(REPO / "public", target_is_directory=True)
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=tmp))
        Thread(target=server.serve_forever, daemon=True).start()
        url = f"http://127.0.0.1:{server.server_port}/fusion-skript/notebooks/slide-disruption.html"
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(executable_path=shutil.which("chromium"),
                                            headless=True, args=["--no-sandbox"])
                page = browser.new_page(viewport={"width": 1280, "height": 905})
                page.on("console", lambda m: m.type == "error" and errors.append(m.text))
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto(url)
                page.wait_for_function("document.querySelector(\"#status\").textContent.includes(\"disruption\")", timeout=60000)
                status = page.inner_text("#status")
                print("default:", " ".join(status.split()))
                if "radiative" not in status and "ballooning" not in status and "islands" not in status:
                    errors.append(f"default density ramp: unexpected cause: {status}")
                page.wait_for_timeout(1500)
                page.screenshot(path=str(shots / "slide-disruption-early.png"))
                last = page.evaluate("+document.querySelector(\"#scrub\").max")
                for frac, tag in [(0.55, "quench"), (0.8, "current-quench")]:
                    page.evaluate(f"(() => {{ const s = document.querySelector(\"#scrub\"); s.value = Math.round({frac} * {last}); s.dispatchEvent(new Event(\"input\")); }})()")
                    page.wait_for_timeout(300)
                    page.screenshot(path=str(shots / f"slide-disruption-{tag}.png"))
                for device in ["ITER", "JET", "ASDEX Upgrade", "SPARC"]:
                    for scenario in ["density ramp", "heating ramp", "current ramp"]:
                        page.select_option("form:has-text(\"device\") select", device)
                        page.select_option("form:has-text(\"scenario\") select", scenario)
                        page.wait_for_timeout(250)
                        page.wait_for_function("!document.querySelector(\"#status\").textContent.includes(\"outside\")", timeout=30000)
                        page.wait_for_timeout(1200)
                        s = " ".join(page.inner_text("#status").split())
                        print(f"{device} / {scenario}: " + s[s.find("ramp:"):][:220])
                page.screenshot(path=str(shots / "slide-disruption-last.png"))
                browser.close()
        finally:
            server.shutdown()
    for e in errors:
        print("ERROR:", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
