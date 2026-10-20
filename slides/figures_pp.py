"""Deck figure pp_fusion_waves: kin6d p-p fusion wave functions and overlap.

Data: derivations/chapters/data/pp_fusion_kin6d.json (kin6d build/pp_fusion_export,
Reid68 potential + point Coulomb, one-body Gamow-Teller).
Run:  python3 slides/figures_pp.py  ->  slides/build/fig/pp_fusion_waves.{svg,png}
"""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figures import BLUE, GREEN, INK, MM, MUTED, ORANGE, ROOT, save, style  # noqa: E402

DATA = ROOT / "derivations/chapters/data/pp_fusion_kin6d.json"


def pp_fusion_waves():
    d = json.loads(DATA.read_text())
    col = {name: k for k, name in enumerate(d["radial_columns"])}
    a = np.array(d["radial"])
    r = a[:, col["r_fm"]]
    fig, (top, bot) = plt.subplots(2, 1, sharex=True, figsize=(150 * MM, 125 * MM),
                                   gridspec_kw={"height_ratios": (2, 3), "hspace": .1})
    # potentials: p-p singlet and deuteron central triplet
    top.plot(r, a[:, col["V_pp_MeV"]], color=GREEN, lw=2)
    top.plot(r, a[:, col["V_d_SS_MeV"]], color=BLUE, lw=2)
    top.axhline(0, color=MUTED, lw=.6)
    top.set_ylim(-120, 120)
    top.set_ylabel(r"$V$ [MeV]")
    top.text(3.2, 25, "p–p", color=GREEN, fontsize=16)
    top.text(3.2, -50, "deuteron", color=BLUE, fontsize=16)
    # wave functions, each scaled to unit maximum on the plotted range
    sel = r <= 15
    ud = a[:, col["u_d_S_fm^-1/2"]]
    upp = a[:, col["u_pp_over_Ck_fm"]]
    integ = a[:, col["Lambda_integrand_per_fm"]]
    for y, color, label, x0, dy in ((ud, BLUE, r"$u_d$", 3.6, .12), (upp, GREEN, r"$u_{pp}$", 12.0, -.17)):
        ys = y / np.max(np.abs(y[sel]))
        bot.plot(r, ys, color=color, lw=2)
        bot.text(x0, np.interp(x0, r, ys) + dy, label, color=color, fontsize=18)
    ig = integ / np.max(integ[sel])
    bot.fill_between(r, 0, ig, color=ORANGE, alpha=.25, lw=0)
    bot.plot(r, ig, color=ORANGE, lw=1.2)
    bot.text(4.6, .07, r"$u_d\,u_{pp}$", color=ORANGE, fontsize=18)
    bot.set_ylim(0, 1.15)
    bot.set_yticks([])
    bot.set_xlim(0, 15)
    bot.set_xlabel(r"$r$ [fm]")
    fig.subplots_adjust(left=.17, right=.97, bottom=.13, top=.97)
    save(fig, "pp_fusion_waves")


if __name__ == "__main__":
    style()
    pp_fusion_waves()
