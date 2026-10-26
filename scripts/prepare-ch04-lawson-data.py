"""Measured Lawson parameters from Wurzel and Hsu (2022), Tables 6-8, as CSV.

Source: S. E. Wurzel and S. C. Hsu, Phys. Plasmas 29, 062103 (2022),
doi:10.1063/5.0083990, CC BY 4.0; the tables are read from the LaTeX source of
arXiv:2105.10954v4 (table_6.tex, table_7.tex, table_8.tex).

    curl -L -o wh.tar.gz https://arxiv.org/e-print/2105.10954v4 && mkdir wh && tar xzf wh.tar.gz -C wh
    python3 -I scripts/prepare-ch04-lawson-data.py wh > data/ch04/wurzel_hsu_2022.csv

MCF rows give the peak ion density n_i0 and the confinement time tau_E*;
ICF rows give n tau and the stagnation time tau_stag, so n = n tau / tau_stag.
"""
import csv
import re
import sys
from pathlib import Path

HEADER = """# Wurzel and Hsu, Phys. Plasmas 29, 062103 (2022), doi:10.1063/5.0083990, CC BY 4.0.
# Tables 6 (tokamaks, stellarators), 7 (alternate magnetic concepts), 8 (ICF, MIF), from arXiv:2105.10954v4.
# MCF: n = n_i0 (peak ion density), tau = tau_E*; ICF/MIF: n = (n tau) / tau_stag. Units: keV, m^-3, s.
# notes: inferences flagged in the source tables. shot = Projected marks design values, not measurements.
"""


def number(cell):
    m = re.search(r"\\num\{([^}]*)\}", cell)
    if m:
        return m.group(1)
    c = re.sub(r"\$[^$]*\$", "", cell).strip()
    return "" if c in ("–", "-", "") else c


def flags(cell):
    out = []
    if "ddagger" in cell:
        out.append("n_i from n_e")
    elif "dagger" in cell:
        out.append("T_i from T_e")
    if "*" in re.sub(r"\\num\{[^}]*\}", "", cell):
        out.append("peak from average")
    if "#" in cell:
        out.append("tau_E* from tau_E")
    return "; ".join(out)


def main(src):
    w = csv.writer(sys.stdout, lineterminator="\n")
    sys.stdout.write(HEADER)
    w.writerow(["project", "concept", "year", "shot", "T_keV", "n_m3", "tau_s", "n_tau_m3s",
                "nTtau_keVsm3", "notes", "table"])
    for name, kind in (("table_6.tex", "6"), ("table_7.tex", "7"), ("table_8.tex", "8")):
        for line in (Path(src) / name).read_text().splitlines():
            if "&" not in line or "thead" in line:
                continue
            c = [x.strip() for x in line.rstrip().rstrip("\\").split("&")]
            shot = re.sub(r"\$([^$]*)\$", r"\1", c[3])
            if kind != "8":
                t, n, tau, ntau, nttau = (number(c[i]) for i in (5, 7, 9, 10, 11))
                note = "; ".join(x for x in (flags(c[5]), flags(c[7]), flags(c[9])) if x)
            else:
                t, tau, ntau, nttau = (number(c[i]) for i in (5, 10, 12, 13))
                n = f"{float(ntau) / float(tau):.3g}" if tau else ""
                note = "n = n tau / tau_stag" if tau else "tau_stag not reported"
            w.writerow([c[0], c[1], c[2], shot, t, n, tau, ntau, nttau, note, kind])


if __name__ == "__main__":
    main(sys.argv[1])
