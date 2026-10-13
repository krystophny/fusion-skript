#import "../theme.typ": *
#let data = json("/data/energy.json").austria_2025
#let per-day(tj) = tj * 1e12 / (3.6e6 * data.population_annual_average * 365)
#let primary = per-day(data.primary_TJ)
#let final = per-day(data.final_TJ)
#let graphic(name, alt, caption: none) = figure(
  image("/derivations/build/fig/" + name + ".svg", width: 100%, alt: plain-text(alt)),
  caption: if caption == none { alt } else { caption },
)
#let exam(q, wording) = exam-prompts((wording,), [Fusion Physics Exam (2026), Chapter 0, Q#q, PDF p. 1])

#let chapter = [
#page-title(number: 0)[The big picture] <energy-context>
#lead[Estimate the scale of an energy system before judging what fusion could contribute.]

#section-title[Standards of living and energy] <standards-living>
The same everyday task can be done with very different equipment and energy
services. Dollar Street arranges household photographs by income rather than
by country label. The monthly values shown here are purchasing-power-adjusted
US dollars per equivalent adult, not total household income. They are
illustrative households, not a statistical sample of national living standards.

#figure(
  image("/slides/photos/earth-at-night-2016.jpg", width: 100%, alt: "Global Black Marble night-lights composite for 2016; illuminated areas are concentrated around populated regions."),
  caption: [Black Marble 2016, NASA Earth Observatory / Suomi NPP VIIRS; public domain. Composite night lights, not a map of electricity access.],
)

To compare living standards in 1981, 2000 and 2024, we use four fixed household
income or consumption bands in 2021 purchasing-power-parity (PPP) dollars
per person per day: below 3, 3–12, 12–48 and at least 48. PPP adjusts for
differences in price levels between countries; the common price basis makes
the three years comparable. The \$3 boundary is the World Bank's current
extreme-poverty line. The \$12 and \$48 boundaries are teaching choices with
fourfold steps, not official poverty lines. These definitions replace the
earlier Gapminder bands in 2011 PPP dollars; they are not a conversion of
those old thresholds.

The World Bank's September 2026 Poverty and Inequality Platform release
estimates global populations of 4.52 billion in 1981, 6.16 billion in 2000
and 8.14 billion in 2024. Taking differences of its cumulative population counts below each
threshold gives about 2.23, 2.50, 0.94 and 0.48 billion people in the four
bands in 2000, and 0.82, 3.96, 2.40 and 0.95 billion in 2024. The share
below \$3/day falls from 47.1% in 1981 to 36.2% in 2000 and 10.1% in 2024.
1981 is the first year in the World Bank global series. These global estimates combine
household surveys with interpolation and extrapolation to a common year;
they are not simultaneous censuses. The plots retain one population scale
and show both counts and shares.

#graphic("income-levels-1981", [World population in 1981, the first PIP global year, by four fixed income or consumption bands in 2021 PPP dollars per person per day.], caption: [1981 global estimates; World Bank PIP, September 2026 release, 2021 PPP; CC BY 4.0; original plot. Same cutoffs and axes as 2000 and 2024.])
#graphic("income-levels-2000", [World population in 2000 by four fixed income or consumption bands in 2021 PPP dollars per person per day.], caption: [2000 global estimates; World Bank PIP, September 2026 release, 2021 PPP; CC BY 4.0; original plot. Cutoffs: \$3, \$12 and \$48.])
#graphic("income-levels-2024", [World population in 2024 by the same four bands, with identical axes.], caption: [2024 global estimates; World Bank PIP, September 2026 release, 2021 PPP; CC BY 4.0; original plot. Same definitions and population scale as 2000.])
#unit-ledger[Fixed bands: below 3, 3–12, 12–48 and at least 48 in 2021 PPP USD/(person day). Population [billion], 2000: 2.23, 2.50, 0.94, 0.48; 2024: 0.82, 3.96, 2.40, 0.95.]

The accompanying slide comparison uses each available year's electricity access:
78.2% in 2000 and 91.9% in 2024. There is no global WDI electricity-access
observation for 1981; that page shows a dash and omits the energy ratio.
Primary energy per person in the EIA
series is approximately 165 times higher in Austria than Ethiopia in 2000,
and 50 times higher in 2024. These ratios describe EIA's accounting boundary,
which does not fully include traditional biomass; they are not ratios of
all useful household energy services.

#grid(columns: 4, gutter: 5pt,
  figure(image("/slides/photos/dollarstreet-stove-5d4bf44ccf0b3a0f3f35b67a.jpg", width: 100%, alt: "Cooking stove in a photographed household in Haiti."), caption: [Haiti · USD 39.9 per equivalent adult per month · Zoriah Miller · CC BY 4.0.]),
  figure(image("/slides/photos/dollarstreet-stove-5d4bec73cf0b3a0f3f34df4c.jpg", width: 100%, alt: "Cooking stove in a photographed household in Bolivia."), caption: [Bolivia · USD 180 per equivalent adult per month · Zoriah Miller · CC BY 4.0.]),
  figure(image("/slides/photos/dollarstreet-stove-5d4be196cf0b3a0f3f33b4c5.jpg", width: 100%, alt: "Cooking stove in a photographed household in Brazil."), caption: [Brazil · USD 685 per equivalent adult per month · Leony Carvalho · CC BY 4.0.]),
  figure(image("/slides/photos/dollarstreet-stove-5ec4f926f0611d7ddd7414e9.jpg", width: 100%, alt: "Cooking stove in a photographed household in Spain."), caption: [Spain · USD 7,639 per equivalent adult per month · Omar Havana · CC BY 4.0.]),
)

For 2024, the United States used about 223 kWh of primary energy per person
per day, China 97, Austria 93 and India 21 in the EIA series. These are national
annual averages with an upstream primary-energy boundary; they do not measure
the energy used directly by each household.
#graphic("energy-gdp", [Country observations for 2024, primary energy per person versus GDP per person at purchasing power parity; marker area follows population.], caption: [188 economies with matched data, 2024. EIA international primary energy (public domain), World Bank WDI GDP and population (CC BY 4.0); original plot, IT Btu converted to kWh/(person day).])

The World Bank reports access to electricity for 91.93% of the world population
in 2024. No clean-cooking share is shown: the current Tracking SDG7 source note
for the otherwise convenient indicator specifies CC BY-NC 3.0 IGO. Global
ownership shares for washing machines, cars and refrigerators are not included
without a comparable, openly reusable source.
#unit-ledger[GDP per person is in constant 2021 international dollars per year; energy is in kWh/(person day); bubble area is proportional to people.]
#exam(1, [How is income distributed globally, and how does it relate to energy consumption?])

#section-title[Numbers, not adjectives] <energy-normalization>
“Cheap”, “abundant” and “large” are comparisons, not measurements. Following
David MacKay's quantitative method, choose a service, an energy boundary, a
population and a time interval, then put every estimate on a common unit basis.
MacKay is a conceptual reference only: the derivation and figures here are
independent, and no book figure or page is reproduced.

Let $E$ be energy in joules, $N$ the number of people, $Delta t$ elapsed time
in seconds, and $bar(P)$ average power in watts. A watt is one joule per second:
$ bar(P) = E / Delta t, quad p = E / (N Delta t). $
Thus $p$ is average power per person. Since a kilowatt-hour is
$1000 times 3600 = 3.6 times 10^6$ joules and a day is 86,400 seconds,
$ 1 "kWh/(person day)" = (3.6 times 10^6)/(86400) "W/person"
  = 41.667 "W/person". $
An annual energy $E_y$ using a 365-day convention gives
$ e_d = E_y/(3.6 times 10^6 N times 365) "kWh/(person day)". $

#graphic("micro-macro", [Three 2025 average-energy estimates on one per-person daily scale: lecturer bottom-up estimate, Austria gross inland consumption and Austria final energy.], caption: [Lecturer's independent 2025 estimate; Statistics Austria preliminary 2025 energy balance and annual-average population; GDP cross-check uses World Bank Austria GDP. Statistics Austria values are replotted with attribution under its custom terms, not labelled CC.])

The lecturer's bottom-up estimate sums home electricity 5, heating and hot
water 20, car 20, public transport and aviation 10, goods 20, and work or
industry 45 kWh/(person day), for 120 in total. Its GDP check uses
€60,000/(person year) times 1 kWh/€ = 164.4 kWh/(person day). These are
teaching estimates, not reconciled measurements. The car example on the source
page evaluates to 15 kWh/(person day), while its rounded budget line is 20.

#unit-ledger[1 kWh/(person day) = 41.667 W/person; 365 days/year; 2025 hand estimate = 120 kWh/(person day).]
#knowledge-check((
  (question: [Convert 48 kWh/(person day) to average power.], answer: [2 kW/person.]),
  (question: [What must be held fixed when comparing daily energy estimates?], answer: [The energy boundary, population, time convention and useful service.]),
))
#exam(2, [Compute the primary energy consumption in a fully developed country per capita and day from a) Estimating a person's individual consumption (heating, electricity, car, etc.) and b) From the macroeconomic perspective of a whole country.])

#section-title[Energy boundaries and intensity] <energy-boundaries>
Primary energy counts energy inputs before conversion. Final energy counts
carriers delivered to users. Consumer electricity is one final carrier, not the
whole energy system. Useful energy is the service after conversion at the point
of use. For an ideal conversion efficiency $eta$, defined as useful output
divided by input, $E_("useful") = eta E_("input")$. A heat pump is described
by a coefficient of performance: delivered heat divided by electricity use;
ambient heat belongs inside the stated system boundary.

Energy intensity relates annual energy $E_y$ to annual economic output $Y_y$:
$ I_E = E_y / Y_y. $
The energy boundary, price basis and year must be named. The reciprocal,
economic output per unit energy, is not a personal electricity tariff. Austria's
2025 gross balance divided by current-euro GDP gives 0.734 kWh/€; this is an
accounting comparison, not an independent measurement of energy needs.

#knowledge-check((
  (question: [Can primary fuel energy and final electricity be added as separate demands?], answer: [No; conversion can count the same energy at two stages.]),
  (question: [What does energy intensity compare?], answer: [Energy use with economic output for a stated boundary, year and price basis.]),
))
#exam(3, [Explain energy intensity])
#exam(4, [How do primary energy consumption and consumer electricity differ?])

#section-title[Austria: national and household budgets] <energy-demand>
Statistics Austria's preliminary 2025 balance reports
#calc.round(data.primary_TJ / 1000, digits: 1) PJ gross inland consumption and
#calc.round(data.final_TJ / 1000, digits: 1) PJ final consumption. With the
annual-average population of #calc.round(data.population_annual_average)
people, these are #calc.round(primary, digits: 1) and
#calc.round(final, digits: 1) kWh per person per day. The first is the
production-side national balance; the second counts delivered carriers.
Neither is a typical household bill.

#graphic("energy-boundaries", [Austria 2025 preliminary gross inland and final energy per person per day, separated by accounting boundary.], caption: [Statistics Austria, preliminary 2025 energy balance, and annual-average population; own calculation. Reused under attributed data terms; not a named CC licence.])
#graphic("energy-sectors", [Final Austrian energy use in 2025 allocated across industry, transport, services, households and agriculture.], caption: [Statistics Austria, preliminary 2025 energy balance; own unit conversion. Reused under attributed data terms, not a named CC licence. Transport and industry are national allocations, not household measurements.])
#graphic("austria-sankey", [Two conserved Austria 2025 energy balances: primary carriers to gross inland consumption and its partitions; final carriers to a final-energy pool and final-use sectors. Each node shows its energy in kWh/(person day).], caption: [Statistics Austria preliminary balance rows 8–19, 2025; population-normalized to kWh/(person day). Reused with attribution under Statistics Austria's custom terms, not CC. Carriers below 2 kWh/(person day) are grouped as Other. Both panels use the same flow scale; final carrier-to-sector cells are pooled into totals, with the complete matrix retained in the source data. Primary inputs are not causally allocated to final sectors.])

The final carrier values are 28.91 kWh/(person day) oil products, 19.01
electricity, 17.96 renewable fuels and direct heat, 13.30 gas, 6.09 district
heat, 1.04 coal and 0.85 waste. The conversion pool is a net input-minus-output
balance; gross energy minus final energy also contains other uses and losses.
The carrier-by-sector CSV and Sankey node/link CSV retain the source cells and
the conservation check.

#graphic("electricity-consumption", [Four national per-person daily energy budgets on one scale: 112.0 kWh primary, 87.2 final, 19.0 final electricity and 6.5 household electricity. The smaller electricity bars are nested subsets. The primary-to-final difference is split into transformation loss, energy-sector use including transport losses, and non-energy use. A separate assumed 40%-efficient thermal plant illustrates rejected heat.], caption: [Own calculations from Statistics Austria's #link("https://www.statistik.at/fileadmin/pages/99/preliminaryEnergyBalancesforAustriaInTerajoule.ods")[preliminary 2025 balance], rows 8–13 and 18, and #link("https://www.statistik.at/en/statistics/population-and-society/population/population-stock/annual-average-population")[annual-average population]. Thermal-efficiency definition: #link("https://www.eia.gov/tools/faqs/faq.php?id=107&t=3")[EIA]. The 40% efficiency is an illustrative assumption.])

Final electricity is 21.8% of final energy consumption. Household electricity
is 34.2% of that electricity, or 7.5% of total final energy. All per-person
values use the national population; household electricity is not the total
household budget, which also includes other heating fuels and district heat.
The 6.4 kWh/(person day) net transformation loss covers all transformation
processes in the balance, including refining; it does not isolate thermal
power plants. For the separate thermal example, electrical efficiency is
$eta_"el" = E_"electric" / E_"heat,in"$. With the assumed
$eta_"el" = 0.40$ and no heat recovery, a 100 kWh heat input gives 40 kWh
electricity and 60 kWh rejected heat. This is not an Austrian fleet average.

For a household estimate, sum appliance electricity, transport and heating
separately. A device drawing power $P_a$ for time $t_a$ uses $E_a=P_a t_a$. A
car travelling distance $d$ at fuel use $b$ litres per distance and fuel energy
$h$ per litre uses $E_("car")=d b h$. Indirect energy in goods and services is
not automatically included in the household estimate.

#unit-ledger[$E_a=P_a t_a$; $I_E=E_y/Y_y$; gross inland = 112.01 and final = 87.16 kWh/(person day), preliminary 2025.]
#knowledge-check((
  (question: [Why is household electricity smaller than a national per-person budget?], answer: [The national budget also includes transport, industry, services, heat and other carriers.]),
  (question: [Why does the Sankey keep primary inputs separate from final sectors?], answer: [The published balance does not trace each primary carrier causally into each final sector.]),
))
#exam(5, [What's the energy mix in Austria?])

#section-title[Finite resources and sustainable rates] <energy-resources>
Let a recoverable stock contain energy $S$ and constant demand be $D$ per year.
The static exhaustion time is $t_"static"=S/D$. A reserve estimate depends on
price, technology and extraction constraints; it is not all material in the
ground. To spread the stock over a chosen horizon $H$, its annual contribution
is at most $S/H$, so its fraction of demand is
$ f = min(1, S/(H D)) = min(1, t_"static"/H). $

If demand grows as $D(t)=D_0 exp(g t)$, where $g$ is the continuous growth rate
per year, then
$ S = integral_0^(t_"end") D_0 exp(g t) dif t
  = (D_0/g)(exp(g t_"end")-1), quad
  t_"end" = ln(1+g S/D_0)/g. $
As $g$ approaches zero, the lifetime approaches $S/D_0$. For a discrete annual
increase $r$, convert it to $g=ln(1+r)$ before using the continuous formula.

#graphic("resource-horizon", [Exhaustion time versus continuous annual demand growth for a stock equal to 100 years of initial use; zero growth gives the static lifetime.], caption: [Original SymPy-derived stock model; no provider figure reused. BGR data re-plotted with attribution; IAEA/NEA Red Book 2024 is CC BY 4.0.])
The 2024 BGR workbook gives world stocks and production in their native units;
the Red Book's broader identified uranium resources are kept separate from
low-cost uranium reserves. R/P divides the stated stock by the stated annual
production; the 1,000-year power assumes fixed world population and once-through
fuel-cycle energy where appropriate. None of these ratios is a forecast.

#unit-ledger[$t_"static"=S/D$; $t_"end"=ln(1+g S/D_0)/g$; $g$ in year⁻¹; $S$ and $D$ must use compatible units.]
#knowledge-check((
  (question: [A stock equals 60 years of demand. What fraction can it supply over 1,000 years?], answer: [6% at constant demand.]),
  (question: [Does positive demand growth increase exhaustion time?], answer: [No; it shortens it for the same initial demand and stock.]),
))
#exam(6, [Given a number for reserves of a single fossile resource, compute a) what part of the energy mix it can contribute sustainably (1000 years) or b) how long would it last at current consumption levels.])

#section-title[Power density, solar and area] <energy-area>
Let $q_A$ be time-averaged delivered power per area in W/m², $A$ area in m²,
and $P$ average power in watts. Since $P=q_A A$, area per person for demand
$p$ is $A/N=p/q_A$. For illustration, at 100 kWh/(person day), $p=4,166.7$
W/person. A delivered density of 20 W/m² uses 208 m²/person; 3 W/m² uses
1,389 m²/person. Collector area, total farm footprint and system land have
different denominators.

At noon in clear weather near normal incidence, incoming solar irradiance can
approach 1,000 W/m². Night removes one half of the daily average at the equator;
latitude, solar angle, day length, season, weather, horizon and tilt modify the
local yearly total. PVGIS gives Graz a 2005–2023 horizontal mean of 1,286.6
kWh/(m² year), or 146.9 W/m². A 35° south-facing model yields 1,542 kWh/m²/a.
At assumed 20% module efficiency and modelled performance ratio, mean module
output is 27.89 W/m² of module area. The symbolic factor chain is
$1000 "W/m²" times 0.318_("day/night") times 0.681_("latitude")
  times 1.009_("season") times 0.672_("atmosphere/weather")
  times 1.199_("tilt") times 0.20_("module") times 0.792_("performance")
  = 27.89 "W/m²".$
Each multiplier has unit 1. The atmosphere/weather factor is a residual
calibrated to PVGIS, not a separate measurement. This is a modelled climatology,
not a measured ground-station time series.

#graphic("solar-monthly", [PVGIS satellite-model horizontal irradiation by month for Graz, SARAH3/ERA5 2005–2023.], caption: [EU Joint Research Centre PVGIS; 47.0707° N, 15.4395° E. Free reuse with attribution under JRC usage conditions; this plot is original.])
#unit-ledger[$q_A = P/A$; Graz horizontal 1,286.6 kWh/(m² year) = 146.9 W/m²; 35° south plane 1,542 kWh/(m² year); modelled module mean 27.89 W/m²; Weesow expected ground mean 12.53 W/m².]

For the scale of a complete site, Weesow-Willmersdorf covers 1.64 km² and has
187 MWp of installed panels. Its operator expected 180 GWh/year at inauguration;
that is an expectation, not a measured annual yield. On the 1.64 km² site
footprint, that expected annual energy corresponds to 12.53 W/m² average ground
density, distinct from 27.89 W/m² of module area. Its same-scale Sentinel-2 image
and Graz boundary both show 16 km square windows without rescaling.

#graphic("true-scale-park-graz", [Same-scale 16 km square views: Weesow-Willmersdorf in Sentinel-2 true colour and the projected Graz municipal boundary, with a square showing the area required for 1 GW average at the operator's expected site yield.], caption: [Weesow-Willmersdorf, 52.650568° N, 13.686692° E; 1.64 km², 187 MWp, 180 GWh/year expected (EnBW site facts; attributed numerical data, expected not measured). Contains modified Copernicus Sentinel data 2025. Boundary: Stadt Graz OGD, CC BY 4.0; translated, not rescaled.])

Using the operator's expected yield, one GW average would require about
79.8 km² of panels and site, or roughly 48.7 park-equivalents. The measured
footprint yield remains a gap; these operator design figures give a documented
scenario. A full-site density must not be compared directly to module-area
efficiency.

Wind spacing reduces average power per farm area even though turbine pads occupy
little land. WindEurope estimates 2024 fleet capacity factors of 23% onshore and
35% offshore; these are Europe-wide fleet values. Austria generated 8.578 TWh
from wind in 2025. Dividing by year-end capacity of 4,221 MW gives a rough 23.2%
capacity-factor proxy, not a time-weighted official factor. A corrected US sample
reports 0.90 W/m² wind and 5.7 W/m² solar under its own footprint conventions.
For Horns Rev, 158 MW over 20 km² times the European offshore fleet factor gives
2.765 W/m², a scenario rather than a measured site result.
#unit-ledger[Europe 2024 fleet: 23% onshore and 35% offshore capacity factor; Austria 2025 year-end proxy 23.2%; Horns Rev scenario 2.765 W/m².]

The area budget below uses explicit delivered-density scenarios of 0.5 W/m²
(biofuel), 2 W/m² (wind), and 10–20 W/m² (solar), scaled to Austria's 2025 final
energy per person. It omits storage, grid changes, crop rotation, ecological
set-asides and changes in the useful services supplied.

In 2023, FAO/WDI reports 0.1717 ha of arable land per person worldwide and
0.1447 ha in Austria. The broader PBL-HYDE cropland series gives 0.2027 and
0.1580 ha/person, respectively. The definitions and source methods differ;
these figures are not additive. They show why a land-intensive energy crop
must be compared with food production and ecosystems on the same area basis.
#unit-ledger[2023 land availability: FAO arable land 0.1717 ha/person (world), 0.1447 (Austria); PBL-HYDE cropland 0.2027 (world), 0.1580 (Austria). FAO database CC BY 4.0; OWID processing CC BY 4.0; PBL source licence not separately asserted.]
#graphic("land-power-density", [Gross corn-ethanol energy per crop area compared with stated wind and solar average-power-density scenarios.], caption: [USDA NASS 2024 corn yield; US DOE ethanol output and lower heating value; wind/solar bars are stated scenarios. Gross ethanol energy excludes farm and distillery inputs and coproduct allocation.])

The illustrative US corn-to-ethanol chain produces about 0.317 W/m² of gross
fuel energy. Matching Austria's 2025 final energy would then require 0.01146
km²/person, or about 105,512 km² nationally, 126% of Austria's land area. At
equal delivered output per area, 2 W/m² wind is 6.31 times denser; 10–20 W/m²
solar is 31.6–63.1 times denser. This is an energy-only illustration, not a
life-cycle result or a forecast for Austrian crops. Biofuel may use residues or
non-food land, while dedicated food crops can compete for fertile land, water
and inputs; coproducts partly change that accounting.

#unit-ledger[$A/N=p/q_A$; corn-ethanol gross $q_A=0.317$ W/m²; Austria final-energy area = 0.01146 km²/person.]
#knowledge-check((
  (question: [What does doubling delivered power density do at fixed demand?], answer: [It halves the required area.]),
  (question: [Can rooftop density and a whole wind-farm density be compared without their area definitions?], answer: [No; their land denominators differ.]),
))
#exam(7, [How much W/m^2 can various energy sources produce? How would you compute it?])
#exam(8, [Discuss whether renewables compete with arable land for food production. What about biofuels?])

#section-title[Solar learning and energy choices] <solar-learning>
The supplied 9 October 2026 sourcebook's OWID module-price extract falls from
USD 36.43/Wp in 1980 to USD 0.267/Wp in 2024, in constant 2025 dollars. The
later series uses IRENA's European pvXchange module benchmark; it is module
price, not installed system cost. The extract uses approximate CPI rebasing
and may differ from later source revisions. For context, year-end solar PV
capacity rose from 293 GW worldwide in 2016
to 2,383 GW in 2025, and from 1.10 to 10.30 GW in Austria.

#graphic("solar-storage-capex", [Separate logarithmic axes for solar module price in constant 2025 USD/W and lithium-ion cell, pack and installed four-hour battery-system prices in USD/kWh of capacity. Modelled intervals are dashed.], caption: [Original plot from the supplied sourcebook's component table: #link("https://ourworldindata.org/grapher/solar-pv-prices")[OWID modules], #link("https://ourworldindata.org/grapher/price-of-lithium-ion-battery-cells")[OWID cells], #link("https://about.bnef.com/insights/clean-transport/lithium-ion-battery-pack-prices-fall-to-108-per-kilowatt-hour-despite-rising-metal-prices-bloombergnef/")[BNEF packs], #link("https://www.irena.org/Publications/2026/Jul/Renewable-Power-Generation-Costs-in-2025")[IRENA installed storage]. Capacity totals in the text: IRENA Renewable Capacity Statistics 2026. Provider data retain their terms; no provider chart is reproduced.])

Cells, packs and installed storage systems have different cost boundaries.
The sourcebook's 2025 benchmarks are USD 108/kWh for packs across uses and
USD 140/kWh for installed four-hour storage. The 2010 installed-storage
figure is a published regression estimate, as identified in IRENA's 2024
report, Figure 9.2; it is marked as a model in the figure. Intermediate
installed-storage values are sourcebook reconstructions.

#graphic("electricity-cost-history", [Logarithmic generation-cost histories for PV, PV plus daily storage, wind, gas, coal and new nuclear, 1980–2035. Benchmarks, historical reconstructions and future scenarios have different line styles. Electricity costs use 2025 US cents per kWh; battery-capacity prices are not on this axis.], caption: [Original plot of the supplied sourcebook's annual table. Global renewables: #link("https://www.irena.org/Publications/2026/Jul/Renewable-Power-Generation-Costs-in-2025")[IRENA 2025] and earlier extract. US conventional generation: #link("https://www.lazard.com/media/y5ldnkil/lazards-lcoeplus-april-2023.pdf")[Lazard 2023] and #link("https://www.lazard.com/media/uounhon4/lazards-lcoeplus-june-2025.pdf")[2025]. Solar and daily-storage 2030–2035 curves are author scenarios; #link("https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2026/May/IRENA_TEC_24-7_renewables_2026.pdf")[IRENA] supplies future capital-cost ratios. Wind and nuclear relative cost-change scenarios use #link("https://atb.nlr.gov/electricity/2025/data")[2025 ATB Moderate R&D] inputs (large nuclear: 60-year cost recovery; Class 4 onshore wind: 30 years). The dimensionless cost ratios multiply the existing 2025 benchmarks, joining both historical curves continuously. ATB nuclear estimates begin in 2030: the anchored nuclear scenario assumes constant real cost from 2025 to 2030, then applies the ATB 2035/2030 ratio. These are anchored scenarios rather than ATB absolute LCOE forecasts. Gas and coal show an explicitly assumed constant-2025-real-cost scenario, not a published fuel-price forecast.])

The levelised cost of electricity (LCOE) is discounted lifetime cost divided by discounted electricity
output. It differs from a retail tariff and from the cost of a complete
reliable electricity system. The IRENA curves are global new-project
benchmarks, while Lazard represents US new-build estimates. Lazard's 2025
coal and nuclear ranges reuse inflation-adjusted earlier estimates; nuclear
uses then-estimated Vogtle costs. Pre-2010 PV LCOE is backcast from module
prices; the early conventional curves are hypothetical reconstructions.
These differences prevent treating the figure as one site's bidding comparison.

For daily shifting, let $f$ be the fraction of delivered energy discharged
from storage, $eta$ the round-trip efficiency, $B$ the assumed usable
installed battery cost in USD/kWh-capacity, and $u$ the full discharge cycles
per day. With real discount rate $r$, lifetime $T$ in years and annual
maintenance fraction $m$, the sourcebook model is
$
  "CRF"(r,T) = r / (1-(1+r)^(-T)), quad
  c_"daily" = c_"PV" (1-f+f/eta)
    + (100 f B ("CRF"(r,T)+m))/(365 u).
$
Costs $c$ are in US cents per kWh delivered. The factor 100 converts dollars
to cents. The Li-ion scenario uses $f=0.60$, $eta=0.85$, $u=0.95$,
$r=0.07$, $T=15$ years and $m=0.01$. Treating the installed-system benchmark
as usable capacity is a simplifying assumption. At $c_"PV"=4.4$ and
$B=140$, the result is 7.77 US cents/kWh. Before 2010 the curve uses assumed
lead-acid systems ($eta=0.75$, $T=5$); later it selects the cheaper of the
two models. It omits seasonal storage, augmentation and wider balancing costs.
The 2030/2035 PV values 3.33/3.10 and daily-storage values 5.92/5.36 are
sourcebook scenarios, not official forecasts of global LCOE.

IRENA's separate Nevada hourly-dispatch example costs 11.32 US cents/kWh in
2025 for 95% of #emph[annual demand energy], with solar overbuild and batteries.
It is a retrospective model at a selected site, not the global daily-shifting
case and not guaranteed firm supply or 95% of hours fully served. Its 2035
5.9-cent value is a projection. The oil-fuel proxy and existing French nuclear
fleet costs are retained in the source material but excluded from this
new-build LCOE comparison.

Rapid cost decline changes the comparison set: a future technology must compete
with a system whose manufacturing scale and installed capacity are changing.
It does not establish that solar alone can supply every service or that a
future fusion plant will be economical. Compare delivered service, timing,
storage, land and total system cost on matching boundaries.
#unit-ledger[USD/Wp is a module cost in constant 2025 USD; installed capacity is year-end nameplate PV in GW.]
#exam(9, [Discuss the ongoing price-drop in solar, and what it means for other alternatives, such as future fusion energy.])

#section-title[Fission and deployment rates] <energy-deployment>
In an illustrative once-through light-water-reactor model, one GW(e) at full
power for 365 days burns 24.58 t enriched uranium. With product assay 4.5%,
natural feed 0.711% and tails 0.22%, enrichment mass balance gives about
214.3 t natural uranium feed and 189.7 t tails. The burnup model assumes
45 GW·day/t and 33% thermal-to-electric conversion; fuel burn is not initial
core inventory.

The 2025 IAEA reactor table covers 1954–2024: maximum grid connections were
33 reactors/year in 1984 and 1985, with a peak 31.129 GW(e) connected in 1985;
construction starts peaked at 43/year in 1976. A 30-year scenario supplying
Austria's 2025 final energy with 1 GW(e), 90%-capacity-factor units requires
1.24 reactors/year. These historical maxima are context, not a deployment
forecast.

#figure(image("/slides/photos/goesgen-nuclear-plant.jpg", width: 100%, alt: "Gösgen nuclear power plant in Switzerland, a large pressurized-water fission plant."), caption: [Gösgen nuclear power plant · 1,010 MW(e) net · GabrielleMerk, Wikimedia Commons · CC BY 4.0.])
#unit-ledger[$M_E=P t/(eta B)$; enriched uranium 24.58 t/(GW(e) year); natural uranium 214.3 t/(GW(e) year); plant counts assume 90% capacity factor.]

#section-title[Perceived and quantitative environmental risk] <environmental-risk>
U.S. model estimates put free-ranging-cat bird mortality at 1.3–4.0 billion per
year, building collisions at 365–988 million (median 599 million), vehicle
collisions at 89–340 million, power-line collision plus electrocution at
12–64 million, and monopole wind-turbine collisions at 140,438–327,586. These
studies use different years, methods, geographic scopes and uncertainty
intervals. The estimates are not a single-year census and must not be added as
though they share one model. A Swedish Environmental Protection Agency review
reported a median 6.5 bird deaths per turbine per year across the European
facilities it reviewed; that is a site-level rate, not a Europe-wide total.

#graphic("bird-mortality", [Published annual United States bird-mortality ranges for cats, buildings, vehicles, power lines and monopole wind turbines; logarithmic horizontal scale.], caption: [Loss et al. 2013/2014, with the corrected cat interval; source numbers re-plotted independently. Naturvårdsverket Vindval Report 6511 reports a separate European rate of median 6.5 birds/turbine/year.])

The 2021 OWID energy table estimates deaths per TWh of electricity from air
pollution and accidents: coal 24.62, gas 2.821, oil 18.43, nuclear 0.030,
wind 0.035 and solar 0.019. These values combine evidence with differing
periods and study boundaries. They are useful for scale and risk perception,
but are not a fully harmonized contemporary life-cycle comparison.
#graphic("energy-deaths-twh", [OWID processed 2021 deaths per TWh of electricity estimates for several energy sources, logarithmic scale.], caption: [Markandya & Wilkinson (2007), Sovacool et al. (2016), UNSCEAR (2008/2018), compiled by Our World in Data under CC BY 4.0; heterogeneous methods and boundaries.])
#unit-ledger[Bird estimates are annual U.S. deaths except the explicitly marked European birds/turbine/year median; energy-health estimates are deaths/TWh electricity, 2021 source compilation.]
#knowledge-check((
  (question: [Why should bird-mortality ranges not simply be summed?], answer: [They use different periods, scopes and estimation methods, and may not be mutually exclusive.]),
  (question: [What is the denominator in the energy-risk plot?], answer: [One terawatt-hour of electricity produced.]),
))
#exam(10, [Discuss the question of perceived and quantitative risk for the environment from various aspects of civilization (e.g. birds vs cats/wind turbines).])

#section-title[Lifecycle greenhouse emissions] <lifecycle-emissions>
No energy source has zero lifecycle greenhouse emissions in every technology
and study boundary. Mining and processing, construction materials, transport,
operation and decommissioning contribute even when a plant has no combustion
stack. The NREL harmonized literature dataset reports lifecycle medians of
1,001 g CO₂-eq/kWh for coal, 450 for natural-gas combined cycle, 43.4 for
photovoltaics, 13 for wind and 13 for light-water nuclear. The reported ranges
overlap to different degrees; hydropower and biomass have broad distributions.
Some sources are low-carbon over their lifecycle, which is different from
claiming they are CO₂-free.

#graphic("lifecycle-emissions", [NREL literature distributions of lifecycle greenhouse-gas emissions by electricity technology, with study minimum-to-maximum range and median marker on a logarithmic scale.], caption: [NREL Life Cycle Emissions Factors for Electricity Generation Technologies, dataset updated 2026-05-22; DOE/NREL/ALLIANCE credit under its full-notice data terms; no CC licence asserted. Original plot, g CO₂-eq/kWh electricity.])
#unit-ledger[Lifecycle emission factor: g CO₂-equivalent per kWh of electricity; values are study ranges and medians, not universal constants.]
#knowledge-check((
  (question: [Why are wind and nuclear described as low-carbon rather than CO₂-free?], answer: [Lifecycle construction, materials, fuel and end-of-life stages can emit greenhouse gases.]),
))
#exam(11, [Are there CO/2-free energy sources? Why/why not?])

#pagebreak()
#section-title[From energy context to fusion physics] <fusion-bridge>
The D–T reaction releases 17.6 MeV per reaction. Dividing one GW(fusion) year
by that energy gives 93.4 kg of burned deuterium-plus-tritium fuel. Supplying the
same thermal energy with coal at an assumed 24 MJ/kg requires about 1.31 million
kg. Seawater contains a very large theoretical deuterium inventory, and USGS
reports 37 Mt of lithium reserves, but inventories are not recoverable reactor
fuel: extraction, isotope separation, tritium breeding and materials all matter.

Under the stated ocean model, the total seawater deuterium inventory is
equivalent to 5.60 × 10⁶ kg D per person at the 2025 world population. The
37 Mt of reported lithium reserves correspond to 4.50 kg Li/person. Both are
inventory comparisons: the deuterium is dispersed in seawater, and lithium
reserves are not all Li-6 or recoverable reactor fuel.

Fusion therefore begins as an energy-density and reaction-rate problem, then
becomes a plasma power-balance and engineering problem. Plasma gain compares
fusion power with plasma heating power. Net electric gain must also include
thermal conversion, recirculating power, plant availability and all auxiliary
loads. Later chapters derive those boundaries from first principles.

#figure(image("/slides/photos/jet-vessel-interior.jpg", width: 100%, alt: "Interior of the JET fusion-device vacuum vessel before operation."), caption: [JET vessel interior · EUROfusion · Wikimedia Commons · CC BY 4.0.])

#let fusion-budget = json("/derivations/build/plotdata/13-fusion-resources.json")
#let budget-round(value, digits: 0) = calc.round(value, digits: digits)

== Fusion fuel and blanket resources

The earlier reserve-lifetime bars divide each fuel stock by its own current
world production, held constant. Oil, gas, coal and low-cost uranium use 2024
production; broad identified uranium resources use 2023 production. They do
not assume that each fuel supplies the entire world energy demand. They also
omit demand growth, discoveries and changes in economic recoverability.

For the fusion estimate, choose a different, explicit denominator. EIA's
2024 world primary-energy total is
#budget-round(fusion-budget.world_primary_EJ_year, digits: 1) EJ/year. Here fusion
electricity is assumed to match that numerical energy total, rather than
today's much smaller electricity consumption. This is an accounting stress
test, not a forecast of useful-energy demand or a primary-energy conversion:
electrification would change the energy required to supply the same services.
The EIA series incompletely covers traditional biomass.

Let $R$ denote a fuel stock in kg, $q_e$ its assumed electricity yield in
kWh/kg, and $dot(E)_e$ the chosen annual electricity demand. Then
$ dot(m) = dot(E)_e/q_e, quad T = R/dot(m) = (R q_e)/dot(E)_e. $
Using #link("https://www.withouthotair.com/c24/page_172.shtml")[MacKay, chapter 24]
and his #link("https://www.withouthotair.com/c24/page_176.shtml")[notes on p. 176],
take $q_e = 2.3 times 10^6$ kWh/kg of natural lithium.
This is a fuel-utilization and electricity-yield *assumption*, not a universal
constant. It must not be combined with a second thermal efficiency factor.
The yield depends on lithium-isotope utilization, blanket neutron balance,
plant conversion and recirculating loads; it does not assume complete use of
every lithium-7 nucleus. A design-specific calculation would replace it.

The chosen demand is
#budget-round(fusion-budget.world_primary_EJ_year*1e18/3.6e6/1e12, digits: 1)
× 10¹² kWh/year. Thus the natural-lithium rate is
#budget-round(fusion-budget.fuel.at(0).consumption_t_year/1000, digits: 1)
kt/year, giving
$ T_"Li" =
  (37 times 10^9 "kg" times 2.3 times 10^6 "kWh/kg") /
  (#budget-round(fusion-budget.world_primary_EJ_year*1e18/3.6e6/1e12, digits: 1) times 10^12 "kWh/year")
  approx #budget-round(fusion-budget.fuel.at(0).static_years) "years". $
All lithium reserves are hypothetically allocated to fusion; batteries and
other users, fuel-cycle losses, startup blanket inventory and demand growth
are omitted. Lifetime scales directly with yield and inversely with demand.
This scenario needs about
#budget-round(100*fusion-budget.fuel.at(0).consumption_t_year/290000) percent of
2025 reported lithium mine production, before other uses and blanket loading.

At 0.17 mg/L and the stated ocean volume, seawater contains about
#budget-round(fusion-budget.fuel.at(1).stock_kg/1e12) billion tonnes of lithium.
Its inventory bound is
#budget-round(fusion-budget.fuel.at(1).static_years/1e6, digits: 1) million years.
This is a dispersed inventory, not an economically recoverable reserve.
The independent D–T deuterium bound uses one D nucleus per 17.6 MeV and an
assumed 40 percent thermal-to-electric conversion, omitting breeding heat and
auxiliaries. It gives about
#budget-round(fusion-budget.fuel.at(2).static_years/1e9) billion years of
constant demand. Such an inventory ratio is not a physical forecast over that
time. D–T still needs lithium and bred tritium; these three bars are separate
fuel constraints, not energy supplies that can be added.

#graphic("fusion-resource-lifetimes", [Fuel inventory divided by constant annual requirement; logarithmic years axis. Lithium uses MacKay's natural-Li electric-yield scenario; deuterium uses D–T at 40 percent conversion and still needs lithium.], caption: [Original calculation from EIA 2024 world energy, USGS MCS 2026 Li reserves, NOAA ocean volume and NIST isotope data; MacKay ch. 24, pp. 172 and 176. Ocean quantities are inventories, not reserves.])

=== Is seawater lithium extraction realistic?

MacKay estimates 2.5 kWh(e)/g for extraction versus 2300 kWh(e)/g from fusion:
$ E_"extraction"/E_"fusion" = 2.5/2300 approx 0.0011 = 0.11 %. $
This supports energetic plausibility under his assumptions. It does not
establish commercial cost, materials durability, environmental acceptability
or an industrial extraction rate.
#link("https://doi.org/10.1039/D1EE00354B")[Li et al. (2021)] demonstrated
electrical membrane enrichment of actual Red Sea seawater. Their reported
76.34 kWh/kg electrical enrichment estimate is a laboratory process result,
not a full industrial life-cycle energy budget. No by-product credit is
needed for MacKay's illustrative energy-ratio calculation above.
Even with perfect recovery, the world-energy scenario must process at least
#budget-round(fusion-budget.seawater_minimum_km3_year) km³/year of seawater.
Incomplete capture increases this volume. Pumping and contacting water,
membrane or sorbent replacement, purification and isotope separation must
all be included in a practical supply-chain assessment.

=== Breeding blanket resources

Lead and beryllium are alternative neutron-multiplier choices, not materials
required by every blanket. Much of their inventory remains in the blanket.
Nuclear reactions transmute some atoms; recycling can recover only the
untransmuted material. Irradiation damage can require component replacement
well before that inventory is consumed.

Use the paired historical 1 GW net-electric HCLL and HCPB concepts in
#link("https://doi.org/10.1016/j.fusengdes.2010.11.040")[Bradshaw et al. (2011)]:
#let pb-budget = fusion-budget.blanket_materials.at(0)
#let be-budget = fusion-budget.blanket_materials.at(1)
#table(columns: (1fr, 1fr, 1fr),
  [Concept / multiplier], [Initial loading per plant], [Nuclear burn-up per full-power year],
  [HCLL / lead], [#budget-round(pb-budget.blanket_charge_t) t],
  [#budget-round(pb-budget.burnup_t_full_power_year, digits: 1) t],
  [HCPB / beryllium], [#budget-round(be-budget.blanket_charge_t) t],
  [#budget-round(be-budget.burnup_t_full_power_year, digits: 2) t],
)
These are internally matched historical concepts, not specifications for all
future fusion plants. Burn-up is about 0.076% of initial Pb loading and
0.158% of initial Be loading per full-power year. Neither blanket is consumed
in a few years. The fleet's large initial inventory is the main stock constraint.

Retain page 25's stress scenario: fusion electricity numerically equals
#budget-round(fusion-budget.world_primary_EJ_year) EJ/year of 2024 world
primary energy. This is not a useful-energy replacement forecast.
At an assumed #budget-round(100*fusion-budget.blanket_capacity_factor)% capacity factor,
the #budget-round(fusion-budget.electric_demand_GW) GW average output requires
#budget-round(fusion-budget.blanket_installed_units) of these 1 GW plants.
Initial loading scales with installed capacity; annual nuclear burn-up scales
with delivered energy, without a second capacity-factor penalty.

$ T = ("stock" - "startup loading") / ("annual nuclear burn-up") $

Assume ideal recovery of untransmuted material, constant demand, no competing
uses, no replacement or processing losses and no growth. Subtract the initial
fleet loading before assigning an operating lifetime. A stock below that
loading has no operating lifetime in this scenario.

#image("/derivations/build/fig/fusion-blanket-lifetimes.svg", width: 100%)

The fleet initially holds #budget-round(pb-budget.fleet_initial_t/1e6) Mt Pb
or #budget-round(be-budget.fleet_initial_t/1e6, digits: 1) Mt Be.
Annual transmutation consumes approximately
#budget-round(pb-budget.fleet_burnup_t_year/1000, digits: 1) kt Pb or
#budget-round(be-budget.fleet_burnup_t_year/1000, digits: 2) kt Be.
USGS MCS 2026 reports
#link("https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-lead.pdf")[95 Mt Pb reserves and more than 2 Gt identified resources].
After startup loading, those stocks give approximately
#budget-round(fusion-budget.blanket_lifetimes.at(0).static_years) years
or more than #budget-round(fusion-budget.blanket_lifetimes.at(1).static_years)
years respectively, under ideal recovery.
Resources are broader than economically recoverable reserves; the two figures
are alternatives, not quantities to add. The reserves result is especially
sensitive to the assumed plant inventory and capacity factor because startup
already takes most of the 95 Mt.

For beryllium,
#link("https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-beryllium.pdf")[USGS reports more than 100 kt identified resources; world reserves are unavailable].
The 100 kt reference cannot load this hypothetical fleet, so no Be lifetime
is assigned. This is a lower-bound reference, not evidence that the world
contains only 100 kt or that the actual total is below the startup requirement.
Current mine production is 4.5 Mt/year Pb and 430 t/year Be, including other
users' demand; building this fleet would require major supply expansion.
Replacing damaged blankets adds demand if material recovery is incomplete.
Recycling cannot restore atoms changed by nuclear reactions.

Other constraints are startup tritium and breeding margin, lithium-6 isotope
separation, tungsten and low-activation structural-material replacement,
magnet conductors and helium recovery. These are component- and design-specific
supply questions; a single geological lifetime is not justified without a bill
of materials, lifetime and recovery assumptions.
For example,
#link("https://research.tue.nl/en/publications/a-theoretical-study-on-the-suitable-enrichment-methods-for-lithiu/")[Paine et al. (2024)]
estimate 46.4 t lithium at 60 percent Li-6 for one HCPB design and 152.8 t at
90 percent for one WCLL design. Large initial enriched inventories can matter
even when the annual lithium burn rate is small.


#unit-ledger[$Q=17.6$ MeV/reaction; burned D + T = 93.4 kg/(GW(fusion) year); coal = 1.314 million kg at 24 MJ/kg; theoretical seawater D = 5.60 × 10⁶ kg/person; Li reserves = 4.50 kg/person (2025).]
#knowledge-check((
  (question: [What distinguishes plasma gain from net electric gain?], answer: [Their input/output boundaries and included conversion and recirculating losses differ.]),
  (question: [What physics connects this energy opening to fusion?], answer: [Reaction energy, reaction rates, plasma heating and confinement power balance.]),
))

#section-title[Energy to 2100] <fusion-outlook>

#figure(image("/derivations/build/fig/energy-outlook.svg", width: 100%),
  caption: [World primary-energy shares: IPCC AR6 scenario medians, with
  10–90% ranges for wind plus solar and bioenergy; observed 2024 markers;
  published MIT and EUROfusion fusion timelines scaled to primary demand.
  The short PV construction-rate guide is illustrative.])

=== A range of energy futures

The #link("https://doi.org/10.5281/zenodo.7197970")[IPCC AR6 Scenarios
Database, version 1.1] provides a multi-model comparison. The figure selects
vetted World pathways in categories C1 (1.5°C with no or limited overshoot)
and C3 (below 2°C with probability greater than 67%). The numerical extract
requires total primary energy and coal, oil, gas, biomass, nuclear, solar
and wind at every decade from 2020 to 2100. Of 360 complete pathways, four
IMAGE pathways are excluded because their components exceed the total beyond
a 0.01 percent reporting tolerance. The retained 356 pathways span ten
model families. No pathway is excluded because of its resulting technology shares.

For every pathway, compute source energy divided by that same pathway's
total, then calculate the median and percentiles across pathways. The median
total demand is calculated separately. The 2100 median shares are about
44 percent wind plus solar, 23 percent fossils, 21 percent bioenergy,
3 percent fission and 6 percent other energy. The latter is the residual,
mainly hydropower and geothermal, together with other reported sources.
The displayed 10–90 percent ranges are approximately 22–66 percent for wind
plus solar and 11–33 percent for bioenergy. These ranges describe the
selected scenario literature; they are not probabilities. Models contribute
unequal numbers of pathways, and component-wise medians need not add to
100 percent. The figure therefore uses lines rather than a stacked mix.

The gray upper fossil line compares the median fossil share in three
NGFS phase-2 current-policy pathways (GCAM, MESSAGE and REMIND), also retained
in AR6. Its policy assumptions date to 2021; it is a contrasting policy case,
not a forecast updated to 2026.

The #link("https://data.ene.iiasa.ac.at/ar6/static/About.html")[IPCC illustrative
pathways] show how strongly the technology mix depends on the chosen strategy.
The following are original reported 2100 values, rounded here:

#table(columns: (2.2fr, 1fr, 1fr, 1fr),
  [Pathway], [Total (EJ/year)], [Bioenergy (EJ/year)], [Wind + solar share],
  [Renewables-led, REMIND], [737], [100], [78%],
  [Low demand, MESSAGE], [326], [69], [64%],
  [High overshoot/removal, COFFEE], [995], [406], [36%],
)

The renewables-led pathway is `DeepElec_SSP2_ HighRE_Budg900`; low demand is
`LowEnergyDemand_1.3_IPCC`; the removal pathway is `EN_NPi2020_400f_lowBECCS`.
The last belongs to C2 (1.5°C after high overshoot) and is shown here for
comparison, outside the plotted C1/C3 ensemble. Its name does not imply low
total bioenergy. These are conditional strategies, not interchangeable forecasts.

=== What the biomass-heavy scenario required

The superseded #link("https://github.com/JGCRI/ssp-data/tree/b3dfbdf34b63a48db97373c27fe2c994855ea5f4")[GCAM4 SSP2-2.6 pathway]
reaches 391.7 EJ/year biomass out of 927.3 EJ/year primary energy in 2100,
or 42.2 percent. Its detailed outputs include:

#table(columns: (2.5fr, 1fr),
  [2100 model output], [Value],
  [Land for energy crops], [1.085 billion hectares],
  [Biomass used with carbon capture and storage], [230 EJ/year],
  [CO₂ captured and stored from biomass], [23.5 Gt/year],
  [Carbon price, in 2005 dollars], [1853 USD/t CO₂],
)

Thus this pathway requires a vast land allocation and a very large carbon
capture and storage industry. The model values biomass both as an energy
source and as a means of removing atmospheric CO₂: plants take up carbon,
and some of that carbon is stored underground after conversion. Whether the
whole chain actually removes CO₂ depends on land-use change, cultivation,
processing, transport, capture and durable storage. The
#link("https://jgcri.github.io/gcam-doc/ssp.html")[GCAM SSP documentation]
also explains that the original scenarios predate a later net-negative-emissions
constraint, with consequences especially for the 2.6 W/m² pathways.

Solar photovoltaics generate much more electricity per unit of suitable land
than dedicated energy crops followed by electricity generation. The carbon
removal credit does not improve photosynthetic conversion efficiency.
Cost optimization under an emissions constraint can nevertheless favor
biomass because it can also supply storable fuels and negative emissions.
That is a different objective from maximizing electricity per square meter.
The literature explicitly identifies large-scale bioenergy with carbon
capture as a potential source of pressure on land, water, biodiversity and
nutrient cycles; see
#link("https://doi.org/10.1038/s41558-017-0064-y")[Heck et al. (2018)].
A large modeled share is not evidence that those sustainability constraints
have been resolved.

Primary-energy accounting matters as well. Combustible biomass is counted
before conversion losses, whereas the direct-equivalent convention counts
wind, solar and nuclear electricity at output. A 42 percent primary share
therefore does not mean 42 percent of delivered electricity or useful energy.

=== Published fusion timelines

The #link("https://energy.mit.edu/research/publications-reports/role-fusion-energy-decarbonized-electricity-system")[MIT fusion study (2024)]
uses the global EPPA model with accelerated climate action and assumed
commercial availability in 2035. Four US overnight capital-cost cases in
2050 span 2800–11,300 USD2021/kW. The base case uses 8000 USD/kW in 2050
and approximately 4300 USD/kW in 2100. The report gives 2 TWh fusion
generation in 2035 and 375 TWh in 2050 for that case. Its fusion share of
electricity reaches 15 percent in 2075 and 27 percent in 2100; the cost
sensitivities reach 10–50 percent in 2100. These are electricity shares,
not all-energy shares.

The figure uses actual five-year vertices of the four generation curves
in Fig. 4.4b, printed p. 43 (PDF p. 48), extracted from vector coordinates
and rounded to 100 TWh. The two exact base-case values from the report text
replace the poorly resolved early vertices. Tiny values below approximately
100 TWh in the other curves are unresolved. Curves are conditional on the
report's renewable-integration costs, resource availability and regional
restrictions on fission.

#link("https://agenda.ciemat.es/event/4431/contributions/6116/attachments/4194/6673/Carlos_Mantilla_ESSRI_2024_SPS1.pdf")[Mantilla et al., ESSRI 2024],
provides a second model's dated fusion results. Its EUROfusion TIMES S02
case assumes availability in 2035, fast deployment linked to tritium supply,
reference costs and restricted variable renewables. The poster explicitly
describes its fusion costs as desired targets rather than estimates.
Its dated global mix bars give approximately 0, 0.5, 7.5 and 29 PWh/year
fusion output in 2030, 2050, 2070 and 2100. They are independently digitized
to approximately 0.5 PWh resolution; dashed connections join those reported
dates without inventing intermediate model outputs. The case reaches
22 percent of electricity in 2100; late availability, slow deployment and
unrestricted wind and solar produce much smaller contributions.

The distinct star retains the newer
#link("https://doi.org/10.1016/j.esr.2026.102326")[Mantilla et al. (2026)]
favorable result: 21 percent of approximately 140 PWh/year electricity,
or 105.84 EJ/year fusion output. This requires commercialisation by 2040,
rapid fleet growth and sufficient tritium, first-fleet cost at most
7200 USD/kW with 10 percent learning, and wind/solar limited to 75 percent
in each model timeslice. Conservative cases yield only a few percent.
The verified 2026 endpoint is not used to invent a 2026 trajectory.

To compare on the requested all-energy axis, convert each fusion output:
$E_"fusion" = G_"fusion" times 0.0036 "EJ/TWh", quad
s_"fusion" = E_"fusion" / E_"primary, AR6 median".$
The same year-specific AR6 median denominator is used for both fusion models.
In 2100 this denominator is approximately 882 EJ/year: the MIT cost cases
scale to approximately 3–18 percent, its base case to 10 percent, and the
favorable EUROfusion cases to approximately 12 percent.
*These are explicit cross-model scalings, not all-energy shares published
by the fusion studies or a combined energy-system run.*
They do not establish which sources fusion would displace.

A complementary #link("https://doi.org/10.1016/j.esr.2023.101144")[EUROfusion TIMES study by Lerede et al. (2023)]
compares ARC and DEMO concepts under three socioeconomic storylines. It
finds fusion concentrated in regions with growing electricity demand,
with no contribution to the transition in Europe and the United States
in its studied cases. This differs from the MIT regional result and
illustrates the sensitivity to competing technologies, reactor concepts
and deployment constraints. All these studies assume that a commercial
fusion technology becomes available; they do not estimate the probability
of achieving that technical milestone.

=== Observations and recent solar growth

The observed 2024 mix uses the revised
#link("https://iea.blob.core.windows.net/assets/df903e1c-49c6-4757-8cbf-6fbcfe7611a0/GlobalEnergyReview2026.pdf")[IEA Global Energy Review 2026, p. 44]:
646 EJ total, including 519 EJ fossil fuels, 31 EJ nuclear and 96 EJ
renewables. Hollow circles show these three aggregates; the renewables
point is not a separate component to add to the curves. IEA counts nuclear
reactor heat, while the IPCC direct-equivalent convention counts nuclear
electricity. The observations and scenario curves are not spliced.

#link("https://www.iea.org/reports/global-energy-review-2026/global-trends")[IEA]
reports nearly 2700 TWh solar PV output in 2025, approximately 600 TWh
above 2024 and more than twice the 2022 output. Rounded 2100/2700 TWh
values divided by matching IEA totals of 646/655 EJ give 1.17/1.48 percent.
The short orange guide holds the 2025
#link("https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2026/Mar/IRENA_DAT_RE_capacity_statistics_2026.pdf")[IRENA]
net addition rate, 510.349 GW/year, through 2035. At an assumed 15 percent
capacity factor, each added annual cohort contributes approximately
671 TWh/year, or 2.41 EJ/year, for a full operating year. The guide assumes
no retirements; demand is anchored to IEA's 655 EJ in 2025 and follows
the relative AR6 ensemble median demand thereafter, interpolated between
decades. It is an illustration of constant construction, not a model update
or an exponential solar projection to 2100.


]
