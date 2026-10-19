#!/usr/bin/env python3
"""Fetch EXFOR entries for D-T and D-D fusion cross sections and convert to S(E).

Usage: python3 -I scripts/prepare-ch02-s-factor.py WORKDIR
WORKDIR must be a new or empty directory; downloaded entries are untrusted data
and are only parsed as text, never executed.

The IAEA EXFOR web service (nds.iaea.org/exfor) answers scripted requests with a
Cloudflare challenge (HTTP 403, cf-mitigated: challenge), so the entries are taken
from the IAEA-NDS EXFOR master-file repository, pinned to one commit.
Output: derivations/chapters/ch02_s_factor_exfor.json (sigma, E_cm, S, provenance).
"""
import hashlib
import json
import math
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "derivations/chapters/ch02_s_factor_exfor.json"
COMMIT = "d2af85eca4ce9b76529f096e7f9603da60654732"
BASE = f"https://raw.githubusercontent.com/IAEA-NDS/exfor_master/{COMMIT}/exforall/"
BH_ALL = json.loads((ROOT / "data/ch02/cross-sections.json").read_text())["bosch_hale"]["reactions"]
# Atomic masses in u (AME2020); only ratios enter the lab -> centre-of-mass conversion.
MASS = {"D": 2.01410178, "T": 3.01604928}
# Gamow constants B_G = sqrt(E_G) in sqrt(keV), Bosch & Hale (1992).
BG = {"DT": 34.3827, "DD": 31.3970}

# One record per data set. cols: (energy, sigma, error) column keys in the EXFOR
# table; err_kind: "abs" (same unit as sigma), "pct" (column, per cent) or
# ("pct", value) for a constant per-cent error from the COMMON block.
SETS = [
    dict(reaction="DT", branch="DT", entry="C0018", subent=2, path="C00/C0018.x4",
         label="Arnold 1954", authors="W.R. Arnold, J.A. Phillips, G.A. Sawyer, E.J. Stovall, J.L. Tuck",
         ref="Phys. Rev. 93, 483 (1954)", doi="10.1103/PhysRev.93.483",
         proj="D", target="T", e="EN", s="DATA", err=("pct_col", "DATA-ERR2"),
         note="Table VI of LA-1479 as compiled; assigned error (twice the standard error)."),
    dict(reaction="DT", branch="DT", entry="C0319", subent=3, path="C03/C0319.x4",
         label="Jarmie 1984", authors="N. Jarmie, R.E. Brown, R.A. Hardekopf",
         ref="Phys. Rev. C 29, 2031 (1984)", doi="10.1103/PhysRevC.29.2031",
         proj="T", target="D", e="EN", s="1DATA", err=("pct_col", "ERR-T"),
         note="Triton beam on D2 gas target (inverse kinematics); EXFOR S column ignored."),
    dict(reaction="DT", branch="DT", entry="C0295", subent=2, path="C02/C0295.x4",
         label="Brown 1987", authors="R.E. Brown, N. Jarmie, G.M. Hale",
         ref="Phys. Rev. C 35, 1999 (1987)", doi="10.1103/PhysRevC.35.1999",
         proj="D", target="T", e="EN", s="1DATA", err=("pct_common", "ERR-T"),
         note="EXFOR S column ignored; total error from COMMON block."),
    dict(reaction="DT", branch="DT", entry="C0004", subent=2, path="C00/C0004.x4",
         label="Bame 1957", authors="S.J. Bame, J.E. Perry",
         ref="Phys. Rev. 107, 1616 (1957)", doi="10.1103/PhysRev.107.1616",
         proj="D", target="T", e="EN", s="DATA", err=("pct_common", "DATA-ERR"),
         note="Only points with E_cm <= 550 keV (Bosch-Hale validity limit)."),
    dict(reaction="DD", branch="n", entry="A1142", subent=2, path="A11/A1142.x4",
         label="Preston 1954", authors="G. Preston, P.F.D. Shaw, J.A. Young",
         ref="Proc. R. Soc. A 226, 206 (1954)", doi="10.1098/rspa.1954.0249",
         proj="D", target="D", e="EN", s="DATA", err=("abs", "DATA-ERR"),
         note="D(d,n)3He."),
    dict(reaction="DD", branch="p", entry="A1142", subent=3, path="A11/A1142.x4",
         label="Preston 1954", authors="G. Preston, P.F.D. Shaw, J.A. Young",
         ref="Proc. R. Soc. A 226, 206 (1954)", doi="10.1098/rspa.1954.0249",
         proj="D", target="D", e="EN", s="DATA", err=("abs", "DATA-ERR"),
         note="D(d,p)T."),
    dict(reaction="DD", branch="n", entry="C1499", subent=3, path="C14/C1499.x4",
         label="Leonard 2006", authors="D.S. Leonard, H.J. Karwowski, C.R. Brune, B.M. Fisher, E.J. Ludwig",
         ref="Phys. Rev. C 73, 045801 (2006)", doi="10.1103/PhysRevC.73.045801",
         proj="D", target="D", e="EN", s="DATA", err=("abs", "DATA-ERR"),
         note="D(d,n)3He; EXFOR energy taken as effective deuteron lab energy."),
    dict(reaction="DD", branch="p", entry="C1499", subent=2, path="C14/C1499.x4",
         label="Leonard 2006", authors="D.S. Leonard, H.J. Karwowski, C.R. Brune, B.M. Fisher, E.J. Ludwig",
         ref="Phys. Rev. C 73, 045801 (2006)", doi="10.1103/PhysRevC.73.045801",
         proj="D", target="D", e="EN", s="DATA", err=("abs", "DATA-ERR"),
         note="D(d,p)T; EXFOR energy taken as effective deuteron lab energy."),
    dict(reaction="DD", branch="n", entry="O1171", subent=2, path="O11/O1171.x4",
         label="Greife 1995", authors="U. Greife, F. Gorris, M. Junker, C. Rolfs, D. Zahnow",
         ref="Z. Phys. A 351, 107 (1995)", doi="10.1007/BF01292792",
         proj=None, target=None, e="EN-CM", s="2DATA", err=("abs", "2ERR-T"),
         note="D(d,n)3He; EXFOR energy already centre-of-mass (second data/error column pair)."),
    dict(reaction="DD", branch="p", entry="O1171", subent=2, path="O11/O1171.x4",
         label="Greife 1995", authors="U. Greife, F. Gorris, M. Junker, C. Rolfs, D. Zahnow",
         ref="Z. Phys. A 351, 107 (1995)", doi="10.1007/BF01292792",
         proj=None, target=None, e="EN-CM", s="1DATA", err=("abs", "1ERR-T"),
         note="D(d,p)T; EXFOR energy already centre-of-mass (first data/error column pair)."),
]
UNIT_TO_BARN = {"B": 1.0, "MB": 1e-3}
UNIT_TO_KEV = {"KEV": 1.0, "MEV": 1e3}


def subentry(text, number):
    """Return the lines of subentry NUMBER (e.g. 2 for C0018002)."""
    lines, take = [], False
    for line in text.splitlines():
        if line.startswith("SUBENT"):
            take = line.split()[1].endswith(f"{number:03d}")
        if take:
            lines.append(line)
    return lines


def block(lines, key):
    """Header names, units and numeric rows of a DATA or COMMON block (11-char fields)."""
    start = next(i for i, ln in enumerate(lines) if ln.startswith(key + " ") and ln[11:].split()[0].isdigit())
    count = int(lines[start].split()[1])
    # A trailing digit in the 11th character is the field number: "DATA      1" -> "1DATA".
    names = []
    for i in range(0, 66, 11):
        field = lines[start + 1][i:i + 11]
        if field.strip():
            names.append(field[10] + field[:10].strip() if field[10:11].isdigit() else field.strip())
    units = [lines[start + 2][i:i + 11].strip() for i in range(0, 66, 11)][:len(names)]
    rows = []
    for ln in lines[start + 3:start + 3 + (count if key == "COMMON" else 10**6)]:
        if ln.startswith("END"):
            break
        rows.append([float(ln[i:i + 11]) if ln[i:i + 11].strip() else None
                     for i in range(0, 11 * len(names), 11)])
    return dict(zip(names, units)), names, rows


def convert(spec, text):
    sub = subentry(text, spec["subent"])
    units, names, rows = block(sub, "DATA")
    ie, isg = names.index(spec["e"]), names.index(spec["s"])
    kind, ekey = spec["err"]
    if kind == "pct_common":
        cunits, cnames, crow = block(sub, "COMMON")
        assert cunits[ekey] == "PER-CENT", cunits
        common_pct = crow[0][cnames.index(ekey)]
    reaction = spec["reaction"]
    if spec["proj"]:
        ratio = MASS[spec["target"]] / (MASS[spec["proj"]] + MASS[spec["target"]])
    else:
        ratio = 1.0
    points = []
    for row in rows:
        e_lab = row[ie] * UNIT_TO_KEV[units[names[ie]]]
        e_cm = e_lab * ratio
        sig = row[isg] * UNIT_TO_BARN[units[names[isg]]]
        if kind == "abs":
            dsig = row[names.index(ekey)] * UNIT_TO_BARN[units[ekey]]
        elif kind == "pct_col":
            assert units[ekey] == "PER-CENT"
            dsig = sig * row[names.index(ekey)] / 100
        else:
            dsig = sig * common_pct / 100
        if reaction == "DT" and e_cm > 550:
            continue
        # S = sigma E exp(sqrt(E_G/E)), E_G = B_G^2, E in keV, sigma in barn.
        boost = math.exp(BG[reaction] / math.sqrt(e_cm))
        points.append(dict(e_lab_keV=round(e_lab, 6), e_cm_keV=round(e_cm, 6),
                           sigma_b=sig, dsigma_b=dsig,
                           S_keVb=sig * e_cm * boost, dS_keVb=dsig * e_cm * boost))
    points.sort(key=lambda pt: pt["e_cm_keV"])
    return points, ratio


def main(workdir):
    work = Path(workdir)
    if work.exists() and any(work.iterdir()):
        raise SystemExit(f"{work} is not empty; use a fresh directory")
    work.mkdir(parents=True, exist_ok=True)
    hashes, series = {}, []
    for spec in SETS:
        local = work / Path(spec["path"]).name
        if not local.exists():
            with urllib.request.urlopen(BASE + spec["path"], timeout=60) as r:
                local.write_bytes(r.read())
        raw = local.read_bytes()
        hashes[spec["entry"]] = hashlib.sha256(raw).hexdigest()
        points, ratio = convert(spec, raw.decode("ascii", "replace"))
        series.append(dict(
            reaction=spec["reaction"], branch=spec["branch"], label=spec["label"],
            exfor_entry=spec["entry"], exfor_subentry=f"{spec['entry']}{spec['subent']:03d}",
            authors=spec["authors"], reference=spec["ref"], doi=spec["doi"],
            columns=f"{spec['e']}, {spec['s']}, {spec['err'][1]} of the EXFOR data table",
            lab_to_cm=("E_cm = E_lab * m_target/(m_proj + m_target) = E_lab * %.6f" % ratio
                       if spec["proj"] else "none; EXFOR energy is centre-of-mass"),
            projectile=spec["proj"], target=spec["target"], note=spec["note"], points=points))
    out = dict(
        description="Measured fusion cross sections from EXFOR converted to the S-factor "
                    "S = sigma E exp(sqrt(E_G/E)); E, E_G in keV, sigma in barn, S in keV b.",
        source=f"IAEA-NDS/exfor_master commit {COMMIT} (EXFOR master files of the IAEA Nuclear Data Section)",
        access_note="nds.iaea.org/exfor returns a Cloudflare challenge (HTTP 403) to scripts.",
        bosch_hale={k: {"A": v["A"], "B": v["B"]} for k, v in BH_ALL.items()},
        bosch_hale_note="Copied from data/ch02/cross-sections.json; Bosch & Hale, Nucl. Fusion 32, 611 (1992), "
                        "Table IV, S in keV mb, E in keV.",
        masses_u=MASS, B_G_sqrt_keV=BG, entry_sha256=hashes, series=series)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    for s in series:
        print(s["reaction"], s["branch"], s["exfor_subentry"], s["label"], len(s["points"]),
              "pts E_cm %.1f-%.1f" % (s["points"][0]["e_cm_keV"], s["points"][-1]["e_cm_keV"]))


if __name__ == "__main__":
    main(sys.argv[1])
