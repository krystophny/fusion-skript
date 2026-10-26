"""A deck without an outline chapter keeps its explicit chapter identity."""
import importlib.util
from pathlib import Path

import pytest


spec = importlib.util.spec_from_file_location(
    "build_present", Path(__file__).resolve().parents[1] / "scripts/build-present.py"
)
presenter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(presenter)


def test_outline_chapter_remains_authoritative():
    chapter = {"number": 0, "title": "The big picture", "label": "energy-context"}
    assert presenter.deck_info(0, {"chapters": [chapter]}, {}) == chapter


def test_deck_first_chapter_uses_explicit_cover_metadata():
    assert presenter.deck_info(1, {"chapters": []}, {
        1: {"chapter": 1, "title": "Discovering fusion"}
    }) == {"number": 1, "title": "Discovering fusion"}


@pytest.mark.parametrize("cover", [
    {}, {"chapter": 2, "title": "Wrong chapter"},
    {"chapter": 1, "title": " "}, {"chapter": 1, "title": None},
])
def test_deck_first_chapter_rejects_missing_or_mismatched_identity(cover):
    with pytest.raises(ValueError, match="matching title-page metadata"):
        presenter.deck_info(1, {"chapters": []}, {1: cover})
