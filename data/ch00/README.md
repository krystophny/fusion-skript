# Chapter 0 data handoff

Prepared 2026-10-06. This directory contains source snapshots, source/licence
records and numerical inputs. Nothing here edits the final deck. The lecturer's
designer can take the files in `derivations/build/plotdata/` and the separate
slide JPEGs; the PNGs in `derivations/build/check/` are diagnostic views only.

`sources.json` is the provenance authority; `processed/inputs.json` attaches
units, years and source keys to each substitution. `processed/numbers.json`
is the full-precision counterpart of `../../NUMBERS.md`. Source snapshots are
hashed in `raw-manifest.json`. **Do not publish `raw/` wholesale**: it contains
research-only, copyrighted and NC candidates.

## Ready data and limitations

| Planned page | Available | Licence / evidence limitation |
|---|---|---|
| 1 Earth at night | NASA 2016 original + 2400 px JPEG | Public domain; composite, not an instantaneous photograph |
| 2 Energy–GDP | 188 matching 2024 economies; exclusions; population bubbles | EIA PD + WDI CC BY 4.0; 365-day normalization; EIA primary boundary differs from Austrian gross inland |
| 3 Daily life | Gapminder four income levels/population (2017 estimate); four CC BY stoves and incomes; electricity access 91.9265% (2024); world/Austria arable land and cropland (2023) | Income-level counts are rounded and use a 2013 survey base extended to 2017. Dollar Street income is per equivalent adult. Clean cooking is excluded under CC BY-NC 3.0 IGO; no comparable open world washer/car/fridge ownership series was verified |
| 4 Micro–macro | Handwritten components =120; GDP check=164.384; 2025 gross=112.006 and final=87.1563 kWh/person/day | Statistics Austria permits attributed reuse under custom terms, not CC. Preliminary. Car arithmetic is 15 versus rounded 20 |
| 5 Austria flow | Conserved node/link graph, actual carrier×sector matrix, TJ and daily units | Statistics Austria custom attribution terms; pools avoid fabricated causal primary→sector allocation |
| 6 Resources | Latest BGR 2024 stocks/production; native R/P; growth curves; 1000-year power; Red Book broad U alternative | BGR data are re-plotted with attribution under lecturer data policy; no CC licence asserted. Red Book CC BY 4.0. RAR reserves ≠ identified resources |
| 7 Solar chain | Horizontal 1,286.61 kWh/m²/year =146.874 W/m²; 35° plane 1,542.13; yield 1,221.69 kWh/kWp/year; module mean 27.8925 W/m² | PVGIS free reuse with attribution; satellite/model climatology 2005–2023, not ground measurement. 20% module efficiency assumed |
| 8 True scale | Sentinel-2 and Graz OGD boundary at identical 16 km scale; Weesow 1.64 km² / 187 MWp; 1 GW average =79.81 km² from 180 GWh/year operator expectation | Contains modified Copernicus Sentinel data 2025; city boundary CC BY 4.0. Operator yield is expected, not measured; no comparable documented measured site yield found |
| 9 PV history | Module price USD 132.38/Wp (1975) → 0.2652 (2024, constant 2025 USD); PV capacity 2016–2025 | OWID processing CC BY 4.0; Nemet/Farmer-Lafond CC BY; IRENA reports permit attribution © IRENA 2025/2026; pvXchange credited |
| 10 Wind | Corrected US onshore mean 0.90 W/m²; EU 23%/35% fleet CF; Austria 8.57793 TWh, year-end proxy CF; CC BY-SA photo | EU/operator facts independently calculated; offshore Horns Rev 2.765 W/m² is a scenario from 158 MW/20 km² × EU CF, not observed site yield |
| 11 Area, food and biofuels | Area scenarios at 0.5/2/10/20 W/m²; corn ethanol gross density 0.3168 W/m²; Austria final-energy equivalent 0.01146 km²/person, 105,512 km² nationally (126% of Austria) | US corn yield and ethanol factors illustrate gross fuel energy before inputs and coproduct allocation; not Austrian yield or lifecycle assessment |
| 12 Fission | 24.5791 t enriched U / 214.254 t natural U per full-power GW(e)-year; deployment scenario and historical grid peak | Gösgen CC BY 4.0 photo downloaded; IAEA 2025 table verifies 33/year grid-connection peak over 1954–2024 and 31.129 GW(e) annual peak |
| 13 Fusion | 17.6 MeV; 37.4037 kg D +56.0107 kg T; coal 1.314 Mt for same thermal GW-year; D/Li inventory per person; CC BY JET photo | Burned mass, not fuel inventory; fusion thermal vs electric distinguished. Li reserves are not all Li-6. Seawater D inventory is not an extraction reserve |
| 14 Environmental risk | U.S. annual bird estimates: cats 1.3–4.0 billion; buildings 365–988 million; vehicles 89–340 million; power lines 12–64 million; wind 140,438–327,586. European reviewed-site wind median 6.5 birds/turbine/year. OWID 2021 deaths/TWh series | Estimates have different years, scopes and methods; not summed. OWID air-pollution/accident rates combine heterogeneous sources; caveats appear in figure captions |
| 15 Lifecycle emissions | NREL/DOE min/median/max literature distributions for nine generation types; coal median 1,001, NGCC 450, PV 43.4, wind 13 and LWR nuclear 13 gCO₂-eq/kWh | Custom NREL terms permit free data use with full notice and DOE/NREL/ALLIANCE credit; no named CC. IPCC candidate excluded under its non-commercial terms. No provider figure reused |

Custom and source-specific terms are recorded by reference rather than falsely
relabelled CC. NonCommercial cooking data are excluded; no suitable open
replacement series was verified. Numerical facts and independent calculations
are distinguished from provider datasets and images; no copyrighted provider
table image or chart is included.

## Geography recipe

The downloaded files were produced without credentials. Saved STAC input and
scene metadata are under `raw/`. Repeat with:

```sh
uv run --no-project --python 3.13 --with rasterio --with pyproj \
  --with pillow --with shapely --with matplotlib \
  python scripts/prepare-ch00-geography.py
```

The script reads `sentinel_selected.json`'s `assets.visual.href`, a public AWS
COG. The selected scene is `S2A_33UVU_20250911_0_L2A`, tile 33UVU, acquired
2025-09-11. Native true-colour resolution is 10 m. The park reference point is
52.650568°N, 13.686692°E. The city boundary comes from the City of Graz OGD
ArcGIS query saved in `raw/graz_boundary.geojson`. No OSM/ODbL data were needed.

Both maps use EPSG:32633 metre coordinates and a 16,000 m square view. Graz's
outline is translated to its centroid, never rescaled. Use the
`map_extent_relative_to_park_m` metadata for the Sentinel panel and metre units
for the city panel; give them the same axis extent, aspect and physical panel
size. Do not use the separate 5 km detail as the same-scale park panel.
Projected current OGD area is 127.466 km²; published city area is 127.58 km².
This small discrepancy is retained instead of forcing a scale fit.

Originals are **native-resolution geographic windows**, GeoTIFF + JPEG, not
full-scene downloads. Credit: **Contains modified Copernicus Sentinel data
2025**. City credit: **Datenquelle: Stadt Graz – data.graz.gv.at**.

## Reproduction and verification

The existing `pyproject.toml` contains the numerical/test dependencies. Run
`uv run pytest -q`; system `python3 -m pytest -q` also works here. The chapter
module has `# %%` notebook cells like the plasma Skript and a shared SI checker.
The builder runs entirely from saved inputs; no network is needed for numerical
regeneration. Every JSON plot payload has units, source caption and licence
status. Page 9 has separate price/capacity files. Symbolic expressions and LaTeX
are in `plotdata/formulas.json`. Clean plot-data JSON and rough diagnostic PNGs
are committed; rendered SVG, PDF, site and deck files are regenerable.

The committed `iaea-history-1954-2024.json` input contains extracted table
values and their source/terms metadata, so regenerating processed files does not
need the report PDF or Poppler. The source report remains local research
evidence; only selected numerical facts and independently computed maxima enter
the deployment comparison.

The independent tests check physical dimensions, conservation at every internal
flow node, published Austrian totals, growing consumption by numerical
quadrature, monthly-to-annual PVGIS totals, rounded published fuel-cycle totals,
isotope conservation, atomic energy accounting and the operator park-energy
budget. They do not test that source text matches a patch.

The dependency repair in `derivations/tool-repairs/` records a reproducible
SymPy/python-flint overflow and a focused upstream patch. It is separate from
the chapter's formulas and source rights.
