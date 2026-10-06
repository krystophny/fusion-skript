#!/usr/bin/env python3
"""Inspect the generated presenter in Chromium at the Pages repository prefix.

Requires Playwright's Python package, Chromium and Pillow. This is an optional
local browser gate, separate from pytest and CI's portable behavioral tests.
Screenshots and a contact sheet are written below .cache/present-review/.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import tempfile
from threading import Thread

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[1]


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def run():
    shots = REPO / ".cache/present-review"
    shots.mkdir(parents=True, exist_ok=True)
    decks = json.loads((REPO / "public/present/decks.json").read_text())["decks"]
    with tempfile.TemporaryDirectory(prefix="fusion-browser-") as tmp:
        (Path(tmp) / "fusion-skript").symlink_to(REPO / "public", target_is_directory=True)
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=tmp))
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}/fusion-skript/"
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(executable_path=shutil.which("chromium"),
                                             headless=True, args=["--no-sandbox"])
                context = browser.new_context(viewport={"width": 1188, "height": 840})
                page = context.new_page()
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(base)
                page.wait_for_selector("main")
                page.screenshot(path=str(shots / "site.png"), full_page=True)
                page.goto(base + "chapters/00-energy-context.html")
                page.wait_for_selector("main")
                page.screenshot(path=str(shots / "chapter.png"), full_page=True)
                page.goto(base + "present/")
                page.wait_for_selector(".decks li a")
                assert page.locator("h1").inner_text() == "Fusion Physics"
                page.evaluate("navigator.serviceWorker.ready")
                page.wait_for_function("navigator.serviceWorker.controller !== null")
                page.screenshot(path=str(shots / "launcher.png"))
                images = []
                for deck in decks:
                    page.goto(base + "present/" + deck["stem"] + "/")
                    page.wait_for_selector(".frame section")
                    assert page.locator(".frame section").count() == deck["pages"]
                    page.wait_for_function("navigator.serviceWorker.controller !== null")
                    for number in range(1, deck["pages"] + 1):
                        page.goto(base + "present/" + deck["stem"] + "/#" + str(number))
                        page.wait_for_function("n => document.querySelector('.where').textContent.startsWith(n + ' /')", arg=number)
                        current = page.locator(".frame section.current")
                        current.locator("img").wait_for()
                        page.wait_for_function("() => [...document.querySelectorAll('.frame section.current img')].every(i => i.complete && i.naturalWidth > 0)")
                        filename = shots / f"{deck['stem']}-{number:02}.png"
                        page.screenshot(path=str(filename))
                        images.append(filename)
                    page.keyboard.press("Home")
                    page.keyboard.press("ArrowRight")
                    assert page.locator(".where").inner_text().startswith("2 /")
                    # Pencil event must light the laser without navigating.
                    page.locator(".stage").evaluate('''el => {
                      for (const type of ["pointerdown", "pointerup"])
                        el.dispatchEvent(new PointerEvent(type, {
                          pointerType: "pen", pointerId: 7, clientX: 950,
                          clientY: 400, bubbles: true, pressure: 0.5}));
                    }''')
                    assert page.locator(".where").inner_text().startswith("2 /")
                    page.keyboard.press("g")
                    assert page.locator("html").get_attribute("class").find("overview-on") >= 0
                    page.screenshot(path=str(shots / "overview.png"))
                    page.keyboard.press("Escape")
                    # Complete the explicit offline download, then reload offline.
                    page.locator('[data-act="offline"]').click(force=True)
                    page.wait_for_function("document.querySelector('.status').textContent === 'Deck available offline'")
                    context.set_offline(True)
                    page.reload()
                    page.wait_for_selector(".frame section.current img")
                    page.keyboard.press("End")
                    assert page.locator(".where").inner_text().startswith(str(deck["pages"]) + " /")
                    page.goto(base + "present/")
                    page.wait_for_selector(".decks li a")
                    assert page.locator("h1").inner_text() == "Fusion Physics"
                    context.set_offline(False)
                assert not errors, errors
                browser.close()
            contact = Image.new("RGB", (4 * 297, ((len(images) + 3) // 4) * 230), "#ddd")
            draw = ImageDraw.Draw(contact)
            for index, path in enumerate(images):
                thumb = Image.open(path).convert("RGB")
                thumb.thumbnail((297, 210))
                x, y = (index % 4) * 297, (index // 4) * 230
                contact.paste(thumb, (x, y))
                draw.text((x + 5, y + 212), str(index + 1), fill="black")
            contact.save(shots / "pages.png")
            print(f"Browser passed: {len(images)} pages, launcher, keys, Pencil, overview, offline reload; screenshots: {shots}")
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    run()
