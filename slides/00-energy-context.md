# The big picture — live route

Chapter 0 of the fusion Skript. Preserve the original energy-opening content,
using the first-lecture slides and the 2024/2025 transcripts as evidence.
The opening solar photo reuses the cleared NASA/SDO asset from plasma;
other pages use original figures. Photo provenance is in `photos/credits.md`.
Hero photos cover the slide with a tiny legible credit at the bottom, matching
Plasma. Mathematical pages and plots stay light. All detailed reasoning is
done on white pages. Future animations use dark full-slide canvases and stable
HTML player links according to the shared teaching rules.

## Opening sequence

The opening connects the country-level GDP/energy plot (page 3), household
stove examples (page 4), and three matching "Living standards" pages for 1981,
2000 and 2024 (pages 5–7), before "Micro and macro" on page 8. All income
plots use the same four fixed bands and population axis: below 3, 3–12,
12–48 and at least 48 in 2021 PPP USD per person per day. These are teaching
bands anchored to the current $3 extreme-poverty line, with fourfold steps;
they are not converted Gapminder levels or four official poverty categories.
Derive each band's population by differencing PIP cumulative counts from
one September 2026 release, with year-specific totals and percentage labels.
PIP line-up estimates include survey interpolation/extrapolation.
Reuse the canonical `income-levels-1981.svg`, `income-levels-2000.svg` and `income-levels-2024.svg`
unchanged in the reference chapter and slides. Keep identical geometry and
a 0–5.5-billion population axis with room for the two-line labels. Mark 1981 as the first PIP global year and electricity access as unavailable
for that year. Match the later pages' electricity access and
Austria/Ethiopia primary-energy ratio to their respective years. Label the latter's EIA
boundary, which does not fully cover traditional biomass. The discussion cue
connects access with useful energy services. This supplies the distribution
part of catalogue Chapter 0, question 1.

The Dollar Street income note belongs with the photographs on page 4:
monthly PPP dollars per equivalent adult. It is distinct from the income
distribution's per-person daily scale and from national GDP per person.

## Consumption boundaries

After "Micro and macro", add one "Energy consumption and electricity" page
before the energy-mix page. Compare Austria's gross inland, final energy,
final electricity and household electricity on a common per-person daily
scale using the preliminary 2025 balance and its annual-average population.
Electricity and household electricity are nested subsets, not conversion
steps. Show their fractions with explicit denominators. Decompose the
gross-to-final difference into net transformation losses, energy-sector use
including transport losses, and non-energy use; the whole difference is
not waste heat. The preliminary balance does not isolate thermal plants.
Use a separate assumed 40%-efficient thermal plant with no heat recovery
to illustrate 100 kWh heat input = 40 kWh electricity + 60 kWh rejected heat.
Link the Statistics Austria balance, population and EIA efficiency definition.
Generate one canonical figure for the slide and reference chapter.

## Electricity costs and storage

Expand the module-price page into two pages in the solar-learning section:
"Solar panels and battery storage" with separate logarithmic axes for module
USD/W and battery USD/kWh of capacity, then "Electricity generation costs"
with logarithmic electricity LCOE in constant 2025 US cents/kWh, 1980–2035.
Use the supplied 9 October 2026 sourcebook, retained verbatim under
`data/ch00/raw/cost-sourcebook/`, including all four CSV tables. Plot six
electricity series: PV, PV with daily storage, onshore wind, gas, coal and new
nuclear. Distinguish published benchmarks, reconstructions/interpolations and
future scenarios with markers and line styles. Keep the US/global samples
visible. The daily-storage curve shifts 60% of delivered energy; it does not
provide seasonal or firm supply. Omit the oil proxy from the LCOE figure.

The hardware page distinguishes cells, packs and installed four-hour storage;
these are capacity prices, not delivered-electricity costs. The 2010 installed
storage anchor is a published model in IRENA Figure 9.2, so correct its plot
flag from B to R while preserving the original CSV. Later IRENA reports revise
historical values; retain this sourcebook's historical extract with that note.
Reuse both original figures unchanged in the reference chapter, with the
daily-storage equation, assumptions and the distinct Nevada 95%-annual-energy
case explained there. Record the source audit and reproduce the model checks.

## Route

1. Primary/final energy plot: define boundaries, E, N and time; two blank pages
   for unit conversion and the Austrian per-person calculation; formula summary.
2. Sector plot: distinguish national allocation from household estimates; two
   blank pages for appliance/car/heat examples; formula summary.
3. Stock-growth plot: choose a horizon and state assumptions; two blank pages
   for constant demand, then the exponential integral; result summary.
4. Area plot: compare explicit delivered-density scenarios; two blank pages
   for area and capacity factor; result summary.
5. Blank pages: construction scale, useful-service comparison and the fusion
   bridge; final deployment equations. Fuel availability is only one condition.

## Sources and checks

Figures are the canonical outputs from `derivations/energy.py`, reused from
the Skript without alternate slide versions. The labels state units; color
and line styles carry redundant distinctions. Energy inputs are the 2025
preliminary balance, with its matching annual-average population. Resource
and area plots are model scenarios. Do not import MacKay pages or old charts.
The missing first fusion recording stays an explicit upload gap.

## Fusion resource estimates after the JET page

After existing page 24, insert two pages before credits: "Fusion fuel reserves"
and "Lead and beryllium". Page 11 remains each fuel's own stock divided
by its current world production; state the years and constant-rate assumption.

The new fuel budget deliberately matches EIA 2024 world primary energy
numerically with fusion electricity. Reuse MacKay's explicit 2300 kWh(e)/g
natural-Li yield scenario with updated 37 Mt reserves, not his old reserve stock.
Show the formula and canonical logarithmic inventory plot from
13-fusion-resources.json. Seawater is an inventory, not a reserve; MacKay's
extraction-energy comparison supports energetic plausibility only. Laboratory
extraction is demonstrated, industrial scale is unproven. The D–T deuterium
bound still needs Li and tritium; these inventories cannot be added.

For blanket multipliers, use the same years axis and layout as the fuel page.
Paired 2011 Bradshaw 1 GW(e) concepts supply initial loading and annual
nuclear burn-up: Pb 4092 t and 3.1 t/full-power-year; Be 120 t and
0.19 t/full-power-year. At 90% capacity factor, subtract startup loading from
each stock before dividing by annual nuclear burn-up. Assume ideal recovery,
no competing uses, growth or recovery losses. Distinguish large initial
inventory from the slow consumption of blanket atoms. Reuse the canonical
`fusion-blanket-lifetimes.svg`; no separate slide-only calculation.
Pb reserves give about 45 years after startup; identified resources >30,353
years. The 100 kt Be reference cannot load the fleet, so assign no lifetime.
USGS reports >100 kt resources, not a total-resource ceiling; world Be reserves
are unavailable. Full assumptions and design limitations belong in the reference.

## Final outlook to 2100

Keep one source-share plot and the observed 2024 markers. Replace the single
GCAM4 pathway with the IPCC AR6 vetted C1/C3 multi-model ensemble: 2020–2100
decades, complete total and seven source variables, nonnegative components,
and no component sum exceeding the total beyond 0.01% reporting tolerance.
Group coal/oil/gas as fossils and solar/wind together. Plot scenario medians;
show 10–90% scenario ranges for wind+solar and bioenergy. These are descriptive
ranges of a selected literature ensemble, not probabilities or a synthetic
energy mix. Keep a current-policy fossil comparison from the AR6 illustrative
current-policy project, clearly identifying its 2021 policy vintage.

Show actual published fusion timelines: all four MIT EPPA 2024 cost cases
(Fig. 4.4b, vector-digitized, approximate), with its base case emphasized;
EUROfusion/CIEMAT 2024 S02 dated output bars (2030/2050/2070/2100, approximate
digitization) as marked dashed segments. Retain the EUROfusion 2026 favourable
endpoint as a distinct star. Convert electricity output to EJ and scale all
fusion cases to the same IPCC ensemble median primary-energy demand. Never
insert these cross-model comparisons into a stack or claim displacement.

Retain the 2025 solar construction-rate guide through 2035, using relative
IPCC ensemble median demand instead of the removed GCAM denominator.
Keep assumptions, the literature comparison, biomass/BECCS land constraints,
primary-energy accounting and extraction precision in the reference.
Use the existing dataset loader, chapter builder, teaching plotter and shared
SVG; remove the superseded GCAM-only data and explanations.
