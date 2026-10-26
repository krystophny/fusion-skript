"""Reactivity and 0-D power balance against independent numbers.

Bosch-Hale D-T at 10 keV (course plan: 1.1e-22 m^3/s), the Maxwell integral of
an S factor, the Gamow peak as a numerical maximum, Monte Carlo pair sampling,
the ignition triple product (about 3e21 keV s m^-3 near 14 keV) and the
alpha/neutron split from momentum conservation.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "derivations/chapters"))
import ch02_reactivity as rx  # noqa: E402
import ch04_power_balance as pb  # noqa: E402


def test_bosch_hale_dt_at_10_keV():
    assert rx.bosch_hale("DT", 10.0) == pytest.approx(1.1e-22, rel=0.05)


@pytest.mark.parametrize("name,tol", [("DT", 0.01), ("DDn", 0.02), ("DDp", 0.025), ("DHe3", 0.035)])
def test_quadrature_of_bosch_hale_s_factor_matches_their_reactivity(name, tol):
    t = np.array([2.0, 10.0, 50.0])
    ratio = rx.maxwell_average(name, t, "bh") / rx.bosch_hale(name, t)
    assert np.all(np.abs(ratio - 1) < tol)


def test_exfor_fit_reactivity_close_to_bosch_hale_for_dt():
    t = np.array([5.0, 10.0, 20.0])
    ratio = rx.maxwell_average("DT", t) / rx.bosch_hale("DT", t)
    assert np.all(np.abs(ratio - 1) < 0.03)


def test_gamow_peak_is_numerical_maximum():
    e_g, t = rx.gamow_energy("DT"), 10.0
    e = np.linspace(1, 150, 300001)
    e_max = e[np.argmax(-e / t - np.sqrt(e_g / e))]
    assert rx.gamow_peak(e_g, t)[0] == pytest.approx(e_max, abs=1e-3)


def test_solar_gamow_peak_near_6_keV():
    assert rx.gamow_peak(rx.gamow_energy("pp"), 1.3)[0] == pytest.approx(6.0, abs=0.1)


def test_reactivity_over_t_squared_peaks_near_14_keV():
    t = np.linspace(5, 40, 7001)
    assert 13.0 < t[np.argmax(rx.bosch_hale("DT", t) / t**2)] < 15.0


def test_monte_carlo_pairs_reproduce_quadrature():
    rng = np.random.default_rng(7)
    e, v = rx.sample_pairs(10.0, 1_000_000, rx.MC2["D"], rx.MC2["T"], rng)
    assert np.mean(rx.sigma("DT", e) * v) == pytest.approx(rx.maxwell_average("DT", 10.0)[0], rel=0.02)
    # Relative energy is Maxwellian: mean 3/2 k_B T.
    assert e.mean() == pytest.approx(15.0, rel=0.005)


def test_alpha_neutron_split_conserves_momentum():
    e_a, e_n = pb.E_ALPHA, pb.E_N
    p_a2 = e_a * (e_a + 2 * rx.MC2["He4"])          # (p c)^2 in keV^2
    p_n2 = e_n * (e_n + 2 * rx.MC2["n"])
    assert p_a2 == pytest.approx(p_n2, rel=1e-12)
    assert e_a + e_n == pytest.approx(17589, abs=1)
    assert e_a / e_n == pytest.approx(rx.MC2["n"] / rx.MC2["He4"], rel=0.01)


def test_ignition_triple_product_minimum():
    t = np.geomspace(3, 100, 5001)
    y = pb.triple_product(t)
    assert y.min() == pytest.approx(3e21, rel=0.1)
    assert 13 < t[y.argmin()] < 15


def test_gain_reduces_required_triple_product():
    t = np.array([14.0])
    for q in (1.0, 10.0):
        x = pb.triple_product(t, q)[0] / pb.triple_product(t)[0]
        assert x == pytest.approx(q / (q + pb.E_FUS / pb.E_ALPHA))


def test_bremsstrahlung_forbids_ignition_below_ideal_temperature():
    assert np.isinf(pb.triple_product(np.array([4.0]), brems=True)[0])
    assert np.isfinite(pb.triple_product(np.array([4.6]), brems=True)[0])


# --- model of the Maxwell-average animations (animations/maxwell_average_model.py) ---
sys.path.insert(0, str(ROOT / "animations"))
import maxwell_average_model as anim  # noqa: E402


@pytest.mark.parametrize("t", [10.0, 50.0])
def test_animation_trace_matches_bosch_hale(t):
    # The traced point is the area under sigma v times the kernel on a log energy axis.
    assert anim.average(t) == pytest.approx(rx.bosch_hale("DT", t), rel=0.01)


def test_animation_kernel_is_the_maxwellian_per_log_energy():
    t = 7.0
    e = np.geomspace(1e-7, 500, 200001)
    f_m = 2 / np.sqrt(np.pi) * t**-1.5 * np.sqrt(e) * np.exp(-e / t)
    assert np.trapezoid(anim.kernel(e, t), np.log(e)) == pytest.approx(1.0, abs=1e-6)
    assert np.allclose(anim.kernel(e, t), e * f_m)
    assert anim.kernel(1.5 * t, t) == pytest.approx(anim.KERNEL_MAX)


def test_relative_velocity_convolution_has_reduced_mass():
    t = 10.0
    s_d, s_t = anim.thermal_width(t, anim.MC2_D), anim.thermal_width(t, anim.MC2_T)
    m_r = anim.MC2_D * anim.MC2_T / (anim.MC2_D + anim.MC2_T)
    g = np.linspace(-3, 3, 13)
    v = np.linspace(-12, 12, 4001)
    assert np.allclose(anim.relative_density(g, v, s_d, s_t), anim.gauss(g, anim.thermal_width(t, m_r)),
                       rtol=1e-9, atol=1e-12)


def test_symbolic_derivation_of_deck_section():
    # Rate, relative velocity, log-energy kernel and Gamow peak as shown on deck 02.
    rx.symbolic_checks()


# --- chapter 4 deck: bremsstrahlung, dilution, plant gain, fixed pressure, measured points ---
def test_chapter4_symbolic_derivations():
    pb.symbolic_checks()


def test_ideal_ignition_temperature_is_root_of_alpha_minus_bremsstrahlung():
    from scipy.optimize import brentq
    # p_alpha / n_e^2 = <sigma v> E_alpha / 4 against C_B sqrt(T), both in W m^3.
    f = lambda t: rx.bosch_hale("DT", t) * pb.E_ALPHA * rx.KEV / 4 - 5.344e-37 * np.sqrt(t)
    root = brentq(f, 2.0, 10.0)
    assert root == pytest.approx(4.3, abs=0.05)
    assert pb.ideal_ignition_temperature() == pytest.approx(root, abs=1e-3)


def test_tungsten_dilution_from_charge_balance():
    n_e, n_w = 1.0, 1e-3
    n_fuel = n_e - 74 * n_w                      # quasineutrality with fully ionised W
    fuel, _, _ = pb.dilution([(74, n_w / n_e)])
    assert fuel == pytest.approx(n_fuel)
    assert 1 - fuel**2 == pytest.approx(0.143, abs=0.001)


def test_helium_ash_raises_ignition_requirement():
    t = np.geomspace(4, 100, 4001)
    pure = pb.ignition_diluted(t)
    assert np.allclose(pure, pb.triple_product(t, brems=True), rtol=1e-12)
    assert pb.ignition_diluted(t, [(2, 0.05)]).min() > 1.2 * pure.min()


def test_engineering_gain_from_power_bookkeeping():
    eta_th, eta_aux, p_ext = 0.4, 0.4, 50.0
    for q in (5.25, 10.0, 11.5):
        gross = eta_th * (q * p_ext + p_ext)
        recirc = p_ext / eta_aux
        assert pb.q_eng(q, eta_th, eta_aux) == pytest.approx((gross - recirc) / recirc)
    assert pb.q_eng(5.25) == pytest.approx(0.0, abs=1e-12)


@pytest.mark.parametrize("q", [0.5, 1.0, 5.0, 10.0, 100.0])
def test_alpha_fraction_from_power_bookkeeping(q):
    p_fus = 300e6
    p_alpha = p_fus * pb.E_ALPHA / pb.E_FUS
    p_ext = p_fus / q
    assert pb.alpha_fraction(q) == pytest.approx(p_alpha / (p_alpha + p_ext), rel=1e-12)


def test_alpha_fraction_reaches_one_at_ignition():
    assert pb.alpha_fraction(np.inf) == 1.0
    assert pb.alpha_fraction(1e9) == pytest.approx(1.0, abs=1e-8)


def test_fixed_pressure_optimum_from_density_at_constant_pressure():
    t = np.linspace(5, 40, 35001)
    p = 1.0
    n = p / (2 * t)                              # p = 2 n T
    p_fus = n**2 / 4 * rx.bosch_hale("DT", t)
    assert 13.0 < t[np.argmax(p_fus)] < 14.0


def test_measured_points_exclude_projections_and_match_table():
    rows = pb.machines()
    assert not any(r["shot"] == "Projected" for r in rows)
    jet = [r for r in rows if r["project"] == "JET" and r["shot"] == "42976"][0]
    assert (jet["n"], jet["tau"], jet["year"]) == (3.3e19, 0.51, 1997)
    nif = [r for r in rows if r["shot"] == "N210808"][0]
    assert nif["n"] * nif["tau"] == pytest.approx(5.7e20, rel=0.01)
