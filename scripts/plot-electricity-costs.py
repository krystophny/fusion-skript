"""Draw the canonical electricity-cost and hardware-price teaching figures.

The two figures share the audited sourcebook payload with the reference text.
Evidence flags control drawing style; neither missing values nor absent years
are replaced with zero or extrapolated by the plotting code.
"""

import argparse
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "derivations/build/plotdata/09-electricity-cost-history.json"
DEFAULT_OUT = ROOT / "derivations/build/fig"
FIGSIZE = (257 / 25.4, 128 / 25.4)
GREY = "#526175"
BENCHMARK_FLAGS = {"B", "A", "L"}
MODEL_FLAGS = {"M", "I", "R"}
STYLES = {
    "benchmark": "-",
    "model": (0, (4, 2.5)),
    "forecast": (0, (1.1, 2.1)),
}
TECHNOLOGIES = {
    "solar_PV": ("Solar PV", "#B86418", "o"),
    "solar_daily_shift": ("Solar + daily storage", "#9B4B90", "s"),
    "onshore_wind": ("Onshore wind", "#2F7D5B", "^"),
    "natural_gas_CCGT": ("Natural gas (CCGT)", "#356AA0", "v"),
    "coal": ("Coal", "#526175", "s"),
    "nuclear_fission_new": ("New nuclear fission", "#B43D3D", "P"),
}


def configure_fonts():
    for font in (ROOT / "fonts").glob("*.otf"):
        font_manager.fontManager.addfont(font)
    plt.rcParams.update({
        "font.family": ["STIX Two Text", "STIX Two Math"],
        "font.size": 14,
        "axes.labelsize": 15,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.fonttype": "path",
    })


def selected_rows(rows, key, series, value_key):
    selected = sorted((r for r in rows if r[key] == series),
                      key=lambda r: int(r["year"]))
    if not selected:
        raise ValueError(f"No data for {series}")
    years = [int(r["year"]) for r in selected]
    if len(years) != len(set(years)):
        raise ValueError(f"Duplicate years in {series}")
    for row in selected:
        value = float(row[value_key])
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"Non-positive or missing {series} value: {row}")
        if row["evidence_flag"] not in BENCHMARK_FLAGS | MODEL_FLAGS | {"F"}:
            raise ValueError(f"Unknown evidence flag in {series}: {row}")
    return selected


def evidence_kind(row, always_model=False):
    flag = row["evidence_flag"]
    if flag == "F":
        return "forecast"
    if always_model or flag in MODEL_FLAGS:
        return "model"
    return "benchmark"


def draw_series(ax, rows, value_key, color, marker="o", always_model=False):
    """Use the weaker evidence class for each connecting line segment.

    Adjacent M/I/R rows therefore cannot acquire solid lines merely by
    touching a published benchmark. Future F intervals retain their own style.
    """
    priority = {"benchmark": 0, "model": 1, "forecast": 2}
    segments = []
    for left, right in zip(rows, rows[1:]):
        # Independent scenario samples must not acquire a historical bridge.
        if left.get("series_basis") != right.get("series_basis"):
            continue
        kind = max((evidence_kind(left, always_model),
                    evidence_kind(right, always_model)), key=priority.get)
        if (segments and segments[-1][0] == kind
                and segments[-1][1][-1] is left):
            segments[-1][1].append(right)
        else:
            segments.append((kind, [left, right]))
    for kind, segment in segments:
        ax.plot([int(r["year"]) for r in segment],
                [float(r[value_key]) for r in segment],
                color=color, linewidth=2.05, linestyle=STYLES[kind],
                solid_capstyle="round", zorder=3)

    for kind, point_marker, face, size in [
            ("benchmark", marker, color, 3.4),
            ("forecast", marker, "white", 5.0)]:
        points = [r for r in rows if evidence_kind(r, always_model) == kind]
        if points:
            ax.plot([int(r["year"]) for r in points],
                    [float(r[value_key]) for r in points],
                    linestyle="none", marker=point_marker, markersize=size,
                    color=color, markerfacecolor=face, markeredgewidth=1.0,
                    clip_on=False, zorder=4)
    retrospective = [r for r in rows if r["evidence_flag"] == "R"]
    if retrospective:
        ax.plot([int(r["year"]) for r in retrospective],
                [float(r[value_key]) for r in retrospective],
                linestyle="none", marker="o", markersize=5,
                color=color, markerfacecolor="white", markeredgewidth=1.1,
                clip_on=False, zorder=4)


def log_axis(ax, ticks):
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(FixedLocator(ticks))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}"))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(which="minor", left=False)
    ax.grid(True, which="major", axis="y", color="#DCE0E4", linewidth=.65)
    ax.set_axisbelow(True)


def evidence_legend(fig, include_forecast=False, include_retrospective=False):
    handles = [
        Line2D([], [], color=GREY, linewidth=1.8, marker="o", markersize=3.5,
               label="Published benchmarks"),
        Line2D([], [], color=GREY, linewidth=1.8, linestyle=STYLES["model"],
               label="Model / interpolation"),
    ]
    if include_forecast:
        handles.append(Line2D([], [], color=GREY, linewidth=1.8,
                              linestyle=STYLES["forecast"], marker="D",
                              markerfacecolor="white", markersize=4.5,
                              label="Projection"))
    if include_retrospective:
        handles.append(Line2D([], [], color=GREY, linestyle="none", marker="o",
                              markerfacecolor="white", markersize=4.5,
                              label="Retrospective model"))
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.53, .065),
               ncol=len(handles), fontsize=11.5, frameon=False,
               columnspacing=1.4, handlelength=2.4, handletextpad=.55)


def save(fig, out, stem, description):
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{stem}.svg", facecolor="white", metadata={
        "Title": stem.replace("-", " "), "Description": description,
        "Creator": "Fusion Physics; scripts/plot-electricity-costs.py",
    })
    fig.savefig(out / f"{stem}.png", facecolor="white", dpi=144)
    plt.close(fig)


def electricity_cost_history(data, out=DEFAULT_OUT):
    fig = plt.figure(figsize=FIGSIZE)
    ax = fig.add_axes((.092, .235, .880, .60))
    ax.axvspan(2025, 2035, color="#EDF0F3", zorder=0)
    ax.axvline(2025, color="#A6AFB8", linewidth=.7, zorder=1)
    ax.text(2030, 780, "Projections", ha="center", va="center",
            fontsize=12, color=GREY)

    handles = []
    for technology, (label, color, marker) in TECHNOLOGIES.items():
        rows = selected_rows(data["annual"], "technology", technology,
                             "us_cents_per_kWh_2025")
        is_daily = technology == "solar_daily_shift"
        draw_series(ax, rows, "us_cents_per_kWh_2025", color, marker,
                    always_model=is_daily)
        handles.append(Line2D([], [], color=color, linewidth=2.1,
                              linestyle=STYLES["model"] if is_daily else "-",
                              marker=None if is_daily else marker,
                              markersize=4, label=label))
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.53, 1.00),
               ncol=3, fontsize=13, frameon=False, columnspacing=1.9,
               handlelength=2.1, handletextpad=.55, labelspacing=.45)
    log_axis(ax, [1, 3, 10, 30, 100, 300, 1000])
    ax.set(xlim=(1980, 2035), ylim=(1, 1000),
           xticks=[1980, 1990, 2000, 2010, 2020, 2025, 2030, 2035],
           xlabel="Year", ylabel="Generation cost [2025 US cents/kWh]")
    evidence_legend(fig, include_forecast=True)
    fig.text(.5, .012,
             "IRENA · Lazard · ATB trends, 2025 anchors (nuclear: flat to 2030)\n"
             "Gas/coal: constant 2025 real cost · Daily storage: 60% shifted",
             ha="center", va="bottom", fontsize=10, color=GREY)
    save(fig, out, "electricity-cost-history",
         "Levelized electricity cost in 2025 US cents per kWh, 1980–2035. "
         "Global renewable benchmarks and US new-build thermal estimates have "
         "different geographic and financial boundaries. Dashed segments are "
         "models/interpolation; the solar daily-storage curve is a model. "
         "The grey 2025–2035 region contains projections. No firm annual "
         "supply or seasonal-storage guarantee is implied. Sourcebook date: "
         + data["sourcebook_date"])


def solar_storage_capex(data, out=DEFAULT_OUT):
    fig = plt.figure(figsize=FIGSIZE)
    axes = fig.subplots(1, 2, gridspec_kw={
        "left": .095, "right": .970, "bottom": .235, "top": .875,
        "wspace": .38,
    })
    module_ax, storage_ax = axes
    modules = selected_rows(data["components"], "series", "solar_module_only", "value")
    draw_series(module_ax, modules, "value", "#B86418", "o")
    module_ax.set_title("Solar modules", fontsize=16, pad=10)
    log_axis(module_ax, [.1, .3, 1, 3, 10, 30, 100])
    module_ax.set(ylim=(.1, 100), ylabel="Module price [2025 USD/W]")

    handles = []
    for series, label, color, marker in [
            ("Li_ion_cell", "Cell", "#167E83", "o"),
            ("Li_ion_pack_all_uses", "Pack, all uses", "#76528B", "s"),
            ("Li_BESS_turnkey_4h_global", "Installed system, 4 h", "#356AA0", "^")]:
        rows = selected_rows(data["components"], "series", series, "value")
        draw_series(storage_ax, rows, "value", color, marker)
        handles.append(Line2D([], [], color=color, linewidth=2, marker=marker,
                              markersize=4, label=label))
    storage_ax.set_title("Lithium-ion storage", fontsize=16, pad=10)
    log_axis(storage_ax, [100, 300, 1000, 3000, 10000])
    storage_ax.set(ylim=(60, 18000), ylabel="Storage price [2025 USD/kWh capacity]")
    storage_ax.legend(handles=handles, loc="upper right", fontsize=11.8,
                      frameon=False, handlelength=1.8, handletextpad=.55,
                      borderaxespad=.25, labelspacing=.5)
    for ax in axes:
        ax.set(xlim=(1980, 2025), xticks=[1980, 1990, 2000, 2010, 2025],
               xlabel="Year")
    evidence_legend(fig, include_retrospective=True)
    fig.text(.5, .024, "Module and cell histories: OWID source series · "
             "Packs: BloombergNEF · Installed systems: IRENA",
             ha="center", va="bottom", fontsize=10, color=GREY)
    save(fig, out, "solar-storage-capex",
         "Separate logarithmic price histories: solar modules in 2025 USD "
         "per watt, and lithium-ion cells, packs, and four-hour installed "
         "battery systems in 2025 USD per kWh of storage capacity. Both "
         "panels span 1980–2025; absent early battery data remain absent. "
         "The installed-system 2010 value is a retrospective model estimate, "
         "2011–2023 values are model/interpolation, and 2024–2025 values are "
         "published benchmarks. Sourcebook date: " + data["sourcebook_date"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    configure_fonts()
    electricity_cost_history(data, args.output_dir)
    solar_storage_capex(data, args.output_dir)


if __name__ == "__main__":
    main()
