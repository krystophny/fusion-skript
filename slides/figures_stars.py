"""Deck figures for Chapter 3, fusion in stars.

Model and data: derivations/chapters/ch03_stars.py and data/ch03 (provenance in
data/ch03/README.md).
Run:  python3 slides/figures_stars.py
      -> slides/build/fig/{sun_profile,abundances,hoyle,onion}.{svg,png}
"""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "derivations/chapters"))
from figures import BLUE, GREEN, GREY, GRID, INK, MM, MUTED, ORANGE, PURPLE_W, ROOT, save, style  # noqa: E402
import ch03_stars as st  # noqa: E402

SKY = "#56B4E9"
DATA = ROOT / "data/ch03"


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


def abundances():
    d = json.loads((DATA / "abundances.json").read_text())
    els = [e for e in d["elements"] if e["log_eps"] is not None]
    z = np.array([e["Z"] for e in els])
    y = np.array([e["log_eps"] for e in els])
    fig, ax = plt.subplots(figsize=(257 * MM, 122 * MM))
    colour = np.where(z <= 3, BLUE, np.where(z <= 30, ORANGE, GREEN))
    ax.plot(z, y, color=GREY, lw=1)
    ax.scatter(z, y, c=colour, s=26, zorder=3)
    for e in els:
        if e["element"] in ("H", "He", "Li", "Be", "B", "C", "O", "Si", "Fe", "Ba", "Pb", "Au", "U", "Eu", "Pt"):
            ax.text(e["Z"], e["log_eps"] + 0.35, e["element"], fontsize=14, ha="center")
    ax.text(3.5, 12.4, "Big Bang", color=BLUE, fontsize=16)
    ax.text(12, 9.7, "fusion in stars", color=ORANGE, fontsize=16)
    ax.text(52, 4.6, "neutron capture (s and r process)", color=GREEN, fontsize=16)
    ax.set_xlabel("atomic number $Z$")
    ax.set_ylabel("$\\log_{10}(N/N_{\\rm H}) + 12$")
    ax.set_xlim(0, 94)
    ax.set_ylim(-1.2, 13.2)
    fig.subplots_adjust(left=.09, right=.98, bottom=.16, top=.96)
    save(fig, "abundances")


def hoyle():
    """Left: 12C levels on the MeV scale. Right: the triple-alpha threshold region in keV."""
    h = st.hoyle_numbers()
    q, be8 = h["Q3a_keV"], h["Be8_above_2a_keV"]
    hoy = 7654.2
    fig, (a, b) = plt.subplots(1, 2, figsize=(257 * MM, 122 * MM), gridspec_kw={"width_ratios": (1, 1.25), "wspace": .05})
    def lv(ax, x0, x1, y, c, lw=3):
        ax.plot([x0, x1], [y, y], color=c, lw=lw, solid_capstyle="butt")
    for y, lab, c in ((0, "$^{12}$C ground state", INK), (4.439, "4.44 MeV, 2$^+$", INK),
                      (hoy / 1e3, "Hoyle state 7.65 MeV, 0$^+$", ORANGE)):
        lv(a, 0, 1, y, c, 4 if c == ORANGE else 3)
        a.text(1.08, y, lab, va="center", fontsize=16, color=c)
    a.annotate("", xy=(0.5, 4.6), xytext=(0.5, 7.5), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.5))
    a.annotate("", xy=(0.25, 0.15), xytext=(0.25, 4.3), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.5))
    a.text(0.55, 6.1, "$\\gamma$ (0.04 %)", fontsize=15)
    a.text(0.3, 2.2, "$\\gamma$", fontsize=15)
    a.set_xlim(-0.1, 3.4)
    a.set_ylim(-0.4, 8.4)
    a.axis("off")
    # Zoom: energies above the 3-alpha threshold in keV.
    for y, lab, c in ((0, "3 $\\alpha$", BLUE), (be8, "$^{8}$Be + $\\alpha$", GREEN),
                      (hoy - q, "Hoyle state", ORANGE)):
        lv(b, 0, 1, y, c, 4)
        b.text(1.06, y, lab, va="center", fontsize=17, color=c)
    for y0, y1, x in ((0, be8, 0.25), (be8, hoy - q, 0.6)):
        b.annotate("", xy=(x, y1 - 4), xytext=(x, y0 + 4), arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.3))
        b.text(x + 0.04, (y0 + y1) / 2, f"{y1 - y0:.0f} keV", fontsize=16, color=MUTED, va="center")
    b.set_ylim(-40, 430)
    b.set_xlim(-0.05, 1.9)
    b.set_ylabel("energy above 3$\\alpha$ [keV]")
    b.spines["bottom"].set_visible(False)
    b.set_xticks([])
    b.set_yticks([0, 100, 200, 300, 400])
    fig.subplots_adjust(left=.02, right=.98, bottom=.05, top=.96)
    save(fig, "hoyle")


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
    abundances()
    hoyle()
    onion()
    print("wrote stars figures")
