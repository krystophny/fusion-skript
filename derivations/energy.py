"""Original energy-budget models and canonical plots (MIT)."""
from pathlib import Path
import json
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/energy.json").read_text())["austria_2025"]
OUT = ROOT / "derivations/build/fig"
BLUE, ORANGE = "#0072B2", "#D55E00"  # Okabe–Ito; labels/styles add redundancy.

def daily_energy(tj, population):
    return tj * 1e12 / (3.6e6 * population * 365)

def area_per_person(daily_kwh, density):
    return daily_kwh * 1000 / 24 / density

def lifetime(stock_years, growth):
    return stock_years if growth == 0 else math.log1p(growth * stock_years) / growth

def save(fig, name):
    fig.tight_layout()
    for ext in ("svg", "pdf", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=150)
    plt.close(fig)

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    for font in (ROOT / "fonts").glob("*.otf"):
        font_manager.fontManager.addfont(font)
    plt.rcParams.update({"font.family": "STIX Two Text", "font.size": 13,
                         "svg.fonttype": "none", "axes.spines.top": False,
                         "axes.spines.right": False})
    n = DATA["population_annual_average"]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    vals = [daily_energy(DATA[k], n) for k in ("primary_TJ", "final_TJ")]
    ax.barh(["Gross inland consumption", "Final consumption"], vals,
            color=[BLUE, ORANGE], height=.55)
    for i, v in enumerate(vals): ax.text(v + 1, i, f"{v:.1f}", va="center")
    ax.set(xlabel="Energy [kWh/(person day)]", xlim=(0, 125))
    save(fig, "energy-boundaries")
    fig, ax = plt.subplots(figsize=(8, 3.8))
    items = list(DATA["sectors_TJ"].items())
    vals = [daily_energy(v, n) for _, v in items]
    ax.barh([k for k, _ in items], vals, color=BLUE, height=.6)
    for i, v in enumerate(vals): ax.text(v + .4, i, f"{v:.1f}", va="center")
    ax.set(xlabel="Final energy [kWh/(person day)]", xlim=(0, 32))
    save(fig, "energy-sectors")
    fig, ax = plt.subplots(figsize=(8, 3.8))
    growth = np.linspace(0, .03, 100)
    ax.plot(growth * 100, [lifetime(100, g) for g in growth], color=BLUE)
    ax.set(xlabel="Annual demand growth [%/year]", ylabel="Exhaustion time [years]",
           xlim=(0, 3), ylim=(0, 110))
    save(fig, "resource-horizon")
    fig, ax = plt.subplots(figsize=(8, 3.8))
    demand = np.linspace(0, 120, 100)
    for q, style, color in [(3, "--", ORANGE), (20, "-", BLUE)]:
        ax.plot(demand, area_per_person(demand, q), style, color=color,
                label=f"Assumed delivered density {q} W/m²")
    ax.set(xlabel="Demand [kWh/(person day)]", ylabel="Area [m²/person]",
           xlim=(0, 120), ylim=(0, 1800))
    ax.legend(frameon=False, fontsize=11)
    save(fig, "energy-area")
    t, g, d, s = sp.symbols("t g D S", positive=True)
    integrated = sp.integrate(d * sp.exp(g * t), (t, 0, t))
    assert sp.simplify(integrated.subs(t, sp.log(1 + g*s/d)/g) - s) == 0
    assert sp.limit(sp.log(1+g*s/d)/g, g, 0) == s/d
    print(f"Primary: {daily_energy(DATA['primary_TJ'],n):.4f}; final: {sum(vals):.4f} kWh/(person day)")
    print("Stock-model identities and zero-growth limit passed")

if __name__ == "__main__": build()
