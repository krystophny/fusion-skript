# Chapter 0 numerical ledger

Accessed 2026-10-06. Full precision is retained in JSON; displayed figures below are rounded to six significant digits. All years are 365-day engineering years. Source keys resolve in [data/ch00/sources.json](data/ch00/sources.json) and [data/README.md](data/README.md). Per-series reuse terms and attribution requirements are authoritative in each plot-data file and data/README.md. Noncommercial sources are excluded.

Every country observation is in `derivations/build/plotdata/02-energy-gdp.json`; the table below selects likely labelled examples. Complete final carrier–sector values are in `05-austria-flow.json`; growth curves are in `06-resource-lifetimes.json`.

## 1. Earth at night

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| Black Marble composite | 2016 | year | 2016 | nasa |

## 2. Energy and GDP

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| Countries/economies plotted | 188 | count | 2024 | eia + wb_gdp_ppp + wb_population |
| Austria energy | 93.3823 | kWh/(person day) | 2024 | eia + wb_population |
| Austria GDP PPP | 63788 | 2021 international dollar/(person year) | 2024 | wb_gdp_ppp |
| Austria population | 9.17798e+06 | person | 2024 | wb_population |
| Switzerland energy | 79.5616 | kWh/(person day) | 2024 | eia + wb_population |
| Switzerland GDP PPP | 85448.1 | 2021 international dollar/(person year) | 2024 | wb_gdp_ppp |
| Switzerland population | 9.00558e+06 | person | 2024 | wb_population |
| China energy | 97.2082 | kWh/(person day) | 2024 | eia + wb_population |
| China GDP PPP | 23841.5 | 2021 international dollar/(person year) | 2024 | wb_gdp_ppp |
| China population | 1.40898e+09 | person | 2024 | wb_population |
| Germany energy | 95.4183 | kWh/(person day) | 2024 | eia + wb_population |
| Germany GDP PPP | 62654.6 | 2021 international dollar/(person year) | 2024 | wb_gdp_ppp |
| Germany population | 8.35166e+07 | person | 2024 | wb_population |
| India energy | 20.7468 | kWh/(person day) | 2024 | eia + wb_population |
| India GDP PPP | 9416.05 | 2021 international dollar/(person year) | 2024 | wb_gdp_ppp |
| India population | 1.45094e+09 | person | 2024 | wb_population |
| United States energy | 223.298 | kWh/(person day) | 2024 | eia + wb_population |
| United States GDP PPP | 75698.2 | 2021 international dollar/(person year) | 2024 | wb_gdp_ppp |
| United States population | 3.40004e+08 | person | 2024 | wb_population |

All 188 EIA countries/economies with positive matching 2024 WDI GDP PPP and population. 41 EIA country records excluded with reasons in processed/energy-gdp-exclusions.json. EIA primary-energy accounting differs from Austria gross inland consumption; 365-day normalization even for leap years.

## 3. Access and Dollar Street

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| electricity access | 91.9265 | % of world population | 2024 | wb_electricity |
| Income band <3 | <3 | 2021 PPP USD/(person day) | 1981 | wb_pip_income |
| Band 1 population | 2.12855 | billion people | 1981 | wb_pip_income |
| Income band 3–12 | 3–12 | 2021 PPP USD/(person day) | 1981 | wb_pip_income |
| Band 2 population | 1.25944 | billion people | 1981 | wb_pip_income |
| Income band 12–48 | 12–48 | 2021 PPP USD/(person day) | 1981 | wb_pip_income |
| Band 3 population | 0.873013 | billion people | 1981 | wb_pip_income |
| Income band ≥48 | ≥48 | 2021 PPP USD/(person day) | 1981 | wb_pip_income |
| Band 4 population | 0.257388 | billion people | 1981 | wb_pip_income |
| Income band <3 | <3 | 2021 PPP USD/(person day) | 2000 | wb_pip_income |
| Band 1 population | 2.2309 | billion people | 2000 | wb_pip_income |
| Income band 3–12 | 3–12 | 2021 PPP USD/(person day) | 2000 | wb_pip_income |
| Band 2 population | 2.50359 | billion people | 2000 | wb_pip_income |
| Income band 12–48 | 12–48 | 2021 PPP USD/(person day) | 2000 | wb_pip_income |
| Band 3 population | 0.944718 | billion people | 2000 | wb_pip_income |
| Income band ≥48 | ≥48 | 2021 PPP USD/(person day) | 2000 | wb_pip_income |
| Band 4 population | 0.482674 | billion people | 2000 | wb_pip_income |
| Income band <3 | <3 | 2021 PPP USD/(person day) | 2024 | wb_pip_income |
| Band 1 population | 0.824298 | billion people | 2024 | wb_pip_income |
| Income band 3–12 | 3–12 | 2021 PPP USD/(person day) | 2024 | wb_pip_income |
| Band 2 population | 3.9599 | billion people | 2024 | wb_pip_income |
| Income band 12–48 | 12–48 | 2021 PPP USD/(person day) | 2024 | wb_pip_income |
| Band 3 population | 2.40475 | billion people | 2024 | wb_pip_income |
| Income band ≥48 | ≥48 | 2021 PPP USD/(person day) | 2024 | wb_pip_income |
| Band 4 population | 0.952856 | billion people | 2024 | wb_pip_income |
| World electricity access | 78.225 | % of world population | 2000 | wb_electricity |
| Austria / Ethiopia primary energy per person | 165.396 | 1 | 2000 | eia + wb_population |
| World electricity access | 91.9265 | % of world population | 2024 | wb_electricity |
| Austria / Ethiopia primary energy per person | 49.7071 | 1 | 2024 | eia + wb_population |
| Austria arable land | 0.14474553 | ha/person | 2023 | faostat_arable |
| Austria cropland | 0.15801372 | ha/person | 2023 | hyde_cropland |
| World arable land | 0.17167939 | ha/person | 2023 | faostat_arable |
| World cropland | 0.20268911 | ha/person | 2023 | hyde_cropland |
| Stove/hob, Spain | 7639 | PPP-adjusted USD per equivalent adult per month | 2019-10-16 | dollarstreet |
| Stove/hob, Brazil | 685 | PPP-adjusted USD per equivalent adult per month | 2018-05-02 | dollarstreet |
| Stove/hob, Bolivia | 180 | PPP-adjusted USD per equivalent adult per month | 2015-01-19 | dollarstreet |
| Stove/hob, Haiti | 39.9 | PPP-adjusted USD per equivalent adult per month | 2014-11-28 | dollarstreet |

PIP global line-up estimates, including survey interpolation/extrapolation, not simultaneous censuses. Fixed teaching bands: $3, $12, $48 in 2021 PPP; only $3 is an official poverty line. Not converted Gapminder levels. Primary energy: EIA annual product 44, activity 2, QBTU, WDI population; 365-day normalization. EIA does not fully cover traditional biomass.

Dollar Street PPP monthly amounts are per equivalent adult, not whole-household totals. Global washing-machine, car and refrigerator ownership shares are not included because a comparable sourced series was not verified. Clean-cooking figures are excluded: the WDI indicator source note specifies CC BY-NC 3.0 IGO.

Arable land is FAO/WDI cropland under temporary crops, temporary meadows, kitchen gardens and temporary fallow; cropland includes arable plus permanent crops under HYDE. The series differ in definition and source method; do not add them.

Band 1 population: Difference of PIP cumulative population counts.

Band 2 population: Difference of PIP cumulative population counts.

Band 3 population: Difference of PIP cumulative population counts.

Band 4 population: Difference of PIP cumulative population counts.

Austria / Ethiopia primary energy per person: EIA coverage does not fully include traditional biomass.

Stove/hob, Spain: Omar Havana; Family 391

Stove/hob, Brazil: Leony Carvalho; Family 266

Stove/hob, Bolivia: Zoriah Miller; Family 148

Stove/hob, Haiti: Zoriah Miller; Family 7

## 4. Micro → macro

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| Home electricity | 5 | kWh/(person day) | 2025 | legacy_handwriting |
| Heating / hot water | 20 | kWh/(person day) | 2025 | legacy_handwriting |
| Car | 20 | kWh/(person day) | 2025 | legacy_handwriting |
| Bus / train / plane | 10 | kWh/(person day) | 2025 | legacy_handwriting |
| Things | 20 | kWh/(person day) | 2025 | legacy_handwriting |
| Work / industry | 45 | kWh/(person day) | 2025 | legacy_handwriting |
| legacy_total | 120 | kWh/(person day) | 2025 | legacy_handwriting |
| legacy_GDP_EUR_person_year | 60000 | EUR/(person year) | 2025 | legacy_handwriting |
| legacy_intensity_kWh_EUR | 1 | kWh/EUR | 2025 | legacy_handwriting |
| legacy_GDP_crosscheck_kWh_person_day | 164.384 | kWh/(person day) | 2025 | legacy_handwriting |
| legacy_car_arithmetic_kWh_person_day | 15 | kWh/(person day) | 2025 | legacy_handwriting |
| gross_kWh_person_day | 112.006 | kWh/(person day) | 2025 | stat_balance + stat_population |
| final_kWh_person_day | 87.1563 | kWh/(person day) | 2025 | stat_balance + stat_population |
| gross_W_person | 4666.92 | W/person | 2025 | stat_balance + stat_population |
| final_W_person | 3631.51 | W/person | 2025 | stat_balance + stat_population |
| gross_GW_average | 42.9565 | GW | 2025 | stat_balance |
| final_GW_average | 33.4261 | GW | 2025 | stat_balance |
| population | 9.20446e+06 | person | 2025 | stat_population |
| GDP_EUR_person_year | 55691.1 | EUR/(person year) | 2025 | wb_gdp_austria |
| derived_gross_intensity_kWh_EUR | 0.734088 | kWh/EUR | 2025 | stat_balance + stat_population + wb_gdp_austria |

GDP × intensity from the same energy balance is an accounting identity, not an independent validation. Handwritten 120 is a bottom-up estimate; car example arithmetic gives 15, while its budget line rounds to 20. Different accounting boundaries prevent interpreting differences as estimation error alone.

## 5. Austria balance flow

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| gross_TJ | 1.35468e+06 | TJ | 2025 | stat_balance |
| final_TJ | 1.05413e+06 | TJ | 2025 | stat_balance |
| conversion_loss | 6.42752 | kWh/(person day) | 2025 | stat_balance + stat_population |
| own_use_and_transport_losses | 12.0163 | kWh/(person day) | 2025 | stat_balance + stat_population |
| nonenergy | 6.40598 | kWh/(person day) | 2025 | stat_balance + stat_population |
| sectors: Industry | 23.4829 | kWh/(person day) | 2025 | stat_balance + stat_population |
| sectors: Transport | 27.7608 | kWh/(person day) | 2025 | stat_balance + stat_population |
| sectors: Services | 8.23145 | kWh/(person day) | 2025 | stat_balance + stat_population |
| sectors: Households | 25.6092 | kWh/(person day) | 2025 | stat_balance + stat_population |
| sectors: Agriculture | 2.07189 | kWh/(person day) | 2025 | stat_balance + stat_population |
| carriers: Coal | 1.03543 | kWh/(person day) | 2025 | stat_balance + stat_population |
| carriers: Oil products | 28.9093 | kWh/(person day) | 2025 | stat_balance + stat_population |
| carriers: Gas | 13.2984 | kWh/(person day) | 2025 | stat_balance + stat_population |
| carriers: Renewable fuels / direct heat | 17.9575 | kWh/(person day) | 2025 | stat_balance + stat_population |
| carriers: Waste | 0.85207 | kWh/(person day) | 2025 | stat_balance + stat_population |
| carriers: District heat | 6.09189 | kWh/(person day) | 2025 | stat_balance + stat_population |
| carriers: Electricity | 19.0117 | kWh/(person day) | 2025 | stat_balance + stat_population |

Aggregated balance pools: primary inputs cannot be traced causally to final sectors. Actual published final-carrier × sector cells are retained. Row 16 is an aggregate and is not added again. Conversion losses are net input minus output, not all gross minus final.

## 6. Resource lifetimes

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| hardcoal stock | 802334 | Mt | 2024 | bgr |
| hardcoal production | 8038.7 | Mt/year | 2024 | bgr |
| hardcoal static_years | 99.8089 | year | 2024 | bgr |
| hardcoal power_W_person_for_1000_years | 77.5441 | W(thermal)/person | 2024 | bgr |
| hardcoal energy reserve | 19908 | EJ | 2024 | bgr |
| hardcoal lifetime at continuous 2%/year | 54.8669 | year | 2024 | bgr + assumptions |
| lignite stock | 319500 | Mt | 2024 | bgr |
| lignite production | 1142.8 | Mt/year | 2024 | bgr |
| lignite static_years | 279.576 | year | 2024 | bgr |
| lignite power_W_person_for_1000_years | 13.9952 | W(thermal)/person | 2024 | bgr |
| lignite energy reserve | 3593 | EJ | 2024 | bgr |
| lignite lifetime at continuous 2%/year | 94.2893 | year | 2024 | bgr + assumptions |
| oil stock | 252374 | Mt | 2024 | bgr |
| oil production | 4553.5 | Mt/year | 2024 | bgr |
| oil static_years | 55.4242 | year | 2024 | bgr |
| oil power_W_person_for_1000_years | 41.0896 | W(thermal)/person | 2024 | bgr |
| oil energy reserve | 10549 | EJ | 2024 | bgr |
| oil lifetime at continuous 2%/year | 37.2985 | year | 2024 | bgr + assumptions |
| gas stock | 207714 | billion m^3 | 2024 | bgr |
| gas production | 4273.2 | billion m^3/year | 2024 | bgr |
| gas static_years | 48.6085 | year | 2024 | bgr |
| gas power_W_person_for_1000_years | 30.7442 | W(thermal)/person | 2024 | bgr |
| gas energy reserve | 7893 | EJ | 2024 | bgr |
| gas lifetime at continuous 2%/year | 33.9567 | year | 2024 | bgr + assumptions |
| uranium_lowcost stock | 1181 | kt U | 2024 | bgr |
| uranium_lowcost production | 62.4 | kt U/year | 2024 | bgr |
| uranium_lowcost static_years | 18.9263 | year | 2024 | bgr |
| uranium_lowcost power_W_person_for_1000_years | 2.29812 | W(thermal)/person | 2024 | bgr |
| uranium_lowcost energy reserve | 590 | EJ | 2024 | bgr |
| uranium_lowcost lifetime at continuous 2%/year | 16.0507 | year | 2024 | bgr + assumptions |
| coal_combined stock | 1.12183e+06 | Mt | 2024 | bgr |
| coal_combined production | 9181.5 | Mt/year | 2024 | bgr |
| coal_combined static_years | 122.184 | year | 2024 | bgr |
| coal_combined power_W_person_for_1000_years | 91.5393 | W(thermal)/person | 2024 | bgr |
| coal_combined energy reserve | 23501 | EJ | 2024 | bgr |
| coal_combined lifetime at continuous 2%/year | 61.8271 | year | 2024 | bgr + assumptions |
| uranium_identified_below_260_USD_kg stock | 7.9345e+06 | t U | resources at 2023-01-01 / production 2023 | redbook + wna_fuel |
| uranium_identified_below_260_USD_kg production | 54345 | t U/year | resources at 2023-01-01 / production 2023 | redbook + wna_fuel |
| uranium_identified_below_260_USD_kg static_years | 146.002 | year | resources at 2023-01-01 / production 2023 | redbook + wna_fuel |
| uranium_identified_below_260_USD_kg power_W_person_for_1000_years | 13.7849 | W(thermal)/person | resources at 2023-01-01 / production 2023 | redbook + wna_fuel |
| uranium_identified_below_260_USD_kg lifetime at continuous 2%/year | 68.3052 | year | resources at 2023-01-01 / production 2023 | redbook + wna_fuel + assumptions |
| 2025 handwritten coal 1000-year power | 114.155 | W/person | 2025 | legacy_handwriting |
| 2025 handwritten coal 1000-year daily energy | 2.73973 | kWh/(person day) | 2025 | legacy_handwriting |
| 2025 handwritten coal lifetime at 100 kWh/person/day | 27.3973 | year | 2025 | legacy_handwriting |
| 2025 handwritten uranium 1000-year power | 1141.55 | W/person | 2025 | legacy_handwriting |
| 2025 handwritten uranium 1000-year daily energy | 27.3973 | kWh/(person day) | 2025 | legacy_handwriting |
| 2025 handwritten uranium lifetime at 100 kWh/person/day | 273.973 | year | 2025 | legacy_handwriting |
| Input: sustainable_horizon | 1000 | year | model | assumptions |
| Input: legacy_world_population | 1e+10 | person | 2025 | legacy_handwriting |
| Input: legacy_daily_demand | 100 | kWh/(person day) | 2025 | legacy_handwriting |
| Input: world_population | 8.1409e+09 | person | 2024 | wb_population |

Static R/P and prescribed-growth exhaustion are stock models, not forecasts. Continuous g differs from a discrete annual rate r: g=ln(1+r). BGR low-cost uranium RAR and Red Book broad identified resources are not interchangeable. Old oil/gas handwriting supplies qualitative lifetimes but no legible separate 1000-year power estimates.

2025 handwritten coal 1000-year power: 10 billion people; coal 10 kWh/kg; uranium 10 million kWh/kg near-complete fission potential.

2025 handwritten uranium 1000-year power: 10 billion people; coal 10 kWh/kg; uranium 10 million kWh/kg near-complete fission potential.

Input: sustainable_horizon: Finite inventory divided over horizon; not sustainability certification.

Input: legacy_world_population: Teaching assumption, not actual 2025 population.

Input: legacy_daily_demand: World stock-lifetime teaching demand on pp.14/29.

## 7. Solar chain

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| horizontal_kWh_m2_year | 1286.61 | kWh/(m² year) | 2005–2023 | pvgis + assumptions |
| horizontal_W_m2 | 146.874 | W/m² | 2005–2023 | pvgis + assumptions |
| inclined_kWh_m2_year | 1542.13 | kWh/(m² year) | 2005–2023 | pvgis + assumptions |
| specific_yield_kWh_kWp_year | 1221.69 | kWh/(kWp year) | 2005–2023 | pvgis + assumptions |
| module_W_m2 | 27.8925 | W/m² | 2005–2023 | pvgis + assumptions |
| day_night factor | 0.31831 | 1 | model / 2005–2023 | pvgis + assumptions |
| latitude factor | 0.681095 | 1 | model / 2005–2023 | pvgis + assumptions |
| season factor | 1.00874 | 1 | model / 2005–2023 | pvgis + assumptions |
| atmosphere_weather_residual factor | 0.671596 | 1 | model / 2005–2023 | pvgis + assumptions |
| tilt_gain factor | 1.1986 | 1 | model / 2005–2023 | pvgis + assumptions |
| module_efficiency factor | 0.2 | 1 | model / 2005–2023 | pvgis + assumptions |
| performance_ratio factor | 0.792209 | 1 | model / 2005–2023 | pvgis + assumptions |
| After noon_peak | 1000 | W/m² | model / 2005–2023 | pvgis + assumptions |
| After day_night | 318.31 | W/m² | model / 2005–2023 | pvgis + assumptions |
| After latitude | 216.799 | W/m² | model / 2005–2023 | pvgis + assumptions |
| After season | 218.694 | W/m² | model / 2005–2023 | pvgis + assumptions |
| After atmosphere_weather_residual | 146.874 | W/m² | model / 2005–2023 | pvgis + assumptions |
| After tilt_gain | 176.042 | W/m² | model / 2005–2023 | pvgis + assumptions |
| After module_efficiency | 35.2084 | W/m² | model / 2005–2023 | pvgis + assumptions |
| After performance_ratio | 27.8925 | W/m² | model / 2005–2023 | pvgis + assumptions |
| l_aoi | -2.79 | % | 2005–2023 | pvgis |
| l_spec | 1.48 | % | 2005–2023 | pvgis |
| l_tg | -6.62 | % | 2005–2023 | pvgis |
| l_total | -20.78 | % | 2005–2023 | pvgis |
| Month 1 horizontal irradiation | 41.3332 | kWh/m² | 2005–2023 | pvgis |
| Month 2 horizontal irradiation | 59.9395 | kWh/m² | 2005–2023 | pvgis |
| Month 3 horizontal irradiation | 104.48 | kWh/m² | 2005–2023 | pvgis |
| Month 4 horizontal irradiation | 137.187 | kWh/m² | 2005–2023 | pvgis |
| Month 5 horizontal irradiation | 159.699 | kWh/m² | 2005–2023 | pvgis |
| Month 6 horizontal irradiation | 175.224 | kWh/m² | 2005–2023 | pvgis |
| Month 7 horizontal irradiation | 183.18 | kWh/m² | 2005–2023 | pvgis |
| Month 8 horizontal irradiation | 156.869 | kWh/m² | 2005–2023 | pvgis |
| Month 9 horizontal irradiation | 114.53 | kWh/m² | 2005–2023 | pvgis |
| Month 10 horizontal irradiation | 78.5216 | kWh/m² | 2005–2023 | pvgis |
| Month 11 horizontal irradiation | 41.9642 | kWh/m² | 2005–2023 | pvgis |
| Month 12 horizontal irradiation | 33.6863 | kWh/m² | 2005–2023 | pvgis |
| Input: solar_noon | 1000 | W/m^2 | model | assumptions |
| Input: pv_efficiency | 0.2 | 1 | model | assumptions |
| Input: graz_latitude | 47.0707 | degree | 2005–2023 | pvgis |
| Input: obliquity | 23.44 | degree | model | assumptions |

Satellite-derived climatology and PVGIS model, not a ground-station measurement. Weather residual is calibrated and includes atmosphere/horizon, not an independently measured weather factor. Geometry toy model uses 12 equal-duration midpoint samples. No factor is applied twice.

l_aoi: Signed PVGIS model percentage; do not apply these again to the exported performance ratio.

l_spec: Signed PVGIS model percentage; do not apply these again to the exported performance ratio.

l_tg: Signed PVGIS model percentage; do not apply these again to the exported performance ratio.

l_total: Signed PVGIS model percentage; do not apply these again to the exported performance ratio.

Input: solar_noon: STC reference irradiance; not a measured Graz noon average.

Input: pv_efficiency: Assumed module efficiency at STC.

Input: obliquity: Simple declination model, ignoring Earth-orbit eccentricity.

## 8. Park and Graz at equal scale

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| park_area_km2 | 1.64 | km² | 2021 | enbw_weesow |
| peak_MWp | 187 | MWp | 2021 | enbw_weesow |
| expected_GWh_year | 180 | GWh/year | 2021 | enbw_weesow |
| ground_W_m2 | 12.5292 | W/m² | 2021 | enbw_weesow |
| capacity_factor_expected | 0.109882 | 1 | 2021 | enbw_weesow |
| area_for_1_GW_average_km2 | 79.8133 | km² | 2021 | enbw_weesow |
| peak_GWp_for_1_GW_average | 9.10067 | GWp | 2021 | enbw_weesow |
| park_equivalents_for_1_GW_average | 48.6667 | 1 | 2021 | enbw_weesow |
| fraction_of_Graz_geometry_for_1_GW_average | 0.626152 | 1 | 2021 | enbw_weesow |
| Graz OGD projected boundary area | 127.466 | km² | 2026 | graz_boundary |
| Graz published area | 127.58 | km² | 2026 | graz_boundary |
| True-colour native pixel | 10 | m | 2025-09-11 | sentinel |
| Each same-scale panel width/height | 16 | km | 2025-09-11 | sentinel |
| Park latitude | 52.6506 | degree | 2026 | wikidata |
| Park longitude | 13.6867 | degree | 2026 | wikidata |

Operator forecast, not a measured park yield. Native 10 m true colour; two 16 km × 16 km panels at identical projected metre scale. Published city area 127.58 km² differs slightly from current projected OGD geometry. Separate 5 km detail must not replace the 16 km panel in the same-scale comparison.

park_area_km2: Design expectation; not observed yield.

peak_MWp: Design expectation; not observed yield.

expected_GWh_year: Design expectation; not observed yield.

ground_W_m2: Design expectation; not observed yield.

capacity_factor_expected: Design expectation; not observed yield.

area_for_1_GW_average_km2: Design expectation; not observed yield.

peak_GWp_for_1_GW_average: Design expectation; not observed yield.

park_equivalents_for_1_GW_average: Design expectation; not observed yield.

fraction_of_Graz_geometry_for_1_GW_average: Design expectation; not observed yield.

## 9. PV prices and capacity

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| PV module price | 132.376 | constant 2025 USD/Wp | 1975 | owid_prices |
| PV module price | 99.5976 | constant 2025 USD/Wp | 1976 | owid_prices |
| PV module price | 72.6611 | constant 2025 USD/Wp | 1977 | owid_prices |
| PV module price | 51.4082 | constant 2025 USD/Wp | 1978 | owid_prices |
| PV module price | 43.1951 | constant 2025 USD/Wp | 1979 | owid_prices |
| PV module price | 36.605 | constant 2025 USD/Wp | 1980 | owid_prices |
| PV module price | 29.2664 | constant 2025 USD/Wp | 1981 | owid_prices |
| PV module price | 26.2952 | constant 2025 USD/Wp | 1982 | owid_prices |
| PV module price | 21.2281 | constant 2025 USD/Wp | 1983 | owid_prices |
| PV module price | 19.725 | constant 2025 USD/Wp | 1984 | owid_prices |
| PV module price | 17.2204 | constant 2025 USD/Wp | 1985 | owid_prices |
| PV module price | 14.2447 | constant 2025 USD/Wp | 1986 | owid_prices |
| PV module price | 12.1104 | constant 2025 USD/Wp | 1987 | owid_prices |
| PV module price | 11.3116 | constant 2025 USD/Wp | 1988 | owid_prices |
| PV module price | 11.6901 | constant 2025 USD/Wp | 1989 | owid_prices |
| PV module price | 12.0911 | constant 2025 USD/Wp | 1990 | owid_prices |
| PV module price | 11.2008 | constant 2025 USD/Wp | 1991 | owid_prices |
| PV module price | 10.4351 | constant 2025 USD/Wp | 1992 | owid_prices |
| PV module price | 9.75867 | constant 2025 USD/Wp | 1993 | owid_prices |
| PV module price | 9.23153 | constant 2025 USD/Wp | 1994 | owid_prices |
| PV module price | 8.53553 | constant 2025 USD/Wp | 1995 | owid_prices |
| PV module price | 7.97983 | constant 2025 USD/Wp | 1996 | owid_prices |
| PV module price | 7.95201 | constant 2025 USD/Wp | 1997 | owid_prices |
| PV module price | 7.16556 | constant 2025 USD/Wp | 1998 | owid_prices |
| PV module price | 6.61926 | constant 2025 USD/Wp | 1999 | owid_prices |
| PV module price | 6.49589 | constant 2025 USD/Wp | 2000 | owid_prices |
| PV module price | 6.28445 | constant 2025 USD/Wp | 2001 | owid_prices |
| PV module price | 5.74725 | constant 2025 USD/Wp | 2002 | owid_prices |
| PV module price | 5.46381 | constant 2025 USD/Wp | 2003 | owid_prices |
| PV module price | 4.6955 | constant 2025 USD/Wp | 2004 | owid_prices |
| PV module price | 4.74567 | constant 2025 USD/Wp | 2005 | owid_prices |
| PV module price | 5.17275 | constant 2025 USD/Wp | 2006 | owid_prices |
| PV module price | 5.21106 | constant 2025 USD/Wp | 2007 | owid_prices |
| PV module price | 4.7492 | constant 2025 USD/Wp | 2008 | owid_prices |
| PV module price | 3.17429 | constant 2025 USD/Wp | 2009 | owid_prices |
| PV module price | 2.51181 | constant 2025 USD/Wp | 2010 | owid_prices |
| PV module price | 2.06089 | constant 2025 USD/Wp | 2011 | owid_prices |
| PV module price | 1.11072 | constant 2025 USD/Wp | 2012 | owid_prices |
| PV module price | 0.856605 | constant 2025 USD/Wp | 2013 | owid_prices |
| PV module price | 0.790531 | constant 2025 USD/Wp | 2014 | owid_prices |
| PV module price | 0.735729 | constant 2025 USD/Wp | 2015 | owid_prices |
| PV module price | 0.680251 | constant 2025 USD/Wp | 2016 | owid_prices |
| PV module price | 0.571353 | constant 2025 USD/Wp | 2017 | owid_prices |
| PV module price | 0.509051 | constant 2025 USD/Wp | 2018 | owid_prices |
| PV module price | 0.466948 | constant 2025 USD/Wp | 2019 | owid_prices |
| PV module price | 0.369742 | constant 2025 USD/Wp | 2020 | owid_prices |
| PV module price | 0.331923 | constant 2025 USD/Wp | 2021 | owid_prices |
| PV module price | 0.365802 | constant 2025 USD/Wp | 2022 | owid_prices |
| PV module price | 0.321767 | constant 2025 USD/Wp | 2023 | owid_prices |
| PV module price | 0.265186 | constant 2025 USD/Wp | 2024 | owid_prices |
| World installed PV | 293159 | MW, year-end | 2016 | irena_capacity |
| Austria installed PV | 1103 | MW, year-end | 2016 | irena_capacity |
| World installed PV | 386711 | MW, year-end | 2017 | irena_capacity |
| Austria installed PV | 1276 | MW, year-end | 2017 | irena_capacity |
| World installed PV | 481485 | MW, year-end | 2018 | irena_capacity |
| Austria installed PV | 1462 | MW, year-end | 2018 | irena_capacity |
| World installed PV | 583393 | MW, year-end | 2019 | irena_capacity |
| Austria installed PV | 1710 | MW, year-end | 2019 | irena_capacity |
| World installed PV | 714728 | MW, year-end | 2020 | irena_capacity |
| Austria installed PV | 2051 | MW, year-end | 2020 | irena_capacity |
| World installed PV | 859674 | MW, year-end | 2021 | irena_capacity |
| Austria installed PV | 2791 | MW, year-end | 2021 | irena_capacity |
| World installed PV | 1.05147e+06 | MW, year-end | 2022 | irena_capacity |
| Austria installed PV | 3800 | MW, year-end | 2022 | irena_capacity |
| World installed PV | 1.41516e+06 | MW, year-end | 2023 | irena_capacity |
| Austria installed PV | 6394 | MW, year-end | 2023 | irena_capacity |
| World installed PV | 1.87281e+06 | MW, year-end | 2024 | irena_capacity |
| Austria installed PV | 8904 | MW, year-end | 2024 | irena_capacity |
| World installed PV | 2.38316e+06 | MW, year-end | 2025 | irena_capacity |
| Austria installed PV | 10304 | MW, year-end | 2025 | irena_capacity |

Module prices, not installed-system cost. OWID splice is global before 2010 / European module benchmark thereafter. The IRENA report permits free reuse with attribution; attribute the pvXchange market benchmark as the underlying source.

Explicit Solar photovoltaic table, not OWID total-solar slug which also includes CSP. IRENA Renewable capacity statistics March 2026 pp. 38–42.

PV module price: IRENA segment: © IRENA 2025; pvXchange benchmark attribution retained.

World installed PV: Provider-reported installed capacity; AC/DC conventions vary. © IRENA 2026.

Austria installed PV: Provider-reported installed capacity. © IRENA 2026.

## 10. Wind

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| eu_onshore_cf | 0.23 | 1 | 2024 | windeurope |
| eu_offshore_cf | 0.35 | 1 | 2024 | windeurope |
| austria_actual_generation_TWh | 8.57793 | TWh/year | 2025 | stat_balance |
| austria_yearend_MW | 4221 | MW | 2025 | igwind |
| austria_cf_endyear_proxy | 0.231987 | 1 | 2025 | stat_balance + igwind |
| us_onshore_W_m2 | 0.9 | W/m² | 2016 | miller_corrigendum |
| us_solar_W_m2 | 5.7 | W/m² | 2016 | miller_corrigendum |
| offshore_HornsRev_W_m2_scenario | 2.765 | W/m² | scenario | vattenfall_hornsrev + windeurope |
| eu_new_onshore_cf_range | [0.3, 0.35] | 1 | 2024 | windeurope |
| eu_new_offshore_cf_range | [0.42, 0.55] | 1 | 2024 | windeurope |
| Input: hornsrev_area | 20 | km^2 | 2026-10-06 | vattenfall_hornsrev |
| Input: hornsrev_peak | 158 | MW | 2026-10-06 | vattenfall_hornsrev |
| Input: austria_wind_capacity | 4221 | MW | 2025 | igwind |

Horns Rev area × current 158 MW operator capacity × EU fleet CF = scenario, not a measured site-specific mean. Austria year-end denominator is a CF proxy, not time-weighted capacity. Corrected US densities are capacity-weighted samples and use different land boundaries from the area-budget assumptions.

eu_new_onshore_cf_range: New-farm estimate.

eu_new_offshore_cf_range: New-farm estimate.

Input: hornsrev_peak: Current operator factbox; original design was 160 MW.

Input: austria_wind_capacity: Year-end installed capacity; CF computed with this is only a proxy.

## 11. Area budget

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| Austria area | 83884 | km² | 2024 | bml_area |
| Austria area per person | 0.00911341 | km²/person | 2025 | bml_area + stat_population |
| final biofuel density_W_m2 | 0.5 | W/m² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final biofuel area_km2_person | 0.00726302 | km²/person | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final biofuel national_area_km2 | 66852.2 | km² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final biofuel fraction_of_Austria | 0.79696 | 1 | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final wind density_W_m2 | 2 | W/m² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final wind area_km2_person | 0.00181576 | km²/person | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final wind national_area_km2 | 16713 | km² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final wind fraction_of_Austria | 0.19924 | 1 | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final solar_low density_W_m2 | 10 | W/m² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final solar_low area_km2_person | 0.000363151 | km²/person | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final solar_low national_area_km2 | 3342.61 | km² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final solar_low fraction_of_Austria | 0.039848 | 1 | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final solar_high density_W_m2 | 20 | W/m² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final solar_high area_km2_person | 0.000181576 | km²/person | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final solar_high national_area_km2 | 1671.3 | km² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| final solar_high fraction_of_Austria | 0.019924 | 1 | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland biofuel density_W_m2 | 0.5 | W/m² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland biofuel area_km2_person | 0.00933384 | km²/person | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland biofuel national_area_km2 | 85912.9 | km² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland biofuel fraction_of_Austria | 1.02419 | 1 | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland wind density_W_m2 | 2 | W/m² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland wind area_km2_person | 0.00233346 | km²/person | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland wind national_area_km2 | 21478.2 | km² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland wind fraction_of_Austria | 0.256047 | 1 | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland solar_low density_W_m2 | 10 | W/m² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland solar_low area_km2_person | 0.000466692 | km²/person | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland solar_low national_area_km2 | 4295.65 | km² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland solar_low fraction_of_Austria | 0.0512094 | 1 | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland solar_high density_W_m2 | 20 | W/m² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland solar_high area_km2_person | 0.000233346 | km²/person | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland solar_high national_area_km2 | 2147.82 | km² | 2025 | assumptions + stat_balance + stat_population + bml_area |
| gross_inland solar_high fraction_of_Austria | 0.0256047 | 1 | 2025 | assumptions + stat_balance + stat_population + bml_area |
| Corn ethanol gross power density | 0.3168 | W/m² | 2024 | usda_corn + doe_ethanol + stat_balance + stat_population |
| Corn ethanol area per person | 0.0114631 | km²/person | 2024 | usda_corn + doe_ethanol + stat_balance + stat_population |
| Corn ethanol national area | 105512 | km² | 2024 | usda_corn + doe_ethanol + stat_balance + stat_population |
| Corn ethanol fraction of Austria | 1.25783 | 1 | 2024 | usda_corn + doe_ethanol + stat_balance + stat_population |
| Wind 2 W/m² divided by corn ethanol | 6.31314 | 1 | 2024 | usda_corn + doe_ethanol + stat_balance + stat_population |
| Solar 10 W/m² divided by corn ethanol | 31.5657 | 1 | 2024 | usda_corn + doe_ethanol + stat_balance + stat_population |
| Solar 20 W/m² divided by corn ethanol | 63.1314 | 1 | 2024 | usda_corn + doe_ethanol + stat_balance + stat_population |
| Input: corn_yield | 179.3 | bushel/(acre year) | 2024 | usda_corn |
| Input: ethanol_yield | 2.8 | gal/bushel | 2024 | doe_ethanol |
| Input: ethanol_lhv | 76330 | Btu/gal | definition | doe_ethanol |
| Input: btu_IT | 1055.05585262 | J | definition | nist_units |

Prescribed delivered densities, not predictions. The corn-to-ethanol chain is a separate gross fuel-energy estimate and should not be mistaken for the 0.5 W/m² area-budget scenario. Food competition depends on the crop, land quality, coproduct allocation and counterfactual; dedicated energy crops can displace food production or ecosystems.

Input: corn_yield: US corn average yield; illustrative crop-to-ethanol chain, not an Austrian field measurement.

Input: ethanol_yield: Dry-mill output; coproduct allocation is not included.

Input: ethanol_lhv: Pure ethanol lower heating value; gross fuel energy before process inputs.

Input: btu_IT: Energy corresponding to one International Table Btu.

## 12. Fission

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| enriched_t_U | 24.5791 | t U/(GW(e) full-power year) | model | wna_fuel |
| natural_t_U | 214.254 | t U/(GW(e) full-power year) | model | wna_fuel |
| tails_t_U | 189.675 | t U/(GW(e) full-power year) | model | wna_fuel |
| Natural uranium thermal energy per kg in once-through model | 4.4603e+11 | J/kg U | model | wna_fuel |
| reactors_1GWe_at_90percent_CF Austria | 37.1401 | reactor | 2025 / scenario | stat_balance + stat_population + wb_population + assumptions |
| reactors_1GWe_at_90percent_CF world_at_Austrian_final_demand | 33149.3 | reactor | 2025 / scenario | stat_balance + stat_population + wb_population + assumptions |
| reactors_per_year_over_30_years Austria | 1.238 | reactor/year | 2025 / scenario | stat_balance + stat_population + wb_population + assumptions |
| reactors_per_year_over_30_years world_at_Austrian_final_demand | 1104.98 | reactor/year | 2025 / scenario | stat_balance + stat_population + wb_population + assumptions |
| Maximum first grid connections in IAEA 1954–2024 table | 33 | reactor/year | 1984 / 1985 | iaea_history |
| Maximum construction starts in that table | 43 | reactor/year | 1976 | iaea_history |
| Maximum annually grid-connected net capacity | 31.129 | GW(e)/year | 1985 | iaea_history |
| First grid connections 2024 | 6 | reactor/year | 2024 | iaea_history |
| Grid-connected net capacity 2024 | 6.803 | GW(e)/year | 2024 | iaea_history |
| Gösgen net electric capacity | 1010 | MW(e) | 2026 | kkg |
| World population for deployment scenario | 8.21542e+09 | person | 2025 | wb_population |
| Input: nuclear_efficiency | 0.33 | 1 | model | wna_fuel |
| Input: nuclear_burnup | 45 | GW day/t | model | wna_fuel |
| Input: enrichment_product | 0.045 | 1 | model | wna_fuel |
| Input: enrichment_feed | 0.00711 | 1 | model | wna_fuel |
| Input: enrichment_tails | 0.0022 | 1 | model | wna_fuel |
| Input: nuclear_capacity_factor | 0.9 | 1 | model | assumptions |
| Input: deployment_horizon | 30 | year | model | assumptions |

Fuel is uranium heavy metal, not UO2 or initial core loading; full-power 1 GW(e) × 365 days. Deployment uses 2025 world population and compares a stated world-at-Austrian-final-energy scenario with first grid connections, not construction starts. Historical reactors vary in size; the scenario units are 1 GW(e). This accounting substitution is not a transition plan. IAEA 2025 historical peak verified over 1954–2024; capacities revised since the 2014 edition.

World annual change in installed nameplate capacity, not gross commissioning. Fossil fuels are aggregated by EIA; hydro excludes pumped storage. Austria benchmark: build in one year enough 90%-capacity-factor generation to match 2025 final energy numerically. It is a nuclear-equivalent accounting comparison, not a wind/solar capacity target or a sector-coupling plan.

Input: nuclear_capacity_factor: Assumed 90% fleet capacity factor; also used in the fusion blanket resource scenario, not a measured fusion operating value.

## 13. Fusion

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| Q_MeV | 17.6 | MeV/reaction | physical constants / model; inventories 2024–2025 | iaea_fusion |
| Q_J | 2.81983e-12 | J/reaction | physical constants / model; inventories 2024–2025 | iaea_fusion + nist_constants |
| thermal_energy_GWh | 8760 | GWh/(GW(fusion) year) | physical constants / model; inventories 2024–2025 | assumptions |
| reactions_per_GW_fusion_year | 1.11836e+28 | reaction | physical constants / model; inventories 2024–2025 | iaea_fusion + nist_constants |
| fuel_thermal_energy_TJ_kg | 337.593 | TJ/kg D+T | physical constants / model; inventories 2024–2025 | iaea_fusion + nist_isotopes + nist_constants |
| deuterium_kg | 37.4037 | kg/(GW(fusion) year) | physical constants / model; inventories 2024–2025 | iaea_fusion + nist_constants + nist_isotopes |
| tritium_kg | 56.0107 | kg/(GW(fusion) year) | physical constants / model; inventories 2024–2025 | iaea_fusion + nist_constants + nist_isotopes |
| fuel_kg | 93.4144 | kg/(GW(fusion) year) | physical constants / model; inventories 2024–2025 | iaea_fusion + nist_constants + nist_isotopes |
| coal_kg | 1.314e+09 | kg/(GW(thermal) year) | physical constants / model; inventories 2024–2025 | assumptions |
| deuterium_g_m3 | 34.4437 | g/m³ | physical constants / model; inventories 2024–2025 | nist_vsmow + nist_isotopes + assumptions |
| ocean_deuterium_kg | 4.59823e+16 | kg D | physical constants / model; inventories 2024–2025 | noaa_ocean + nist_vsmow + assumptions |
| ocean_deuterium_kg_per_person | 5.59707e+06 | kg D/person | physical constants / model; inventories 2024–2025 | noaa_ocean + nist_vsmow + assumptions + wb_population |
| lithium_kg_per_person | 4.50372 | kg Li/person | physical constants / model; inventories 2024–2025 | usgs_lithium + wb_population |
| Input: world_population_2025 | 8.21542e+09 | person | 2025 | wb_population |
| Input: elementary_charge | 1.602176634e-19 | C | 2019 | nist_constants |
| Input: atomic_mass | 1.66053906892e-27 | kg | 2022 | nist_constants |
| Input: deuterium_atomic_mass | 2.01410177812 | u | NIST isotopes | nist_isotopes |
| Input: tritium_atomic_mass | 3.0160492779 | u | NIST isotopes | nist_isotopes |
| Input: coal_heat | 24 | MJ/kg | model | assumptions |
| Input: ocean_volume | 1.335e+09 | km^3 | 2026-10-06 | noaa_ocean |
| Input: seawater_density | 1025 | kg/m^3 | model | assumptions |
| Input: seawater_water_fraction | 0.965 | 1 | model | assumptions |
| Input: water_molecular_mass | 18.01528 | u | model | nist_isotopes |
| Input: deuterium_hydrogen_ratio | 155.76e-6 | 1 | VSMOW standard | nist_vsmow |
| Input: lithium_reserves | 3.7e+07 | t Li | 2025 | usgs_lithium |
| Input: lithium_production | 290000 | t Li/year | 2025 | usgs_lithium |
| Input: seconds_per_year | 3.1536e+07 | s/year | model | assumptions |

GW(fusion) is thermal reaction power, not net electric output. Burned D+T only, excluding inventory, recycling losses and breeding overhead. Coal lower heating value assumed 24 MJ/kg. Seawater D is an inventory, not a recoverable reserve. Lithium reserves are elemental Li, not all Li-6; tritium must be bred, not extracted as a natural fuel reserve. Per-person normalization uses latest WDI 2025 population with 2025 lithium reserves.

Constant 2024 demand matched as electricity; no growth, competing uses or fuel losses; initial blanket stocks are not deducted from the fuel budget. EIA traditional biomass coverage is incomplete. Ocean inventories are not economic reserves. The D-T deuterium bound needs lithium and bred tritium; the fuels are not additive alternatives. Blanket budget uses paired historical 1 GW(e) HCLL/HCPB models at assumed 90% capacity factor. Subtract initial fleet inventories, then divide remaining stock by annual nuclear burn-up. Assume ideal recovery of untransmuted material: no processing/replacement losses, other users or demand growth. Beryllium 100 kt is a reference below the USGS reported >100 kt resources, not available reserves or a ceiling. Insufficient reference stocks have no operating lifetime; this is not evidence that total world Be is only 100 kt.

Input: elementary_charge: Exact SI eV conversion.

Input: atomic_mass: Mass corresponding to one unified atomic mass unit (1 u).

Input: coal_heat: Illustrative coal lower heating value, not universal.

Input: seawater_water_fraction: 35 g/kg salinity model.

Input: deuterium_hydrogen_ratio: D/H atomic ratio; not a mass fraction.

Input: lithium_production: Excludes withheld US production.

Input: seconds_per_year: 365-day engineering year throughout; calendar 2024 is leap year.

## 14. Risk

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| Free-ranging domestic cats low | 1300000000.0 | birds/year | 2013 corrected | loss_cats |
| Free-ranging domestic cats high | 4000000000.0 | birds/year | 2013 corrected | loss_cats |
| Building collisions low | 365000000.0 | birds/year | 2014 | loss_buildings |
| Building collisions median | 599000000.0 | birds/year | 2014 | loss_buildings |
| Building collisions high | 988000000.0 | birds/year | 2014 | loss_buildings |
| Vehicle collisions low | 89000000.0 | birds/year | 2014 | loss_vehicles |
| Vehicle collisions high | 340000000.0 | birds/year | 2014 | loss_vehicles |
| Power lines, collision + electrocution low | 12000000.0 | birds/year | 2014 | loss_powerlines |
| Power lines, collision + electrocution high | 64000000.0 | birds/year | 2014 | loss_powerlines |
| Wind turbine collisions, monopole estimate low | 140438 | birds/year | 2013 | loss_wind |
| Wind turbine collisions, monopole estimate median | 234012 | birds/year | 2013 | loss_wind |
| Wind turbine collisions, monopole estimate high | 327586 | birds/year | 2013 | loss_wind |
| European wind-farm fatality rate (median) median | 6.5 | birds/turbine/year | 2012 review | naturvardsverket_birds |
| Biomass deaths per TWh | 4.63 | deaths/TWh electricity | 2021 | owid_deaths |
| Brown coal deaths per TWh | 32.72 | deaths/TWh electricity | 2021 | owid_deaths |
| Coal deaths per TWh | 24.62 | deaths/TWh electricity | 2021 | owid_deaths |
| Gas deaths per TWh | 2.821 | deaths/TWh electricity | 2021 | owid_deaths |
| Hydropower deaths per TWh | 1.3 | deaths/TWh electricity | 2021 | owid_deaths |
| Nuclear deaths per TWh | 0.03 | deaths/TWh electricity | 2021 | owid_deaths |
| Oil deaths per TWh | 18.43 | deaths/TWh electricity | 2021 | owid_deaths |
| Solar deaths per TWh | 0.019 | deaths/TWh electricity | 2021 | owid_deaths |
| Wind deaths per TWh | 0.035 | deaths/TWh electricity | 2021 | owid_deaths |

United States estimates cover different years, models, and taxa; ranges must not be summed as a common-year census. European wind-farm result is a median per-turbine rate from the reviewed sites, not a Europe-wide total.

2021 processed rates per TWh of electricity combine air-pollution and accidents using studies with different boundaries and observation periods. They are contextual estimates, not direct counts from a single harmonized life-cycle study.

Free-ranging domestic cats low: contiguous United States

Free-ranging domestic cats high: contiguous United States

Building collisions low: United States

Building collisions median: United States

Building collisions high: United States

Vehicle collisions low: United States roads

Vehicle collisions high: United States roads

Power lines, collision + electrocution low: United States

Power lines, collision + electrocution high: United States

Wind turbine collisions, monopole estimate low: contiguous United States

Wind turbine collisions, monopole estimate median: contiguous United States

Wind turbine collisions, monopole estimate high: contiguous United States

European wind-farm fatality rate (median) median: surveyed European wind farms

Biomass deaths per TWh: Processed source estimates mix air-pollution and accident evidence.

Brown coal deaths per TWh: Processed source estimates mix air-pollution and accident evidence.

Coal deaths per TWh: Processed source estimates mix air-pollution and accident evidence.

Gas deaths per TWh: Processed source estimates mix air-pollution and accident evidence.

Hydropower deaths per TWh: Processed source estimates mix air-pollution and accident evidence.

Nuclear deaths per TWh: Processed source estimates mix air-pollution and accident evidence.

Oil deaths per TWh: Processed source estimates mix air-pollution and accident evidence.

Solar deaths per TWh: Processed source estimates mix air-pollution and accident evidence.

Wind deaths per TWh: Processed source estimates mix air-pollution and accident evidence.

## 15. Lifecycle emissions

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| Solar PV min | 10.9 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Solar PV median | 43.4 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Solar PV max | 226 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Concentrating solar power min | 11 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Concentrating solar power median | 28 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Concentrating solar power max | 241 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Geothermal min | 5.6 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Geothermal median | 36.7 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Geothermal max | 245.2 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Hydropower min | 0.574 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Hydropower median | 20.5 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Hydropower max | 74.8770828326524 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Wind min | 1.2999999933983777 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Wind median | 13 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Wind max | 81 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Nuclear (LWR) min | 3.1 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Nuclear (LWR) median | 13 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Nuclear (LWR) max | 220 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Natural gas (NGCC) min | 307 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Natural gas (NGCC) median | 450 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Natural gas (NGCC) max | 682 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Oil min | 510 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Oil median | 840 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Oil max | 1170 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Coal min | 675 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Coal median | 1001 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |
| Coal max | 1689 | g CO2-eq/kWh electricity | 2026 | nrel_lifecycle |

NREL harmonized literature dataset, updated 2026-05-22; min/median/max for total lifecycle estimates. Technology/system boundaries vary; these distributions are not universal constants.

NREL data-use notice (required by source terms):

The National Renewable Energy Laboratory (NREL) is operated for the U.S. Department of Energy (DOE) by Alliance for Sustainable Energy, LLC ("Alliance").
Unless data or software is explicitly made available on this server under separate license terms (in which case such license terms shall apply only to such data or software), access to or use of any data or software made available on this server ("Data") shall impose the following obligations on the user, and use of the Data constitutes user's agreement to these terms. The user is granted the right, without any fee or cost, to use or copy the Data, provided that this entire notice appears in all copies of the Data. Further, the user agrees to credit DOE/NREL/ALLIANCE in any publication that results from the use of the Data. The names DOE/NREL/ALLIANCE, however, may not be used in any advertising or publicity to endorse or promote any products or commercial entities unless specific written permission is obtained from DOE/NREL/ ALLIANCE. The user also understands that DOE/NREL/ALLIANCE are not obligated to provide the user with any support, consulting, training or assistance of any kind with regard to the use of the Data or to provide the user with any updates, revisions or new versions thereof. DOE, NREL, and ALLIANCE do not guarantee or endorse any results generated by use of the Data, and user is entirely responsible for the results and any reliance on the results or the Data in general.
USER AGREES TO INDEMNIFY DOE/NREL/ALLIANCE AND ITS SUBSIDIARIES, AFFILIATES, OFFICERS, AGENTS, AND EMPLOYEES AGAINST ANY CLAIM OR DEMAND, INCLUDING REASONABLE ATTORNEYS' FEES, RELATED TO USER'S USE OF THE DATA. THE DATA ARE PROVIDED BY DOE/NREL/ALLIANCE "AS IS," AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. DOE/NREL/ALLIANCE ASSUME NO LEGAL LIABILITY OR RESPONSIBILITY FOR THE ACCURACY, COMPLETENESS, OR USEFULNESS OF THE DATA, OR REPRESENT THAT ITS USE WOULD NOT INFRINGE PRIVATELY OWNED RIGHTS. IN NO EVENT SHALL DOE/NREL/ALLIANCE BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER, INCLUDING BUT NOT LIMITED TO CLAIMS ASSOCIATED WITH THE LOSS OF DATA OR PROFITS, THAT MAY RESULT FROM AN ACTION IN CONTRACT, NEGLIGENCE OR OTHER TORTIOUS CLAIM THAT ARISES OUT OF OR IN CONNECTION WITH THE ACCESS, USE OR PERFORMANCE OF THE DATA.

## 16. Energy to 2100

| Quantity | Value | Unit | Year | Source key |
|---|---:|---|---|---|
| AR6 C1/C3 median total primary energy | 565.369 | EJ/year | 2020 | ipcc_ar6_energy |
| AR6 C1/C3 median total primary energy | 562.578 | EJ/year | 2030 | ipcc_ar6_energy |
| AR6 C1/C3 median total primary energy | 538.236 | EJ/year | 2040 | ipcc_ar6_energy |
| AR6 C1/C3 median total primary energy | 564.288 | EJ/year | 2050 | ipcc_ar6_energy |
| AR6 C1/C3 median total primary energy | 625.62 | EJ/year | 2060 | ipcc_ar6_energy |
| AR6 C1/C3 median total primary energy | 689.016 | EJ/year | 2070 | ipcc_ar6_energy |
| AR6 C1/C3 median total primary energy | 764.397 | EJ/year | 2080 | ipcc_ar6_energy |
| AR6 C1/C3 median total primary energy | 830.222 | EJ/year | 2090 | ipcc_ar6_energy |
| AR6 C1/C3 median total primary energy | 881.971 | EJ/year | 2100 | ipcc_ar6_energy |
| Favourable EUROfusion 2026 case: fusion output | 105.84 | EJ/year | 2100 | eurofusion_etm_2026 |
| EUROfusion 2026 output / AR6 median primary demand | 12.0004 | percent | 2100 | eurofusion_etm_2026 + ipcc_ar6_energy |
| MIT fusion 2800 USD/kW cost case | 0 | EJ/year | 2020 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 0 | EJ/year | 2025 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 0 | EJ/year | 2030 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 0 | EJ/year | 2035 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 0 | EJ/year | 2040 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 0.36 | EJ/year | 2045 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 2.16 | EJ/year | 2050 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 6.12 | EJ/year | 2055 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 15.84 | EJ/year | 2060 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 34.92 | EJ/year | 2065 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 54 | EJ/year | 2070 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 79.2 | EJ/year | 2075 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 97.2 | EJ/year | 2080 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 114.84 | EJ/year | 2085 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 130.68 | EJ/year | 2090 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 146.52 | EJ/year | 2095 | mit_fusion_2024 |
| MIT fusion 2800 USD/kW cost case | 160.56 | EJ/year | 2100 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 0 | EJ/year | 2020 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 0 | EJ/year | 2025 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 0 | EJ/year | 2030 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 0 | EJ/year | 2035 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 0 | EJ/year | 2040 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 0.36 | EJ/year | 2045 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 1.44 | EJ/year | 2050 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 5.76 | EJ/year | 2055 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 12.6 | EJ/year | 2060 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 27 | EJ/year | 2065 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 41.04 | EJ/year | 2070 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 57.24 | EJ/year | 2075 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 70.56 | EJ/year | 2080 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 82.08 | EJ/year | 2085 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 93.96 | EJ/year | 2090 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 108.36 | EJ/year | 2095 | mit_fusion_2024 |
| MIT fusion 5600 USD/kW cost case | 121.68 | EJ/year | 2100 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 0 | EJ/year | 2020 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 0 | EJ/year | 2025 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 0 | EJ/year | 2030 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 0.0072 | EJ/year | 2035 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 0 | EJ/year | 2040 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 0.36 | EJ/year | 2045 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 1.35 | EJ/year | 2050 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 4.32 | EJ/year | 2055 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 11.88 | EJ/year | 2060 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 19.08 | EJ/year | 2065 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 30.24 | EJ/year | 2070 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 39.6 | EJ/year | 2075 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 52.2 | EJ/year | 2080 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 61.92 | EJ/year | 2085 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 71.28 | EJ/year | 2090 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 77.76 | EJ/year | 2095 | mit_fusion_2024 |
| MIT fusion 8000 USD/kW cost case | 86.4 | EJ/year | 2100 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 0 | EJ/year | 2020 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 0 | EJ/year | 2025 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 0 | EJ/year | 2030 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 0 | EJ/year | 2035 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 0 | EJ/year | 2040 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 0 | EJ/year | 2045 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 0.36 | EJ/year | 2050 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 0.72 | EJ/year | 2055 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 1.8 | EJ/year | 2060 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 3.96 | EJ/year | 2065 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 6.84 | EJ/year | 2070 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 10.08 | EJ/year | 2075 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 12.96 | EJ/year | 2080 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 17.64 | EJ/year | 2085 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 21.24 | EJ/year | 2090 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 25.2 | EJ/year | 2095 | mit_fusion_2024 |
| MIT fusion 11300 USD/kW cost case | 29.16 | EJ/year | 2100 | mit_fusion_2024 |
| EUROfusion 2024 S02 fusion | 0 | EJ/year | 2030 | eurofusion_etm_2024 |
| EUROfusion 2024 S02 fusion | 1.8 | EJ/year | 2050 | eurofusion_etm_2024 |
| EUROfusion 2024 S02 fusion | 27 | EJ/year | 2070 | eurofusion_etm_2024 |
| EUROfusion 2024 S02 fusion | 104.4 | EJ/year | 2100 | eurofusion_etm_2024 |

IPCC AR6 C1/C3 literature ranges, not probabilities or a forecast. Source-wise medians are not a coherent energy mix. Fusion cases are published electricity outputs scaled to the AR6 median total with direct-equivalent accounting, not integrated model results.

EUROfusion 2026 output / AR6 median primary demand: Cross-model scaling, not a combined run.

MIT fusion 2800 USD/kW cost case: Approximate published curve.

MIT fusion 5600 USD/kW cost case: Approximate published curve.

MIT fusion 8000 USD/kW cost case: Approximate published curve.

MIT fusion 11300 USD/kW cost case: Approximate published curve.

EUROfusion 2024 S02 fusion: Approximate published dated bar.
