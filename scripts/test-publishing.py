"""Behavioral oracles: physical page metadata, local revisions and safe exports.

Run with python3 -m pytest -q scripts/test-publishing.py. Fixtures are isolated
from concurrently edited scientific sources and do not make Git commits.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
from types import SimpleNamespace
from urllib.parse import unquote, urlsplit

import pytest

REPO = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


present = load("present_builder", "build-present.py")
exporter = load("course_exporter", "export-course-folder.py")


@pytest.fixture
def course(tmp_path):
    root = tmp_path / "course"
    (root / "slides/build").mkdir(parents=True)
    (root / "public/slides").mkdir(parents=True)
    (root / "src").mkdir()
    shutil.copytree(REPO / "src/present", root / "src/present")
    shutil.copyfile(REPO / "slides/present-meta.typ", root / "slides/present-meta.typ")
    (root / "slides/build/script-outline.json").write_text(json.dumps({
        "chapters": [{"number": 0, "title": "Independent fixture"}]}))
    (root / "public/slides/00-fixture.pdf").write_bytes(b"fixture pdf")
    (root / "public/fusion-physics.pdf").write_bytes(b"current script")
    (root / "public/media").mkdir()
    (root / "public/media/movie.mp4").write_bytes(b"independent movie payload")
    source = root / "slides/00-fixture.typ"
    source.write_text('''#import "present-meta.typ": present-meta
#set page(width: 297mm, height: 210mm)
#page[#present-meta(background: "dark") First]
#page[#present-meta(kind: "animation", background: "dark",
  video: "/media/movie.mp4", loop: false) Second]
''')
    return root


def args(root, strict=True):
    return SimpleNamespace(root=root, site_dir=None, course="Fusion Physics",
                           short_name="Fusion", author="Fixture author",
                           strict_metadata=strict)


def resolve_revision(parent, value):
    parts = urlsplit(value)
    assert not parts.scheme and not parts.netloc
    path = parent / unquote(parts.path)
    expected = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    assert parts.query == "v=" + expected
    return path


def test_physical_pages_and_course_identity(course):
    present.build(args(course))
    output = course / "public/present"
    index = json.loads((output / "decks.json").read_text())
    assert (index["course"], index["author"]) == ("Fusion Physics", "Fixture author")
    manifest = json.loads((output / "00-fixture/manifest.json").read_text())
    assert manifest["aspect"] == pytest.approx(297 / 210, rel=1e-5)
    assert [p["kind"] for p in manifest["pages"]] == ["static", "animation"]
    assert [p["background"] for p in manifest["pages"]] == ["dark", "dark"]
    assert manifest["pages"][1]["loop"] is False
    for page in manifest["pages"]:
        resolve_revision(output / "00-fixture", page["src"])
    assert resolve_revision(output / "00-fixture", manifest["pages"][1]["video"]).read_bytes() == b"independent movie payload"
    resolve_revision(output / "00-fixture", manifest["pdf"])
    app = json.loads((output / "manifest.webmanifest").read_text())
    assert (app["name"], app["short_name"]) == ("Fusion Physics", "Fusion")
    assert '"fusion-physics-present-v1"' in (output / "sw.js").read_text()


def test_strict_missing_page_preserves_previous_build(course):
    present.build(args(course))
    marker = course / "public/present/marker.txt"
    marker.write_text("last usable build")
    (course / "slides/00-fixture.typ").write_text('#set page(width: 297mm, height: 210mm)\n#page[No metadata]')
    with pytest.raises(ValueError, match="metadata missing"):
        present.build(args(course))
    assert marker.read_text() == "last usable build"
    present.build(args(course, strict=False))
    manifest = json.loads((course / "public/present/00-fixture/manifest.json").read_text())
    assert manifest["pages"][0]["kind"] == "static"


def test_duplicate_metadata_is_rejected(course):
    (course / "slides/00-fixture.typ").write_text('''#import "present-meta.typ": present-meta
#page[#present-meta() #present-meta() Duplicate]
''')
    with pytest.raises(ValueError, match="Duplicate"):
        present.build(args(course))


def test_external_and_escaping_media_are_rejected(course):
    deck = course / "destination"
    deck.mkdir()
    for url in ("https://outside.example/video.mp4", "../slides/00-fixture.typ"):
        with pytest.raises(ValueError):
            present.stage_media(url, {}, course / "public", deck)


def test_stale_export_preserves_unowned_and_modified_files(course, tmp_path):
    dest = tmp_path / "students"
    (dest / "slides").mkdir(parents=True)
    unowned = dest / "slides/personal.pdf"
    unowned.write_bytes(b"lecturer addition")
    # First full export establishes exporter ownership.
    for name in ("LICENSE", "LICENSE-CONTENT.md"):
        (course / name).write_text("fixture license")
    (course / "derivations").mkdir()
    (course / "derivations/build/fig").mkdir(parents=True)
    obsolete_figure = course / "derivations/build/fig/old-plot.svg"
    obsolete_figure.write_text("old generated plot")
    exporter.export(course, course / "public", dest)
    (course / "public/slides/00-fixture.pdf").unlink()
    obsolete_figure.unlink()
    (course / "public/slides/01-next.pdf").write_bytes(b"next deck")
    exporter.export(course, course / "public", dest)
    assert not (dest / "slides/00-fixture.pdf").exists()
    assert not (dest / "figures/old-plot.svg").exists()
    assert unowned.read_bytes() == b"lecturer addition"
    (dest / "slides/01-next.pdf").write_bytes(b"student annotation")
    (course / "public/slides/01-next.pdf").unlink()
    (course / "public/slides/02-next.pdf").write_bytes(b"new deck")
    exporter.export(course, course / "public", dest)
    assert (dest / "slides/01-next.pdf").read_bytes() == b"student annotation"


def test_export_copies_every_build_product(course, tmp_path):
    dest = tmp_path / "public-course-folder"
    (course / "derivations/build/fig").mkdir(parents=True)
    (course / "derivations/build/fig/energy.svg").write_text("derived plot")
    (course / "derivations/energy.py").write_text("source calculation")
    (course / "slides/build").mkdir(exist_ok=True)
    (course / "slides/build/script-outline.json").write_text("{}")
    for name in ("LICENSE", "LICENSE-CONTENT.md"):
        (course / name).write_text("license")
    exporter.export(course, course / "public", dest)
    assert (dest / "skript/fusion-physics.pdf").read_bytes() == b"current script"
    assert (dest / "slides/00-fixture.pdf").read_bytes() == b"fixture pdf"
    assert (dest / "figures/energy.svg").read_text() == "derived plot"
    assert (dest / "derivations/energy.py").read_text() == "source calculation"
    manifest = json.loads((dest / ".fusion-skript-export.json").read_text())
    assert "figures/energy.svg" in manifest["files"]
