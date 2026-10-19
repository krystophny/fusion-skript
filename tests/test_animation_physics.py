"""Physics oracles for the head-on Coulomb reflection animation (l = 0)."""
from pathlib import Path
import runpy

import mpmath
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
model = runpy.run_path(str(ROOT / "animations/radial_coulomb.py"))


@pytest.fixture(scope="module")
def packet():
    return model["RadialPacket"]()


def test_evolution_conserves_norm_and_mean_energy(packet):
    for t in (0.0, 20.0, 35.0, 70.0):
        u = packet.at(t)
        assert abs(np.sum(np.abs(u) ** 2) * packet.dr - 1.0) < 1e-12
        assert abs(packet.energy(u) - 1.0) < 1e-12


def test_energy_spread_is_narrow(packet):
    weight = np.abs(packet.coeff) ** 2 * packet.dr
    spread = np.sqrt(np.sum(weight * packet.levels**2) - np.sum(weight * packet.levels) ** 2)
    assert spread < 0.15


def test_reflection_time_matches_classical_orbit(packet):
    # Time of closest approach of <r> against the classical turning time at E;
    # the return to the start radius after twice that time.
    t_turn = model["classical_orbit"]([0.0])[1]
    times = np.linspace(0.0, 2 * t_turn, 281)
    mean_r = np.array([np.sum(packet.r * np.abs(packet.at(t)) ** 2) * packet.dr for t in times])
    i = mean_r.argmin()
    assert abs(times[i] - t_turn) / t_turn < 0.02
    assert abs(mean_r[-1] - model["R0"]) / model["R0"] < 0.05


def test_classical_orbit_reaches_rc_and_conserves_energy():
    t_turn = model["classical_orbit"]([0.0])[1]
    t = np.linspace(0.0, 2 * t_turn, 2001)
    r, _ = model["classical_orbit"](t)
    assert abs(r.min() - 1.0) < 1e-6 and abs(r[0] - model["R0"]) < 1e-6
    v = np.gradient(r, t)
    energy = model["ETA"] ** 2 * v**2 + 1 / r       # m v^2/2 with m = 2 eta^2
    assert np.max(np.abs(energy[5:-5] - 1.0)) < 1e-3


def test_tail_inside_rc_follows_wkb(packet):
    # Inside r_c: |u|^2 ~ exp(-2 int_r^{r_c} kappa dr)/kappa (WKB), slope within 10 %.
    t_turn = model["classical_orbit"]([0.0])[1]
    density = np.abs(packet.at(t_turn)) ** 2
    inside = (packet.r > 0.3) & (packet.r < 0.85)
    r = packet.r[inside]
    kappa = 2 * model["ETA"] * np.sqrt(1 / r - 1)
    slope = np.polyfit(model["wkb_exponent"](r), np.log(density[inside] * kappa), 1)[0]
    assert abs(slope + 1.0) < 0.1


def test_discrete_hamiltonian_matches_coulomb_function():
    # Stationary l = 0 solution at E = 1 is the regular Coulomb function
    # F_0(eta, k r) with k = 2 eta: residual of H u = u on the grid.
    eta = model["ETA"]
    r, dr = model["grid"](4000, 4.0)
    u = np.array([float(mpmath.coulombf(0, eta, 2 * eta * x)) for x in r])
    hu = model["hamiltonian"](r, dr, eta) @ u
    assert np.max(np.abs(hu[1:-1] - u[1:-1])) < 1e-3 * np.max(np.abs(u))
