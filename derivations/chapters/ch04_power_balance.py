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
"""
import sys
from pathlib import Path

import numpy as np
from scipy import constants as k

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ch02_reactivity import KEV, MC2, bosch_hale  # noqa: E402

C_B = 1.69e-32 * 1e-6 * np.sqrt(1e3)        # W m^3 keV^(-1/2)


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


if __name__ == "__main__":
    checks()
    print("Chapter 4 power-balance checks passed")
