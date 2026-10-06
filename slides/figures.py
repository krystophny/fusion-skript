"""Deck figures for Fusion Physics chapter 0, drawn from derivations/build/plotdata.

Slide geometry: figures are made at their final size on the A4-landscape deck
(full width 257 mm), so 18 pt here is 18 pt on the slide, matching the deck
body text. Direct labels replace legends. Writes slides/build/fig/<name>.svg.

    python3 slides/figures.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "derivations/build/plotdata"
OUT = ROOT / "slides/build/fig"
FONTS = ROOT / "fonts"

INK = "#17202A"
MUTED = "#526175"
GRID = "#E3E6EA"
BLUE = "#0072B2"
ORANGE = "#B55000"
GREEN = "#1B7F5B"
GREY = "#9AA5B1"
MM = 1 / 25.4


def style():
    for f in ("STIXTwoText-Regular.otf", "STIXTwoText-Italic.otf", "STIXTwoMath-Regular.otf"):
        font_manager.fontManager.addfont(str(FONTS / f))
    plt.rcParams.update({
        "font.family": "STIX Two Text",
        "mathtext.fontset": "custom",
        "mathtext.rm": "STIX Two Text",
        "mathtext.it": "STIX Two Text:italic",
        "mathtext.bf": "STIX Two Text",
        "font.size": 18,
        "axes.labelsize": 18,
        "xtick.labelsize": 16,
        "ytick.labelsize": 16,
        "axes.edgecolor": INK,
        "axes.linewidth": 0.8,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.fonttype": "path",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    })


def load(name):
    return json.loads((DATA / f"{name}.json").read_text())


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg")
    fig.savefig(OUT / f"{name}.png", dpi=110)
    plt.close(fig)


def energy_gdp():
    """Rosling-style: primary energy per person against income, bubble area ∝ population."""
    d = load("02-energy-gdp")
    obs = [o for o in d["observations"] if o["x"] > 0 and o["y"] > 0]
    x = np.array([o["x"] for o in obs])
    y = np.array([o["y"] for o in obs])
    pop = np.array([o["population"] for o in obs], dtype=float)
    fig, ax = plt.subplots(figsize=(257 * MM, 128 * MM))
    size = 2600 * pop / pop.max()
    order = np.argsort(-pop)
    ax.scatter(x[order], y[order], s=size[order] + 6, color=BLUE, alpha=0.45,
               edgecolor="white", linewidth=0.6, zorder=2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(700, 2.2e5)
    ax.set_ylim(1, 1000)
    ax.set_xlabel("income: GDP per person [international \\$/a, PPP]")
    ax.set_ylabel("primary energy [kWh/(person d)]")
    ax.grid(True, which="major", color=GRID, linewidth=0.6, zorder=0)
    label = {"USA": (1.12, 1.0), "CHN": (0.42, 1.35), "IND": (1.12, 0.78), "AUT": (1.15, 0.62),
             "NGA": (1.12, 0.8), "BRA": (0.55, 1.22), "DEU": (0.55, 1.45), "QAT": (0.62, 1.15),
             "ETH": (1.12, 1.15)}
    for o in obs:
        if o["iso3"] in label:
            fx, fy = label[o["iso3"]]
            colour = ORANGE if o["iso3"] == "AUT" else INK
            ax.annotate(o["country"].replace("United States", "USA"), (o["x"], o["y"]),
                        (o["x"] * fx, o["y"] * fy), fontsize=15, color=colour, zorder=3)
    aut = next(o for o in obs if o["iso3"] == "AUT")
    ax.scatter([aut["x"]], [aut["y"]], s=size[[o["iso3"] for o in obs].index("AUT")] + 6,
               color=ORANGE, edgecolor="white", linewidth=0.6, zorder=3)
    ax.text(0.01, 0.97, "bubble area: population, 2024", transform=ax.transAxes,
            fontsize=14, color=MUTED, va="top")
    fig.subplots_adjust(left=0.09, right=0.99, bottom=0.16, top=0.98)
    save(fig, "energy_gdp")


def micro_macro():
    """The lecturer's bottom-up estimate as a stack, next to Austria's measured balance."""
    d = load("04-micro-macro")
    comp = d["legacy_components"]
    fig, ax = plt.subplots(figsize=(257 * MM, 118 * MM))
    colours = [BLUE, "#3D8CC4", "#6FAAD4", "#9CC5E4", "#C2DBEE", "#DCE9F5"]
    left = 0
    for (name, value), c in zip(comp.items(), colours):
        ax.barh(1, value, left=left, color=c, edgecolor="white", height=0.55)
        k = list(comp).index(name)
        yl = (1.36, 1.68, 2.0)[k % 3]
        ax.plot([left + value / 2] * 2, [1.28, yl - 0.02], color=GREY, lw=0.7)
        ax.text(left + value / 2, yl, f"{name} {value:g}", ha="center", va="bottom",
                fontsize=13, color=INK)
        left += value
    ax.text(left + 2, 1, f"{left:g}", va="center", fontsize=18, color=BLUE)
    ax.barh(0, d["gross_kWh_person_day"], color=ORANGE, height=0.55)
    ax.barh(0, d["final_kWh_person_day"], color="#D98A55", height=0.55)
    ax.text(d["final_kWh_person_day"] / 2, 0, f"final {d['final_kWh_person_day']:.0f}",
            ha="center", va="center", color="white", fontsize=16)
    ax.text(d["gross_kWh_person_day"] + 2, 0, f"gross {d['gross_kWh_person_day']:.0f}",
            va="center", fontsize=18, color=ORANGE)
    ax.axvline(d["legacy_GDP_crosscheck_kWh_person_day"], color=MUTED, linestyle=":", lw=1.2)
    ax.text(d["legacy_GDP_crosscheck_kWh_person_day"] - 1.5, -0.55,
            "GDP × energy intensity", ha="right", fontsize=14, color=MUTED)
    ax.set_yticks([0, 1], ["Austria 2025\n(Statistics Austria)", "bottom-up\nestimate"])
    ax.set_xlim(0, 180)
    ax.set_ylim(-0.7, 2.4)
    ax.set_xlabel("energy [kWh/(person d)]")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=0.17, right=0.98, bottom=0.17, top=0.99)
    save(fig, "micro_macro")


def resources():
    """Static reserve-to-production years: stock divided by today's rate."""
    d = load("06-resource-lifetimes")
    names = {"oil": "oil", "gas": "natural gas", "coal_combined": "coal",
             "uranium_lowcost": "uranium, low cost", "uranium_identified_below_260_USD_kg": "uranium, < 260 \\$/kg"}
    rows = [(names[r["resource"]], r["static_years"]) for r in d["resources"] if r["resource"] in names]
    rows.sort(key=lambda r: r[1])
    fig, ax = plt.subplots(figsize=(257 * MM, 110 * MM))
    ys = np.arange(len(rows))
    colours = [ORANGE if "uranium" in n else BLUE for n, _ in rows]
    ax.barh(ys, [v for _, v in rows], color=colours, height=0.6)
    for yy, (_, v) in zip(ys, rows):
        ax.text(v + 2, yy, f"{v:.0f} a", va="center", fontsize=17)
    ax.set_yticks(ys, [n for n, _ in rows])
    ax.axvline(100, color=MUTED, linestyle=":", lw=1.2)
    ax.text(102, -0.75, "one human lifetime", fontsize=14, color=MUTED, va="center")
    ax.set_ylim(-1.1, len(rows) - 0.5)
    ax.set_xlabel("reserves / current production [years]")
    ax.set_xlim(0, 175)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=0.2, right=0.98, bottom=0.18, top=0.97)
    save(fig, "resources")


def solar_chain():
    """From 1000 W/m² at noon to delivered electric power per module area in Graz."""
    d = load("07-solar-chain")
    labels = {"noon_peak": "noon peak", "day_night": "day/night", "latitude": "sun angle",
              "season": "seasons", "atmosphere_weather_residual": "weather",
              "tilt_gain": "tilted module", "module_efficiency": "efficiency 20 %",
              "performance_ratio": "system losses"}
    st = d["stages"]
    fig, ax = plt.subplots(figsize=(257 * MM, 122 * MM))
    xs = np.arange(len(st))
    vals = [s["W_m2"] for s in st]
    elec = [i >= 6 for i in range(len(st))]
    ax.bar(xs, vals, color=[ORANGE if e else BLUE for e in elec], width=0.62)
    for x, v in zip(xs, vals):
        ax.text(x, v * 1.12, f"{v:.0f}", ha="center", fontsize=17)
    ax.set_yscale("log")
    ax.set_ylim(10, 2500)
    ax.set_xticks(xs, [labels[s["stage"]].replace(" ", "\n", 1) for s in st], rotation=0, fontsize=14)
    ax.set_ylabel("power per area [W/m²]")
    ax.text(0.99, 0.97, "Graz, PVGIS 2005–2023", transform=ax.transAxes, ha="right",
            va="top", fontsize=14, color=MUTED)
    ax.text(6.5, 300, "electric", ha="center", fontsize=16, color=ORANGE)
    ax.text(2.5, 600, "sunlight", ha="center", fontsize=16, color=BLUE)
    fig.subplots_adjust(left=0.09, right=0.99, bottom=0.16, top=0.98)
    save(fig, "solar_chain")


def pv_prices():
    """Module price history, constant 2025 dollars, log scale."""
    d = load("09-pv-prices")
    yrs = np.array(d["years"])
    p = np.array(d["prices"])
    fig, ax = plt.subplots(figsize=(257 * MM, 122 * MM))
    ax.plot(yrs, p, color=BLUE, lw=2.2)
    ax.scatter(yrs[[0, -1]], p[[0, -1]], color=BLUE, zorder=3, s=40)
    ax.text(yrs[0] + 0.8, p[0], f"{p[0]:.0f} \\$/W", va="center", fontsize=17)
    ax.text(yrs[-1] - 1.2, p[-1] * 0.72, f"{p[-1]:.2f} \\$/W", ha="right", va="top", fontsize=17)
    ax.set_ylim(0.12, 300)
    ax.set_yscale("log")
    ax.set_xlim(1973, 2026)
    ax.set_ylabel("PV module price [2025 \\$/W]")
    ax.grid(True, which="major", axis="y", color=GRID, linewidth=0.6)
    ax.text(0.99, 0.97, rf"$\approx$ {round(p[0] / p[-1], -2):.0f} times cheaper", transform=ax.transAxes,
            ha="right", va="top", fontsize=20, color=ORANGE)
    fig.subplots_adjust(left=0.09, right=0.99, bottom=0.1, top=0.98)
    save(fig, "pv_prices")


def area_budget():
    """Share of Austria's area needed to deliver Austria's final energy demand."""
    d = load("11-area-budget")
    rows = [s for s in d["scenarios"] if s["boundary"] == "final"]
    rows.sort(key=lambda s: -s["fraction_of_Austria"])
    names = {"biofuel": "biofuel", "wind": "wind", "solar": "solar PV", "solar_low": "solar PV", "solar_high": "solar PV"}
    fig, ax = plt.subplots(figsize=(257 * MM, 112 * MM))
    ys = np.arange(len(rows))[::-1]
    frac = [100 * s["fraction_of_Austria"] for s in rows]
    ax.barh(ys, frac, color=[GREEN if s["technology"] == "biofuel" else BLUE if s["technology"] == "wind" else ORANGE for s in rows], height=0.6)
    for yy, s, f in zip(ys, rows, frac):
        ax.text(f + 1, yy, f"{f:.0f} %" if f >= 10 else f"{f:.1f} %", va="center", fontsize=17)
    ax.set_yticks(ys, [f"{names.get(s['technology'], s['technology'])}  {s['density_W_m2']:g} W/m²" for s in rows])
    ax.axvline(100, color=INK, lw=1.0)
    ax.text(99, ys[0] + 0.45, "all of Austria", ha="right", fontsize=14, color=MUTED)
    ax.set_xlim(0, 105)
    ax.set_xlabel("area needed for Austria's final energy [% of national area]")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=0.24, right=0.98, bottom=0.17, top=0.97)
    save(fig, "area_budget")


def fuel_mass():
    """Fuel mass for one gigawatt-year of heat or electricity, log scale."""
    f = load("13-fusion")
    n = load("12-fission")
    rows = [("coal", f["coal_kg"], "1 GW heat"),
            ("natural uranium", n["natural_t_U"] * 1e3, "1 GW electric"),
            ("enriched uranium", n["enriched_t_U"] * 1e3, "1 GW electric"),
            ("deuterium + tritium", f["fuel_kg"], "1 GW heat")]
    fig, ax = plt.subplots(figsize=(257 * MM, 112 * MM))
    ys = np.arange(len(rows))[::-1]
    ax.barh(ys, [r[1] for r in rows], color=[GREY, BLUE, BLUE, ORANGE], height=0.6)
    def human(kg):
        return f"{kg / 1e9:.1f} Mt" if kg >= 1e8 else f"{kg / 1e3:.0f} t" if kg >= 1e3 else f"{kg:.0f} kg"
    for yy, r in zip(ys, rows):
        ax.text(r[1] * 1.5, yy, f"{human(r[1])}  · {r[2]}", va="center", fontsize=16)
    ax.set_xscale("log")
    ax.set_xlim(10, 1e13)
    ax.set_yticks(ys, [r[0] for r in rows])
    ax.set_xlabel("fuel mass per gigawatt-year [kg]")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=0.22, right=0.98, bottom=0.17, top=0.97)
    save(fig, "fuel_mass")


def true_scale():
    """Weesow solar park (Sentinel-2) and the city of Graz on identical metre axes."""
    d = load("08-park-and-graz")
    img = plt.imread(ROOT / "slides/photos/weesow-sentinel-same-scale.jpg")
    ext = [v / 1000 for v in d["map_extent_relative_to_park_m"]]
    graz = json.loads((ROOT / "data/ch00/processed/graz-outline-metres.geojson").read_text())
    ring = np.array(graz["features"][0]["geometry"]["coordinates"][0]) / 1000
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(257 * MM, 128 * MM))
    a1.imshow(img, extent=ext)
    a1.add_patch(matplotlib.patches.Circle((0, -0.1), 1.6, fill=False, edgecolor=ORANGE, lw=2.0))
    a1.annotate("solar park", (1.2, 1.1), (3.0, 3.6), color="white", fontsize=16,
                arrowprops=dict(arrowstyle="-", color="white", lw=1.0))
    a1.set_title(f"solar park Weesow, {d['park_area_km2']:.2f} km², {d['peak_MWp']:.0f} MW peak",
                 fontsize=15, color=INK, loc="left")
    a2.fill(ring[:, 0], ring[:, 1], color="#EEF2F6", edgecolor=INK, lw=1.0)
    side = d["area_for_1_GW_average_km2"] ** 0.5
    cx, cy = ring[:, 0].mean(), ring[:, 1].mean()
    a2.add_patch(plt.Rectangle((cx - side / 2, cy - side / 2), side, side, fill=True,
                               facecolor="#B5500033", edgecolor=ORANGE, lw=1.6))
    a2.text(cx, cy, f"{d['area_for_1_GW_average_km2']:.0f} km²\n= 1 GW average", ha="center",
            va="center", fontsize=16, color=ORANGE)
    a2.set_title(f"city of Graz, {d['graz_published_area_km2']:.0f} km²", fontsize=15,
                 color=INK, loc="left")
    for a in (a1, a2):
        a.set_xlim(-8, 8)
        a.set_ylim(-8, 8)
        a.set_aspect("equal")
        a.set_xlabel("x [km]")
        a.tick_params(labelsize=14)
    a1.set_ylabel("y [km]")
    fig.subplots_adjust(left=0.07, right=0.99, bottom=0.13, top=0.92, wspace=0.15)
    save(fig, "true_scale")


def csv_rows(name):
    import csv
    lines = [l for l in (ROOT / "data/ch00/processed" / name).read_text().splitlines() if not l.startswith("#")]
    return list(csv.DictReader(lines))


def austria_mix():
    """Gross inland energy by carrier and final energy by sector, Austria 2025."""
    d = load("05-austria-flow")
    label = {n["id"]: n["label"] for n in d["nodes"]}
    prim = [(label[l["source"]], l["value"]) for l in d["links"] if l["target"] == "gross"]
    sect = {}
    for l in d["links"]:
        if l["target"].startswith("sector_"):
            sect[label[l["target"]]] = sect.get(label[l["target"]], 0) + l["value"]
    prim.sort(key=lambda r: -r[1])
    sect = sorted(sect.items(), key=lambda r: -r[1])
    fig, ax = plt.subplots(figsize=(257 * MM, 122 * MM))
    pal = [BLUE, "#3D8CC4", "#6FAAD4", "#9CC5E4", "#C2DBEE", "#DCE9F5"]
    for row, items, cols in ((1, prim, pal), (0, sect, [ORANGE, "#C9733A", "#D98A55", "#E7A97F", "#F2CDB4"])):
        left = 0
        for k, ((name, v), c) in enumerate(zip(items, cols)):
            ax.barh(row, v, left=left, color=c, edgecolor="white", height=0.5)
            if v > 9:
                ax.text(left + v / 2, row, f"{name}\n{v:.0f}", ha="center", va="center",
                        fontsize=13, color="white" if k < 2 else INK, linespacing=1.1)
            left += v
        ax.text(left + 1.5, row, f"{left:.0f}", va="center", fontsize=18,
                color=BLUE if row else ORANGE)
    ax.set_yticks([0, 1], ["final energy\nby sector", "gross inland\nby carrier"])
    ax.set_xlim(0, 125)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xlabel("energy [kWh/(person d)], Austria 2025 (preliminary)")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=0.15, right=0.98, bottom=0.17, top=0.98)
    save(fig, "austria_mix")


def land_density():
    """Average power per land area: why biofuel loses."""
    rows = [("corn ethanol", 0.317, GREEN), ("wind", 2, BLUE), ("solar PV, park", 10, ORANGE),
            ("solar PV, module", 20, ORANGE)]
    land = {r["place"]: float(r["faostat_arable_ha_person"]) for r in csv_rows("land-use.csv")}
    fig, ax = plt.subplots(figsize=(257 * MM, 112 * MM))
    ys = np.arange(len(rows))[::-1]
    ax.barh(ys, [r[1] for r in rows], color=[r[2] for r in rows], height=0.6)
    for yy, r in zip(ys, rows):
        ax.text(r[1] * 1.15, yy, f"{r[1]:g} W/m²", va="center", fontsize=17)
    ax.set_xscale("log")
    ax.set_xlim(0.1, 100)
    ax.set_yticks(ys, [r[0] for r in rows])
    ax.set_xlabel("average power per land area [W/m²]")
    ax.text(0.99, 0.97, f"arable land: world {land['World'] * 1e4:.0f} m², Austria {land['Austria'] * 1e4:.0f} m² per person (2023)",
            transform=ax.transAxes, ha="right", va="top", fontsize=14, color=MUTED)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=0.2, right=0.98, bottom=0.17, top=0.97)
    save(fig, "land_density")


def risk():
    """Birds killed per year by cause (USA) and deaths per TWh of electricity."""
    birds = [r for r in csv_rows("wildlife-risk.csv") if r["unit"] == "birds/year"]
    deaths = sorted(csv_rows("energy-deaths-per-TWh.csv"), key=lambda r: float(r["deaths_per_TWh"]))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(257 * MM, 122 * MM))
    names = {"Free-ranging domestic cats": "cats", "Building collisions": "buildings",
             "Vehicle collisions": "vehicles", "Power lines, collision + electrocution": "power lines",
             "Wind turbine collisions, monopole estimate": "wind turbines"}
    for k, r in enumerate(birds):
        lo, hi = float(r["low"]), float(r["high"])
        c = ORANGE if "Wind" in r["cause"] else BLUE
        a1.plot([lo, hi], [k, k], color=c, lw=9, solid_capstyle="butt")
    a1.set_yticks(range(len(birds)), [names.get(r["cause"], r["cause"]) for r in birds])
    a1.invert_yaxis()
    a1.set_xscale("log")
    a1.set_xlim(5e4, 1e10)
    a1.set_xlabel("birds killed per year, USA")
    a2.barh(range(len(deaths)), [float(r["deaths_per_TWh"]) for r in deaths],
            color=[ORANGE if r["source_type"] in ("Solar", "Wind", "Nuclear", "Hydropower") else GREY for r in deaths],
            height=0.6)
    for k, r in enumerate(deaths):
        v = float(r["deaths_per_TWh"])
        a2.text(v * 1.2, k, f"{v:g}", va="center", fontsize=14)
    a2.set_yticks(range(len(deaths)), [r["source_type"].lower() for r in deaths])
    a2.set_xscale("log")
    a2.set_xlim(0.01, 200)
    a2.set_xlabel("deaths per TWh of electricity")
    for a in (a1, a2):
        a.spines["left"].set_visible(False)
        a.tick_params(axis="y", length=0, labelsize=15)
    fig.subplots_adjust(left=0.13, right=0.98, bottom=0.16, top=0.97, wspace=0.45)
    save(fig, "risk")


def lifecycle():
    """Life-cycle greenhouse emissions per kWh: median and range of studies."""
    rows = sorted(csv_rows("lifecycle-emissions.csv"), key=lambda r: float(r["median_gCO2eq_kWh"]))
    fig, ax = plt.subplots(figsize=(257 * MM, 122 * MM))
    for k, r in enumerate(rows):
        lo, med, hi = (float(r[c]) for c in ("min_gCO2eq_kWh", "median_gCO2eq_kWh", "max_gCO2eq_kWh"))
        c = GREY if med > 200 else BLUE
        ax.plot([lo, hi], [k, k], color=c, lw=2.2)
        ax.scatter([med], [k], color=c, s=70, zorder=3)
        ax.text(hi * 1.15, k, f"{med:.0f}", va="center", fontsize=15, color=c)
    ax.set_yticks(range(len(rows)), [r["technology"].replace("Concentrating solar power", "solar thermal (CSP)") for r in rows])
    ax.set_xscale("log")
    ax.set_xlim(0.4, 4000)
    ax.set_xlabel("life-cycle emissions [g CO₂-eq per kWh electricity]; dot: median of studies")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=15)
    fig.subplots_adjust(left=0.22, right=0.98, bottom=0.15, top=0.98)
    save(fig, "lifecycle")


if __name__ == "__main__":
    style()
    for fn in (energy_gdp, micro_macro, resources, solar_chain, pv_prices, area_budget, fuel_mass, true_scale, austria_mix, land_density, risk, lifecycle):
        fn()
        print("wrote", fn.__name__)
