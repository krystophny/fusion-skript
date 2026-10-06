"""Check rendered quantities against the independent processed source tables."""
import csv
import importlib.util
from pathlib import Path

import pytest
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_agg import FigureCanvasAgg

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'ch00_figures', ROOT / 'scripts/plot-ch00-teaching.py')
plots = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plots)


@pytest.fixture
def rendered(monkeypatch, tmp_path):
    figures = []
    plots.configure_fonts()
    finish = plots.finish
    monkeypatch.setattr(plots, 'OUT', tmp_path)

    def capture(fig, *args, **kwargs):
        finish(fig, *args, **kwargs)
        figures.append(fig)

    monkeypatch.setattr(plots, 'finish', capture)
    yield figures
    for fig in figures:
        plots.plt.close(fig)


def test_mortality_bar_widths_match_csv(rendered):
    with (ROOT / 'data/ch00/processed/energy-deaths-per-TWh.csv').open() as stream:
        expected = {r['source_type']: float(r['deaths_per_TWh'])
                    for r in csv.DictReader(stream)}
    plots.risk_energy()
    ax = rendered[0].axes[0]
    actual = {label.get_text(): bar.get_width()
              for label, bar in zip(ax.get_yticklabels(), ax.containers[0])}
    assert actual == pytest.approx(expected)
    assert list(actual.values()) == sorted(expected.values())
    assert ax.get_xscale() == 'log'


def test_sankey_display_conserves_csv_boundaries_and_groups_minor_carriers(rendered):
    with (ROOT / 'data/ch00/processed/austria-sankey-links.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    totals = {}
    for row in rows:
        for endpoint in ('source', 'target'):
            key = (endpoint, row[endpoint])
            totals[key] = totals.get(key, 0) + float(row['energy_kWh_person_day'])
    gross = totals['target', 'gross']
    plots.austria_sankey()
    fig = rendered[0]
    for ax in fig.axes:
        nodes = {p.get_gid(): p.get_height()*gross
                 for p in ax.patches if isinstance(p, Rectangle)}
        for key, value in nodes.items():
            if key == 'gross_other_supply':
                expected = totals['source', 'primary_31']
            elif key == 'final_other_supply':
                expected = totals['target', 'final_32'] + totals['target', 'final_36']
            else:
                expected = max(totals.get(('source', key), 0),
                               totals.get(('target', key), 0))
            assert value == pytest.approx(expected), key
        left = sum(p.get_height()*gross for p in ax.patches
                   if isinstance(p, Rectangle) and p.get_x() < 0)
        right = sum(p.get_height()*gross for p in ax.patches
                    if isinstance(p, Rectangle) and p.get_x() > 1)
        assert left == pytest.approx(right)
    final_nodes = {p.get_gid() for p in fig.axes[1].patches if isinstance(p, Rectangle)}
    assert 'final_other_supply' in final_nodes
    assert 'final_32' not in final_nodes and 'final_36' not in final_nodes


def test_sankey_labels_are_legible_and_do_not_overlap_at_web_width(rendered):
    plots.austria_sankey()
    fig = rendered[0]
    # Desktop chapter images are about 682 CSS pixels after figure padding.
    fig.set_dpi(85)  # Test slightly narrower, at 680 pixels.
    FigureCanvasAgg(fig)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    texts = [text for ax in fig.axes for text in [*ax.texts, ax.title]] + fig.texts
    boxes = [text.get_window_extent(renderer) for text in texts]
    for i, (text, box) in enumerate(zip(texts, boxes)):
        assert text.get_fontsize()*fig.bbox.width/768 >= 10
        assert text.get_fontproperties().get_name() == 'STIX Two Text'
        assert fig.bbox.contains(box.x0, box.y0) and fig.bbox.contains(box.x1, box.y1)
        for other in boxes[i+1:]:
            assert not box.overlaps(other), text.get_text()
