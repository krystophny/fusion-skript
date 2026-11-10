#!/usr/bin/env python3
"""Reduce MIST v1.2 evolutionary tracks to the core quantities of the star widget.

Usage: python3 -I scripts/prepare-ch03-mist.py MIST_DIR
MIST_DIR holds the unpacked EEP tarballs
MIST_v1.2_feh_<feh>_afe_p0.0_vvcrit0.4_EEPS (https://mist.science/, files
tarballs_v1.2/MIST_v1.2_feh_<feh>_afe_p0.0_vvcrit0.4_EEPS.txz). The tracks are
parsed as text only.
MIST: Dotter, ApJS 222, 8 (2016), doi:10.3847/0067-0049/222/1/8; Choi et al.,
ApJ 823, 102 (2016), doi:10.3847/0004-637X/823/2/102; computed with MESA.
Output: data/ch03/mist.json, one record per [Fe/H] and initial mass, each
column subsampled to at most NMAX points (every primary EEP is kept).
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/ch03/mist.json"
FEH = ["m2.00", "m1.00", "p0.00", "p0.50"]
MASSES = [0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0, 8.0, 10.0, 15.0, 20.0, 30.0, 40.0, 60.0, 100.0]
COLS = ["star_age", "star_mass", "log_L", "log_Teff", "log_center_T", "log_center_Rho",
        "center_degeneracy", "center_h1", "center_he4", "center_c12", "center_n14", "center_o16",
        "center_ne20", "center_mg24", "center_si28", "pp", "cno", "tri_alfa", "burn_c", "phase"]
NMAX = 220


def read(path):
    lines = path.read_text().splitlines()
    head = next(l for l in lines if l.lstrip("# ").startswith("star_age")).lstrip("#").split()
    meta = lines[4].lstrip("#").split()
    eeps = [int(x) for x in next(l for l in lines if l.startswith("# EEPs:")).split()[2:]]
    data = np.array([l.split() for l in lines if l.strip() and not l.startswith("#")], dtype=float)
    return dict(zip(head, data.T)), {"Y": float(meta[0]), "Z": float(meta[1]), "feh": float(meta[2])}, eeps


def keep(n, eeps):
    idx = set(np.linspace(0, n - 1, min(n, NMAX - len(eeps))).round().astype(int).tolist())
    idx |= {e - 1 for e in eeps if e - 1 < n}
    return sorted(idx)


def main(mist):
    out = {"source": "MIST v1.2 EEP tracks, [a/Fe] = 0, v/v_crit = 0.4 (https://mist.science/); "
                      "Dotter, ApJS 222, 8 (2016), doi:10.3847/0067-0049/222/1/8; "
                      "Choi et al., ApJ 823, 102 (2016), doi:10.3847/0004-637X/823/2/102",
           "columns": COLS,
           "units": {"star_age": "yr", "star_mass": "M_sun", "log_L": "log10 L/L_sun",
                     "log_Teff": "log10 K", "log_center_T": "log10 K",
                     "log_center_Rho": "log10 g/cm^3", "center_*": "mass fraction",
                     "log_t_left": "log10 yr until nuclear burning ends (first phase-6 model, else the last model)", "pp, cno, tri_alfa, burn_c": "log10 L/L_sun of each burning channel",
                     "phase": "-1 PMS, 0 MS, 2 RGB, 3 CHeB, 4 EAGB, 5 TPAGB, 6 post-AGB/WD, 9 WR"},
           "sets": []}
    for feh in FEH:
        d = next(Path(mist).glob(f"MIST_v1.2_feh_{feh}_afe_p0.0_vvcrit0.4_EEPS"))
        tracks = []
        for m in MASSES:
            cols, meta, eeps = read(d / f"{round(m * 100):05d}M.track.eep")
            idx = keep(len(cols["star_age"]), eeps)
            rec = {"mass": m}
            # Time left until nuclear burning ends (first white-dwarf model, MIST phase 6,
            # else the last model), at full precision, resolves the short late stages.
            age = cols["star_age"]
            wd = np.flatnonzero(cols["phase"] == 6)
            end = age[wd[0]] if len(wd) else age[-1]
            step = np.diff(age)
            left = np.maximum(end - age, 0.5 * np.min(step[step > 0]))
            rec["log_t_left"] = [float(f"{x:.4g}") for x in np.log10(left[idx])]
            for c in COLS:
                v = cols[c][idx]
                rec[c] = [float(f"{x:.8g}") for x in v] if c == "star_age" else [float(f"{x:.4g}") for x in v]
            tracks.append(rec)
        out["sets"].append({"feh": meta["feh"], "Z": meta["Z"], "Y": meta["Y"], "tracks": tracks})
        print(feh, "Z =", meta["Z"], len(tracks), "tracks")
    OUT.write_text(json.dumps(out, separators=(",", ":")))
    print("written", OUT, OUT.stat().st_size // 1024, "kB")


if __name__ == "__main__":
    main(sys.argv[1])
