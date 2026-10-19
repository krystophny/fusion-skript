"""Chapter 2: SymPy checks for the Coulomb barrier and Gamow tunnelling (MIT).

Script: src/chapters/02-fusion-reactions.typ. Run:
    python3 derivations/chapters/ch02_fusion_reactions.py
Cross-section constants come from data/ch02/cross-sections.json, the source
shared with slides/figures.py.
"""
import json
import sys
from pathlib import Path

import sympy as sp
from sympy.physics import units as u

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "derivations"))
from si import check  # noqa: E402

XS = json.loads((ROOT / "data/ch02/cross-sections.json").read_text())

# CODATA 2018: fine-structure constant, hbar c and nuclear rest energies (keV).
ALPHA = 1 / sp.Rational("137.035999084")
HBAR_C_MEV_FM = sp.Rational("197.3269804")
E2_MEV_FM = ALPHA * HBAR_C_MEV_FM  # e^2/(4 pi eps0)
MC2_KEV = {"p": sp.Rational("938272.08816"), "D": sp.Rational("1875612.94257"),
           "T": sp.Rational("2808921.13298")}

E, m, c, alpha, Z1, Z2, hbar = sp.symbols("E m c alpha Z_1 Z_2 hbar", positive=True)
r, r_c, x, theta = sp.symbols("r r_c x theta", positive=True)
UNITS = {E: u.joule, m: u.kilogram, c: u.meter / u.second, alpha: 1, Z1: 1, Z2: 1,
         hbar: u.joule * u.second}


def reduced_keV(a, b):
    return MC2_KEV[a] * MC2_KEV[b] / (MC2_KEV[a] + MC2_KEV[b])


def gamow_energy_keV(a, b, z1, z2):
    return float(2 * reduced_keV(a, b) * (sp.pi * ALPHA * z1 * z2) ** 2)


def coulomb_barrier():
    """Turning point r_c from V(r_c) = E and the classical estimate (eq. ch02-turning-point)."""
    # Rutherford table: alpha on Au at 5 MeV, on Al at 7.7 MeV.
    for z, energy, expected in ((79, 5, 45), (13, sp.Rational("7.7"), 5)):
        rc = float(2 * z * E2_MEV_FM / energy)
        assert abs(rc - expected) / expected < 0.03, (z, rc)
    # Turning point at r_0 = 1 fm for Z_1 = Z_2 = 1: E = e^2/(4 pi eps0 r_0) ~ 1.4 MeV.
    assert abs(float(E2_MEV_FM) - 1.44) < 0.005
    # Animation example: D-T at 7.5 keV turns at 0.19 pm.
    assert abs(float(E2_MEV_FM / sp.Rational("0.0075")) / 1000 - 0.19) < 0.005


def quantum_ballpark():
    """lambda-bar = r_c gives E = 2 m c^2 (alpha Z1 Z2)^2 (eq. ch02-ballpark)."""
    lam = hbar / sp.sqrt(2 * m * E)
    rc = alpha * Z1 * Z2 * hbar * c / E  # e^2/(4 pi eps0) = alpha hbar c
    ratio = sp.simplify(rc / lam)
    assert sp.simplify(ratio - alpha * Z1 * Z2 * c * sp.sqrt(2 * m / E)) == 0
    assert sp.simplify(sp.diff(sp.log(ratio), E) * E + sp.Rational(1, 2)) == 0
    balance = sp.solve(sp.Eq(ratio, 1), E)
    assert len(balance) == 1
    check(balance[0], 2 * m * c**2 * (alpha * Z1 * Z2) ** 2, u.joule, UNITS)
    dt = gamow_energy_keV("D", "T", 1, 1) / float(sp.pi**2)
    assert abs(dt - 120) < 1, dt


def gamow():
    """Turning-point integral and Gamow energy (eqs. ch02-kappa ... ch02-gamow-energy)."""
    integrand = sp.sqrt(1 / x - 1)
    direct = sp.integrate(integrand, (x, 0, 1))
    # Independent route: x = sin^2(theta) turns the integrand into 2 cos^2(theta).
    substituted = sp.simplify(integrand.subs(x, sp.sin(theta) ** 2)
                              * sp.diff(sp.sin(theta) ** 2, theta))
    substituted = substituted.replace(sp.Abs, lambda a: a)  # tan(theta) > 0 on (0, pi/2)
    assert sp.simplify(substituted - 2 * sp.cos(theta) ** 2) == 0
    assert sp.simplify(direct - sp.pi / 2) == 0
    assert sp.integrate(2 * sp.cos(theta) ** 2, (theta, 0, sp.pi / 2)) == sp.pi / 2

    lam = hbar / sp.sqrt(2 * m * E)
    kappa = sp.sqrt(2 * m * (E * r_c / r - E)) / hbar
    assert sp.simplify(kappa - sp.sqrt(r_c / r - 1) / lam) == 0
    exponent = 2 * r_c / lam * sp.pi / 2  # 2 int_0^{r_c} kappa dr with r = r_c x
    rc = alpha * Z1 * Z2 * hbar * c / E
    E_G = 2 * m * c**2 * (sp.pi * alpha * Z1 * Z2) ** 2
    assert sp.simplify(exponent.subs(r_c, rc) - sp.sqrt(E_G / E)) == 0
    check(E_G / sp.pi**2, 2 * m * c**2 * (alpha * Z1 * Z2) ** 2, u.joule, UNITS)

    # Gamow energies against the Bosch-Hale / Adelberger constants in the shared data.
    bh = XS["bosch_hale"]["reactions"]
    cases = (("DT", ("D", "T"), bh["DT"]["B_G_sqrt_keV"], 1180),
             ("DD", ("D", "D"), bh["DDn"]["B_G_sqrt_keV"], 990),
             ("pp", ("p", "p"), XS["pp"]["B_G_sqrt_keV"], 490))
    for name, (a, b), bg, rounded in cases:
        eg = gamow_energy_keV(a, b, 1, 1)
        assert abs(eg - bg**2) / eg < 2e-3, (name, eg, bg**2)
        assert abs(eg - rounded) / rounded < 0.01, (name, eg)
        print(f"E_G({name}) = {eg / 1000:.4f} MeV, B_G^2 = {bg**2 / 1000:.4f} MeV")


if __name__ == "__main__":
    coulomb_barrier()
    quantum_ballpark()
    gamow()
    print("Chapter 2 Coulomb-barrier and Gamow checks passed")
