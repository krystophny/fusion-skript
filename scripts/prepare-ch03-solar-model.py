#!/usr/bin/env python3
"""Reduce Model S of the present Sun to a radial profile for the stars deck.

Usage: python3 -I scripts/prepare-ch03-solar-model.py FGONG
FGONG = fgong.l5bi.d.15 from https://users-phys.au.dk/jcd/solar_models/
(GONG format; read as text only). Model S: Christensen-Dalsgaard et al.,
Science 272, 1286 (1996), doi:10.1126/science.272.5266.1286.
Output: data/ch03/solar-model.json with r/R, T [K], rho [kg/m^3], X, L_r/L,
eps [W/kg] and the integrated core quantities used on the slides.
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/ch03/solar-model.json"


def read_fgong(path):
    lines = path.read_text().splitlines()
    nn, iconst, ivar, _ = (int(x) for x in lines[4].split()[:4])
    text = "".join(l.rstrip("\n").ljust(80) for l in lines[5:])
    vals = np.array([float(text[i:i + 16].replace("D", "E")) for i in range(0, len(text) - 15, 16)
                     if text[i:i + 16].strip()])
    glob, var = vals[:iconst], vals[iconst:iconst + nn * ivar].reshape(nn, ivar)
    return glob, var[::-1]          # centre first


def main(path):
    glob, v = read_fgong(Path(path))
    M, R, L = glob[0] * 1e-3, glob[1] * 1e-2, glob[2] * 1e-7   # cgs -> SI
    r, T, rho, X, Lr, eps = v[:, 0] * 1e-2, v[:, 2], v[:, 4] * 1e3, v[:, 5], v[:, 6] * 1e-7, v[:, 8] * 1e-4
    q = np.exp(v[:, 1])
    pick = np.unique(np.concatenate([np.searchsorted(r / R, np.linspace(0, 1, 301)), [len(r) - 1]]))
    pick = pick[pick < len(r)]
    core = np.searchsorted(Lr / L, 0.99)
    out = {
        "source": "Model S, Christensen-Dalsgaard et al., Science 272, 1286 (1996), "
                  "doi:10.1126/science.272.5266.1286; file fgong.l5bi.d.15, https://users-phys.au.dk/jcd/solar_models/",
        "M_kg": M, "R_m": R, "L_W": L, "age_yr": float(glob[12]),
        "centre": {"T_K": float(T[0]), "rho_kg_m3": float(rho[0]), "X": float(X[0]), "eps_W_kg": float(eps[0])},
        "r99": {"r_over_R": float(r[core] / R), "m_over_M": float(q[core])},
        "profile": {k: [float(f"{x:.5g}") for x in a[pick]] for k, a in
                    {"r_over_R": r / R, "m_over_M": q, "T_K": T, "rho_kg_m3": rho, "X": X,
                     "L_over_L": Lr / L, "eps_W_kg": eps}.items()},
    }
    OUT.write_text(json.dumps(out, indent=1))
    c = out["centre"]
    print(f"M={M:.4e} R={R:.4e} L={L:.4e}; centre T={c['T_K']:.4e} K rho={c['rho_kg_m3']:.4e} X={c['X']:.3f} "
          f"eps={c['eps_W_kg']:.3e} W/kg -> {c['eps_W_kg'] * c['rho_kg_m3']:.0f} W/m^3; 99% L inside r/R={out['r99']['r_over_R']:.3f}")


if __name__ == "__main__":
    main(sys.argv[1])
