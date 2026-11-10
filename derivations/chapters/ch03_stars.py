"""Chapter 3: fusion in stars (MIT).

Run:  python3 derivations/chapters/ch03_stars.py
Model functions are shared with slides/figures_stars.py and the stars widgets.
Units: SI unless named (keV, MeV in names); k_B T is written T.

Data (data/ch03/, provenance in data/ch03/README.md): Model S of the present
Sun (Christensen-Dalsgaard et al. 1996), MIST v1.2 tracks (Dotter 2016; Choi
et al. 2016), LINX primordial nucleosynthesis (Giovanetti et al. 2025),
AME2020 atomic masses (Wang et al. 2021), solar-system abundances (Asplund,
Amarsi & Grevesse 2021), solar neutrino fluxes B16-GS98 (Vinyoles et al. 2017)
and S factors from Adelberger et al., Rev. Mod. Phys. 83, 195 (2011).
"""
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import sympy as sp
from scipy import constants as k
from scipy.optimize import brentq
from scipy.special import zeta

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/ch03"
OUT = ROOT / "derivations/build/plotdata"

G, C, HBAR, KB, MU, ME, MP = k.G, k.c, k.hbar, k.k, k.atomic_mass, k.m_e, k.m_p
KEV, MEV = 1e3 * k.e, 1e6 * k.e
YEAR = 365.25 * 86400
ALPHA = k.fine_structure
BARN = 1e-28
M_SUN, R_SUN, L_SUN = 1.98892e30, 6.957e8, 3.828e26     # IAU 2015 nominal R, L; M from GM_sun / G

SUN = json.loads((DATA / "solar-model.json").read_text())


# ------------------------------------------------------------------ AME2020 ---
@lru_cache
def ame():
    """{(Z, A): (symbol, mass excess keV, binding energy per nucleon keV)} from AME2020."""
    out = {}
    for line in (DATA / "ame2020-mass_1.mas20").read_text().splitlines()[36:]:
        if len(line) < 60:
            continue
        try:
            z, a = int(line[9:14]), int(line[14:19])
            dm = float(line[28:42].replace("#", "."))
            ba = float(line[54:67].replace("#", "."))
        except ValueError:
            continue
        estimated = "#" in line[28:67]
        out[(z, a)] = (line[20:22].strip(), dm, ba, estimated)
    return out


def atomic_mass_u(z, a):
    return a + ame()[(z, a)][1] * KEV / (MU * C**2)


def q_value_mev(initial, final):
    """Q in MeV from atomic masses; initial/final are lists of (Z, A)."""
    dm = sum(atomic_mass_u(*x) for x in initial) - sum(atomic_mass_u(*x) for x in final)
    return dm * MU * C**2 / MEV


# --------------------------------------------------- non-resonant reaction rate ---
def gamow_energy_kev(z1, z2, mr_u):
    return 2 * mr_u * MU * C**2 / KEV * (np.pi * ALPHA * z1 * z2) ** 2


def sigma_v(z1, z2, a1, a2, s0_kev_b, t_kev, s1_per_kev=0.0, n=20000):
    """Maxwellian <sigma v> in m^3/s for sigma = S(E)/E exp(-sqrt(E_G/E)), S = S0 (1 + S1 E)."""
    mr = a1 * a2 / (a1 + a2)
    eg = gamow_energy_kev(z1, z2, mr)
    out = []
    for t in np.atleast_1d(t_kev):
        e0 = (eg * t * t / 4) ** (1 / 3)
        e = np.linspace(max(e0 / 50, 1e-4), 8 * e0 + 30 * t, n)
        s = s0_kev_b * (1 + s1_per_kev * e) * BARN * KEV          # J m^2
        integrand = s * np.exp(-e / t - np.sqrt(eg / e))           # sigma * E with E in keV -> J m^2
        integral = np.trapezoid(integrand, e) * KEV                # J^2 m^2
        out.append(np.sqrt(8 / (np.pi * mr * MU)) * (t * KEV) ** -1.5 * integral)
    return np.array(out)


# Adelberger et al. (2011): S11(0) = 4.01e-25 MeV b, S'/S = 11.2/MeV; S114(0) = 1.66 keV b.
S_PP, S1_PP = 4.01e-22, 11.2e-3
S_N14 = 1.66
Q_PP_CHAIN = 26.2      # MeV deposited per 4He in pp I (26.73 MeV minus 2 x 0.265 MeV neutrinos)
Q_CNO = 25.0           # MeV deposited per 4He in the CN cycle (26.73 MeV minus 0.71 + 0.996 MeV neutrinos)


def eps_pp(rho, x, t_kev):
    """pp-chain heating in W/kg: r_pp = n_p^2/2 <sigma v>; two pp reactions per 4He."""
    n_p = rho * x / MP
    return n_p**2 / 2 * sigma_v(1, 1, 1.00728, 1.00728, S_PP, t_kev, S1_PP) * Q_PP_CHAIN / 2 * MEV / rho


def eps_cno(rho, x, x_cno, t_kev):
    """CN-cycle heating in W/kg, rate set by 14N(p,gamma)15O with all CNO nuclei as 14N."""
    n_p, n_n = rho * x / MP, rho * x_cno / (14 * MU)
    return n_p * n_n * sigma_v(1, 7, 1.00728, 13.9992, S_N14, t_kev) * Q_CNO * MEV / rho


def cno_mass_fraction(x=0.7121):
    """Initial C+N+O mass fraction from Asplund et al. (2021) with X_initial = 0.7121."""
    ab = {e["element"]: e["log_eps"] for e in json.loads((DATA / "abundances.json").read_text())["elements"]}
    a = {"C": 12.011, "N": 14.007, "O": 15.999}
    return x * sum(10 ** (ab[el] - 12) * a[el] for el in a) / 1.008


# --------------------------------------------------------------------- Sun ---
def sun_numbers():
    c = SUN["centre"]
    t_kh = G * M_SUN**2 / (R_SUN * L_SUN) / YEAR
    dm = (4 * atomic_mass_u(1, 1) - atomic_mass_u(2, 4)) / (4 * atomic_mass_u(1, 1))
    t_nuc = 0.1 * dm * M_SUN * C**2 / L_SUN / YEAR
    t_c = KB * c["T_K"] / KEV
    y_c = 1 - c["X"] - 0.02
    n_ion = c["rho_kg_m3"] / MU * (c["X"] / 1.008 + y_c / 4.0026)
    n_e = c["rho_kg_m3"] / MU * (c["X"] / 1.008 + 2 * y_c / 4.0026)
    p_c = c["eps_W_kg"] * c["rho_kg_m3"]
    # Energy confinement: thermal energy (virial: half the gravitational binding) over L.
    w_th = 0.5 * 3 / (5 - 3.0) * G * M_SUN**2 / R_SUN        # polytrope n = 3: |U| = 3/(5-n) GM^2/R
    tau_e = w_th / L_SUN
    return dict(t_kh_yr=t_kh, mass_defect=dm, t_nuc_yr=t_nuc, T_c_keV=t_c, n_ion=n_ion, n_e=n_e,
                p_c=p_c, tau_E_s=tau_e, tau_E_yr=tau_e / YEAR,
                triple=n_ion * t_c * tau_e, virial_mean_T_keV=0.2 * G * M_SUN * 0.62 * MU / R_SUN / KEV)


def model_s_luminosity():
    """Our pp + CNO heating integrated over Model S's T, rho, X, in units of the model L."""
    p = SUN["profile"]
    r, m = np.array(p["r_over_R"]), np.array(p["m_over_M"]) * SUN["M_kg"]
    core = r < 0.35
    t = np.array(p["T_K"])[core] * KB / KEV
    rho, x = np.array(p["rho_kg_m3"])[core], np.array(p["X"])[core]
    x_cno = cno_mass_fraction()
    e = [eps_pp(rho[i], x[i], t[i])[0] + eps_cno(rho[i], x[i], x_cno, t[i])[0] for i in range(len(t))]
    return float(np.trapezoid(e, m[core]) / SUN["L_W"])


# ------------------------------------------------------------ solar neutrinos ---
NU = json.loads((DATA / "neutrinos.json").read_text())


def pp_branches():
    """Fractions of 4He made by pp I, II, III from the B16 neutrino fluxes.

    Per 4He: pp I uses two pp (or pep) reactions, pp II and III one each and
    make one 7Be; pp III makes one 8B. With f = (II + III) share,
    Phi(7Be)/Phi(pp + pep) = f/(2 - f) and Phi(8B)/Phi(pp + pep) = f_III/(2 - f).
    """
    f = NU["fluxes"]
    pp = f["pp"] + f["pep"]
    r = f["Be7"] / pp
    f23 = 2 * r / (1 + r)
    f3 = f["B8"] / pp * (2 - f23)
    return {"ppI": 1 - f23, "ppII": f23 - f3, "ppIII": f3}


def beta_spectrum(q_mev, e_nu, z_daughter=0):
    """Allowed beta+ neutrino spectrum dN/dE_nu (unnormalised), non-relativistic Fermi function."""
    me = ME * C**2 / MEV
    t = q_mev - e_nu                                    # positron kinetic energy
    w = t + me
    p = np.sqrt(np.clip(w * w - me * me, 0, None))
    eta = -z_daughter * ALPHA * w / np.where(p > 0, p, 1)
    fermi = np.where(p > 0, 2 * np.pi * eta / np.expm1(2 * np.pi * eta), 0) if z_daughter else 1.0
    return np.where((e_nu > 0) & (t > 0), e_nu**2 * p * w * fermi, 0.0)


def neutrino_spectra(e):
    """{source: flux per MeV at Earth [cm^-2 s^-1 MeV^-1]} for the continuum sources."""
    # Q of the neutrino-emitting step (MeV) and daughter charge; 8B decays to the broad
    # 3.0 MeV 8Be state, approximated by a single allowed branch with Q = 14.02 MeV.
    q = {"pp": (0.4202, 1), "N13": (1.1985, 6), "O15": (1.7317, 7), "F17": (1.7395, 8),
         "B8": (14.02, 4), "hep": (18.773, 2)}
    out = {}
    for name, (qq, z) in q.items():
        shape = beta_spectrum(qq, e, z)
        out[name] = NU["fluxes"][name] * shape / np.trapezoid(shape, e)
    return out


# --------------------------------------------------------------------- BBN ---
Q_NP_MEV = (k.m_n - k.m_p) * C**2 / MEV
B_D_MEV = (atomic_mass_u(0, 1) + atomic_mass_u(1, 1) - atomic_mass_u(1, 2)) * MU * C**2 / MEV
TAU_N = 878.4        # s, PDG 2024


def deuterium_saha_T(eta):
    """T [MeV] at which n_D = n_n in Saha equilibrium of n + p <-> D + gamma."""
    m_n = 939.0                                         # MeV, nucleon mass
    def f(t):
        n_gamma_over_t3 = 2 * zeta(3) / np.pi**2
        return np.log(0.75 * (4 * np.pi / (m_n * t)) ** 1.5 * eta * n_gamma_over_t3 * t**3) + B_D_MEV / t
    return brentq(f, 0.01, 1.0)


def helium_estimate(t_freeze=0.8, t_d=None, eta=6.1e-10):
    """n/p frozen at T_f, neutron decay until the deuterium bottleneck opens, Y_p = 2x/(1+x)."""
    x_f = np.exp(-Q_NP_MEV / t_freeze)
    bbn = json.loads((DATA / "bbn.json").read_text())
    run = next(r for r in bbn["runs"] if r["N_nu"] == 3)
    t_s, t_mev = np.array(bbn["t_s"]), np.array(run["T_MeV"])
    if t_d is None:
        t_d = deuterium_saha_T(eta)
    time_d = float(np.interp(-t_d, -t_mev, t_s))
    time_f = float(np.interp(-t_freeze, -t_mev, t_s))
    x_d = x_f * np.exp(-(time_d - time_f) / TAU_N)
    return dict(n_over_p_freeze=x_f, T_D=t_d, t_D=time_d, n_over_p_D=x_d, Yp=2 * x_d / (1 + x_d))


def baryon_density(eta, t_mev):
    """Baryon mass density in kg/m^3 at photon temperature T (MeV)."""
    t = t_mev * MEV / (HBAR * C)                          # 1/m
    return eta * 2 * zeta(3) / np.pi**2 * t**3 * MU


# ------------------------------------------------------- dense matter lines ---
def degeneracy_rho(t_k, mu_e=2.0):
    """rho [kg/m^3] where the non-relativistic electron Fermi energy equals k_B T."""
    p_f = np.sqrt(2 * ME * KB * np.asarray(t_k))
    return p_f**3 / (3 * np.pi**2 * HBAR**3) * mu_e * MU


def radiation_rho(t_k, mu=0.62):
    """rho [kg/m^3] where radiation pressure a T^4/3 equals gas pressure rho k T/(mu m_u)."""
    a = 4 * k.Stefan_Boltzmann / C
    return a * np.asarray(t_k) ** 3 / 3 * mu * MU / KB


def chandrasekhar_mass(mu_e=2.0):
    omega3 = 2.01824                                       # Lane-Emden n = 3
    return np.sqrt(3 * np.pi) / 2 * omega3 * (HBAR * C / G) ** 1.5 / (mu_e * MU) ** 2 / M_SUN


def white_dwarf(rho_c, mu_e=2.0, n=4000):
    """Mass [M_sun] and radius [m] of a cold, fully degenerate electron star (Chandrasekhar EOS)."""
    from scipy.integrate import solve_ivp
    m_c = ME * C
    def pressure_derivs(rho):
        x = (3 * np.pi**2 * rho / (mu_e * MU)) ** (1 / 3) * HBAR / m_c
        dpdx = ME * C**2 * m_c**3 / (3 * np.pi**2 * HBAR**3) * x**4 / np.sqrt(1 + x * x)
        dxdrho = x / (3 * rho)
        return dpdx * dxdrho
    def rhs(r, y):
        rho, m = y
        if rho <= 0:
            return [0, 0]
        return [-G * m * rho / (r * r) / pressure_derivs(rho), 4 * np.pi * r * r * rho]
    stop = lambda r, y: y[0] - rho_c * 1e-10
    stop.terminal = True
    r0 = 1.0
    sol = solve_ivp(rhs, [r0, 1e8], [rho_c, 4 / 3 * np.pi * r0**3 * rho_c], events=stop,
                    rtol=1e-8, atol=[1e-3, 1e10], max_step=2e4)
    return sol.y[1, -1] / M_SUN, sol.t[-1]


def supernova_numbers():
    """Energy of burning a 50:50 C/O white dwarf of 1.4 M_sun to 56Ni, and core-collapse binding."""
    ba = {key: ame()[key][2] for key in ((6, 12), (8, 16), (28, 56))}     # keV per nucleon
    q = (ba[(28, 56)] - 0.5 * (ba[(6, 12)] + ba[(8, 16)])) / 1e3
    e_ia = q * MEV * 1.4 * M_SUN / MU
    e_cc = 0.6 * G * (1.4 * M_SUN) ** 2 / 12e3
    return dict(q_CO_Ni_MeV=q, E_Ia_J=e_ia, E_cc_J=e_cc)


# ---------------------------------------------------------------- triple alpha ---
def hoyle_numbers():
    q3a = 3 * atomic_mass_u(2, 4) - atomic_mass_u(6, 12)
    q3a *= MU * C**2 / KEV
    be8 = (atomic_mass_u(4, 8) - 2 * atomic_mass_u(2, 4)) * MU * C**2 / KEV
    e_hoyle = 7654.2                                   # keV, excitation of 12C(0+_2), ENSDF
    return dict(Q3a_keV=q3a, Be8_above_2a_keV=be8, Hoyle_above_3a_keV=e_hoyle - q3a,
                Hoyle_above_Be8a_keV=e_hoyle - q3a - be8)


def binding_curve():
    rows = [(z, a, v[0], v[2]) for (z, a), v in ame().items() if a > 0 and not v[3] and v[2] > 0]
    best = {}
    for z, a, sym, ba in rows:
        if a not in best or ba > best[a][3]:
            best[a] = (z, a, sym, ba)
    return [best[a] for a in sorted(best)]



# ---------------------------------------------------- the Sun from measurements ---
MEAS = json.loads((DATA / "sun-measurements.json").read_text())
# Exponents of each input in the derived quantity: GM_sun = 4 pi^2 d^3/T^2 (Kepler),
# GM_earth = g R_E^2, R_sun = theta d/2, L = 4 pi d^2 S, t_KH = (GM)^2/(G R L) = 8 pi^3 d^3/(G theta S T^4).
EXPONENTS = {
    "R_sun": {"theta": 1, "d": 1},
    "R_sun_over_R_E": {"theta": 1, "d": 1, "R_E": -1},
    "M_ratio": {"d": 3, "T": -2, "g": -1, "R_E": -2},
    "M_E": {"g": 1, "R_E": 2, "G": -1},
    "M_sun": {"d": 3, "T": -2, "G": -1},
    "L_sun": {"d": 2, "S": 1},
    "t_KH": {"d": 3, "G": -1, "theta": -1, "S": -1, "T": -4},
}


def sun_from_measurements(name):
    """R, M, L and t_KH of the Sun from one set of measured inputs, with 1-sigma relative errors."""
    m = {key: v["value"] for key, v in MEAS["sets"][name].items() if isinstance(v, dict)}
    e = {key: v["rel_err"] for key, v in MEAS["sets"][name].items() if isinstance(v, dict)}
    gm_sun = 4 * np.pi**2 * m["d"] ** 3 / m["T"] ** 2
    r_sun = m["theta"] * m["d"] / 2
    lum = 4 * np.pi * m["d"] ** 2 * m["S"]
    val = {"R_sun": r_sun, "R_sun_over_R_E": r_sun / m["R_E"], "M_ratio": gm_sun / (m["g"] * m["R_E"] ** 2),
           "M_E": m["g"] * m["R_E"] ** 2 / m["G"], "M_sun": gm_sun / m["G"], "L_sun": lum,
           "t_KH": gm_sun**2 / (m["G"] * r_sun * lum) / YEAR}
    err = {q: float(np.sqrt(sum((p * e[x]) ** 2 for x, p in EXPONENTS[q].items()))) for q in val}
    return {q: {"value": float(val[q]), "rel_err": err[q]} for q in val}


# ------------------------------------------------------------ age of the Earth ---
AGE = json.loads((DATA / "earth-age.json").read_text())


def pb_ratio(t_yr, lam5, lam8, k):
    """Radiogenic 207Pb*/206Pb* after t: (exp(l5 t) - 1)/(k (exp(l8 t) - 1)), k = 238U/235U today."""
    return (np.expm1(lam5 * t_yr)) / (k * np.expm1(lam8 * t_yr))


def isochron_age(constants=None, n_mc=4000, seed=1):
    """Least-squares isochron through Patterson's meteorites; age from the slope, error by Monte Carlo."""
    c = constants or AGE["decay_constants"]
    lam5, lam8, k = c["lambda_235_per_yr"], c["lambda_238_per_yr"], c["U238_U235"]
    met = AGE["patterson_1956"]["meteorites"]
    x = np.array([m["r64"] for m in met])
    y = np.array([m["r74"] for m in met])
    rel = np.array([m["rel_err"] for m in met])
    age = lambda slope: brentq(lambda t: pb_ratio(t, lam5, lam8, k) - slope, 1e8, 1e10)
    slope, icpt = np.polyfit(x, y, 1)
    rng = np.random.default_rng(seed)
    ages = [age(np.polyfit(x * (1 + rel * rng.standard_normal(5)), y * (1 + rel * rng.standard_normal(5)), 1)[0])
            for _ in range(n_mc)]
    return {"slope": float(slope), "intercept": float(icpt), "age_yr": age(slope), "age_err_yr": float(np.std(ages))}


def decay_chains():
    """Q of the U/Th chains and 40K from AME2020 atomic masses (beta electrons included)."""
    he = (2, 4)
    return {"U238": q_value_mev([(92, 238)], [(82, 206)] + [he] * 8),
            "U235": q_value_mev([(92, 235)], [(82, 207)] + [he] * 7),
            "Th232": q_value_mev([(90, 232)], [(82, 208)] + [he] * 6),
            "K40": q_value_mev([(19, 40)], [(20, 40)]),
            "U238_alpha": q_value_mev([(92, 238)], [(90, 234), he])}


# ------------------------------------------------------------------- checks ---
def symbolic_checks():
    G_, M_, R_, mu_, mu_u, kT, N = sp.symbols("G M R mu m_u kT N", positive=True)
    # Virial theorem for a uniform ideal-gas sphere: 2 K + U = 0.
    K = sp.Rational(3, 2) * (M_ / (mu_ * mu_u)) * kT
    U = -sp.Rational(3, 5) * G_ * M_**2 / R_
    sol = sp.solve(sp.Eq(2 * K + U, 0), kT)[0]
    assert sp.simplify(sol - G_ * M_ * mu_ * mu_u / (5 * R_)) == 0
    # Y_p = 2 (n/p) / (1 + n/p): every neutron ends in 4He.
    x = sp.symbols("x", positive=True)
    nn, npr = x / (1 + x), 1 / (1 + x)
    assert sp.simplify(4 * (nn / 2) - 2 * x / (1 + x)) == 0
    # Gamow peak E0 = (E_G T^2/4)^(1/3).
    E, EG, T = sp.symbols("E E_G T", positive=True)
    e0 = sp.solve(sp.diff(-E / T - sp.sqrt(EG / E), E), E)[0]
    assert sp.simplify(e0 - (EG * T**2 / 4) ** sp.Rational(1, 3)) == 0
    print("symbolic: virial kT = GM mu m_u/(5R), Y_p = 2x/(1+x), Gamow E0")


def checks():
    s = sun_numbers()
    print(f"Sun: t_KH = {s['t_kh_yr']:.2e} yr, mass defect 4p->He {100 * s['mass_defect']:.3f} %, "
          f"t_nuc(10 % burnt) = {s['t_nuc_yr']:.2e} yr")
    assert 2.5e7 < s["t_kh_yr"] < 3.5e7 and abs(s["mass_defect"] - 0.00712) < 2e-5
    assert 0.9e10 < s["t_nuc_yr"] < 1.1e10
    print(f"     virial mean k_BT = {s['virial_mean_T_keV']:.2f} keV; Model S centre {s['T_c_keV']:.2f} keV, "
          f"n_ion = {s['n_ion']:.2e} m^-3, p = {s['p_c']:.0f} W/m^3")
    print(f"     tau_E = W_th/L = {s['tau_E_yr']:.2e} yr; n T tau_E = {s['triple']:.1e} keV s m^-3 (D-T needs 3e21)")
    assert abs(s["T_c_keV"] - 1.35) < 0.02 and 250 < s["p_c"] < 275

    c = SUN["centre"]
    e_pp = float(eps_pp(c["rho_kg_m3"], c["X"], s["T_c_keV"])[0])
    x_cno = cno_mass_fraction()
    e_cno = float(eps_cno(c["rho_kg_m3"], c["X"], x_cno, s["T_c_keV"])[0])
    print(f"     eps_pp(centre) = {e_pp:.2e} W/kg against Model S {c['eps_W_kg']:.2e}; eps_CNO = {e_cno:.2e} "
          f"(X_CNO = {x_cno:.4f}, ratio {e_cno / e_pp:.3f})")
    lum = model_s_luminosity()
    print(f"     pp + CNO rates on the Model S profiles give {lum:.2f} L (no screening, pp I energy release)")
    assert 0.8 < lum < 1.0
    tk = np.geomspace(0.8, 4, 400)
    r = eps_cno(1e5, 0.7, x_cno, tk) / eps_pp(1e5, 0.7, tk)
    t_cross = float(np.interp(0, np.log(r), tk))
    print(f"     pp = CNO at k_BT = {t_cross:.2f} keV = {t_cross * KEV / KB / 1e6:.1f} MK")
    assert 15e6 < t_cross * KEV / KB < 22e6

    br = pp_branches()
    print("pp branches from B16 fluxes: pp I {ppI:.3f}, pp II {ppII:.3f}, pp III {ppIII:.5f}".format(**br))
    assert 0.83 < br["ppI"] < 0.86 and 1e-4 < br["ppIII"] < 3e-4
    e = np.linspace(1e-4, 20, 200001)
    for name, f in neutrino_spectra(e).items():
        assert abs(np.trapezoid(f, e) / NU["fluxes"][name] - 1) < 1e-3, name

    print(f"BBN: Q_np = {Q_NP_MEV:.4f} MeV, B_D = {B_D_MEV:.4f} MeV")
    he = helium_estimate()
    print(f"     n/p(0.8 MeV) = {he['n_over_p_freeze']:.3f}, deuterium Saha T_D = {he['T_D']:.3f} MeV at "
          f"t = {he['t_D']:.0f} s, n/p = {he['n_over_p_D']:.3f}, Y_p ~ {he['Yp']:.3f}")
    assert 0.05 < he["T_D"] < 0.08 and 0.22 < he["Yp"] < 0.28
    print(f"     baryon density at T = 0.07 MeV: {baryon_density(6.1e-10, 0.07):.2e} kg/m^3")

    h = hoyle_numbers()
    print("Hoyle: Q(3a->12C) = {Q3a_keV:.1f} keV, 8Be - 2a = {Be8_above_2a_keV:.2f} keV, "
          "Hoyle above 3a {Hoyle_above_3a_keV:.1f} keV, above 8Be+a {Hoyle_above_Be8a_keV:.1f} keV".format(**h))
    assert abs(h["Be8_above_2a_keV"] - 91.84) < 0.1 and abs(h["Hoyle_above_Be8a_keV"] - 287.7) < 1

    bc = binding_curve()
    top = max(bc, key=lambda r: r[3])
    print(f"binding: most bound per nucleon {top[2]}-{top[1]} {top[3]:.1f} keV; "
          f"Fe-56 {ame()[(26, 56)][2]:.1f}, He-4 {ame()[(2, 4)][2]:.1f} keV")
    assert top[1] == 62 and top[0] == 28

    mch = chandrasekhar_mass()
    m_wd, r_wd = white_dwarf(3.5e9)      # 3.5e6 g/cm^3
    print(f"Chandrasekhar mass (mu_e = 2) {mch:.3f} M_sun; rho_c = 3.5e6 g/cm^3 -> {m_wd:.2f} M_sun, R = {r_wd / 1e3:.0f} km")
    assert abs(mch - 1.457) < 0.01 and 0.5 < m_wd < 0.7

    sn = supernova_numbers()
    print("Type Ia: C/O -> 56Ni releases {q_CO_Ni_MeV:.2f} MeV/nucleon, 1.4 M_sun -> {E_Ia_J:.1e} J; "
          "core collapse: 3/5 GM^2/R (1.4 M_sun, 12 km) = {E_cc_J:.1e} J".format(**sn))
    assert 1e44 < sn["E_Ia_J"] < 3e44 and 2e46 < sn["E_cc_J"] < 4e46

    for name in ("home", "1862", "today"):
        r = sun_from_measurements(name)
        print(f"Sun from {name}: M = {r['M_sun']['value']:.3e} kg ({r['M_ratio']['value']:.3g} M_E), "
              f"R = {r['R_sun_over_R_E']['value']:.0f} R_E, L = {r['L_sun']['value']:.3e} W, "
              f"t_KH = {r['t_KH']['value']:.2e} yr +- {100 * r['t_KH']['rel_err']:.0f} %")
    today = sun_from_measurements("today")
    assert abs(today["M_sun"]["value"] / M_SUN - 1) < 1e-3 and abs(today["L_sun"]["value"] / L_SUN - 1) < 2e-3
    assert abs(today["t_KH"]["value"] / s["t_kh_yr"] - 1) < 3e-3

    iso, iso56 = isochron_age(), isochron_age(AGE["patterson_1956"]["decay_constants_used"])
    q = decay_chains()
    print(f"Patterson isochron: slope {iso['slope']:.4f}, age {iso['age_yr'] / 1e9:.2f} +- {iso['age_err_yr'] / 1e9:.2f} Gyr "
          f"(1956 decay constants: {iso56['age_yr'] / 1e9:.2f} Gyr); chains Q: "
          + ", ".join(f"{key} {v:.2f} MeV" for key, v in q.items()))
    assert 4.4e9 < iso["age_yr"] < 4.65e9 and 4.5e9 < iso56["age_yr"] < 4.65e9
    assert abs(q["U238"] - 51.69) < 0.05 and abs(q["U235"] - 46.40) < 0.05 and abs(q["Th232"] - 42.65) < 0.05

    write_plotdata(s, t_cross, he, h, mch)


def widget_data():
    """Arrays for the slide widgets: neutrino spectra, white-dwarf mass-radius, reaction energies."""
    e = np.geomspace(0.05, 20, 400)
    spectra = {k: [float(f"{x:.4g}") for x in v] for k, v in neutrino_spectra(e).items()}
    rho = np.geomspace(1e7, 1e15, 60)
    mr = [white_dwarf(r) for r in rho]
    reactions = [("D + T → ⁴He + n", [(1, 2), (1, 3)], [(2, 4), (0, 1)]),
                 ("4 p → ⁴He", [(1, 1)] * 4, [(2, 4)]), ("3 ⁴He → ¹²C", [(2, 4)] * 3, [(6, 12)]),
                 ("¹²C + ⁴He → ¹⁶O", [(6, 12), (2, 4)], [(8, 16)]),
                 ("2 ¹²C → ²⁰Ne + ⁴He", [(6, 12)] * 2, [(10, 20), (2, 4)]),
                 ("2 ¹⁶O → ²⁸Si + ⁴He", [(8, 16)] * 2, [(14, 28), (2, 4)]),
                 ("2 ²⁸Si → ⁵⁶Ni (net)", [(14, 28)] * 2, [(28, 56)]),
                 ("n + ²³⁵U → ¹⁴¹Ba + ⁹²Kr + 3 n", [(0, 1), (92, 235)], [(56, 141), (36, 92)] + [(0, 1)] * 3)]
    rx = []
    for name, ini, fin in reactions:
        q = q_value_mev(ini, fin)          # atomic masses: e+ annihilation included
        rx.append({"name": name, "Q_MeV": round(q, 3), "A": sum(a for _, a in ini),
                   "from": [list(x) for x in ini], "to": [list(x) for x in fin]})
    return {"neutrino_E_MeV": [float(f"{x:.4g}") for x in e], "neutrino_spectra": spectra,
            "wd": {"rho_c": [float(f"{x:.3g}") for x in rho], "M": [round(m, 4) for m, _ in mr],
                   "R_Rsun": [float(f"{r / R_SUN:.4g}") for _, r in mr], "M_ch": chandrasekhar_mass()},
            "reactions": rx,
            "kelvin": {name: {"label": MEAS["sets"][name]["label"], "derived": sun_from_measurements(name)}
                       for name in ("home", "1862", "today")},
            "isochron": {"fit": isochron_age(), "fit_1956_constants": isochron_age(AGE["patterson_1956"]["decay_constants_used"]),
                         "chains_Q_MeV": decay_chains()},
            "binding": [{"Z": z, "A": a, "el": sym, "BA": round(ba / 1e3, 4)} for z, a, sym, ba in binding_curve()]}


def write_plotdata(s, t_cross, he, h, mch):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ch03_stars.json").write_text(json.dumps({"widgets": widget_data(),
        "supernova": supernova_numbers(), "sun": s, "pp_cno_cross_keV": t_cross, "pp_branches": pp_branches(), "bbn": he, "hoyle": h, "M_ch": mch,
        "binding": [{"Z": z, "A": a, "el": sym, "B_per_A_keV": ba} for z, a, sym, ba in binding_curve()],
    }, indent=1, default=float))


if __name__ == "__main__":
    symbolic_checks()
    checks()
    print("Chapter 3 stars checks passed")
