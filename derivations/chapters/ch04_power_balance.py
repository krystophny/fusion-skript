"""Chapter 4: alpha/neutron split and the 0-D power balance of a D-T plasma (MIT).

Run:  python3 derivations/chapters/ch04_power_balance.py
Shared with slides/figures_power_balance.py.

Model (stated assumptions): 50:50 D-T, n_D = n_T = n/2, n_e = n, T_e = T_i = T,
uniform profiles, steady state. Stored energy W = 3 n T per volume, loss W/tau_E.
    p_fus = n_D n_T <sigma v> E_fus = n^2 <sigma v> E_fus / 4,  p_alpha = p_fus E_alpha/E_fus
    Q = P_fus / P_ext
    3 n T / tau_E + p_brems = p_alpha + p_ext = (n^2 <sigma v>/4) (E_alpha + E_fus/Q)
=>  n T tau_E = 12 T^2 / (<sigma v> (E_alpha + E_fus/Q) - 4 C_B sqrt(T))
with bremsstrahlung p_brems = C_B n_e^2 sqrt(T) (Z_eff = 1); without it C_B = 0.
<sigma v>: Bosch and Hale (1992); C_B: NRL Plasma Formulary (2018), eq. (30) p. 58,
1.69e-32 W cm^3 eV^(-1/2) = 5.34e-37 W m^3 keV^(-1/2).

Also: dilution by impurities (quasineutrality n_e = n_D + n_T + sum Z n_Z), the
fixed-pressure form p_fus = p^2 <sigma v> E_fus / (16 T^2), Lawson's 1957
conversion loop against alpha self-heating, the engineering gain
Q_eng = eta_th eta_aux (Q + 1) - 1, and the measured Lawson parameters of
Wurzel and Hsu, Phys. Plasmas 29, 062103 (2022), doi:10.1063/5.0083990 (CC BY 4.0),
read from data/ch04/wurzel_hsu_2022.csv.
"""
import csv
import sys
from pathlib import Path

import numpy as np
from scipy import constants as k

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ch02_reactivity import KEV, MC2, bosch_hale  # noqa: E402

C_B = 1.69e-32 * 1e-6 * np.sqrt(1e3)        # W m^3 keV^(-1/2)
ROOT = Path(__file__).resolve().parents[2]


def two_body_split():
    """Kinetic energies (keV) of alpha and neutron from D + T at rest, exact relativistic."""
    q = MC2["D"] + MC2["T"] - MC2["He4"] - MC2["n"]
    m_tot = MC2["D"] + MC2["T"]                       # invariant mass, CM at rest
    e_a = (m_tot**2 + MC2["He4"] ** 2 - MC2["n"] ** 2) / (2 * m_tot) - MC2["He4"]
    return q, e_a, q - e_a


E_FUS, E_ALPHA, E_N = two_body_split()               # keV


def triple_product(t, q=np.inf, brems=False):
    """Required n T tau_E in keV s m^-3 for gain Q at temperature t (keV)."""
    t = np.asarray(t, float)
    heat = bosch_hale("DT", t) * (E_ALPHA + (0 if np.isinf(q) else E_FUS / q)) * KEV   # W m^3
    loss = 4 * C_B * np.sqrt(t) if brems else 0.0
    net = heat - loss
    out = np.full_like(t, np.inf)
    ok = net > 0
    out[ok] = 12 * t[ok] ** 2 * KEV / net[ok]                                       # keV s m^-3
    return out


def ideal_ignition_temperature(z_eff=1.0):
    """T (keV) where alpha heating equals bremsstrahlung, 50:50 D-T; independent of n."""
    tt = np.linspace(2, 20, 180001)
    return tt[np.argmax(bosch_hale("DT", tt) * E_ALPHA * KEV > 4 * C_B * z_eff * np.sqrt(tt))]


def dilution(impurities):
    """Fuel fraction (n_D + n_T)/n_e, ion fraction n_i/n_e and Z_eff for [(Z, n_Z/n_e), ...]."""
    fuel = 1 - sum(z * c for z, c in impurities)
    ions = fuel + sum(c for _, c in impurities)
    z_eff = fuel + sum(z * z * c for z, c in impurities)
    return fuel, ions, z_eff


def ignition_diluted(t, impurities=()):
    """Ignition n_e T tau_E (keV s m^-3) with fuel dilution and bremsstrahlung (fully stripped)."""
    t = np.asarray(t, float)
    fuel, ions, z_eff = dilution(impurities)
    net = fuel**2 / 4 * bosch_hale("DT", t) * E_ALPHA * KEV - C_B * z_eff * np.sqrt(t)
    out = np.full_like(t, np.inf)
    ok = net > 0
    out[ok] = 1.5 * (1 + ions) * t[ok] ** 2 * KEV / net[ok]
    return out


def q_eng(q, eta_th=0.4, eta_aux=0.4):
    """Engineering gain: all fusion and heating power to heat at eta_th; heating from the grid at eta_aux."""
    return eta_th * eta_aux * (np.asarray(q, float) + 1) - 1


def n_tau(t, q=np.inf):
    """Required n tau_E (s m^-3) at temperature t (keV), no radiation."""
    return triple_product(np.atleast_1d(t), q) / np.atleast_1d(t)


def machines(path=None):
    """Measured Lawson parameters (Wurzel and Hsu 2022, Tables 6-8); projections excluded."""
    path = path or ROOT / "data/ch04/wurzel_hsu_2022.csv"
    rows = []
    with open(path) as f:
        for r in csv.DictReader(line for line in f if not line.startswith("#")):
            if r["shot"] == "Projected" or not r["n_m3"] or not r["tau_s"]:
                continue
            rows.append(dict(r, n=float(r["n_m3"]), tau=float(r["tau_s"]), year=int(r["year"])))
    return rows


def kelvin_helmholtz_time():
    """Thermal energy content of the Sun over its luminosity, G M^2 / (R L), in s (IAU 2015 nominal)."""
    gm, r, lum = 1.3271244e20, 6.957e8, 3.828e26
    return gm * (gm / k.G) / (r * lum)


def sun_mean_density():
    """Mean mass density of the Sun in kg/m^3 (IAU 2015 nominal GM and R)."""
    gm, r = 1.3271244e20, 6.957e8
    return gm / k.G / (4 / 3 * np.pi * r**3)


def symbolic_checks():
    """Every formula on the chapter-4 slides (SymPy)."""
    import sympy as sp
    m_a, m_n, Qdt, p = sp.symbols("m_alpha m_n Q_DT p", positive=True)
    n, ne, T, tau, sv, Ea, Ef, Q, x = sp.symbols("n n_e T tau_E sigmav E_alpha E_fus Q x", positive=True)
    CB, Zeff, eta, eth, eaux, c, Z = sp.symbols("C_B Z_eff eta eta_th eta_aux c Z", positive=True)
    pr, beta, B, mu0, V = sp.symbols("p_th beta B mu_0 V", positive=True)

    # 4.1 Momentum conservation from rest: |p_alpha| = |p_n|, E = p^2/(2m).
    e_a, e_n = p**2 / (2 * m_a), p**2 / (2 * m_n)
    assert sp.simplify(e_a / e_n - m_n / m_a) == 0
    psol = sp.solve(sp.Eq(e_a + e_n, Qdt), p)[0]
    assert sp.simplify(e_a.subs(p, psol) - Qdt * m_n / (m_a + m_n)) == 0

    # 4.2 n_D = n_T = n_e/2 from n_e = n_D + n_T; the product x(1-x) is maximal at x = 1/2.
    assert sp.simplify((ne / 2) * (ne / 2) - ne**2 / 4) == 0
    assert sp.solve(sp.diff(x * (1 - x), x), x) == [sp.Rational(1, 2)]

    # 4.3 W = (3/2) n_e T + (3/2) n_i T = 3 n T for n_e = n_i = n.
    assert sp.simplify(sp.Rational(3, 2) * n * T * 2 - 3 * n * T) == 0

    # 4.4 Ideal ignition: n^2 cancels in p_alpha = p_br.
    p_alpha = n**2 / 4 * sv * Ea
    p_br = CB * n**2 * Zeff * sp.sqrt(T)
    assert sp.simplify((p_alpha / p_br).diff(n)) == 0

    # 4.5 Balance P_ext + P_alpha = W/tau_E with P_ext = P_fus/Q.
    p_fus = n**2 / 4 * sv * Ef
    tau_sol = sp.solve(sp.Eq(p_fus / Q + p_alpha, 3 * n * T / tau), tau)[0]
    assert sp.simplify(n * tau_sol - 12 * T / (sv * (Ea + Ef / Q))) == 0
    # Self-heating fraction f_alpha = P_alpha/(P_alpha + P_ext) = Q/(Q + E_fus/E_alpha).
    f_a = sp.simplify(p_alpha / (p_alpha + p_fus / Q))
    assert sp.simplify(f_a - Q / (Q + Ef / Ea)) == 0
    assert f_a.subs({Ef: 5 * Ea, Q: 5}) == sp.Rational(1, 2)      # burning plasma: Q = 5
    assert f_a.subs({Ef: 5 * Ea, Q: 1}) == sp.Rational(1, 6)      # breakeven
    # n tau_E(Q)/n tau_E(ignition) = Q/(Q + E_fus/E_alpha).
    ratio = (12 * T / (sv * (Ea + Ef / Q))) / (12 * T / (sv * Ea))
    assert sp.simplify(ratio - Q / (Q + Ef / Ea)) == 0
    # <sigma v> = a T^2 makes n T tau_E independent of T: 12/(a (E_alpha + E_fus/Q)).
    a = sp.symbols("a", positive=True)
    assert sp.diff(T * 12 * T / (a * T**2 * (Ea + Ef / Q)), T) == 0
    # With bremsstrahlung: n T tau_E = 12 T^2 / (<sigma v>(E_alpha + E_fus/Q) - 4 C_B sqrt(T)).
    tau_b = sp.solve(sp.Eq(p_fus / Q + p_alpha, 3 * n * T / tau + CB * n**2 * sp.sqrt(T)), tau)[0]
    assert sp.simplify(n * T * tau_b - 12 * T**2 / (sv * (Ea + Ef / Q) - 4 * CB * sp.sqrt(T))) == 0
    # Pressure p = 2 n T, so p tau_E = 2 n T tau_E.
    assert sp.simplify(2 * n * T * tau - 2 * (n * T * tau)) == 0

    # 4.6 Lawson 1957: all output converted at eta and returned as heating,
    # eta (P_fus + P_loss) = P_loss  =>  P_fus/P_loss = (1 - eta)/eta.
    P_loss, P_f = sp.symbols("P_loss P_f", positive=True)
    sol = sp.solve(sp.Eq(eta * (P_f + P_loss), P_loss), P_f)[0]
    assert sp.simplify(sol / P_loss - (1 - eta) / eta) == 0
    assert ((1 - eta) / eta).subs(eta, sp.Rational(1, 3)) == 2
    tau_l = sp.solve(sp.Eq(p_fus, (1 - eta) / eta * 3 * n * T / tau), tau)[0]
    assert sp.simplify(n * tau_l - 12 * T / (sv * Ef * eta / (1 - eta))) == 0
    # Q_eng: gross electric eta_th (P_fus + P_ext), recirculated P_ext/eta_aux.
    P_ext = sp.symbols("P_ext", positive=True)
    q_e = (eth * (Q * P_ext + P_ext) - P_ext / eaux) / (P_ext / eaux)
    assert sp.simplify(q_e - (eth * eaux * (Q + 1) - 1)) == 0
    assert sp.solve(sp.Eq(eth * eaux * (Q + 1) - 1, 0), Q)[0] == 1 / (eth * eaux) - 1
    assert sp.solve(sp.Eq(eth * eaux * (Q + 1) - 1, 1), Q)[0] == 2 / (eth * eaux) - 1

    # 4.7 Quasineutrality with one impurity of charge Z and c = n_Z/n_e:
    # n_D + n_T = n_e (1 - Z c), Z_eff = sum n_j Z_j^2 / n_e = (1 - Z c) + Z^2 c.
    nf = sp.solve(sp.Eq(ne, sp.Symbol("n_f") + Z * c * ne), sp.Symbol("n_f"))[0]
    assert sp.simplify(nf - ne * (1 - Z * c)) == 0
    assert sp.simplify((nf * 1 + c * ne * Z**2) / ne - ((1 - Z * c) + Z**2 * c)) == 0
    # Fusion power at fixed n_e: (n_f/2)^2 = (1 - Z c)^2 n_e^2/4.
    assert sp.simplify((nf / 2) ** 2 - (1 - Z * c) ** 2 * ne**2 / 4) == 0
    w_c = sp.Rational(1, 1000)
    assert sp.Rational(1, 1) - 74 * w_c == sp.Rational(926, 1000)
    # Diluted ignition reduces to the pure formula for c = 0 (with bremsstrahlung).
    f, ions = 1 - Z * c, 1 - Z * c + c
    dil = sp.Rational(3, 2) * (1 + ions) * T**2 / (f**2 / 4 * sv * Ea - CB * (f + Z**2 * c) * sp.sqrt(T))
    assert sp.simplify(dil.subs(c, 0) - 12 * T**2 / (sv * Ea - 4 * CB * sp.sqrt(T))) == 0

    # 4.8 Fixed pressure p = 2 n T: p_fus = p^2 <sigma v> E_fus / (16 T^2);
    # with beta = 2 mu_0 p / B^2: P_fus = E_fus beta^2 B^4 V <sigma v> / (64 mu_0^2 T^2).
    p_fixed = p_fus.subs(n, pr / (2 * T))
    assert sp.simplify(p_fixed - pr**2 * sv * Ef / (16 * T**2)) == 0
    P_beta = (p_fixed * V).subs(pr, beta * B**2 / (2 * mu0))
    assert sp.simplify(P_beta - Ef * beta**2 * B**4 * V * sv / (64 * mu0**2 * T**2)) == 0
    print("Chapter 4 symbolic checks passed")


def checks():
    q, e_a, e_n = two_body_split()
    # Non-relativistic partition: equal and opposite momenta, E_alpha/E_n = m_n/m_alpha.
    nr_a = q * MC2["n"] / (MC2["n"] + MC2["He4"])
    # Relativity moves 20 keV to the alpha: E_n (E_n + 2 m_n c^2) = E_a (E_a + 2 m_a c^2).
    assert abs(e_a / nr_a - 1) < 7e-3, (e_a, nr_a)
    assert abs(e_a * (e_a + 2 * MC2["He4"]) / (e_n * (e_n + 2 * MC2["n"])) - 1) < 1e-12
    assert abs(q - 17589) < 1 and abs(e_a - 3.5e3) < 70 and abs(e_n - 14.1e3) < 80
    print(f"Q = {q:.1f} keV; E_alpha = {e_a:.1f} keV, E_n = {e_n:.1f} keV (relativistic); "
          f"non-relativistic E_alpha = {nr_a:.1f} keV; E_alpha/Q = {e_a / q:.4f}")

    t = np.geomspace(2, 200, 20001)
    for brems in (False, True):
        ign = triple_product(t, brems=brems)
        i = np.argmin(ign)
        print(f"ignition{' + bremsstrahlung' if brems else ''}: min n T tau_E = {ign[i]:.3e} "
              f"keV s m^-3 at T = {t[i]:.2f} keV; n tau_E there = {ign[i] / t[i]:.3e} s m^-3")
        if not brems:
            assert abs(ign[i] / 3e21 - 1) < 0.1 and 13 < t[i] < 15, (ign[i], t[i])
    # Ideal ignition temperature: alpha heating equals bremsstrahlung.
    tt = np.linspace(2, 10, 80001)
    ideal = tt[np.argmax(bosch_hale("DT", tt) * E_ALPHA * KEV > 4 * C_B * np.sqrt(tt))]
    assert 4.0 < ideal < 4.6, ideal
    print(f"ideal ignition (p_alpha = p_brems, Z_eff = 1): T = {ideal:.2f} keV")
    for qq in (1, 5, 10):
        v = triple_product(t, qq)
        print(f"Q = {qq:>2}: min n T tau_E = {v.min():.3e} keV s m^-3 at {t[v.argmin()]:.1f} keV")
    # Q from the balance: Q = 5 x/(1 - x) with x = n T tau_E / (n T tau_E)_ign at fixed T.
    t0 = np.array([14.0])
    for qq in (1.0, 10.0):
        x = triple_product(t0, qq)[0] / triple_product(t0)[0]
        assert abs(E_FUS / E_ALPHA * x / (1 - x) - qq) < 1e-9
    print(f"n T tau_E(Q) / n T tau_E(ignition) = Q / (Q + E_fus/E_alpha), E_fus/E_alpha = {E_FUS / E_ALPHA:.3f}")

    # Bremsstrahlung constant in keV units (NRL: 1.69e-32 W cm^3 eV^-1/2): the eV value
    # used with T in keV would be 31.6 times too small.
    assert abs(C_B / 5.344e-37 - 1) < 1e-3
    ideal = ideal_ignition_temperature()
    assert abs(ideal - 4.3) < 0.1, ideal
    # The ignition minimum in n T tau_E converted to pressure units: n T tau_E and p tau_E = 2 n T tau_E.
    i = triple_product(t).argmin()
    nttau = triple_product(t)[i] * KEV
    print(f"n T tau_E = {nttau:.3e} Pa s = {nttau / 1e5:.1f} bar s; p tau_E = {2 * nttau / 1e5:.1f} bar s")
    assert 4.0e5 < nttau < 4.8e5
    # The lecture approximation <sigma v> = 1.1e-24 T^2 m^3/s gives 12/(1.1e-24 E_alpha).
    approx = 12 / (1.1e-24 * E_ALPHA)
    assert abs(approx / 3.06e21 - 1) < 0.01, approx
    # Fusion power density at n_e = 1e20 m^-3, 14 keV.
    p14 = 1e40 / 4 * bosch_hale("DT", 14.0) * E_FUS * KEV
    print(f"p_fus(n_e = 1e20 m^-3, 14 keV) = {p14 / 1e6:.2f} MW/m^3")
    assert 1.6e6 < p14 < 1.8e6
    # n tau_E for ignition and breakeven at 14 keV; minimum of n tau_E over T.
    nt_i, nt_1 = n_tau(14.0)[0], n_tau(14.0, 1.0)[0]
    tt = np.geomspace(5, 100, 20001)
    nt = n_tau(tt)
    print(f"n tau_E at 14 keV: ignition {nt_i:.2e}, Q = 1 {nt_1:.2e} s m^-3; "
          f"minimum {nt.min():.2e} at {tt[nt.argmin()]:.1f} keV")
    assert 1.9e20 < nt_i < 2.0e20 and 3.2e19 < nt_1 < 3.4e19
    # Lawson 1957 with eta = 1/3: P_fus = 2 P_loss, so (n tau_E)_Lawson/(n tau_E)_ign = E_alpha/(E_fus/2).
    print(f"Lawson (eta = 1/3) needs {E_ALPHA / (E_FUS / 2):.2f} of the ignition n tau_E")
    # Self-heating fraction and engineering gain.
    for qq, fa in ((1, 0.168), (5, 0.503), (10, 0.669)):
        assert abs(qq / (qq + E_FUS / E_ALPHA) - fa) < 2e-3
    assert abs(q_eng(1 / 0.16 - 1)) < 1e-12 and abs(q_eng(2 / 0.16 - 1) - 1) < 1e-12
    print(f"Q_eng (0.4, 0.4): zero at Q = {1 / 0.16 - 1:.2f}, one at Q = {2 / 0.16 - 1:.2f}, "
          f"{q_eng(10.0):.2f} at Q = 10")
    # Dilution: 0.1 % tungsten (fully stripped bookkeeping) and 5 % helium ash.
    fw, _, zw = dilution([(74, 1e-3)])
    fh, _, zh = dilution([(2, 0.05)])
    assert abs(fw - 0.926) < 1e-12 and abs(1 - fw**2 - 0.1425) < 1e-3
    print(f"W 0.1 %: fuel {fw:.3f}, p_fus x {fw**2:.3f} ({100 * (1 - fw**2):.1f} % less), Z_eff {zw:.2f}; "
          f"He 5 %: fuel {fh:.2f}, p_fus x {fh**2:.2f}, Z_eff {zh:.2f}")
    for c in (0.05, 0.10):
        v = ignition_diluted(t, [(2, c)])
        print(f"ignition with {100 * c:.0f} % He: min {v.min():.2e} at {t[v.argmin()]:.1f} keV")
    assert np.allclose(ignition_diluted(t), triple_product(t, brems=True), rtol=1e-12)
    # Fixed pressure: the maximum of <sigma v>/T^2 near 13.5 keV, of <sigma v> near 65-70 keV.
    tp = np.linspace(5, 100, 95001)
    t_p, t_n = tp[np.argmax(bosch_hale("DT", tp) / tp**2)], tp[np.argmax(bosch_hale("DT", tp))]
    assert 13 < t_p < 14 and 60 < t_n < 75
    print(f"fixed p: maximum at {t_p:.1f} keV; fixed n: maximum at {t_n:.1f} keV")
    # Greenwald: n_G [1e20 m^-3] = I_p [MA] / (pi a^2 [m^2]); e.g. 1 MA, a = 0.5 m -> 1.27e20.
    assert abs(1 / (np.pi * 0.25) - 1.273) < 1e-3
    # Sun: thermal content over luminosity ~ 3e7 years.
    tk = kelvin_helmholtz_time()
    assert 0.9e15 < tk < 1.1e15
    print(f"Sun: G M^2/(R L) = {tk:.2e} s = {tk / 3.156e7:.2e} yr")
    rows = machines()
    assert len(rows) > 60 and all(r["n"] > 0 and r["tau"] > 0 for r in rows)
    # Table consistency: n tau equals the tabulated Lawson parameter to the table's rounding.
    for r in rows:
        assert abs(r["n"] * r["tau"] / float(r["n_tau_m3s"]) - 1) < 0.06, r["project"]
    print(f"Wurzel-Hsu measured points: {len(rows)}")


if __name__ == "__main__":
    symbolic_checks()
    checks()
    print("Chapter 4 power-balance checks passed")
