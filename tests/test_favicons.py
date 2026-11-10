"""Every published widget and notebook page names a favicon, so browsers do not request /favicon.ico."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICON = re.compile(r"""<link\s+rel=["']icon["']""")


def test_inlined_widgets_carry_the_course_icon():
    spec = importlib.util.spec_from_file_location("inline_widget", ROOT / "scripts/inline-widget.py")
    inline = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inline)
    pages = sorted((ROOT / "notebooks").glob("slide-*.html"))
    assert pages
    for page in pages:
        out = inline.inline(page)
        assert ICON.search(out), page.name
        assert 'href="data:image/svg+xml;base64,' in out, page.name


def test_notebooks_name_the_course_icon():
    config = (ROOT / "notebooks/_quarto.yml").read_text()
    assert ICON.search(config) and "../present/icon.svg" in config
    assert (ROOT / "src/present/icon.svg").is_file()
