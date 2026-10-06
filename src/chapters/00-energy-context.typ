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
#page-title(number: 0)[Energy context] <energy-context>
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

Rosling's four income levels describe household income or consumption per
person per day in 2011 purchasing-power-parity dollars: below 2, 2–8, 8–32 and
above 32. Gapminder's rounded 2017 estimate places about 0.75, 3.3, 2.5 and
0.9 billion people in Levels 1–4. Its estimate uses a 2013 household-survey
base extended by Gapminder; it is a dated scale comparison, not a current
survey or precise census.
#graphic("income-levels", [Approximate 2017 world population by Gapminder's four household-income levels, expressed in 2011 PPP dollars per person per day.], caption: [Gapminder Factfulness notes, p. 32; 2017 rounded estimates based on PovcalNet 2013 and Gapminder extensions; CC BY 4.0; original plot.])
#unit-ledger[Income bands: below 2, 2–8, 8–32 and above 32 2011 PPP USD/(person day); approximate 2017 population: 0.75, 3.3, 2.5 and 0.9 billion.]

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
#graphic("austria-sankey", [Austria 2025 energy balance from primary carriers through gross inland consumption, losses and final carriers to final-use sectors.], caption: [Statistics Austria preliminary balance rows 8–19, 2025; population-normalized to kWh/(person day). Reused with attribution under Statistics Austria's custom terms, not CC. Published carrier-to-sector cells are shown; primary inputs are not causally allocated to final sectors.])

The final carrier values are 28.91 kWh/(person day) oil products, 19.01
electricity, 17.96 renewable fuels and direct heat, 13.30 gas, 6.09 district
heat, 1.04 coal and 0.85 waste. The conversion pool is a net input-minus-output
balance; gross energy minus final energy also contains other uses and losses.
The carrier-by-sector CSV and Sankey node/link CSV retain the source cells and
the conservation check.

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
The OWID module-price splice falls from USD 132.38/Wp in 1975 to USD 0.265/Wp
in 2024, in constant 2025 dollars. The later series uses IRENA's European
pvXchange module benchmark; it is module price, not installed system cost. The
same period saw year-end solar PV capacity rise from 293 GW worldwide in 2016
to 2,383 GW in 2025, and from 1.10 to 10.30 GW in Austria.

#graphic("pv-price-capacity", [Solar photovoltaic module prices and installed PV capacity for the world and Austria.], caption: [OWID compilation CC BY 4.0; Nemet, Farmer and Lafond; IRENA Renewable Power Generation Costs 2024 (© IRENA 2025; attributed reuse), pvXchange benchmark; IRENA Renewable Capacity Statistics 2026 (© IRENA 2026). Original plots.])

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
#unit-ledger[$Q=17.6$ MeV/reaction; burned D + T = 93.4 kg/(GW(fusion) year); coal = 1.314 million kg at 24 MJ/kg; theoretical seawater D = 5.60 × 10⁶ kg/person; Li reserves = 4.50 kg/person (2025).]
#knowledge-check((
  (question: [What distinguishes plasma gain from net electric gain?], answer: [Their input/output boundaries and included conversion and recirculating losses differ.]),
  (question: [What physics connects this energy opening to fusion?], answer: [Reaction energy, reaction rates, plasma heating and confinement power balance.]),
))
]
