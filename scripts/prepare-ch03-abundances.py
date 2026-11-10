#!/usr/bin/env python3
"""Solar-system element abundances from Asplund, Amarsi & Grevesse (2021).

Usage: python3 -I scripts/prepare-ch03-abundances.py HTML
HTML = https://ar5iv.labs.arxiv.org/html/2105.01661 (arXiv version of
A&A 653, A141 (2021), doi:10.1051/0004-6361/202140445, CC BY 4.0), Table 2,
parsed as text only. Photospheric log eps (log10 N/N_H + 12) where measured,
otherwise CI-chondrite values (meteoritic scale).
Output: data/ch03/abundances.json.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/ch03/abundances.json"


def cell_text(c):
    c = re.sub(r"<annotation.*?</annotation>", "", c, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip()


def value(s):
    m = re.match(r"^\s*(-?)\s*(\d+\.\d+)", s.replace("−", "-"))
    return float(m.group(1) + m.group(2)) if m else None


def main(path):
    t = Path(path).read_text()
    table = re.findall(r"<table.*?</table>", t, re.S)[1]
    rows = []
    for tr in re.findall(r"<tr.*?</tr>", table, re.S):
        cells = [cell_text(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
        for k in (0, 5):
            if len(cells) >= k + 4 and cells[k].isdigit():
                rows.append({"Z": int(cells[k]), "element": cells[k + 1],
                             "photosphere": value(cells[k + 2]), "meteorite": value(cells[k + 3])})
    rows.sort(key=lambda r: r["Z"])
    # Volatile elements are depleted in CI chondrites; Li is depleted in the photosphere.
    volatile = {"H", "He", "C", "N", "O", "Ne", "Ar", "Kr", "Xe"}
    for r in rows:
        use_met = r["element"] not in volatile and r["meteorite"] is not None
        r["log_eps"] = r["meteorite"] if use_met else r["photosphere"]
    out = {"source": "Asplund, Amarsi & Grevesse, A&A 653, A141 (2021), doi:10.1051/0004-6361/202140445, "
                     "Table 2 (CC BY 4.0); photosphere for H, He, C, N, O and noble gases, CI chondrites otherwise",
           "note": "log_eps = log10(N_el / N_H) + 12", "elements": rows}
    OUT.write_text(json.dumps(out, indent=0))
    print(len(rows), "elements;", [(r["element"], r["log_eps"]) for r in rows[:8]], rows[25])


if __name__ == "__main__":
    main(sys.argv[1])
