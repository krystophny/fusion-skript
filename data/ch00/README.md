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

## Capacity additions and cost scenarios (12 October 2026)

- `raw/eia-world-capacity-1979-2024.json`: complete EIA International API
  response, world (WORL), activity 7 (capacity), MK (million kW = GW), requested
  1979–2024; annual observations begin in 1980, wind in 1981, solar and biomass
  in 2000. [EIA capacity data](https://www.eia.gov/international/data/world/electricity/electricity-capacity).
  US government numerical data, public domain. Annual first differences are
  **net installed-capacity changes**, including closures, reclassifications and
  revisions; they are not gross construction. EIA aggregates fossil fuels;
  hydro excludes pumped storage. Missing earlier observations stay missing.
  The canonical derivation emits `12-capacity-additions.json`; the existing
  deck figure builder renders it. Austria's line retains the former one-year
  accounting comparison: 2025 final energy / 0.9 capacity factor / one-year
  build = 37.1401 GW/year. This nuclear-equivalent reference is not a solar or
  wind target; electrification, storage and sector coupling are not modeled.

- `raw/atb-2025-projections.csv`: five unrounded records selected from the
  [2025 ATB v1.0.0 dataset](https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/parquet/2025/v1.0.0/ATBe.parquet),
  accessed 12 October 2026. Filter: LCOE, Moderate, R&D without tax credits,
  years 2030 and 2035 plus the 2025 wind baseline. Wind: Class 4, Wind Turbine Technology 1, 30-year cost
  recovery. Nuclear: large reactor, 60-year cost recovery. Values are in
  2023 USD/MWh. Plotting uses dimensionless ratios, so the dollar base cancels;
  each relative change multiplies the existing 2025 cost benchmark. Source
  records and the historical sourcebook are retained separately. [ATB methods and terms](https://atb.nlr.gov/electricity/2025/disclaimer);
  numerical facts are attributed, not provider artwork.
  Wind projections apply the ATB relative cost change (future / 2025) to
  the existing 3.3 cents/kWh global 2025 benchmark, joining continuously at
  2025. Nuclear uses the same anchoring method, but ATB nuclear estimates start
  in 2030. The nuclear scenario explicitly holds the 2025 benchmark constant
  through 2030, then applies the ATB 2035/2030 LCOE ratio. Both dotted curves
  join their historical 2025 anchors. These are anchored scenarios, not ATB
  absolute LCOE forecasts or a prediction of a cost drop between samples.

The [2025 ATB definitions](https://atb.nlr.gov/electricity/2025/definitions)
explicitly exclude fossil-fuel LCOE calculations. Gas and coal therefore use
a labelled **constant-2025-real-cost scenario** through 2035, not a published
fuel-price forecast. Solar and daily-storage scenarios retain the supplied
IRENA-based model. All future rows use evidence flag F; historical data,
sourcebook and daily-storage assumptions remain unchanged.

### Fusion fuel and blanket resource scenarios (12 October 2026)

`13-fusion-resources.json` reuses the saved EIA 2024 world primary-energy
record (`eia_2024.json`, WORL, product 44, activity 2, QBTU), existing Li
reserves and NOAA/NIST ocean-D inputs. Electricity is assumed to match that
primary-energy total numerically, not today's electricity demand; this is an
accounting scenario, not a useful-energy transition forecast. Constant demand,
no other uses, fuel losses or initial blanket loading deducted from the fuel budget. MacKay chapter 24, pp.172/176 supplies
the assumed natural-Li yield 2300 kWh(e)/g and seawater extraction estimate
2.5 kWh(e)/g. The 0.17 mg/L seawater concentration gives an inventory, not
economic reserves. D–T deuterium uses 17.6 MeV per D at assumed 40% conversion;
it still needs Li and bred T. No DD energy claim is made. The canonical
`fusion-resource-lifetimes.svg` is reused unchanged in the deck and reference.

Blanket lifetimes use paired historical 1 GW net-electric concepts from
[Bradshaw et al. (2011)](https://doi.org/10.1016/j.fusengdes.2010.11.040):
HCLL Pb loading 4092 t and nuclear burn-up 3.1 t/full-power-year;
HCPB Be loading 120 t and nuclear burn-up 0.19 t/full-power-year.
The same world-energy stress scenario and assumed 90% capacity factor require
22,528 installed units: startup loading is 92.2 Mt Pb or 2.70 Mt Be.
Compute (stock - startup loading) / annual nuclear burn-up, assuming ideal
recovery of untransmuted material, no growth, competing uses or recovery losses.
Burn-up scales with average output; startup scales with installed capacity.

USGS MCS 2026: Pb reserves 95 Mt, identified resources >2 Gt, mine output
4.5 Mt/year. After startup, these give about 45 years or >30,353 years
respectively; resources and reserves are alternatives, not additive.
Be identified resources are >100 kt, mine output 430 t/year; world Be reserves
are unavailable. The 100 kt reference cannot cover startup, so its lifetime is
null, not zero or negative. A lower bound is not a total-resource ceiling;
the actual Be stock cannot be inferred from that reference.
These are design-specific stress estimates, not transition forecasts.
Recycling cannot restore transmuted atoms, and replacement losses shorten
lifetimes. Both canonical figures use one shared years-scale plot renderer;
`fusion-blanket-lifetimes.svg` is reused unchanged in deck and reference.

New input records and primary-source links are in `processed/inputs.json` and
`sources.json`. MacKay is a conceptual/numerical reference only; no source
text or artwork is reused. Li et al. 2021 (doi:10.1039/D1EE00354B) demonstrates
lab enrichment from actual seawater, not a full-scale supply chain. Paine et al.
2024 provides design-specific enriched blanket-Li examples. Lab energy
estimates and historical extraction estimates are not industrial cost promises.

### Global outlook to 2100 (revised 13 October 2026)

The single GCAM4 pathway is replaced by a multi-model literature comparison.
`raw/ar6-primary-energy.jsonl` is a small World numerical subset of the
IIASA/IAMC AR6 Scenarios Database v1.1; provider database rights and attribution
terms remain applicable. It retains model/scenario identity, climate category,
literature citation, and original values in EJ/year. The full 353 MB database
and metadata workbook are not redistributed. Their URLs and SHA-256 checksums
are recorded in `raw/energy-scenarios.json`.

Selection uses `meta_Ch3vetted_withclimate` categories C1 and C3. Require total
and coal/oil/gas/biomass/nuclear/solar/wind at every decade 2020–2100, positive
totals, nonnegative components and component sums not exceeding total beyond
0.01%. Four IMAGE cases fail closure; 356 complete cases from ten model
families remain. The excluded identities are recorded. Selection never filters
by the resulting source shares. Source/own-total ratios precede unweighted
10/50/90 percentiles. These descriptive ranges are not probabilities or a
model-balanced consensus; unequal scenario representation remains a limitation.
Component medians do not form one feasible mix and are never stacked.
Fossils and wind+solar are grouped; other energy is the residual. Three
NGFS phase-2 current-policy cases have **2021** policy assumptions.
The 2024 IEA observations retain physical heat-content accounting and are
not spliced to direct-equivalent IPCC curves.

The same input file holds four MIT EPPA **actual five-year fusion output
curves** from the 2024 report Fig.4.4b (printed p.43, PDF p.48).
Vector coordinates are calibrated to its axes and rounded to 100 TWh;
early tiny values are unresolved. Exact text base-case values 2 TWh in 2035
and 375 TWh in 2050 replace those two vertices. Costs are 2800, 5600, 8000
and 11300 USD2021/kW in 2050; availability in 2035 is assumed.
EUROfusion/CIEMAT ESSRI 2024 S02 supplies independently digitized dated bars
at 2030/2050/2070/2100, about 0/0.5/7.5/29 PWh/year at 0.5 PWh resolution.
The source explicitly calls its fusion costs desired targets rather than
estimates. Connections join the reported dates without inventing intervening
model output. The newer Mantilla et al.2026 favourable 21% of 140 PWh
endpoint remains a separate star, not an invented 2026 trajectory.

All fusion outputs are converted to EJ and divided by the **same
year-specific AR6 median primary total**. This explicitly accepted
cross-model scaling is not an integrated model run, a published primary
share or an assumption about displaced technologies. Approximately 882 EJ
in 2100 gives about 3–18% for MIT cost cases, 10% for its base case and
12% for the favourable EUROfusion cases.

The discarded GCAM example is retained only as explanatory numerical
evidence: 391.7 EJ biomass, 230.3 EJ with CCS, 1084.8 million hectares energy
crops, 23.5 Gt CO2/year biomass CCS and 1853 USD2005/t CO2 carbon price in
2100. This explains the 42% result without presenting it as consensus.
Three IPCC illustrative pathways contrast renewable-led, low-demand and
high-overshoot/removal strategies; the last is C2 and outside the plotted
ensemble. The reference discusses land efficiency, conversion losses,
negative-emissions credits and sustainability constraints.

Recent PV observations and the short 2025–2035 construction-rate guide are
retained: IRENA net additions 510.349 GW/year, assumed 15% capacity factor,
full-year production and no retirement. The denominator now follows AR6
median demand, anchored to IEA's 655 EJ in 2025. It is illustrative, not an
integrated model update or a century-long exponential extrapolation.
The existing chapter builder and teaching plotter produce the one canonical
`16-energy-scenarios.json` and `energy-outlook.svg` for reference and deck.
