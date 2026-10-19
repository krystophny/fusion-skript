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


def tag(ax, x, y, text, k, color, size=11):
    """Experiment name in small text, led by that experiment's marker."""
    ax.plot([x], [y], MARKERS[k], ms=4.5, color=color, mfc="white" if k % 2 else color, mew=1,
            clip_on=False)
    ax.text(x * 1.12, y, text, color=color, fontsize=size, ha="left", va="center")


def s_factor_data():
    data, result = fit.fit_all()
    fig, (top, bot) = plt.subplots(2, 1, sharex=True, figsize=(170 * MM, 128 * MM),
                                   gridspec_kw={"height_ratios": (3, 2), "hspace": .08})
    e = np.geomspace(3, 500, 500)

    # --- D-T
    series = data[("DT", "DT")]
    sc = 1e-3
    for k, s in enumerate(series):
        top.errorbar(s["e"], s["s"] * sc, s["ds"] * sc, fmt=MARKERS[k], ms=4.5, color=ORANGE,
                     mfc="white" if k % 2 else ORANGE, mew=1, elinewidth=.8, capsize=0, zorder=3)
    ed = e[(e >= 4.5) & (e <= 500)]
    top.plot(ed, fit.bh_curve("DT", ed) * sc, color=GREY, lw=1.2, ls=(0, (4, 3)), zorder=1)
    top.plot(ed, fit.model_curve(result, "DT", ed) * sc, color=ORANGE, lw=2, zorder=2)
    top.set_ylim(0, 31)
    top.set_ylabel(r"$S$ [$10^3$ keV b]")
    top.text(1.04, .5, "D–T", transform=top.transAxes, color=ORANGE, fontsize=18, va="center")
    top.text(7, 17.5, "this fit", color=ORANGE, fontsize=12, va="center")
    top.text(120, 15, "Bosch–Hale", color=MUTED, fontsize=12, va="center")
    pos = {"Arnold 1954": (4.6, 6.5), "Jarmie 1984": (11, 27.5), "Brown 1987": (80, 28.8),
           "Bame 1957": (230, 6.5)}
    for k, s_ in enumerate(series):
        tag(top, *pos[s_["label"]], s_["label"], k, ORANGE)

    # --- D-D
    scol = {"n": BLUE, "p": GREEN}
    for br in ("n", "p"):
        for k, s in enumerate(data[("DD", br)]):
            bot.errorbar(s["e"], s["s"], s["ds"], fmt=MARKERS[k], ms=4.5, color=scol[br],
                         mfc="white" if k % 2 else scol[br], mew=1, elinewidth=.8, capsize=0, zorder=3)
        name = "DD" + br
        lo = min(s["e"].min() for s in data[("DD", br)])
        ed = e[(e >= lo * .9) & (e <= 350)]
        bot.plot(ed, fit.bh_curve(name, ed), color=GREY, lw=1.2, ls=(0, (4, 3)), zorder=1)
        bot.plot(ed, fit.model_curve(result, name, ed), color=scol[br], lw=2, zorder=2)
    bot.set_ylim(40, 175)
    bot.set_ylabel(r"$S$ [keV b]")
    bot.text(1.04, .75, "D(d,n)³He", transform=bot.transAxes, color=BLUE, fontsize=14, va="center")
    bot.text(1.04, .30, "D(d,p)T", transform=bot.transAxes, color=GREEN, fontsize=14, va="center")
    pos = {"Greife 1995": (3.6, 47), "Preston 1954": (150, 62), "Leonard 2006": (28, 150)}
    for k, s_ in enumerate(data[("DD", "n")]):
        tag(bot, *pos[s_["label"]], s_["label"], k, INK)

    bot.set_xscale("log")
    bot.set_xlim(3, 500)
    bot.set_xticks([5, 10, 20, 50, 100, 200, 500], ["5", "10", "20", "50", "100", "200", "500"])
    bot.minorticks_off()
    bot.set_xlabel(r"$E$ (centre of mass) [keV]")
    top.tick_params(labelbottom=False)
    for ax in (top, bot):
        ax.grid(axis="y", color="#E3E6EA", lw=.6)
        ax.set_axisbelow(True)
    fig.subplots_adjust(left=.14, right=.80, bottom=.13, top=.98)
    save(fig, "s_factor_data")


if __name__ == "__main__":
    style()
    s_factor_data()
    print("wrote s_factor_data")
