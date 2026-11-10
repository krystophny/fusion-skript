"""Chapter 3 (stars) numbers against independent data and calculations.

Model S and MIST are independent solar/stellar models; LINX is an independent
nucleosynthesis network; the slide statements (T^4 and T^18 scaling, Y_p
estimate, pp branches, Chandrasekhar limit) are checked against them.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "derivations/chapters"))
import ch03_stars as st  # noqa: E402

MIST = json.loads((ROOT / "data/ch03/mist.json").read_text())
BBN = json.loads((ROOT / "data/ch03/bbn.json").read_text())


def log_slope(f, t):
    h = 1e-3
    return (np.log(f(t * (1 + h))) - np.log(f(t * (1 - h)))) / (np.log(1 + h) - np.log(1 - h))


def test_temperature_exponents_match_gamow_formula():
    # pp at the solar centre ~ T^4, 14N(p,gamma) near the crossover ~ T^18 (slide 3.4).
    t_sun = st.SUN["centre"]["T_K"] * st.KB / st.KEV
    nu_pp = log_slope(lambda t: st.sigma_v(1, 1, 1.00728, 1.00728, st.S_PP, t)[0], t_sun)
    nu_cno = log_slope(lambda t: st.sigma_v(1, 7, 1.00728, 13.9992, st.S_N14, t)[0], 1.64)
    tau = lambda eg, t: 3 * (eg * t * t / 4) ** (1 / 3) / t
    assert nu_pp == pytest.approx((tau(st.gamow_energy_kev(1, 1, 0.50364), t_sun) - 2) / 3, rel=0.03)
    assert round(nu_pp) == 4 and round(nu_cno) == 18


def test_mist_sun_agrees_with_model_s():
    sol = next(s for s in MIST["sets"] if s["feh"] == 0)
    sun = next(t for t in sol["tracks"] if t["mass"] == 1.0)
    i = int(np.argmin(np.abs(np.array(sun["star_age"]) - 4.57e9)))
    assert 10 ** sun["log_center_T"][i] == pytest.approx(st.SUN["centre"]["T_K"], rel=0.03)
    assert 10 ** sun["log_center_Rho"][i] * 1e3 == pytest.approx(st.SUN["centre"]["rho_kg_m3"], rel=0.05)


def test_our_rates_reproduce_most_of_the_solar_luminosity():
    assert 0.8 < st.model_s_luminosity() < 1.0


def test_helium_estimate_close_to_network():
    he = st.helium_estimate()
    std = next(r for r in BBN["runs"] if r["N_nu"] == 3)
    k = int(np.argmin(np.abs(np.log(np.array(std["final"]["eta"]) / BBN["planck"]["eta"]))))
    yp_network = 4 * 10 ** std["final"]["log10Y"][BBN["species"].index("He4")][k]
    assert yp_network == pytest.approx(BBN["observed"]["Yp"]["value"], abs=3 * BBN["observed"]["Yp"]["sigma"])
    assert he["Yp"] == pytest.approx(yp_network, abs=0.01)


def test_helium_counts_neutrino_species():
    # Each extra light species speeds up the expansion: earlier freeze-out, more helium.
    he4 = BBN["species"].index("He4")
    yp = []
    for run in sorted(BBN["runs"], key=lambda r: r["N_nu"]):
        k = int(np.argmin(np.abs(np.log(np.array(run["final"]["eta"]) / BBN["planck"]["eta"]))))
        yp.append(4 * 10 ** run["final"]["log10Y"][he4][k])
    assert all(0.010 < b - a < 0.016 for a, b in zip(yp, yp[1:]))
    obs = BBN["observed"]["Yp"]
    assert [abs(y - obs["value"]) < 2 * obs["sigma"] for y in yp] == [False, True, False, False]


def test_pp_branches_and_neutrino_spectra():
    br = st.pp_branches()
    assert sum(br.values()) == pytest.approx(1)
    assert br["ppI"] == pytest.approx(0.848, abs=0.002)
    e = np.linspace(1e-4, 20, 100001)
    for name, f in st.neutrino_spectra(e).items():
        assert np.all(f >= 0) and np.trapezoid(f, e) == pytest.approx(st.NU["fluxes"][name], rel=2e-3)


def test_white_dwarfs_approach_the_chandrasekhar_mass():
    masses = [st.white_dwarf(rho)[0] for rho in (1e9, 1e11, 1e13)]
    assert masses == sorted(masses)
    assert masses[-1] == pytest.approx(st.chandrasekhar_mass(), rel=0.05)


def test_conditions_have_references_and_photos_exist():
    cond = json.loads((ROOT / "data/ch03/conditions.json").read_text())
    for o in cond["objects"]:
        assert o["ref"] and o["rho"] > 0 and o["T"] > 0
        if o["photo"]:
            assert (ROOT / "notebooks/data/stars" / f"{o['photo']}.jpg").is_file()


def test_kelvin_helmholtz_time_from_measurements():
    # Closed form with G kept once: t_KH = 8 pi^3 d^3 / (G theta S T^4); linear error
    # propagation against a Monte Carlo of the home-experiment inputs.
    for name in ("home", "1862", "today"):
        m = {k: v["value"] for k, v in st.MEAS["sets"][name].items() if isinstance(v, dict)}
        closed = 8 * np.pi**3 * m["d"] ** 3 / (m["G"] * m["theta"] * m["S"] * m["T"] ** 4) / st.YEAR
        assert st.sun_from_measurements(name)["t_KH"]["value"] == pytest.approx(closed, rel=1e-12)
    sets = st.MEAS["sets"]["home"]
    rng = np.random.default_rng(0)
    draw = {k: v["value"] * (1 + v["rel_err"] * rng.standard_normal(200000)) for k, v in sets.items() if isinstance(v, dict)}
    t = 8 * np.pi**3 * draw["d"] ** 3 / (draw["G"] * draw["theta"] * draw["S"] * draw["T"] ** 4) / st.YEAR
    lin = st.sun_from_measurements("home")["t_KH"]["rel_err"]
    assert np.std(np.log(t)) == pytest.approx(lin, rel=0.15)
    # Even the home result is a factor > 50 short of the age of the Earth.
    assert st.sun_from_measurements("home")["t_KH"]["value"] * (1 + 3 * lin) < 4.54e9 / 50


def test_patterson_isochron_and_earth_lead():
    # With his 1956 decay constants the fit reproduces Patterson's 4.55 +- 0.07 Gyr, and the
    # ocean-sediment lead (Earth) lies on the meteorite isochron within the 2 % lead error.
    old = st.isochron_age(st.AGE["patterson_1956"]["decay_constants_used"])
    assert abs(old["age_yr"] / 1e9 - 4.55) < 0.07
    sed = st.AGE["patterson_1956"]["ocean_sediment"]
    assert old["slope"] * sed["r64"] + old["intercept"] == pytest.approx(sed["r74"], rel=0.02)


def test_decay_chain_energies():
    # Total Q of the chains, Dye, Rev. Geophys. 50, RG3007 (2012), Table 1: 51.698, 46.402, 42.652 MeV.
    q = st.decay_chains()
    assert q["U238"] == pytest.approx(51.698, abs=0.01)
    assert q["U235"] == pytest.approx(46.402, abs=0.01)
    assert q["Th232"] == pytest.approx(42.652, abs=0.01)
