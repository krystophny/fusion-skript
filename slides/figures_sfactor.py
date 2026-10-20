"""Deck figure s_factor_data: EXFOR S-factor points, our fit and Bosch-Hale (dashed).

Data: derivations/chapters/ch02_s_factor_exfor.json (scripts/prepare-ch02-s-factor.py).
Fit:  derivations/chapters/ch02_s_factor_fit.py.
Run:  python3 slides/figures_sfactor.py  ->  slides/build/fig/s_factor_data.{svg,png}
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "derivations/chapters"))
from figures import BLUE, GREEN, GREY, INK, MM, MUTED, ORANGE, save, style  # noqa: E402
import ch02_s_factor_fit as fit  # noqa: E402

MARKERS = ["o", "s", "^", "D"]
PURPLE = "#7B3294"


def tag(ax, x, y, text, k, color, size=11):
    """Experiment name in small text, led by that experiment's marker."""
    ax.plot([x], [y], MARKERS[k], ms=4.5, color=color, mfc="white" if k % 2 else color, mew=1,
            clip_on=False)
    ax.text(x * 1.12, y, text, color=color, fontsize=size, ha="left", va="center")


def s_factor_data():
    data, result = fit.fit_all()
    fig, (ax, low) = plt.subplots(2, 1, sharex=True, figsize=(170 * MM, 125 * MM),
                                  gridspec_kw={"height_ratios": (4, 1), "hspace": .1})
    e = np.geomspace(3, 500, 500)

    # D-T
    series = data[("DT", "DT")]
    for k, s in enumerate(series):
        ax.errorbar(s["e"], s["s"], s["ds"], fmt=MARKERS[k], ms=4.5, color=ORANGE,
                    mfc="white" if k % 2 else ORANGE, mew=1, elinewidth=.8, capsize=0, zorder=3)
    ed = e[(e >= 4.5) & (e <= 500)]
    ax.plot(ed, fit.bh_curve("DT", ed), color=GREY, lw=1.2, ls=(0, (4, 3)), zorder=1)
    ax.plot(ed, fit.model_curve(result, "DT", ed), color=ORANGE, lw=2, zorder=2)
    ax.text(1100, 3e3, r"D + T $\rightarrow$ $^4$He + n", color=ORANGE, fontsize=14, va="center")
    pos = {"Arnold 1954": (2.2, 6.0e3), "Jarmie 1984": (11, 4.6e4), "Brown 1987": (80, 4.6e4),
           "Bame 1957": (130, 6e2)}
    for k, s_ in enumerate(series):
        tag(ax, *pos[s_["label"]], s_["label"], k, ORANGE)

    # D-D, both branches
    scol = {"n": BLUE, "p": GREEN}
    for br in ("n", "p"):
        for k, s in enumerate(data[("DD", br)]):
            ax.errorbar(s["e"], s["s"], s["ds"], fmt=MARKERS[k], ms=4.5, color=scol[br],
                        mfc="white" if k % 2 else scol[br], mew=1, elinewidth=.8, capsize=0, zorder=3)
        name = "DD" + br
        lo = min(s["e"].min() for s in data[("DD", br)])
        ed = e[(e >= lo * .9) & (e <= 350)]
        ax.plot(ed, fit.bh_curve(name, ed), color=GREY, lw=1.2, ls=(0, (4, 3)), zorder=1)
        ax.plot(ed, fit.model_curve(result, name, ed), color=scol[br], lw=2, zorder=2)
    ax.text(1100, 200, r"D + D $\rightarrow$ $^3$He + n", color=BLUE, fontsize=14, va="center")
    ax.text(1100, 90, r"D + D $\rightarrow$ T + p", color=GREEN, fontsize=14, va="center")
    pos = {"Greife 1995": (2.2, 40), "Preston 1954": (90, 40), "Leonard 2006": (20, 330)}
    for k, s_ in enumerate(data[("DD", "n")]):
        tag(ax, *pos[s_["label"]], s_["label"], k, INK)

    # p-p: computed, no data (Adelberger et al. 2011: S(0) and S'(0)/S(0))
    ep = np.geomspace(1, 100, 200)    # linear S' expansion: low energies only
    sp = 4.01e-22 * (1 + 11.2e-3 * ep)
    low.fill_between(ep, sp * (1 - .04 / 4.01), sp * (1 + .04 / 4.01), color=PURPLE, alpha=.35, lw=0)
    low.plot(ep, sp, color=PURPLE, lw=1.2)
    low.text(1100, 6e-22, r"p + p $\rightarrow$ D + e$^+$ + $\nu_e$", color=PURPLE, fontsize=14, va="center")
    low.set_yscale("log")
    low.set_ylim(1e-22, 1e-20)
    low.yaxis.set_minor_formatter(plt.NullFormatter())
    low.set_yticks([1e-22, 1e-21, 1e-20])

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 1000)
    ax.set_ylim(30, 1e5)
    low.set_xlabel(r"$E$ [keV]")
    fig.text(.005, .55, r"$S$ [keV b]", rotation=90, va="center", fontsize=18)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(which="both", bottom=False)
    for a_, y0 in ((ax, 0), (low, 1)):
        a_.plot((-.012, .012), (y0 - .03, y0 + .03), transform=a_.transAxes, color=INK, lw=.8,
                clip_on=False)
    for a_ in (ax, low):
        a_.grid(axis="y", color="#E3E6EA", lw=.6)
        a_.set_axisbelow(True)
    fig.subplots_adjust(left=.13, right=.72, bottom=.12, top=.98)
    save(fig, "s_factor_data")

if __name__ == "__main__":
    style()
    s_factor_data()
    print("wrote s_factor_data")
