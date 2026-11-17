"""Reduce the public NCSX benchmark files to data/ch05/ncsx.json.

Inputs (STELLOPT, BENCHMARKS/FIELDLINES_TEST, https://github.com/PrincetonUniversity/STELLOPT):
  coils.NCSX             MAKEGRID filaments, all NCSX coil groups
  wout_NCSX_plasma.nc    VMEC equilibrium of the NCSX reference plasma
Run:  python3 scripts/prepare-ch05-ncsx.py COILS WOUT
Keeps the 18 modular coils (every 4th filament point) and the last flux
surface: R, Z and the stream function lambda as Fourier series, and iota.
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.io import netcdf_file

OUT = Path(__file__).resolve().parents[1] / "data/ch05/ncsx.json"


def modular_coils(path, stride=4):
    coils, pts = [], []
    for line in Path(path).read_text().splitlines()[3:]:
        f = line.split()
        if len(f) < 4 or f[0] == "end":
            continue
        pts.append([float(v) for v in f[:4]])
        if len(f) >= 6:
            if f[5].startswith("Mod"):
                p = np.array(pts)
                xyz = p[::stride, :3]
                coils.append({"group": f[5], "current_A": p[0, 3],
                              "xyz_m": np.round(xyz, 4).tolist()})
            pts = []
    return coils


def surface(path):
    v = netcdf_file(path, "r", mmap=False).variables
    keep = lambda a: [round(float(x), 7) for x in a]  # noqa: E731
    return {"nfp": int(v["nfp"].data), "xm": v["xm"].data.astype(int).tolist(),
            "xn": v["xn"].data.astype(int).tolist(), "rmnc": keep(v["rmnc"].data[-1]),
            "zmns": keep(v["zmns"].data[-1]), "lmns": keep(v["lmns"].data[-1]),
            "iota": float(v["iotaf"].data[-1]), "R0_m": float(v["Rmajor_p"].data),
            "a_m": float(v["Aminor_p"].data)}


if __name__ == "__main__":
    coils = modular_coils(sys.argv[1])
    assert len(coils) == 18, len(coils)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"modular_coils": coils, "boundary": surface(sys.argv[2])}, separators=(",", ":")))
    print(OUT, OUT.stat().st_size)
