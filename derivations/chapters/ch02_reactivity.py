"""Chapter 2, last section: Maxwellian reactivity <sigma v> and the Gamow peak (MIT).

Run:  python3 derivations/chapters/ch02_reactivity.py
Model functions are shared with slides/figures_reactivity.py and
ch04_power_balance.py. Units: E, T in keV (k_B T written as T), sigma in m^2,
<sigma v> in m^3/s.

For two Maxwellian species at one temperature the relative motion is again
Maxwellian with the reduced mass m_r, so
    <sigma v> = sqrt(8/(pi m_r)) T^(-3/2) int_0^inf sigma(E) E exp(-E/T) dE.
With sigma = (S/E) exp(-sqrt(E_G/E)) the integrand is S(E) exp(-E/T - sqrt(E_G/E)),
peaked at the Gamow energy E_0 = (E_G T^2/4)^(1/3), 1/e full width 4 sqrt(E_0 T/3).

Sources: Bosch and Hale, Nucl. Fusion 32, 611 (1992) for D-T, D-D, D-3He;
Nevins and Swain, Nucl. Fusion 40, 865 (2000) for p-11B; constants and
coefficients in data/ch02/reactivity.json. The independent cross-check
integrates our own EXFOR S-factor fit (ch02_s_factor_fit.py) numerically.
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy import constants as k

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ch02_s_factor_fit as sfit  # noqa: E402

RX = json.loads((ROOT / "data/ch02/reactivity.json").read_text())
BH = RX["bosch_hale_reactivity"]["reactions"]
EXTRA = RX["bosch_hale_s_factor_extra"]
PB = RX["p11B"]

KEV = 1e3 * k.e                      # J
C = k.c                              # m/s
BARN = 1e-28                         # m^2
# CODATA (scipy.constants) rest energies in keV.
MC2 = {name: 1e3 * k.physical_constants[f"{key} mass energy equivalent in MeV"][0]
       for name, key in (("p", "proton"), ("D", "deuteron"), ("T", "triton"),
                         ("n", "neutron"), ("He3", "helion"), ("He4", "alpha particle"))}
PAIRS = {"DT": ("D", "T", 1, 1), "DDn": ("D", "D", 1, 1), "DDp": ("D", "D", 1, 1),
         "DHe3": ("D", "He3", 1, 2), "p11B": ("p", "B11", 1, 5), "pp": ("p", "p", 1, 1)}


def reduced_mc2(name):
    if name == "p11B":
        return PB["mrc2_keV"]                 # Nevins and Swain, Table 2
    a, b, _, _ = PAIRS[name]
    return MC2[a] * MC2[b] / (MC2[a] + MC2[b])


def gamow_energy(name):
    """E_G = 2 m_r c^2 (pi alpha Z1 Z2)^2 in keV."""
    _, _, z1, z2 = PAIRS[name]
    return 2 * reduced_mc2(name) * (np.pi * k.alpha * z1 * z2) ** 2


def gamow_peak(e_g, t):
    """Peak E_0 and 1/e full width Delta of exp(-E/T - sqrt(E_G/E)), keV."""
    e0 = (e_g * t**2 / 4) ** (1 / 3)
    return e0, 4 * np.sqrt(e0 * t / 3)


# --- Bosch-Hale and Nevins-Swain parametrisations -------------------------------------
def bosch_hale(name, t):
    """Bosch-Hale (1992) Table VII reactivity in m^3/s; t in keV."""
    r = BH[name]
    c1, c2, c3, c4, c5, c6, c7 = r["C"]
    t = np.asarray(t, float)
    theta = t / (1 - t * (c2 + t * (c4 + t * c6)) / (1 + t * (c3 + t * (c5 + t * c7))))
    xi = (r["B_G_sqrt_keV"] ** 2 / (4 * theta)) ** (1 / 3)
    return c1 * theta * np.sqrt(xi / (r["mrc2_keV"] * t**3)) * np.exp(-3 * xi) * 1e-6


def nevins_swain_fit(t):
    """Nevins-Swain (2000) eq. (13) p-11B reactivity in m^3/s, non-resonant part, 50-500 keV."""
    p1, p2, p3, p4, p5, p6, p7 = PB["high_T_fit"]["P"]
    t = np.asarray(t, float)
    theta = t / (1 - t * (p2 + t * (p4 + t * p6)) / (1 + t * (p3 + t * (p5 + t * p7))))
    xi = (gamow_energy_p11b() / (4 * theta)) ** (1 / 3)
    return p1 * theta * np.sqrt(xi / (PB["mrc2_keV"] * t**3)) * np.exp(-3 * xi)


def gamow_energy_p11b():
    """E_G as used by Nevins and Swain: (E_G/4)^(1/3) = 17.81 keV^(1/3)."""
    return 4 * PB["E_G_quarter_cuberoot_keV"] ** 3


# --- cross sections sigma(E) in m^2 -------------------------------------------------------
def _pade(e, a, b):
    num = a[0] + e * (a[1] + e * (a[2] + e * (a[3] + e * a[4])))
    return num / (1 + e * (b[0] + e * (b[1] + e * (b[2] + e * b[3]))))


def s_factor(name, e, source="fit"):
    """S(E) in keV b. source='fit': our EXFOR fit (D-T, D-D); 'bh': Bosch-Hale Table IV."""
    e = np.asarray(e, float)
    if name == "p11B":
        return 1e3 * s_p11b(e)
    if name == "DHe3":
        lo, hi = EXTRA["DHe3_low"], EXTRA["DHe3_high"]
        return 1e-3 * np.where(e <= 900, _pade(e, lo["A"], lo["B"]),
                               _pade(np.minimum(e, 4800), hi["A"], hi["B"]))
    if name == "DT":
        hi = EXTRA["DT_high"]
        low = sfit.model_curve(FIT, "DT", e) if source == "fit" else sfit.bh_curve("DT", e)
        return np.where(e <= 550, low, 1e-3 * _pade(np.minimum(e, 4700), hi["A"], hi["B"]))
    return sfit.model_curve(FIT, name, e) if source == "fit" else sfit.bh_curve(name, e)


def s_p11b(e):
    """Nevins-Swain (2000) eqs. (2)-(4), S in MeV b; e in keV."""
    lo, mid, hi = PB["S_low"], PB["S_mid"], PB["S_high"]
    s_lo = (lo["C0_MeVb"] + lo["C1_MeVb"] * e + lo["C2_MeVb"] * e**2
            + lo["AL_MeVb"] / ((e - lo["EL_keV"]) ** 2 + lo["dEL_keV"] ** 2))
    x = (e - 400) / 100
    s_mid = mid["D0_MeVb"] + mid["D1_MeVb"] * x + mid["D2_MeVb"] * x**2 + mid["D5_MeVb"] * x**5
    s_hi = hi["B_MeVb"] + sum(a / ((e - ei) ** 2 + de**2)
                              for a, ei, de in zip(hi["A_MeVb"], hi["E_keV_i"], hi["dE_keV"]))
    return np.where(e <= 400, s_lo, np.where(e <= 642, s_mid, s_hi))


def b_g(name):
    if name == "p11B":
        return np.sqrt(gamow_energy_p11b())
    return BH[name]["B_G_sqrt_keV"]


def sigma(name, e, source="fit"):
    """Cross section in m^2 from S(E): sigma = S/E exp(-B_G/sqrt(E))."""
    e = np.asarray(e, float)
    return s_factor(name, e, source) / e * np.exp(-b_g(name) / np.sqrt(e)) * BARN


def mrc2_for(name):
    return PB["mrc2_keV"] if name == "p11B" else BH[name]["mrc2_keV"]


def maxwell_average(name, t, source="fit", n=40000):
    """<sigma v>(T) in m^3/s by direct quadrature of the centre-of-mass Maxwellian."""
    out = []
    for tt in np.atleast_1d(t):
        e0, _ = gamow_peak(b_g(name) ** 2, tt)
        e = np.geomspace(1e-3, max(60 * tt, 12 * e0, 2000), n)
        integrand = sigma(name, e, source) * e * np.exp(-e / tt)
        integral = np.trapezoid(integrand, e)                              # m^2 keV^2
        out.append(C * np.sqrt(8 / (np.pi * mrc2_for(name))) * tt**-1.5 * integral)
    return np.array(out)


def sample_pairs(t, n, m1, m2, rng):
    """Centre-of-mass energies (keV) and relative speeds (m/s) of n random ion pairs.

    Each ion's velocity components are drawn from its own Maxwellian at T."""
    s1, s2 = np.sqrt(t / m1), np.sqrt(t / m2)              # velocity / c
    v = rng.normal(0, s1, (n, 3)) - rng.normal(0, s2, (n, 3))
    v2 = np.sum(v**2, axis=1)
    mr = m1 * m2 / (m1 + m2)
    return 0.5 * mr * v2, np.sqrt(v2) * C


FIT = sfit.fit_all()[1]


# --- checks ------------------------------------------------------------------------------
def checks():
    # 1. Gamow energies from first principles against the Bosch-Hale B_G^2.
    for name in ("DT", "DDn", "DHe3"):
        eg = gamow_energy(name)
        assert abs(eg / BH[name]["B_G_sqrt_keV"] ** 2 - 1) < 2e-3, (name, eg)
        assert abs(reduced_mc2(name) / BH[name]["mrc2_keV"] - 1) < 1e-4, name
    eg_b = gamow_energy("p11B")               # with the Nevins-Swain reduced mass
    assert abs(eg_b / gamow_energy_p11b() - 1) < 2e-3, eg_b
    print(f"E_G: D-T {gamow_energy('DT'):.0f} keV, D-D {gamow_energy('DDn'):.0f} keV, "
          f"D-3He {gamow_energy('DHe3'):.0f} keV, p-11B {eg_b:.0f} keV (N-S {gamow_energy_p11b():.0f})")

    # 2. Gamow peak: E_0 maximises exp(-E/T - sqrt(E_G/E)) (numerical argmax).
    for name, t in (("DT", 10.0), ("pp", 1.3)):
        eg = gamow_energy(name)
        e = np.linspace(0.01, 200, 400001)
        e0, width = gamow_peak(eg, t)
        f = -e / t - np.sqrt(eg / e)
        assert abs(e[f.argmax()] - e0) < 1e-3, (name, e0)
        print(f"Gamow peak {name} at T = {t} keV: E_0 = {e0:.2f} keV, width = {width:.1f} keV")
    assert abs(gamow_peak(gamow_energy("pp"), 1.3)[0] - 6.0) < 0.1

    # 3. Bosch-Hale D-T at 10 keV and the <sigma v>/T^2 optimum.
    sv10 = float(bosch_hale("DT", 10.0))
    assert abs(sv10 / 1.1e-22 - 1) < 0.05, sv10
    t = np.linspace(5, 40, 35001)
    t_opt = t[np.argmax(bosch_hale("DT", t) / t**2)]
    assert 13 < t_opt < 15, t_opt
    print(f"Bosch-Hale D-T: <sv>(10 keV) = {sv10:.4e} m^3/s; <sv>/T^2 maximal at {t_opt:.2f} keV")
    tt = np.geomspace(10, 1000, 4001)
    print(f"   D-T <sv> maximum on 10-1000 keV: T = {tt[np.argmax(bosch_hale('DT', tt))]:.0f} keV "
          f"(parametrisation valid to 100 keV)")

    # 4. Numerical Maxwell average against Bosch-Hale, (a) with their own S(E) (quadrature
    # and parametrisation consistency), (b) with our EXFOR S-factor fit (independent data).
    temps = np.array([1, 2, 5, 10, 14, 20, 50, 100.0])
    rows = []
    for name, src, tol in (("DT", "bh", 0.01), ("DDn", "bh", 0.025), ("DDp", "bh", 0.025),
                           ("DHe3", "bh", 0.035), ("DT", "fit", 0.04), ("DDn", "fit", 0.11),
                           ("DDp", "fit", 0.13)):
        dev = maxwell_average(name, temps, src) / bosch_hale(name, temps) - 1
        rows.append((name, src, dev))
        assert np.all(np.abs(dev) < tol), (name, src, dev)
    print("Numerical <sv> / Bosch-Hale - 1 [%] at T = " + ", ".join(f"{x:g}" for x in temps) + " keV")
    for name, src, dev in rows:
        print(f"   {name:5s} {'EXFOR fit S' if src == 'fit' else 'B-H S(E)   '}: "
              + " ".join(f"{100 * d:+6.2f}" for d in dev))
    # The D-D gap follows the S factors: our fit lies 4-12 % above Bosch-Hale below 40 keV.
    e = np.array([5.0, 10, 20, 40])
    print("   S_fit/S_BH at E = 5, 10, 20, 40 keV: " + "; ".join(
        f"{n} " + " ".join(f"{x:.3f}" for x in s_factor(n, e) / s_factor(n, e, "bh"))
        for n in ("DT", "DDn", "DDp")))

    # 5. p-11B: numerical average of the Nevins-Swain S(E) against their eq. (13) fit.
    # Eq. (13) omits the narrow 148 keV resonance (their eq. (11)); without it the two
    # agree to 2 % up to 200 keV but drift to +9 % at 500 keV (open: the paper quotes
    # 0.22 %). The plots use the numerical average of their S(E).
    tb = np.array([50, 60, 100, 200, 300, 400, 500.0])
    full = maxwell_average("p11B", tb)
    dev = full / nevins_swain_fit(tb) - 1
    lo = PB["S_low"]
    peak = lo["AL_MeVb"] * np.pi / lo["dEL_keV"] * 1e3       # int of the Lorentzian, keV^2 b
    e_l = lo["EL_keV"]
    res = (C * np.sqrt(8 / (np.pi * PB["mrc2_keV"])) * tb**-1.5 * peak * BARN
           * np.exp(-np.sqrt(gamow_energy_p11b() / e_l) - e_l / tb))
    dev_nr = (full - res) / nevins_swain_fit(tb) - 1
    print("p-11B numerical / Nevins-Swain eq. (13) - 1 [%] at T = " + ", ".join(f"{t:g}" for t in tb) + " keV")
    print("   full S(E):              " + " ".join(f"{100 * d:+6.2f}" for d in dev))
    print("   minus 148 keV resonance: " + " ".join(f"{100 * d:+6.2f}" for d in dev_nr))
    assert np.all(np.abs(dev_nr[:4]) < 0.02) and np.all(np.abs(dev_nr) < 0.10), dev_nr

    # 6. Monte Carlo pair sampling reproduces <sigma v> at 10 keV.
    rng = np.random.default_rng(1)
    e, v = sample_pairs(10.0, 4_000_000, MC2["D"], MC2["T"], rng)
    w = sigma("DT", e) * v
    mc, err = w.mean(), w.std() / np.sqrt(len(w))
    assert abs(mc / sv10 - 1) < 0.03, (mc, err)
    print(f"Monte Carlo D-T <sv>(10 keV) = {mc:.4e} +- {err:.1e} m^3/s ({mc / sv10 - 1:+.2%} vs Bosch-Hale)")
    return rows


if __name__ == "__main__":
    checks()
    print("Chapter 2 reactivity checks passed")
