"""Deck figures for Chapter 3, fusion in stars.

Model and data: derivations/chapters/ch03_stars.py and data/ch03 (provenance in
data/ch03/README.md).
Run:  python3 slides/figures_stars.py
      -> slides/build/fig/{sun_profile,onion}.{svg,png}
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "derivations/chapters"))
from figures import BLUE, GREEN, GREY, GRID, INK, MM, MUTED, ORANGE, save, style  # noqa: E402
import ch03_stars as st  # noqa: E402


def sun_profile():
    """Model S: temperature, density and where the power is made."""
    p = st.SUN["profile"]
    r = np.array(p["r_over_R"])
    t = np.array(p["T_K"]) * st.KB / st.KEV
    rho = np.array(p["rho_kg_m3"]) / 1e3
    lum = np.array(p["L_over_L"])
    x = np.array(p["X"])
    fig, (a, b) = plt.subplots(1, 2, figsize=(257 * MM, 120 * MM), gridspec_kw={"wspace": .55})
    a.plot(r, t, color=ORANGE, lw=2.5)
    a.set_xlabel("$r/R_\\odot$")
    a.set_ylabel("$k_BT$ [keV]", color=ORANGE)
    a.set_xlim(0, 1)
    a.set_ylim(0, 1.45)
    a2 = a.twinx()
    a2.semilogy(r, rho, color=BLUE, lw=2.5, ls=(0, (6, 3)))
    a2.set_ylabel("$\\rho$ [g cm$^{-3}$]", color=BLUE)
    a2.spines["right"].set_visible(True)
    a2.set_ylim(1e-7, 300)
    a.text(.2, 0.98, "1.35 keV at $r = 0$", color=ORANGE, fontsize=16, va="top")
    a2.text(.36, 12, "154 g cm$^{-3}$ at $r = 0$", color=BLUE, fontsize=16)
    a.text(0.68, 0.3, "convective\nzone", color=MUTED, fontsize=15, ha="left")
    a.axvspan(0.713, 1, color=GRID, zorder=0)
    b.plot(r, lum, color=INK, lw=2.5)
    b.plot(r, x / x[-1], color=GREEN, lw=2, ls=(0, (1.5, 2)))
    b.set_xlim(0, 0.5)
    b.set_ylim(0, 1.05)
    b.set_xlabel("$r/R_\\odot$")
    b.set_ylabel("fraction")
    r99 = st.SUN["r99"]["r_over_R"]
    b.axvline(r99, color=GREY, lw=1, ls=(0, (3, 3)))
    b.text(r99 + .01, .12, f"99 % of $L_\\odot$\ninside {r99:.2f} $R_\\odot$", fontsize=15, color=MUTED)
    b.text(.27, .97, "$L(r)/L_\\odot$", fontsize=17, color=INK, va="top")
    b.text(.08, .46, "$X(r)/X_{\\rm surface}$", fontsize=17, color=GREEN)
    for ax in (a, b):
        ax.tick_params(length=4)
    fig.subplots_adjust(left=.08, right=.97, bottom=.17, top=.95)
    save(fig, "sun_profile")


def onion():
    """Shells of a pre-supernova massive star (schematic, not to scale)."""
    shells = [("H, He", "#F4E3C1"), ("He", "#F2C79A"), ("C, O", "#DDB6D9"), ("O, Ne, Mg", "#B7C9E8"),
              ("Si, S", "#A8D5C2"), ("Fe, Ni", "#9AA5B1")]
    fig, ax = plt.subplots(figsize=(150 * MM, 125 * MM))
    for k, (lab, col) in enumerate(shells):
        r = 1 - k * 0.16
        ax.add_patch(Circle((0, 0), r, facecolor=col, edgecolor=INK, lw=1))
        ax.text(0, r - 0.08, lab, ha="center", va="top", fontsize=16)
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    save(fig, "onion")


if __name__ == "__main__":
    style()
    sun_profile()
    onion()
    print("wrote stars figures")
