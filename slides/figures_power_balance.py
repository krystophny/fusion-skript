"""Deck figures for the start of power balance: alpha/neutron split, Lawson plane, power flow.

Model: derivations/chapters/ch04_power_balance.py (0-D D-T balance, Bosch-Hale
<sigma v>, NRL bremsstrahlung). Descriptions: slides/04-power-balance-visuals.md.
Run:  python3 slides/figures_power_balance.py
      -> slides/build/fig/{alpha_neutron_split,lawson_plane,power_flow}.{svg,png}
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrow, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "derivations/chapters"))
from figures import BLUE, GREEN, GREY, GRID, INK, MM, MUTED, ORANGE, PURPLE_W, save, style  # noqa: E402
import ch04_power_balance as pb  # noqa: E402
from ch02_reactivity import MC2  # noqa: E402


def alpha_neutron_split():
    """Centre-of-mass picture: equal and opposite momenta, energy inversely to mass."""
    q = pb.E_FUS / 1e3                                                   # MeV
    # Non-relativistic split, as derived on the figure; relativistic values in the note.
    e_a = q * MC2["n"] / (MC2["n"] + MC2["He4"])
    e_n = q - e_a
    fig, ax = plt.subplots(figsize=(230 * MM, 110 * MM))
    ax.set_xlim(0, 23)
    ax.set_ylim(-.6, 10.4)
    ax.set_aspect("equal")
    ax.axis("off")
    r = {s: .55 * (MC2[s] / MC2["n"]) ** (1 / 3) for s in ("D", "T", "He4", "n")}
    # before: D and T meet with (almost) zero total momentum
    y0 = 7.3
    ax.text(.4, 10.2, "before", fontsize=17, color=MUTED, va="top")
    ax.add_patch(Circle((2.6, y0), r["D"], color=BLUE))
    ax.add_patch(Circle((2.6 + r["D"] + r["T"], y0), r["T"], color=GREEN))
    ax.text(2.6, y0 - 1.25, "D", ha="center", fontsize=18, color=BLUE)
    ax.text(2.6 + r["D"] + r["T"], y0 - 1.25, "T", ha="center", fontsize=18, color=GREEN)
    ax.text(3.2, y0 - 2.35, r"$p_{\rm tot}\approx 0$", ha="center", fontsize=17)
    # after: alpha left, neutron right, equal arrow lengths = equal |p|
    xc = 14.2
    ax.text(8.6, 10.2, "after (centre-of-mass frame)", fontsize=17,
            color=MUTED, va="top")
    ax.add_patch(Circle((xc - 1.1, y0), r["He4"], color=ORANGE))
    ax.add_patch(Circle((xc + 1.1, y0), r["n"], color=INK))
    L = 4.0
    for x, sgn, lab in ((xc - 1.1 - r["He4"] - .1, -1, r"$-\vec p$"), (xc + 1.1 + r["n"] + .1, 1, r"$\vec p$")):
        ax.add_patch(FancyArrow(x, y0, sgn * L, 0, width=.09, head_width=.45, head_length=.55,
                                length_includes_head=True, color=INK))
        ax.text(x + sgn * L / 2, y0 + .35, lab, ha="center", va="bottom", fontsize=18)
    ax.text(xc - 1.1, y0 - 1.5, r"$\alpha$ ($^4$He)", ha="center", fontsize=18, color=ORANGE)
    ax.text(xc + 1.1, y0 - 1.5, "n", ha="center", fontsize=18, color=INK)
    ax.text(xc, y0 - 2.75, r"$E = \dfrac{p^2}{2m}\ \Rightarrow\ \dfrac{E_\alpha}{E_n} = \dfrac{m_n}{m_\alpha}"
            r"\approx \dfrac{1}{4}$", ha="center", va="center", fontsize=18)
    # energy bar, MeV to scale
    s = 20.5 / q
    x0, yb, h = 1.2, .6, 1.1
    ax.add_patch(FancyBboxPatch((x0, yb), e_a * s, h, boxstyle="square,pad=0", color=ORANGE))
    ax.add_patch(FancyBboxPatch((x0 + e_a * s, yb), e_n * s, h, boxstyle="square,pad=0", color=BLUE))
    ax.text(x0 + e_a * s / 2, yb + h / 2, f"{e_a:.2f} MeV", ha="center", va="center", color="white", fontsize=17)
    ax.text(x0 + e_a * s + e_n * s / 2, yb + h / 2, f"neutron  {e_n:.2f} MeV  ({100 * e_n / q:.0f} %)",
            ha="center", va="center", color="white", fontsize=17)
    ax.text(x0 + e_a * s / 2, yb + h + .2, rf"alpha ({100 * e_a / q:.0f} %)", ha="center", va="bottom",
            color=ORANGE, fontsize=16)
    ax.text(x0 + 20.5, yb + h + .2, rf"$Q_{{\rm DT}} = {q:.2f}$ MeV", ha="right", va="bottom", fontsize=17)
    ax.text(x0, yb - .3, f"with relativistic kinematics: {pb.E_ALPHA / 1e3:.2f} MeV and {pb.E_N / 1e3:.2f} MeV",
            fontsize=13, color=MUTED, va="top")
    fig.subplots_adjust(left=.01, right=.99, bottom=.01, top=.99)
    save(fig, "alpha_neutron_split")


QS = ((1, "#9AA5B1"), (5, "#5A8DB8"), (10, BLUE), (np.inf, ORANGE))


def lawson_plane():
    """Required n T tau_E vs T for several Q; right: n T tau_E vs Q at the optimum."""
    t = np.geomspace(2, 100, 2000)
    fig, (ax, qx) = plt.subplots(1, 2, figsize=(250 * MM, 120 * MM),
                                 gridspec_kw={"width_ratios": (1.6, 1), "wspace": .55})
    for q, color in QS:
        y = pb.triple_product(t, q)
        ax.loglog(t, y, color=color, lw=2.5 if np.isinf(q) else 2)
        lab = "ignition" if np.isinf(q) else f"$Q = {q}$"
        nudge = {1: 1.0, 5: .82, 10: 1.05, np.inf: 1.3}[q]
        ax.text(108, y[-1] * nudge, lab, color=color, fontsize=15, ha="left", va="center", clip_on=False)
    yb = pb.triple_product(t, brems=True)
    ax.loglog(t, yb, color=ORANGE, lw=1.8, ls=(0, (5, 3)))
    ax.text(4.6, 6e22, "ignition with\nbremsstrahlung", color=ORANGE, fontsize=15, ha="left", va="center")
    ign = pb.triple_product(t)
    i = ign.argmin()
    ax.plot([t[i]], [ign[i]], "o", color=ORANGE, ms=8, zorder=5)
    m, e = f"{ign[i]:.1e}".split("e")
    ax.annotate(rf"${m}\times10^{{{int(e)}}}$ keV s m$^{{-3}}$" "\n" rf"at {t[i]:.1f} keV",
                (t[i], ign[i]), (t[i] * .62, ign[i] * .28), fontsize=15, ha="center", va="top",
                arrowprops=dict(arrowstyle="-", color=INK, lw=.8))
    ax.set_xlim(2, 100)
    ax.set_ylim(1e20, 1e23)
    ax.set_xlabel(r"$k_BT$ [keV]")
    ax.set_ylabel(r"$n\,T\,\tau_E$ [keV s m$^{-3}$]")
    ax.grid(which="major", color=GRID, lw=.6)
    ax.set_axisbelow(True)

    q = np.geomspace(.1, 1000, 400)
    t0 = np.array([t[i]])
    ref = pb.triple_product(t0)[0]
    y = np.array([pb.triple_product(t0, qq)[0] for qq in q])
    qx.semilogx(q, y / 1e21, color=BLUE, lw=2.5)
    qx.axhline(ref / 1e21, color=ORANGE, lw=1.5, ls=(0, (5, 3)))
    qx.text(.12, ref / 1e21 * 1.03, "ignition", color=ORANGE, fontsize=15, va="bottom")
    for qq, color in QS[:-1]:
        v = pb.triple_product(t0, qq)[0] / 1e21
        qx.plot([qq], [v], "o", color=color, ms=7, zorder=5)
        qx.text(qq * 1.4, v - .07, f"$Q={qq}$", color=INK, fontsize=14, va="top")
    qx.set_xlim(.1, 1000)
    qx.set_ylim(0, 3.2)
    qx.set_xlabel(r"$Q = P_{\rm fus}/P_{\rm ext}$")
    qx.set_ylabel(r"$n\,T\,\tau_E$ [$10^{21}$ keV s m$^{-3}$]")
    qx.text(.97, .04, rf"$k_BT = {t[i]:.1f}$ keV", transform=qx.transAxes, ha="right", fontsize=15)
    qx.grid(color=GRID, lw=.6)
    qx.set_axisbelow(True)
    fig.subplots_adjust(left=.09, right=.98, bottom=.15, top=.97)
    save(fig, "lawson_plane")
    return t[i], ign[i]


def _flow(ax, x, y, dx, dy, w, color):
    ax.add_patch(FancyArrow(x, y, dx, dy, width=w, head_width=w * 1.35 + .25, head_length=.7,
                            length_includes_head=True, color=color, lw=0))


def power_flow(q=10.0, p_fus=500.0):
    """0-D steady state at gain Q: arrow widths proportional to power (MW)."""
    p_ext = p_fus / q
    p_a = p_fus * pb.E_ALPHA / pb.E_FUS
    p_n = p_fus - p_a
    p_loss = p_ext + p_a
    k = 1 / 200                                        # arrow width per MW (axis units)
    fig, ax = plt.subplots(figsize=(230 * MM, 112 * MM))
    ax.set_xlim(0, 23)
    ax.set_ylim(.9, 12.2)
    ax.set_aspect("equal")
    ax.axis("off")

    def box(x, y, w, h, text, color, sub=None):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.25",
                                    fc="white", ec=color, lw=2))
        ax.text(x + w / 2, y + h / 2 + (.3 if sub else 0), text, ha="center", va="center", fontsize=18, color=color)
        if sub:
            ax.text(x + w / 2, y + h / 2 - .45, sub, ha="center", va="center", fontsize=15, color=MUTED)

    box(7.2, 7.0, 6.6, 2.6, "plasma", INK, r"$W = 3nk_BT\,V$")
    box(7.2, 1.6, 6.6, 2.6, "fusion reactions", INK, r"$P_{\rm fus} = n_Dn_T\langle\sigma v\rangle E_{\rm fus}V$")
    box(18.4, 1.6, 4.3, 2.6, "blanket", BLUE)
    box(18.4, 7.0, 4.3, 2.6, "wall,\ndivertor", MUTED)
    # external heating in
    _flow(ax, .6, 8.3, 6.5, 0, p_ext * k, PURPLE_W)
    ax.text(.6, 8.3 + p_ext * k / 2 + .25, rf"$P_{{\rm ext}} = {p_ext:.0f}$ MW", fontsize=17,
            color=PURPLE_W, va="bottom")
    # alpha heating up from fusion to plasma
    _flow(ax, 10.5, 4.3, 0, 2.6, p_a * k, ORANGE)
    ax.text(10.5 + p_a * k / 2 + .45, 5.6, rf"$P_\alpha = {p_a:.0f}$ MW", fontsize=17, color=ORANGE, va="center")
    # losses out
    _flow(ax, 13.9, 8.3, 4.4, 0, p_loss * k, MUTED)
    ax.text(15.9, 8.3 + p_loss * k / 2 + .2, rf"$P_{{\rm loss}} = W/\tau_E$", fontsize=16, color=MUTED,
            ha="center", va="bottom")
    ax.text(15.9, 8.3 - p_loss * k / 2 - .2, f"{p_loss:.0f} MW", fontsize=16, color=MUTED, ha="center", va="top")
    # neutrons out
    _flow(ax, 13.9, 2.9, 4.4, 0, p_n * k, BLUE)
    ax.text(16.0, 2.9 - p_n * k / 2 - .3, rf"$P_n = {p_n:.0f}$ MW", fontsize=17, color=BLUE,
            ha="center", va="top")
    ax.text(.6, 11.9, rf"$Q = P_{{\rm fus}}/P_{{\rm ext}} = {q:g}$,  $P_{{\rm fus}} = {p_fus:.0f}$ MW",
            fontsize=18, va="top")
    ax.text(.6, 10.9, r"steady state: $P_{\rm ext} + P_\alpha = P_{\rm loss}$", fontsize=16, color=MUTED, va="top")
    ax.text(.6, 2.9, "fuel\nD + T", fontsize=17, color=INK, va="center")
    ax.add_patch(FancyArrow(2.6, 2.9, 4.5, 0, width=.05, head_width=.35, head_length=.5,
                            length_includes_head=True, color=INK))
    ax.text(22.7, 11.9, "arrow widths proportional to power", fontsize=13, color=MUTED, ha="right",
            va="top")
    fig.subplots_adjust(left=.01, right=.99, bottom=.01, top=.99)
    save(fig, "power_flow")
    return dict(p_ext=p_ext, p_alpha=p_a, p_n=p_n, p_loss=p_loss)


if __name__ == "__main__":
    style()
    alpha_neutron_split()
    print(f"wrote alpha_neutron_split: E_alpha = {pb.E_ALPHA:.0f} keV, E_n = {pb.E_N:.0f} keV")
    t_min, ign = lawson_plane()
    print(f"wrote lawson_plane: ignition minimum {ign:.3e} keV s m^-3 at {t_min:.2f} keV")
    print("wrote power_flow:", {k: f"{v:.1f} MW" for k, v in power_flow().items()})
