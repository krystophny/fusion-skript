"""Fit the fusion S-factor to measured EXFOR cross sections.

README: reads ch02_s_factor_exfor.json (same folder), converts each measured
cross section to S_i = sigma_i E_i exp(sqrt(E_G/E_i)), fits the Bosch-Hale
form by weighted least squares, prints coefficients, uncertainties and the reduced
chi^2, and draws data, our fit and (dashed) the published Bosch-Hale curve.
Run:  python3 ch02_s_factor_fit.py   (needs numpy, scipy, matplotlib; writes
ch02_s_factor_fit.png next to the script).

Units: E in keV (centre of mass), sigma in barn, S in keV b.
Bosch & Hale, Nucl. Fusion 32, 611 (1992); coefficients below in their keV mb units.
"""
import json
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent
DATA = HERE / "ch02_s_factor_exfor.json"
META = json.loads(DATA.read_text())
BG = META["B_G_sqrt_keV"]                                  # B_G = sqrt(E_G), sqrt(keV)
# Published Bosch-Hale S(E) coefficients in keV mb: numerator A1..A5, denominator B1..B4.
BH = {k: (v["A"], v["B"]) for k, v in META["bosch_hale"].items()}
E0 = 100.0   # keV; the fit uses x = E/E0 so that all coefficients are of order one


def rational(x, a, b):
    """Bosch-Hale form (a0 + a1 x + ...)/(1 + b1 x + ...), Horner evaluation."""
    num = sum(c * x**k for k, c in enumerate(a))
    den = 1 + sum(c * x**(k + 1) for k, c in enumerate(b))
    return num / den


def bh_curve(name, e):
    """Published Bosch-Hale S in keV b."""
    a, b = BH[name]
    return rational(e, a, b) * 1e-3


def load():
    """Return {(reaction, branch): list of series}, each point with S computed from sigma."""
    out = {}
    for s in META["series"]:
        e = np.array([p["e_cm_keV"] for p in s["points"]])
        sig = np.array([p["sigma_b"] for p in s["points"]])
        dsig = np.array([p["dsigma_b"] for p in s["points"]])
        boost = e * np.exp(BG[s["reaction"]] / np.sqrt(e))    # S = sigma E exp(sqrt(E_G/E))
        out.setdefault((s["reaction"], s["branch"]), []).append(
            dict(label=s["label"], doi=s["doi"], reference=s["reference"],
                 e=e, s=sig * boost, ds=dsig * boost))
    return out


def stack(series):
    return [np.concatenate([s[k] for s in series]) for k in ("e", "s", "ds")]


def fit(series, name, free):
    """Weighted least squares (error bars as weights) of S(E) = rational(E/E0).

    Parameters are ordered A1..A5, B1..B4 as in Bosch-Hale, scaled to keV b and
    x = E/E0. Those listed in `free` are fitted; the others stay at their
    Bosch-Hale values. Returns the full parameter vector, the errors of the
    free ones (zero for fixed ones), reduced chi^2 and the covariance condition number."""
    e, s, ds = stack(series)
    a, b = BH[name]
    full = np.array([1e-3 * c * E0**k for k, c in enumerate(a)]
                    + [c * E0**(k + 1) for k, c in enumerate(b)])

    def model(x, *q):
        p = full.copy()
        p[free] = q
        return rational(x, p[:5], p[5:])

    popt, pcov = curve_fit(model, e / E0, s, p0=full[free], sigma=ds,
                           absolute_sigma=True, maxfev=200000)
    chi2 = np.sum(((s - model(e / E0, *popt)) / ds) ** 2) / (len(e) - len(popt))
    best, err = full.copy(), np.zeros_like(full)
    best[free], err[free] = popt, np.sqrt(np.diag(pcov))
    return best, err, chi2, np.linalg.cond(pcov)


# Which Bosch-Hale coefficients are fitted (indices into A1..A5, B1..B4).
# D-T: the data (4.5-450 keV, only two points above 70 keV) cannot fix all eight
#   coefficients: the full fit has cond(cov) ~ 1e14 and several coefficients consistent with
#   zero (A1 comes out negative). We fit A2, B1, B2 (resonance height, position and
#   width; all to 2 % or better) and keep A1, A3, A4, B3, B4 at the Bosch-Hale
#   values. The reduced chi^2 is the same as for the full fit.
# D-D: Bosch-Hale use a polynomial numerator A1..A5 (valid to 4.9 MeV). Our data end
#   at 323 keV, so only A1..A3 are fitted; A4, A5 stay at Bosch-Hale (negligible here).
FREE = {"DT": [1, 5, 6], "DDn": [0, 1, 2], "DDp": [0, 1, 2]}
KEY = {"DT": ("DT", "DT"), "DDn": ("DD", "n"), "DDp": ("DD", "p")}


def fit_all():
    data = load()
    result = {name: dict(zip(("p", "err", "chi2", "cond"), fit(data[KEY[name]], name, FREE[name])))
              for name in FREE}
    return data, result


def model_curve(result, name, e):
    p = result[name]["p"]
    return rational(np.asarray(e) / E0, p[:5], p[5:])


def report(data, result):
    for name in FREE:
        r = result[name]
        e = stack(data[KEY[name]])[0]
        print(f"{name}: {len(e)} points, E = {e.min():.1f}-{e.max():.1f} keV, "
              f"reduced chi^2 = {r['chi2']:.2f}, cond(cov) = {r['cond']:.1e}")
        labels = [f"A{k + 1}" for k in range(5)] + [f"B{k + 1}" for k in range(4)]
        for k, lab in enumerate(labels):
            if lab[0] == "B" and name != "DT":
                continue
            power = k if k < 5 else k - 4                  # coefficient of E^power
            scale = E0**power / (1e3 if k < 5 else 1.0)    # back to keV, A in keV mb
            tag = "fitted" if k in FREE[name] else "fixed at Bosch-Hale"
            print(f"   {lab} = {r['p'][k] / scale:.5g} +- {r['err'][k] / scale:.2g}  ({tag})")
        for en in (10, 64, 100):
            print(f"   S({en} keV): fit {model_curve(result, name, en):.5g}, "
                  f"Bosch-Hale {bh_curve(name, en):.5g} keV b")


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data, result = fit_all()
    report(data, result)
    fig, (top, bot) = plt.subplots(2, 1, sharex=True, figsize=(8, 7))
    e = np.geomspace(2, 500, 400)
    for ax, keys, names in ((top, [("DT", "DT")], ["DT"]), (bot, [("DD", "n"), ("DD", "p")], ["DDn", "DDp"])):
        for key in keys:
            for s in data[key]:
                ax.errorbar(s["e"], s["s"], s["ds"], fmt="o", ms=3, label=f"{s['label']} {key[1]}")
        for name in names:
            ax.plot(e, model_curve(result, name, e), label=f"fit {name}")
            ax.plot(e, bh_curve(name, e), "k--", lw=0.8, label=f"Bosch-Hale {name}")
        ax.set_ylabel("S [keV b]")
        ax.legend(fontsize=7)
    bot.set_xscale("log")
    bot.set_xlabel("E (centre of mass) [keV]")
    fig.savefig(HERE / "ch02_s_factor_fit.png", dpi=130)


if __name__ == "__main__":
    main()
