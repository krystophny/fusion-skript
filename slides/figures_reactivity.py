"""Deck figures for the reactivity section: Gamow peak, <sigma v>(T), Monte Carlo tail.

Model: derivations/chapters/ch02_reactivity.py (Bosch-Hale 1992, Nevins-Swain 2000,
our EXFOR S-factor fit). Descriptions: slides/04-power-balance-visuals.md.
Run:  python3 slides/figures_reactivity.py
      -> slides/build/fig/{gamow_peak,gamow_peak_pp,reactivity,tail_fuses}.{svg,png}
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "derivations/chapters"))
from figures import BLUE, GREEN, GREY, GRID, INK, MM, MUTED, ORANGE, PURPLE_W, save, style  # noqa: E402
import ch02_reactivity as rx  # noqa: E402

SKY = "#56B4E9"


def gamow(name, t, e_max, fname, label):
    """Top: the two factors and their product (log). Bottom: who is there, who reacts."""
    e_g = rx.gamow_energy(name)
    e0, width = rx.gamow_peak(e_g, t)
    e = np.linspace(e_max / 4000, e_max, 4000)
    boltz = np.exp(-e / t)
    tunnel = np.exp(-np.sqrt(e_g / e))
    fig, (top, bot) = plt.subplots(2, 1, sharex=True, figsize=(230 * MM, 140 * MM),
                                   gridspec_kw={"height_ratios": (1, 1), "hspace": .12})
    top.semilogy(e, boltz, color=BLUE, lw=2, ls=(0, (6, 3)))
    top.semilogy(e, tunnel, color=GREEN, lw=2, ls=(0, (1.5, 2)))
    top.semilogy(e, boltz * tunnel, color=ORANGE, lw=2.5)
    top.set_ylim(1e-12, 30)
    top.set_yticks([1e-12, 1e-8, 1e-4, 1])
    top.yaxis.set_minor_locator(plt.NullLocator())
    x_m, x_t = .06 * e_max, .78 * e_max
    top.text(x_m, np.exp(-x_m / t) * 2.5, r"$e^{-E/k_BT}$  Maxwell tail", color=BLUE, fontsize=17,
             ha="left", va="bottom", bbox=dict(fc="white", ec="none", pad=.5))
    top.text(x_t, np.exp(-np.sqrt(e_g / x_t)) * 4, r"$e^{-\sqrt{E_G/E}}$  tunnelling",
             color=GREEN, fontsize=17, ha="center", va="bottom")
    x_p = .17 * e_max
    top.text(x_p, np.exp(-x_p / t - np.sqrt(e_g / x_p)) / 12, "product", color=ORANGE, fontsize=17,
             ha="center", va="top")
    top.axvline(e0, color=MUTED, lw=.8, ls=":")

    # Probability densities over the centre-of-mass energy, unit area each (1/keV).
    f_all = 2 / np.sqrt(np.pi) * t**-1.5 * np.sqrt(e) * np.exp(-e / t)
    react = boltz * tunnel
    react /= np.trapezoid(react, e)
    bot.axvspan(e0 - width / 2, e0 + width / 2, color=ORANGE, alpha=.10, lw=0)
    bot.plot(e, f_all, color=BLUE, lw=2, ls=(0, (6, 3)))
    bot.plot(e, react, color=ORANGE, lw=2.5)
    ymax = 1.3 * max(f_all.max(), react.max())
    bot.axvline(e0, color=MUTED, lw=.8, ls=":")
    bot.text(e[np.argmax(f_all)] * 1.25, f_all.max() * 1.0, "all pairs", color=BLUE,
             fontsize=17, ha="left", va="center")
    bot.text(e0 + width / 2 + .01 * e_max, react.max() * .78, "pairs that fuse\n" r"($S$ = const)",
             color=ORANGE, fontsize=17, ha="left", va="center")
    nd = 0 if e0 > 20 else 1
    bot.text(e0, ymax * .97, rf"$E_0 = {e0:.{nd}f}$ keV,  $\Delta = {width:.{nd}f}$ keV", color=INK,
             fontsize=16, ha="center", va="top", bbox=dict(fc="white", ec="none", pad=1))
    bot.set_ylim(0, ymax)
    bot.set_xlim(0, e_max)
    bot.set_xlabel(r"centre-of-mass energy $E$ [keV]")
    bot.set_ylabel(r"density [keV$^{-1}$]")
    top.set_ylabel("factor")
    bot.text(.995, .97, label + rf",  $k_BT = {t:g}$ keV", transform=bot.transAxes, ha="right",
             va="top", fontsize=17, color=INK)
    for ax in (top, bot):
        ax.grid(axis="y", color=GRID, lw=.6)
        ax.set_axisbelow(True)
    fig.subplots_adjust(left=.11, right=.98, bottom=.12, top=.96)
    save(fig, fname)
    return e0, width



def reaction_product(t=10.0):
    """Cross section, Maxwellian energy density and their sigma*v-weighted product.

    D-T at k_B T = 10 keV: the *area* under the third panel is <sigma v>,
    not the height of that curve. E is centre-of-mass energy in keV.
    """
    e = np.linspace(0.3, 150.0, 2500)
    sig = rx.sigma("DT", e, "bh")  # m^2, Bosch-Hale (1992) S(E)
    v = rx.C * np.sqrt(2 * e / rx.mrc2_for("DT"))  # relative speed in m/s
    f_e = 2 / np.sqrt(np.pi) * t**-1.5 * np.sqrt(e) * np.exp(-e / t)  # keV^-1
    weight = sig * v * f_e  # m^3 / (s keV)
    peak = e[np.argmax(weight)]
    area = np.trapezoid(weight, e)

    fig, axes = plt.subplots(1, 3, figsize=(246 * MM, 112 * MM),
                             gridspec_kw={"wspace": .43})
    left, centre, right = axes
    left.plot(e, sig / rx.BARN, color=BLUE, lw=2.6)
    left.set_title("Cross section", loc="left", fontsize=16, pad=8)
    left.set_ylabel(r"$\sigma(E)$ [b]", fontsize=14)

    centre.plot(e, f_e, color=GREEN, lw=2.6)
    centre.axvline(t / 2, color=MUTED, lw=1, ls=":")
    centre.text(.98, .91, rf"peak: {t / 2:g} keV", transform=centre.transAxes,
                ha="right", va="top", fontsize=12, color=MUTED)
    centre.set_title("Thermal distribution", loc="left", fontsize=16, pad=8)
    centre.set_ylabel(r"$f_M(E)$ [keV$^{-1}$]", fontsize=14)

    right.plot(e, weight / 1e-24, color=ORANGE, lw=2.6)
    right.fill_between(e, 0, weight / 1e-24, color=ORANGE, alpha=.15)
    right.axvline(peak, color=MUTED, lw=1, ls=":")
    right.text(.98, .91, rf"peak: {peak:.0f} keV", transform=right.transAxes,
               ha="right", va="top", fontsize=12, color=MUTED)
    right.set_title("Reaction contribution", loc="left", fontsize=16, pad=8)
    right.set_ylabel(r"$\sigma v f_M$ [$10^{-24}$ m$^3$/(s keV)]", fontsize=12)

    for ax in axes:
        ax.set_xlim(0, 150)
        ax.set_ylim(bottom=0)
        ax.set_xticks([0, 50, 100, 150])
        ax.set_xlabel(r"$E$ [keV]", fontsize=14)
        ax.tick_params(labelsize=12)
        ax.grid(axis="y", color=GRID, lw=.6)
        ax.set_axisbelow(True)
    fig.suptitle(rf"D–T, $k_BT = {t:g}$ keV · Bosch–Hale cross section",
                 fontsize=16, y=.98)
    fig.subplots_adjust(left=.095, right=.985, bottom=.16, top=.79)
    save(fig, "reaction_product")
    return peak, area


REACTIONS = (  # name, label, colour, line style
    ("DT", "D–T", ORANGE, "-"),
    ("DHe3", "D–³He", PURPLE_W, (0, (8, 2, 2, 2))),
    ("DDn", None, BLUE, (0, (6, 3))),
    ("DDp", None, BLUE, (0, (1.5, 2))),
    ("p11B", "p–¹¹B", INK, (0, (3, 2))),
)


def reactivity():
    """<sigma v>(T) for five reactions, with the numerical check; <sigma v>/T^2 for D-T."""
    fig, (ax, opt) = plt.subplots(1, 2, figsize=(250 * MM, 120 * MM),
                                  gridspec_kw={"width_ratios": (1.55, 1), "wspace": .3})
    for name, label, color, ls in REACTIONS:
        if name == "p11B":
            t = np.geomspace(20, 500, 120)
            y = rx.maxwell_average(name, t)
        else:
            t = np.geomspace(1, rx.BH[name]["T_keV"][1], 300)
            y = rx.bosch_hale(name, t)
        ax.loglog(t, y, color=color, lw=2.2, ls=ls)
        if name == "DHe3":
            ax.text(t[-1], y[-1] * .45, label, color=color, fontsize=17, ha="center", va="top")
        elif label:
            ax.text(t[-1] * 1.08, y[-1], label, color=color, fontsize=17, va="center")
    ax.text(115, 1.6e-23, "D–D\n" r"$\rightarrow$ ³He n" "\n" r"$\rightarrow$ T p", color=BLUE,
            fontsize=15, va="top", linespacing=1.1)
    # Independent check: our EXFOR S-factor fit, Maxwell-averaged by quadrature.
    tm = np.array([2, 5, 10, 20, 50, 100.0])
    for name, color, marker in (("DT", ORANGE, "o"), ("DDn", BLUE, "s"), ("DDp", BLUE, "^")):
        ax.plot(tm, rx.maxwell_average(name, tm), marker, ms=6.5, mfc="white", mec=color, mew=1.4,
                ls="none", zorder=5)
    ax.text(900, 2e-27, "lines: published parametrisations\n"
            "symbols: our S-factor fit, integrated", fontsize=13, color=MUTED, ha="right", va="bottom")
    ax.set_xlim(1, 1000)
    ax.set_ylim(1e-27, 2e-21)
    ax.set_xlabel(r"$k_BT$ [keV]")
    ax.set_ylabel(r"$\langle\sigma v\rangle$ [m$^3$/s]")
    ax.grid(which="major", color=GRID, lw=.6)
    ax.set_axisbelow(True)

    t = np.linspace(1, 60, 600)
    ratio = rx.bosch_hale("DT", t) / t**2 / 1e-24
    i = ratio.argmax()
    opt.plot(t, ratio, color=ORANGE, lw=2.5)
    opt.plot([t[i]], [ratio[i]], "o", color=ORANGE, ms=7)
    opt.axvline(t[i], color=MUTED, lw=.8, ls=":")
    opt.text(t[i] + 2, ratio[i] * 1.02, rf"{t[i]:.1f} keV", color=INK, fontsize=17, va="bottom")
    opt.text(58, ratio[i] * .2, "D–T", color=ORANGE, fontsize=17, ha="right")
    opt.set_xlim(0, 60)
    opt.set_ylim(0, 1.3 * ratio[i])
    opt.set_xlabel(r"$k_BT$ [keV]")
    opt.set_ylabel(r"$\langle\sigma v\rangle/T^2$ [$10^{-24}$ m$^3$ s$^{-1}$ keV$^{-2}$]", fontsize=16)
    opt.grid(color=GRID, lw=.6)
    opt.set_axisbelow(True)
    fig.subplots_adjust(left=.09, right=.98, bottom=.15, top=.97)
    save(fig, "reactivity")
    return t[i], ratio[i]


def tail_fuses(t=10.0, n=2_000_000, seed=1):
    """Monte Carlo: sample D-T ion pairs at T, weight by sigma v, compare distributions."""
    rng = np.random.default_rng(seed)
    e, v = rx.sample_pairs(t, n, rx.MC2["D"], rx.MC2["T"], rng)
    w = rx.sigma("DT", e) * v
    bins = np.linspace(0, 150, 151)
    h_all, _ = np.histogram(e, bins, density=True)
    h_fus, _ = np.histogram(e, bins, weights=w, density=True)
    centre = .5 * (bins[1:] + bins[:-1])
    e0, width = rx.gamow_peak(rx.gamow_energy("DT"), t)
    lo, hi = e0 - width / 2, e0 + width / 2
    frac_pairs = np.mean((e > lo) & (e < hi))
    frac_fus = w[(e > lo) & (e < hi)].sum() / w.sum()
    cut = 3 * t
    pairs_above, fus_above = np.mean(e > cut), w[e > cut].sum() / w.sum()

    fig, ax = plt.subplots(figsize=(230 * MM, 115 * MM))
    ax.axvspan(3 * t, 150, color=GREY, alpha=.12, lw=0)
    ax.stairs(h_all, bins, color=BLUE, lw=2, fill=False)
    ax.stairs(h_fus, bins, color=ORANGE, lw=2.5, fill=False)
    # Analytic densities underneath the samples: Maxwell f(E) and sigma v f(E) normalised.
    ee = np.linspace(.05, 150, 1500)
    f = 2 / np.sqrt(np.pi) * t**-1.5 * np.sqrt(ee) * np.exp(-ee / t)
    g = rx.sigma("DT", ee) * ee * np.exp(-ee / t)
    g /= np.trapezoid(g, ee)
    ax.plot(ee, f, color=INK, lw=.9, ls=(0, (3, 2)))
    ax.plot(ee, g, color=INK, lw=.9, ls=(0, (3, 2)))
    ax.text(13, h_all.max() * .98, f"all pairs ({n / 1e6:.0f} million sampled)", color=BLUE,
            fontsize=17, va="center")
    ax.text(e0 + 22, h_fus.max() * .95, "pairs weighted by $\\sigma v$\n= where reactions come from",
            color=ORANGE, fontsize=17, va="center")
    ax.text(3 * t + 2, h_all.max() * 1.15, f"tail $E > 3k_BT$: {100 * pairs_above:.0f} % of pairs, "
            f"{100 * fus_above:.0f} % of reactions", color=INK, fontsize=17, ha="left", va="top")
    ax.text(148, h_all.max() * .30, "dashed: analytic densities", color=MUTED, fontsize=13, ha="right")
    ax.set_xlim(0, 150)
    ax.set_ylim(0, h_all.max() * 1.18)
    ax.set_xlabel(r"centre-of-mass energy $E$ [keV]")
    ax.set_ylabel(r"density [keV$^{-1}$]")
    ax.text(.995, .80, rf"D–T,  $k_BT = {t:g}$ keV", transform=ax.transAxes, ha="right", va="top",
            fontsize=17)
    ax.grid(axis="y", color=GRID, lw=.6)
    ax.set_axisbelow(True)
    fig.subplots_adjust(left=.1, right=.98, bottom=.15, top=.97)
    save(fig, "tail_fuses")
    mc = w.mean()
    return dict(frac_pairs=frac_pairs, frac_fus=frac_fus, pairs_above=pairs_above,
                fus_above=fus_above, mc=mc, mc_err=w.std() / np.sqrt(n))


if __name__ == "__main__":
    style()
    peak, area = reaction_product()
    print(f"wrote reaction_product: peak {peak:.1f} keV, area {area:.3e} m^3/s")
    e0, dw = gamow("DT", 10.0, 120, "gamow_peak", "D–T")
    print(f"wrote gamow_peak: E_0 = {e0:.2f} keV, width {dw:.1f} keV")
    e0, dw = gamow("pp", 1.3, 16, "gamow_peak_pp", "p–p, solar core")
    print(f"wrote gamow_peak_pp: E_0 = {e0:.2f} keV, width {dw:.1f} keV")
    t_opt, peak = reactivity()
    print(f"wrote reactivity: <sv>/T^2 maximal at {t_opt:.2f} keV ({peak:.3f}e-24)")
    print("wrote tail_fuses:", {k: f"{v:.4g}" for k, v in tail_fuses().items()})
