#!/usr/bin/env python3
"""Primordial nucleosynthesis with LINX: abundance histories over eta.

Usage: python3 scripts/prepare-ch03-bbn.py      (in an environment with LINX)
LINX (MIT): https://github.com/cgiovanetti/LINX, Giovanetti et al.,
Phys. Rev. D 112, 063531 (2025), doi:10.1103/f3tj-r882; key network
key_PRIMAT_2023 (Pitrou et al.), standard model background, tau_n from LINX.
Output: data/ch03/bbn.json (Y_i = n_i/n_b against t and T_gamma for each eta
and number of light neutrino species N_nu = 2..5, final abundances on a fine
eta grid, Planck eta and observed abundances). LINX takes Delta N_eff before
e+e- annihilation; it is scaled so that N_eff - 3.045 = N_nu - 3 afterwards.
"""
import json
import subprocess
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np

import linx
import linx.const as const
from linx.abundances import AbundanceModel
from linx.background import BackgroundModel
from linx.nuclear import NuclearRates
from linx.thermo import T_g

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/ch03/bbn.json"
NAMES = ["n", "p", "D", "T", "He3", "He4", "Li7", "Be7"]
NETWORK = "key_PRIMAT_2023"

bkg = BackgroundModel()
model = AbundanceModel(NuclearRates(nuclear_net=NETWORK))
NNU = [2, 3, 4, 5]
_, _, _, _, _, _, neff0 = bkg(jnp.asarray(0.0))
_, _, _, _, _, _, neff1 = bkg(jnp.asarray(1.0))
dilution = float(neff1[-1] - neff0[-1])          # late Delta N_eff per unit of initial Delta N_eff
print(f"N_eff(standard) = {float(neff0[-1]):.4f}, dilution of initial Delta N_eff {dilution:.4f}")
eta0 = const.Omegabh2 * const.Omegabh2_to_eta0
t_out = np.logspace(-2, np.log10(2e4), 160)
eta_hist = np.logspace(-10.5, -8.5, 21)          # 3.2e-11 ... 3.2e-9
eta_fine = np.logspace(-10.5, -8.5, 121)
runs = []
for nnu in NNU:
    t_vec, a_vec, rho_g, rho_nu, rho_np, p_np, neff = bkg(jnp.asarray((nnu - 3) / dilution))
    Tg = np.asarray(T_g(rho_g))
    T_out = np.interp(np.log(t_out), np.log(np.asarray(t_vec)), Tg)
    hist = []
    for eta in eta_hist:
        sol = model(rho_g, rho_nu, rho_np, p_np, t_vec=t_vec, a_vec=a_vec,
                    eta_fac=jnp.asarray(eta / eta0), tau_n_fac=jnp.asarray(1.0),
                    nuclear_rates_q=jnp.zeros(12), save_history=True)
        Y = np.array([np.asarray(sol.evaluate(t)) for t in t_out])[:, :8]
        hist.append(np.clip(Y, 1e-30, None))
    final = jax.jit(jax.vmap(lambda f: model(rho_g, rho_nu, rho_np, p_np, t_vec=t_vec, a_vec=a_vec, eta_fac=f)))
    F = np.asarray(final(jnp.asarray(eta_fine / eta0)))[:, :8]
    k = int(np.argmin(abs(eta_fine - eta0)))
    print(f"N_nu = {nnu}: N_eff = {float(neff[-1]):.3f}, Planck eta: Yp = {4 * F[k, 5]:.4f}, D/H = {F[k, 2] / F[k, 1]:.3e}")
    runs.append((nnu, float(neff[-1]), T_out, hist, F))

sig = lambda x: float(f"{x:.4g}")
data = {
    "source": "LINX " + subprocess.run(["git", "-C", str(Path(linx.__file__).parents[1]), "rev-parse", "--short", "HEAD"],
                                      capture_output=True, text=True).stdout.strip()
              + f", network {NETWORK}; Giovanetti et al., Phys. Rev. D 112, 063531 (2025), doi:10.1103/f3tj-r882",
    "species": NAMES,
    "note": "Y_i = n_i / n_b (number per baryon); helium mass fraction Y_p = 4 Y_He4; D/H = Y_D / Y_p.",
    "t_s": [sig(x) for x in t_out],
    "eta": [sig(x) for x in eta_hist],
    "runs": [{"N_nu": nnu, "N_eff": round(neff, 3), "T_MeV": [sig(x) for x in T_out],
              "Y": [[[sig(v) for v in row] for row in np.log10(h).T] for h in hist],  # log10 Y[eta][species][t]
              "final": {"eta": [sig(x) for x in eta_fine],
                        "log10Y": [[float(f"{v:.6g}") for v in col] for col in np.log10(np.clip(F, 1e-30, None)).T]}}
             for nnu, neff, T_out, hist, F in runs],
    "planck": {"eta": sig(eta0), "sigma": sig(const.sigma_Omegabh2 / const.Omegabh2 * eta0),
               "ref": "Planck 2018 Omega_b h^2 as used by LINX (linx.const)"},
    "observed": {
        "Yp": {"value": 0.2449, "sigma": 0.0040, "ref": "Aver et al., JCAP 07 (2015) 011, doi:10.1088/1475-7516/2015/07/011"},
        "DH": {"value": 2.527e-5, "sigma": 0.030e-5, "ref": "Cooke, Pettini & Steidel, ApJ 855, 102 (2018), doi:10.3847/1538-4357/aaab53"},
        "Li7H": {"value": 1.6e-10, "sigma": 0.3e-10, "ref": "Particle Data Group, BBN review (2024)"},
    },
}
OUT.write_text(json.dumps(data, separators=(",", ":")))
print("written", OUT, OUT.stat().st_size // 1024, "kB")
