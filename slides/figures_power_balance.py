"""Deck figures for the start of power balance: alpha/neutron split, Lawson plane, power flow.

Model: derivations/chapters/ch04_power_balance.py (0-D D-T balance, Bosch-Hale
<sigma v>, NRL bremsstrahlung). Descriptions: slides/04-power-balance-visuals.md.
Run:  python3 slides/figures_power_balance.py
      -> slides/build/fig/{alpha_neutron_split,lawson_plane,power_flow,density_scaling,
         alpha_brems,q_eng,alpha_fraction,impurity_dilution,fixed_pressure,n_tau_plane}.{svg,png}
Measured points: Wurzel and Hsu, Phys. Plasmas 29, 062103 (2022), CC BY 4.0.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrow, FancyBboxPatch
from matplotlib.ticker import FuncFormatter

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "derivations/chapters"))
from figures import BLUE, GREEN, GREY, GRID, INK, MM, MUTED, ORANGE, PURPLE_W, save, style  # noqa: E402
import ch04_power_balance as pb  # noqa: E402
from ch02_reactivity import KEV, MC2, bosch_hale  # noqa: E402


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


PLAIN = FuncFormatter(lambda v, _: f"{v:g}")
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
    ax.text(5.6, 6e22, "ignition with\nbremsstrahlung", color=ORANGE, fontsize=15, ha="left", va="center")
    ign = pb.triple_product(t)
    i = ign.argmin()
    ax.plot([t[i]], [ign[i]], "o", color=ORANGE, ms=8, zorder=5)
    m, e = f"{ign[i]:.1e}".split("e")
    ax.annotate(rf"${m}\times10^{{{int(e)}}}$ keV s m$^{{-3}}$" "\n" rf"at {t[i]:.1f} keV",
                (t[i], ign[i]), (t[i] * .62, ign[i] * .28), fontsize=15, ha="center", va="top",
                arrowprops=dict(arrowstyle="-", color=INK, lw=.8))
    ax.set_xlim(2, 100)
    ax.xaxis.set_major_formatter(PLAIN)
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
    qx.xaxis.set_major_formatter(PLAIN)
    qx.set_ylim(0, 3.2)
    qx.set_xlabel(r"$Q = P_{\rm fus}/P_{\rm ext}$")
    qx.set_ylabel(r"$n\,T\,\tau_E$ [$10^{21}$ keV s m$^{-3}$]")
    qx.text(.97, .04, rf"$k_BT = {t[i]:.1f}$ keV", transform=qx.transAxes, ha="right", fontsize=15)
    qx.grid(color=GRID, lw=.6)
    qx.set_axisbelow(True)
    fig.subplots_adjust(left=.09, right=.965, bottom=.15, top=.97)
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
    ax.text(15.6, 2.9 - p_n * k / 2 - .3, rf"$P_n = {p_n:.0f}$ MW", fontsize=17, color=BLUE,
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


# Half-page plots sit on six grid columns (125 mm) next to their derivation.
HALF = (125 * MM, 118 * MM)


def _axes(ax):
    ax.grid(which="major", color=GRID, lw=.6)
    ax.set_axisbelow(True)


def density_scaling(t=14.0):
    """At fixed T: alpha heating grows as n^2, conduction loss 3 n T / tau_E as n."""
    n = np.geomspace(1e18, 1e22, 200)
    sv = bosch_hale("DT", t)
    fig, ax = plt.subplots(figsize=HALF)
    p_a = n**2 / 4 * sv * pb.E_ALPHA * KEV
    ax.loglog(n, p_a, color=ORANGE, lw=2.5)
    ax.text(1.2e21, 2e9, r"$p_\alpha \propto n^2$", color=ORANGE, fontsize=18, ha="right")
    ax.set_xlim(1e18, 1e22)
    ax.set_ylim(1e2, 1e10)
    fig.subplots_adjust(left=.2, right=.94, bottom=.15, top=.97)
    (x0, y0), (x1, y1) = ax.transData.transform([(1e18, 1e3), (1e19, 1e4)])
    angle = np.degrees(np.arctan2(y1 - y0, x1 - x0))
    for tau, ls in ((0.1, (0, (2, 2))), (1.0, "-"), (10.0, (0, (6, 3)))):
        loss = 3 * n * t * KEV / tau
        ax.loglog(n, loss, color=INK, lw=1.6, ls=ls)
        cross = 12 * t / (sv * pb.E_ALPHA * tau)
        ax.plot([cross], [3 * cross * t * KEV / tau], "o", color=INK, ms=6, zorder=5)
        ax.text(1.3e18, 3 * 1.3e18 * t * KEV / tau * 1.6, rf"$\tau_E = {tau:g}$ s", fontsize=15,
                color=INK, rotation=angle, rotation_mode="anchor", va="bottom")
    ax.text(.97, .13, r"loss $3nk_BT/\tau_E$", transform=ax.transAxes, ha="right", fontsize=15)
    ax.set_xlabel(r"$n$ [m$^{-3}$]")
    ax.set_ylabel(r"power density [W m$^{-3}$]")
    ax.text(.97, .05, rf"$k_BT = {t:g}$ keV", transform=ax.transAxes, ha="right", fontsize=15, color=MUTED)
    _axes(ax)
    save(fig, "density_scaling")


def alpha_brems():
    """p_alpha / n_e^2 and p_br / n_e^2 against T: they cross at the ideal ignition temperature."""
    t = np.geomspace(1, 100, 600)
    fig, ax = plt.subplots(figsize=HALF)
    a = bosch_hale("DT", t) / 4 * pb.E_ALPHA * KEV
    b = pb.C_B * np.sqrt(t)
    ax.loglog(t, a, color=ORANGE, lw=2.5)
    ax.loglog(t, b, color=BLUE, lw=2.2, ls=(0, (6, 3)))
    ti = pb.ideal_ignition_temperature()
    ax.axvline(ti, color=MUTED, lw=.8, ls=":")
    ax.plot([ti], [pb.C_B * np.sqrt(ti)], "o", color=INK, ms=7, zorder=5)
    ax.text(ti * 1.12, 2.2e-38, f"{ti:.1f} keV", fontsize=16, color=INK)
    ax.text(30, 4.5e-36, r"$p_\alpha / n_e^2$", color=ORANGE, fontsize=18, ha="center")
    ax.text(25, 1.3e-36, r"$p_{\rm br} / n_e^2$", color=BLUE, fontsize=18, ha="center", va="top")
    ax.set_xlim(1, 100)
    ax.xaxis.set_major_formatter(PLAIN)
    ax.set_ylim(1e-39, 1e-35)
    ax.set_xlabel(r"$k_BT$ [keV]")
    ax.set_ylabel(r"$p / n_e^2$ [W m$^3$]")
    ax.text(.04, .95, r"$Z_{\rm eff} = 1$", transform=ax.transAxes, fontsize=15, color=MUTED, va="top")
    _axes(ax)
    fig.subplots_adjust(left=.2, right=.93, bottom=.15, top=.97)
    save(fig, "alpha_brems")
    return ti


def q_eng_plot():
    """Engineering gain against plasma gain for two efficiency products."""
    q = np.geomspace(1, 100, 400)
    fig, ax = plt.subplots(figsize=HALF)
    for (eth, eaux), color, ls in (((0.4, 0.4), BLUE, "-"), ((0.5, 0.6), GREY, (0, (6, 3)))):
        ax.semilogx(q, pb.q_eng(q, eth, eaux), color=color, lw=2.4, ls=ls)
    ax.text(26, 2.2, r"$0.4 \times 0.4$", color=BLUE, fontsize=15, ha="left")
    ax.text(9, 3.6, r"$0.5 \times 0.6$", color=MUTED, fontsize=15, ha="right")
    ax.axhline(0, color=INK, lw=.9)
    ax.axhline(1, color=INK, lw=.6, ls=":")
    for qq, y, lab in ((1 / .16 - 1, 0, "5.25"), (2 / .16 - 1, 1, "11.5")):
        ax.plot([qq], [y], "o", color=BLUE, ms=7, zorder=5)
        ax.text(qq * 1.08, y - .15, f"$Q = {lab}$", fontsize=15, va="top")
    ax.text(1.1, .1, "net electricity", fontsize=14, color=MUTED, va="bottom")
    ax.text(1.1, 1.1, "half recirculated", fontsize=14, color=MUTED, va="bottom")
    ax.set_xlim(1, 100)
    ax.xaxis.set_major_formatter(PLAIN)
    ax.set_ylim(-1, 6)
    ax.set_xlabel(r"$Q = P_{\rm fus}/P_{\rm ext}$")
    ax.set_ylabel(r"$Q_{\rm eng}$")
    ax.text(.04, .95, r"$\eta_{\rm th}\,\eta_{\rm aux}$", transform=ax.transAxes, fontsize=16, va="top")
    _axes(ax)
    fig.subplots_adjust(left=.16, right=.93, bottom=.15, top=.97)
    save(fig, "q_eng")


def alpha_fraction_plot():
    """Self-heating fraction against Q, with the gains of the table on the same page."""
    q = np.geomspace(.1, 1000, 400)
    fig, ax = plt.subplots(figsize=(103 * MM, 84 * MM))
    ax.semilogx(q, pb.alpha_fraction(q), color=INK, lw=2.4)
    ax.axhline(1, color=ORANGE, lw=1.5, ls=(0, (5, 3)))
    ax.text(.13, .97, r"ignition, $Q \to \infty$", color=ORANGE, fontsize=15, va="top")
    for qq, color in QS[:-1]:
        f = float(pb.alpha_fraction(qq))
        ax.plot([qq], [f], "o", color=color, ms=8, zorder=5)
        ax.text(qq * 1.5, f - .03, f"$Q={qq}$", fontsize=15, va="top")
    ax.set_xlim(.1, 1000)
    ax.set_xticks([.1, 1, 10, 100, 1000])
    ax.xaxis.set_major_formatter(PLAIN)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel(r"$Q$")
    ax.set_ylabel(r"$f_\alpha$", rotation=0, labelpad=14, va="center")
    _axes(ax)
    fig.subplots_adjust(left=.21, right=.92, bottom=.2, top=.97)
    save(fig, "alpha_fraction")


HE = ((0.0, ORANGE, "-"), (0.05, "#5A8DB8", (0, (6, 3))), (0.10, BLUE, (0, (2, 2))), (0.15, INK, (0, (6, 2, 1, 2))))


def impurity_dilution():
    """Left: ignition n_e T tau_E with helium ash; right: fusion power against Z c at fixed n_e."""
    t = np.geomspace(3, 100, 2000)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(250 * MM, 120 * MM),
                                 gridspec_kw={"width_ratios": (1.5, 1), "wspace": .42})
    for c, color, ls in HE:
        y = pb.ignition_diluted(t, [(2, c)] if c else [])
        ax.loglog(t, y, color=color, lw=2.2, ls=ls)
        i = np.argmin(y)
        ax.plot([t[i]], [y[i]], "o", color=color, ms=6, zorder=5)
        ax.text(108, y[-1], f"{100 * c:.0f} % He", color=color, fontsize=15, va="center", clip_on=False)
    ax.set_xlim(3, 100)
    ax.xaxis.set_major_formatter(PLAIN)
    ax.set_ylim(1e21, 1e23)
    ax.set_xlabel(r"$k_BT$ [keV]")
    ax.set_ylabel(r"ignition $n_e T \tau_E$ [keV s m$^{-3}$]")
    ax.text(.04, .05, "with bremsstrahlung", transform=ax.transAxes, fontsize=15, color=MUTED)
    _axes(ax)

    zc = np.linspace(0, 0.3, 200)
    bx.plot(zc, (1 - zc) ** 2, color=INK, lw=2.2)
    for z, c, lab, dx, dy in ((74, 1e-3, "0.1 % W", .012, .02), (2, .05, "5 % He", .012, .02)):
        f = 1 - z * c
        bx.plot([z * c], [f**2], "o", color=ORANGE if z == 74 else BLUE, ms=8, zorder=5)
        bx.text(z * c + dx, f**2 + dy, lab, fontsize=15, color=ORANGE if z == 74 else BLUE)
    bx.set_xlim(0, .3)
    bx.set_ylim(.4, 1.02)
    bx.set_xlabel(r"$Z c$")
    bx.set_ylabel(r"$p_{\rm fus} / p_{\rm fus}(c = 0)$")
    bx.text(.95, .93, r"$(1 - Zc)^2$", transform=bx.transAxes, fontsize=17, ha="right", va="top")
    _axes(bx)
    fig.subplots_adjust(left=.1, right=.98, bottom=.15, top=.97)
    save(fig, "impurity_dilution")


def fixed_pressure():
    """D-T fusion power density against T at fixed density and at fixed pressure, each scaled to its maximum."""
    t = np.geomspace(2, 100, 20001)
    sv = bosch_hale("DT", t)
    fig, ax = plt.subplots(figsize=HALF)
    for y, color, ls in ((sv / sv.max(), GREY, (0, (6, 3))), (sv / t**2 / (sv / t**2).max(), ORANGE, "-")):
        ax.semilogx(t, y, color=color, lw=2.4, ls=ls)
        i = y.argmax()
        ax.plot([t[i]], [y[i]], "o", color=color, ms=7, zorder=5)
        ax.text(t[i], 1.04, f"{t[i]:.0f} keV" if t[i] > 30 else f"{t[i]:.1f} keV", color=INK,
                fontsize=15, ha="center", va="bottom")
    ax.text(58, .5, r"fixed $n$:" "\n" r"$\propto \langle\sigma v\rangle$", color=MUTED, fontsize=16, ha="center")
    ax.text(2.2, .86, r"fixed $p$:" "\n" r"$\propto \langle\sigma v\rangle / T^2$", color=ORANGE, fontsize=16,
            ha="left")
    ax.set_xlim(2, 100)
    ax.xaxis.set_major_formatter(PLAIN)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel(r"$k_BT$ [keV]")
    ax.set_ylabel(r"$p_{\rm fus}$ / maximum")
    _axes(ax)
    fig.subplots_adjust(left=.17, right=.93, bottom=.15, top=.97)
    save(fig, "fixed_pressure")


# Labelled experiments and label offsets in points.
LABELS = {("ZETA", 1957): (-10, -14), ("JET", 1997): (14, 20), ("W7-X", 2017): (-14, -36),
          ("NIF", 2021): (12, 6), ("MagLIF", 2015): (12, -2), ("FuZE", 2018): (-12, 14),
          ("Alcator C", 1984): (20, 42)}


def n_tau_plane():
    """Density against confinement time: confinement routes and measured experiments."""
    rows = pb.machines()
    fig, ax = plt.subplots(figsize=(250 * MM, 128 * MM))
    tau = np.geomspace(1e-12, 1e3, 50)
    # Q thresholds need T, which this plane does not show; only constant n tau is drawn.
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-12, 1e3)
    ax.set_ylim(1e17, 1e34)
    fig.subplots_adjust(left=.09, right=.98, bottom=.14, top=.98)
    # Screen angle of a line n tau = const on these log axes.
    (x0, y0), (x1, y1) = ax.transData.transform([(1e-6, 1e26), (1e0, 1e20)])
    angle = np.degrees(np.arctan2(y1 - y0, x1 - x0))
    for e, tx in ((16, 1e-10), (18, 1e-8), (20, 1e-6), (22, 1e-4)):
        ax.loglog(tau, 10.0**e / tau, color=GREY, lw=1, ls=(0, (6, 3)), zorder=1)
        lab = rf"$n\tau = 10^{{{e}}}$ s m$^{{-3}}$" if e == 22 else rf"$10^{{{e}}}$"
        ax.text(tx, 10.0**e / tx * 1.8, lab, color=MUTED, fontsize=13,
                rotation=angle, rotation_mode="anchor", ha="left", va="bottom")
    mag = [r for r in rows if r["table"] in ("6", "7")]
    icf = [r for r in rows if r["table"] == "8"]
    ax.scatter([r["tau"] for r in mag], [r["n"] for r in mag], s=22, marker="o", color=BLUE, zorder=4, lw=0)
    ax.scatter([r["tau"] for r in icf], [r["n"] for r in icf], s=34, marker="s", color=INK, zorder=4, lw=0)
    done = set()
    for r in rows:
        key = (r["project"], r["year"])
        if key in LABELS and key not in done:
            done.add(key)
            dx, dy = LABELS[key]
            ax.annotate(f"{r['project']} {r['year']}", (r["tau"], r["n"]), (dx, dy),
                        textcoords="offset points", fontsize=13, ha="left" if dx > 0 else "right",
                        va="center", color=INK, arrowprops=dict(arrowstyle="-", color=MUTED, lw=.6))
    # Sun: thermal content over luminosity; electron density from the mean (computed, hydrogen
    # mass fraction 0.7) to the core (rho_c = 150 g/cm^3, X_c = 0.35: standard solar model).
    tk = pb.kelvin_helmholtz_time()
    n_mean = pb.sun_mean_density() * 1.7 / (2 * 1.66054e-27)
    n_core = 150e3 * 1.35 / (2 * 1.66054e-27)
    edge = ("axes fraction", "data")
    ax.annotate("", (.995, n_core), (.995, n_mean), xycoords=edge, textcoords=edge,
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=5, capstyle="round"))
    n_sun = np.sqrt(n_mean * n_core)
    ax.annotate("", (1.0, n_sun), (.93, n_sun), xycoords=edge, textcoords=edge,
                arrowprops=dict(arrowstyle="-|>,head_width=.35,head_length=.7", color=GREEN, lw=2))
    yr = tk / 3.156e7
    ax.text(.92, n_sun, "Sun, off scale:\n" rf"$\tau \approx {yr / 1e7:.0f}\times10^7$ yr"
            "\n" rf"$= {tk / 1e15:.0f}\times10^{{15}}$ s", transform=ax.get_yaxis_transform(),
            color=GREEN, fontsize=15, ha="right", va="center")
    ax.text(.5e-11, 4e31, "inertial", color=INK, fontsize=17, ha="left")
    ax.text(1.5e-3, 2.2e17, "magnetic", color=BLUE, fontsize=17, ha="right")
    ax.set_xlabel(r"$\tau$ [s]")
    ax.set_ylabel(r"$n$ [m$^{-3}$]")
    _axes(ax)
    save(fig, "n_tau_plane")


if __name__ == "__main__":
    style()
    alpha_neutron_split()
    print(f"wrote alpha_neutron_split: E_alpha = {pb.E_ALPHA:.0f} keV, E_n = {pb.E_N:.0f} keV")
    t_min, ign = lawson_plane()
    print(f"wrote lawson_plane: ignition minimum {ign:.3e} keV s m^-3 at {t_min:.2f} keV")
    print("wrote power_flow:", {k: f"{v:.1f} MW" for k, v in power_flow().items()})
    density_scaling()
    print(f"wrote alpha_brems: ideal ignition at {alpha_brems():.2f} keV")
    q_eng_plot()
    alpha_fraction_plot()
    impurity_dilution()
    fixed_pressure()
    n_tau_plane()
    print("wrote density_scaling, q_eng, alpha_fraction, impurity_dilution, fixed_pressure, n_tau_plane")
