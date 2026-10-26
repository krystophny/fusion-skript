"""Chapter 2: SymPy checks for the Coulomb barrier and Gamow tunnelling (MIT).

Deck: slides/02-fusion-reactions.typ. Run:
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
    # Turning point at the contact distance R ~ 3 fm for Z_1 = Z_2 = 1: E = e^2/(4 pi eps0 R) ~ 0.5 MeV.
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


def classical_cross_section():
    """sigma_cl = pi R^2 (1 - V(R)/E) (eqs. ch02-closest-approach ... ch02-classical-cross-section)."""
    b, R, V_R, rmin = sp.symbols("b R V_R r_min", positive=True)
    # Energy at closest approach: E = V(r_min) + E b^2 / r_min^2; contact r_min = R.
    contact = sp.Eq(E, V_R + E * b**2 / R**2)
    bmax2 = sp.solve(contact, b**2)
    assert len(bmax2) == 1
    assert sp.simplify(bmax2[0] - R**2 * (1 - V_R / E)) == 0
    sigma_cl = sp.pi * bmax2[0]
    assert sp.limit(sigma_cl, E, sp.oo) == sp.pi * R**2
    assert sigma_cl.subs(E, V_R) == 0
    assert sp.simplify(sigma_cl.subs(E, 2 * V_R) - sp.pi * R**2 / 2) == 0
    # The effective Coulomb potential decreases outwards, so r_min <= R iff b <= b_max.
    v_eff = E * r_c / rmin + E * b**2 / rmin**2
    assert sp.simplify(sp.diff(v_eff, rmin) + E * r_c / rmin**2 + 2 * E * b**2 / rmin**3) == 0
    # Table: R = r_0 (A_1^(1/3) + A_2^(1/3)), r_0 = 1.2 fm; V(R) in keV; pi R^2 in b.
    r0 = sp.Rational("1.2")
    for (a1, a2), (r_fm, v_keV, area_b) in (((2, 3), (3.2, 440, 0.33)),
                                            ((2, 2), (3.0, 480, 0.29)),
                                            ((1, 1), (2.4, 600, 0.18))):
        rr = float(r0 * (sp.Integer(a1) ** sp.Rational(1, 3) + sp.Integer(a2) ** sp.Rational(1, 3)))
        assert abs(rr - r_fm) < 0.05, (a1, a2, rr)
        assert abs(float(E2_MEV_FM) / rr * 1000 - v_keV) / v_keV < 0.02, (a1, a2)
        assert abs(float(sp.pi) * rr**2 / 100 - area_b) < 0.006, (a1, a2)  # 1 b = 100 fm^2


def barrier_to_contact():
    """2 int_0^R kappa dr -> 4 sqrt(R/a) for R << r_c; a ~ 12 fm for D-T (eq. ch02-s-and-r)."""
    R, a, lam, eps = sp.symbols("R a lambdabar epsilon", positive=True)
    # kappa = sqrt(r_c/r - 1)/lambdabar and r_c / lambdabar^2 = 1/a.
    rc = lam**2 / a
    # a = 4 pi eps0 hbar^2 / (2 m Z1 Z2 e^2) = hbar / (2 m alpha Z1 Z2 c) is a length.
    a_phys = hbar / (2 * m * alpha * Z1 * Z2 * c)
    rc_phys = alpha * Z1 * Z2 * hbar * c / E
    lam_phys = hbar / sp.sqrt(2 * m * E)
    assert sp.simplify(rc_phys / lam_phys**2 - 1 / a_phys) == 0
    check(a_phys, rc_phys * a_phys / rc_phys, u.meter, UNITS)
    # Exact integral with r = r_c x up to eps = R / r_c (0 < eps < 1):
    # int_0^eps sqrt(1/x - 1) dx = asin(sqrt(eps)) + sqrt(eps (1 - eps)).
    inner = sp.asin(sp.sqrt(eps)) + sp.sqrt(eps * (1 - eps))
    assert sp.simplify(sp.diff(inner, eps) ** 2 - (1 / eps - 1)) == 0
    assert inner.subs(eps, 0) == 0 and inner.subs(eps, 1) == sp.pi / 2
    series = sp.series(inner, eps, 0, 1).removeO()
    assert sp.simplify(series - 2 * sp.sqrt(eps)) == 0
    leading = (rc / lam) * 2 * sp.sqrt(R / rc)  # int_0^R kappa dr
    assert sp.simplify(leading - 2 * sp.sqrt(R / a)) == 0
    # Numerically: the exact integral approaches 2 sqrt(R/a) when R << r_c.
    a_v, R_v = 12.0, 3.2
    lam_v = (1000 * a_v) ** 0.5  # r_c = 1000 a = 12000 fm >> R
    exact = float(lam_v / a_v * inner.subs(eps, R_v * a_v / lam_v**2))
    assert abs(exact - 2 * (R_v / a_v) ** 0.5) / exact < 0.01, exact
    # Bohr length of the pair a = (hbar c)^2 / (2 m c^2 e^2/(4 pi eps0)) for D-T: ~ 12 fm.
    a_dt = float(HBAR_C_MEV_FM**2 / (2 * reduced_keV("D", "T") / 1000 * E2_MEV_FM))
    assert abs(a_dt - 12.0) < 0.1, a_dt
    enhancement = float(sp.exp(4 * sp.sqrt(sp.Rational("3.24") / a_dt)))
    assert 7.5 < enhancement < 8.5, enhancement
    print(f"a(DT) = {a_dt:.2f} fm, exp(4 sqrt(R/a)) = {enhancement:.2f}")


def force_ranges():
    """Yukawa ranges lambda = hbar/(m c) for the pion and the W boson (eq. ch02-force-range)."""
    check(hbar / (m * c), hbar / (m * c), u.meter, UNITS)
    # PDG masses: m_pi+ c^2 = 139.570 MeV, M_W c^2 = 80.37 GeV (80.4 GeV in the text).
    lam_pi = float(HBAR_C_MEV_FM / sp.Rational("139.57039"))
    lam_w = float(HBAR_C_MEV_FM / sp.Rational("80369.2"))
    assert abs(lam_pi - 1.41) < 0.005, lam_pi
    assert abs(lam_w / 2.45e-3 - 1) < 0.005, lam_w
    assert abs(float(HBAR_C_MEV_FM / 80400) - 2.45e-3) < 0.005e-3
    # Yukawa potential solves (nabla^2 - 1/lambda^2) phi = 0 for r > 0.
    lam = sp.symbols("lambda", positive=True)
    phi = sp.exp(-r / lam) / r
    assert sp.simplify(sp.diff(r * phi, r, 2) / r - phi / lam**2) == 0
    print(f"hbar/(m_pi c) = {lam_pi:.3f} fm, hbar/(M_W c) = {lam_w:.3e} fm")


if __name__ == "__main__":
    coulomb_barrier()
    quantum_ballpark()
    gamow()
    classical_cross_section()
    barrier_to_contact()
    force_ranges()
    print("Chapter 2 Coulomb-barrier, Gamow, classical cross-section and force-range checks passed")
