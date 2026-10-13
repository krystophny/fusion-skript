// Fusion Physics live deck, script chapter 0 (energy context). LOOK deck: photos,
// measured data and results; the estimates are derived live on the tablet.
// Figures: slides/figures.py (deck) from derivations/build/plotdata.
#import "theme.typ": *
#show: deck.with(chapter: 0, title: [The big picture])

#let named(formula, name) = align(center)[#formula #v(5mm) #text(fill: muted, name)]

// Dollar Street: the same object at four income levels.
#let stove(file, country, income) = block(width: 100%, height: 100%, clip: true,
  image("/slides/photos/" + file, width: 100%, height: 100%, fit: "cover"))
#let stove-page() = page(margin: 0mm, fill: rgb("#111418"), foreground: {
  place(top + right, dx: -4mm, dy: 3mm, block(inset: 1.5mm, fill: black, text(size: 8pt, fill: white)[
    Dollar Street, Gapminder: Z. Miller (Haiti, Bolivia), L. Carvalho (Brazil), O. Havana (Spain); CC BY 4.0]))
  place(top + left, dx: 4mm, dy: 12mm, block(inset: 1.5mm, fill: black, text(size: small-size, fill: white)[
    Monthly income: PPP US dollars per equivalent adult · Dollar Street]))
})[
  #present-page(background: "dark", title: "Cooking at four income levels")
  #let cell(file, country, income) = block(width: 100%, height: 100%, {
    image("/slides/photos/" + file, width: 100%, height: 100%, fit: "cover")
    place(bottom + left, dx: 4mm, dy: -4mm, block(fill: rgb("#111418cc"), inset: (x: 3mm, y: 2mm),
      text(fill: white, size: 18pt)[#country #h(0.6em) #text(fill: rgb("#F2A33A"))[#income \$]]))
  })
  #grid(columns: (1fr, 1fr), rows: (1fr, 1fr), gutter: 1.5mm,
    cell("dollarstreet-stove-5d4bf44ccf0b3a0f3f35b67a.jpg", [Haiti], [40]),
    cell("dollarstreet-stove-5d4bec73cf0b3a0f3f34df4c.jpg", [Bolivia], [180]),
    cell("dollarstreet-stove-5d4be196cf0b3a0f3f33b4c5.jpg", [Brazil], [685]),
    cell("dollarstreet-stove-5ec4f926f0611d7ddd7414e9.jpg", [Spain], [7639]),
  )
  #metadata("stoves") <photo-stoves>
]

#photo-page("earth-at-night-2016.jpg", [NASA Earth Observatory / Suomi NPP VIIRS, public domain], "photo-night")

#slide(section: "standards-living", title: [Energy and income])[
  #at(1, 12, y: -2mm, deck-fig("energy_gdp"))
]
#stove-page()
#let living-standards-sources = text(size: small-size, fill: muted)[
  World Bank PIP, Sep 2026 · 2021 PPP · fixed bands: 3 / 12 / 48 USD/(person day) \
  WDI electricity access ·
  EIA primary energy: traditional biomass incomplete
]

#slide(section: "standards-living", title: [Living standards · 1981])[
  #at(1, 9, y: 0mm, text(fill: muted)[World population · 4.52 billion])
  #at(1, 9, y: 12mm, image("/derivations/build/fig/income-levels-1981.svg",
    width: cols(9), alt: "1981 world population in four fixed income or consumption bands: 2.13, 1.26, 0.87 and 0.26 billion. Thresholds: 3, 12 and 48 in 2021 PPP USD per person per day; bars also show population shares. Same population axis in all three years."))
  #at(10, 3, y: 16mm, named(text(size: result-size, [—]),
    [Electricity access \ no series for 1981]))
  #at(10, 3, y: 72mm, named(text(size: result-size, [—]),
    [Primary energy \ comparison omitted]))
  #at(1, 12, y: 125mm, align(center,
    [Electricity access → lighting, refrigeration, cooking, heating?]))
  #at(1, 12, y: 144mm, living-standards-sources)
]

#slide(section: "standards-living", title: [Living standards · 2000])[
  #at(1, 9, y: 0mm, text(fill: muted)[World population · 6.16 billion])
  #at(1, 9, y: 12mm, image("/derivations/build/fig/income-levels-2000.svg",
    width: cols(9), alt: "2000 world population in four fixed income or consumption bands: 2.23, 2.50, 0.94 and 0.48 billion. Thresholds: 3, 12 and 48 in 2021 PPP USD per person per day; bars also show population shares. Same population axis in all three years."))
  #at(10, 3, y: 16mm, named(text(size: result-size, $78.2 %$),
    [Electricity access \ world]))
  #at(10, 3, y: 72mm, named(text(size: result-size, $approx 165 times$),
    [Primary energy \ per person \ Austria / Ethiopia]))
  #at(1, 12, y: 125mm, align(center,
    [Electricity access → lighting, refrigeration, cooking, heating?]))
  #at(1, 12, y: 144mm, living-standards-sources)
]

#slide(section: "standards-living", title: [Living standards · 2024])[
  #at(1, 9, y: 0mm, text(fill: muted)[World population · 8.14 billion])
  #at(1, 9, y: 12mm, image("/derivations/build/fig/income-levels-2024.svg",
    width: cols(9), alt: "2024 world population in four fixed income or consumption bands: 0.82, 3.96, 2.40 and 0.95 billion. Thresholds: 3, 12 and 48 in 2021 PPP USD per person per day; bars also show population shares. Same population axis in all three years."))
  #at(10, 3, y: 16mm, named(text(size: result-size, $91.9 %$),
    [Electricity access \ world]))
  #at(10, 3, y: 72mm, named(text(size: result-size, $approx 50 times$),
    [Primary energy \ per person \ Austria / Ethiopia]))
  #at(1, 12, y: 125mm, align(center,
    [Electricity access → lighting, refrigeration, cooking, heating?]))
  #at(1, 12, y: 144mm, living-standards-sources)
]

#slide(section: "energy-demand", title: [Micro and macro])[
  #at(1, 12, y: 0mm, deck-fig("micro_macro"))
  #at(1, 12, y: 128mm, align(center, text(fill: muted)[gross inland = primary; final = delivered to users; Austria 2025, Statistics Austria (preliminary)]))
]
#slide(section: "energy-demand", title: [Energy consumption and electricity])[
  #at(1, 12, y: 0mm, image("/derivations/build/fig/electricity-consumption.svg", width: cols(12),
    alt: "Austria 2025 preliminary, in kWh per person per day: primary energy 112.0, final energy 87.2, of which electricity 19.0, of which households 6.5. Electricity is 21.8% of final energy; households use 34.2% of electricity and 7.5% of final energy as electricity. Primary minus final comprises 6.4 net transformation loss, 12.0 energy-sector use plus transport losses, and 6.4 non-energy use. Separate assumed 40%-efficient thermal plant without heat recovery: 100 kWh heat gives 40 kWh electricity and 60 kWh rejected heat."))
  #at(1, 12, y: 140mm, text(size: small-size, fill: muted)[
    Sources: Statistics Austria,
    #link("https://www.statistik.at/fileadmin/pages/99/preliminaryEnergyBalancesforAustriaInTerajoule.ods")[2025 energy balance] (rows 8–13, 18),
    #link("https://www.statistik.at/en/statistics/population-and-society/population/population-stock/annual-average-population")[population]
    · EIA, #link("https://www.eia.gov/tools/faqs/faq.php?id=107&t=3")[thermal efficiency].
  ])
]
#slide(section: "energy-demand", title: [Austria's energy mix])[
  #at(1, 12, y: 0mm, deck-fig("austria_mix"))
  #at(1, 12, y: 128mm, align(center, text(fill: muted)[gross inland − conversion and grid losses − non-energy use = final energy; Statistics Austria 2025]))
]

#slide(section: "energy-resources", title: [How long do reserves last?])[
  #at(1, 12, y: 0mm, deck-fig("resources"))
  #at(1, 12, y: 120mm, align(center, [Each fuel at its current world production rate · constant]))
  #at(1, 12, y: 135mm, text(size: small-size, fill: muted)[BGR: 2024 production; broad uranium resources: 2023 production, IAEA/NEA Red Book. \
    No demand growth or reserve additions; each fuel retains its own present share.])
]
#slide(section: "energy-area", title: [Solar power per area in Graz])[
  #at(1, 12, y: 0mm, deck-fig("solar_chain"))
  #at(1, 12, y: 134mm, align(center, text(fill: muted)[PVGIS (EU JRC) for Graz; module at 20 % efficiency]))
]
#slide(section: "energy-area", title: [How big is a gigawatt?])[
  #at(1, 12, y: -4mm, deck-fig("true_scale"))
  #at(1, 12, y: 132mm, text(size: small-size, fill: muted)[Contains modified Copernicus Sentinel data 2025 (Sentinel-2A, 11 Sep 2025); Graz boundary: Stadt Graz, data.graz.gv.at, CC BY 4.0; park data: EnBW (2021), expected yield 180 GWh/a.])
]
#photo-page("wind-freilaenderalm.jpg", [Naturpuur, Wikimedia Commons, CC BY-SA 4.0], "photo-wind")
#slide(section: "energy-area", title: [Wind power per area])[
  #at(1, 12, y: 0mm, image("/slides/build/fig/capacity_factor.svg",
    width: cols(12), alt: "Illustrative output of a 1 MW turbine over one year. Twelve equal-duration intervals include zero, partial and full output, with an annual average of 0.23 MW. The dashed average-power line is 23 percent of the dotted rated-power line. These are constructed teaching values, not measured wind data."))
  #at(1, 12, y: 94mm, align(center, text(size: result-size,
    $"capacity factor" = P_"average"/P_"rated" = (0.23 "MW")/(1 "MW") = 23 %$)))
  #at(1, 8, y: 125mm, text(fill: muted)[Annual-average power \
    per wind-farm area])
  #at(9, 4, y: 125mm, align(center, text(size: result-size,
    $P_"average"/A approx 1 "to" 2 "W"/"m"^2$)))
]
#slide(section: "energy-area", title: [Land for Austria's energy])[
  #at(1, 12, y: 0mm, deck-fig("area_budget"))
]
#slide(section: "energy-area", title: [Food or fuel?])[
  #at(1, 12, y: 0mm, deck-fig("land_density"))
  #at(1, 12, y: 122mm, align(center, text(fill: muted)[FAO arable land via World Bank; USDA corn yield, DOE ethanol energy; wind and solar: stated scenarios]))
]
#slide(section: "solar-learning", title: [Solar panels and battery storage])[
  #at(1, 12, y: 0mm, image("/derivations/build/fig/solar-storage-capex.svg", width: cols(12),
    alt: "Two logarithmic hardware-price histories in constant 2025 dollars. Solar module prices in USD per watt fall from 36.43 in 1980 to 0.267 in 2024. A separate battery-capacity axis distinguishes lithium-ion cells, all-use packs and installed four-hour systems. Packs reach 108 USD per kWh capacity in 2025; installed systems reach 140. Dashed portions are modelled; the 2010 system estimate is a published reconstruction."))
  #at(1, 12, y: 134mm, text(size: small-size, fill: muted)[
    Sources: #link("https://ourworldindata.org/grapher/solar-pv-prices")[OWID module prices],
    #link("https://ourworldindata.org/grapher/price-of-lithium-ion-battery-cells")[cell prices],
    #link("https://about.bnef.com/insights/clean-transport/lithium-ion-battery-pack-prices-fall-to-108-per-kilowatt-hour-despite-rising-metal-prices-bloombergnef/")[BNEF packs],
    #link("https://www.irena.org/Publications/2026/Jul/Renewable-Power-Generation-Costs-in-2025")[IRENA installed storage]. \
    Supplied sourcebook, 9 Oct 2026 · constant 2025 USD · cell, pack and installed-system cost boundaries
  ])
]
#slide(section: "solar-learning", title: [Electricity generation costs])[
  #at(1, 12, y: 0mm, image("/derivations/build/fig/electricity-cost-history.svg", width: cols(12),
    alt: "Logarithmic electricity-cost history, 1980–2035. Solar PV and solar with daily storage retain the supplied IRENA-based scenarios. Wind follows ATB 2025 Moderate relative cost changes anchored at the 2025 global value, with a continuous dotted projection. Nuclear connects to the 2025 historical value, held constant to 2030 and then following the ATB Moderate relative cost change. This anchored scenario does not use ATB absolute cost estimates. Gas and coal use an explicitly assumed constant-2025-real-cost scenario. Solid lines: published historical benchmarks; dashed: models; dotted with open technology markers: future scenarios. Daily storage shifts 60 percent of delivered energy."))
]

#slide(section: "energy-deployment", title: [Fuel for one gigawatt-year])[
  #at(1, 12, y: 0mm, deck-fig("fuel_mass"))
  #at(1, 12, y: 126mm, align(center, text(fill: muted)[
    D + T → #super[4]He + n + 17.6 MeV; coal 24 MJ/kg; uranium once-through]))
]
#slide(section: "energy-deployment", title: [Annual capacity additions])[
  #at(1, 12, y: 0mm, image("build/fig/capacity_additions.svg", width: cols(12),
    alt: "World annual net nameplate capacity additions, 1981–2024, from EIA. Solar, wind and aggregated fossil fuels use the upper linear scale; hydro, nuclear, and biomass and waste use the lower linear scale. Negative values show net capacity reductions. Both panels show an Austria benchmark of 37.1 GW per year: a one-year build at 90 percent capacity factor matching Austria's 2025 final-energy demand."))
  #at(1, 12, y: 138mm, text(size: small-size, fill: muted)[
    EIA · annual changes in installed capacity · Austria: final energy, 90% capacity factor, 1-year build
  ])
]

#slide(section: "environmental-risk", title: [Perceived and measured risk])[
  #at(1, 12, y: 0mm, deck-fig("risk"))
  #at(1, 12, y: 130mm, align(center, text(fill: muted)[birds: Loss et al. (2013, 2014), USA; deaths: Markandya & Wilkinson (2007), Sovacool et al. (2016), via Our World in Data]))
]
#slide(section: "lifecycle-emissions", title: [Is anything CO#sub[2]-free?])[
  #at(1, 12, y: 0mm, deck-fig("lifecycle"))
  #at(1, 12, y: 130mm, align(center, text(fill: muted)[DOE/NREL/ALLIANCE Life Cycle Emissions Factors; no source is zero over its life cycle, some are low-carbon]))
]
#photo-page("jet-vessel-interior.jpg", [EUROfusion, Wikimedia Commons, CC BY 4.0], "photo-jet", section: "fusion-bridge")


#let fusion-budget = json("/derivations/build/plotdata/13-fusion-resources.json")
#let rounded(value, digits: 0) = calc.round(value, digits: digits)
#slide(section: "fusion-bridge", title: [Fusion fuel reserves])[
  #at(1, 12, y: 0mm, [World 2024 primary energy matched as electricity:
    #rounded(fusion-budget.world_primary_EJ_year) EJ/year])
  #at(1, 12, y: 15mm, align(center,
    $T = ("stock" times "electricity per kg") / ("electricity per year")$))
  #at(1, 12, y: 33mm, image("/derivations/build/fig/fusion-resource-lifetimes.svg", width: cols(12),
    alt: "Constant-demand inventory bounds: 37 Mt lithium reserves last about 479 years; ocean lithium about 2.9 million years, with MacKay's assumed 2300 kWh electric per gram of natural lithium. Ocean deuterium alone gives a 24-billion-year D-T bound at assumed 40 percent conversion, but still requires lithium and bred tritium. Logarithmic years axis; these are not forecasts or interchangeable fuel alternatives."))
  #at(1, 12, y: 120mm, [MacKay · extraction / fusion:
    #fusion-budget.extraction_kWh_g / #rounded(fusion-budget.lithium_electric_yield_kWh_g)
    ≈ #rounded(100*fusion-budget.extraction_fraction, digits: 1) %])
  #at(1, 12, y: 133mm, [Laboratory extraction demonstrated · industrial scale unproven])
  #at(1, 12, y: 145mm, text(size: small-size, fill: muted)[
    EIA 2024 · USGS 2026 · NOAA/NIST · MacKay ch. 24 · Li et al. 2021 (doi:10.1039/D1EE00354B) \
    Li yield: 2300 kWh(e)/g, assumed · D–T: 40% conversion, still needs Li · no growth, fuel losses or competing uses
  ])
]
#slide(section: "fusion-bridge", title: [Lead and beryllium])[
  #let lead = fusion-budget.blanket_materials.at(0)
  #let be = fusion-budget.blanket_materials.at(1)
  #at(1, 12, y: 0mm, [Fusion electricity:
    #rounded(fusion-budget.world_primary_EJ_year) EJ/year])
  #at(1, 12, y: 15mm, align(center,
    $T = ("stock" - "material in plants") / ("annual consumption")$))
  #at(1, 12, y: 33mm, image("/derivations/build/fig/fusion-blanket-lifetimes.svg", width: cols(12),
    alt: "Same constant world-energy benchmark and logarithmic years axis as page 25. Alternative lead- and beryllium-based 2011 conceptual 1 GW net-electric plants, at 90 percent capacity factor. Subtract initial fleet loading before depletion by nuclear transmutation. With ideal recovery, 95 Mt Pb reserves leave about 45 years; identified Pb resources above 2 Gt give more than 30353 years. Beryllium resources are reported only as above 100 kt; their total is unknown, so no lifetime is assigned. The illustrative fleet needs 2.7 Mt initially. USGS reports more than 100 kt Be resources, not a total resource ceiling or world reserve estimate."))
  #at(1, 12, y: 120mm, [Initially in all plants: #rounded(lead.fleet_initial_t/1e6) Mt lead
    or #rounded(be.fleet_initial_t/1e6, digits: 1) Mt beryllium])
  #at(1, 12, y: 145mm, text(size: small-size, fill: muted)[
    Bradshaw et al. 2011 · USGS 2026 · 639 EJ/year: world primary energy, 2024 \
    90% capacity factor · full recycling · constant demand · no other uses
  ])
]


#slide(section: "fusion-outlook", title: [Energy to 2100])[
  #at(1, 12, y: 0mm, image("/derivations/build/fig/energy-outlook.svg", width: cols(12),
    alt: "One plot of world primary-energy shares to 2100. IPCC AR6 C1/C3 multi-model medians; wind plus solar and bioenergy have 10–90 percent scenario ranges. A current-policy fossil comparison stays high. Hollow circles retain observed 2024 aggregates. Four actual MIT fusion cost-case timelines and the dated EUROfusion 2024 S02 trajectory are scaled to AR6 median primary demand; a star marks the favourable 2026 EUROfusion endpoint. A short orange guide holds 2025 PV additions through 2035." ))
  #at(1, 12, y: 145mm, text(size: small-size, fill: muted)[
    IPCC AR6: 356 pathways · current-policy assumptions: 2021 · IEA observed 2024 \
    Fusion: published output ÷ AR6 median primary demand · PV guide: 2025 build rate, 15% capacity factor
  ])
]

#credits-page((
  ("photo-night", [NASA Earth Observatory, Black Marble 2016, public domain], "science.nasa.gov/earth/earth-observatory/earth-at-night"),
  ("photo-stoves", [Dollar Street, Gapminder, CC BY 4.0], "gapminder.org/dollar-street"),
  ("photo-wind", [Naturpuur, Windpark Freiländeralm, CC BY-SA 4.0], "commons.wikimedia.org"),
  ("photo-jet", [EUROfusion, JET vessel internal view, CC BY 4.0], "commons.wikimedia.org/wiki/File:JET_vessel_internal_view.jpg"),
), [Data: EIA and USGS (public domain); World Bank WDI (CC BY 4.0); Statistics Austria; BGR; IAEA/NEA (CC BY 4.0); PVGIS (EU JRC); Our World in Data (CC BY 4.0); FAO; USDA; DOE/NREL/ALLIANCE; Loss et al.; Copernicus Sentinel-2; Stadt Graz OGD (CC BY 4.0). \ Plots and calculations: Christopher Albert, CC BY 4.0. Method after D. MacKay, Sustainable Energy — without the hot air (2009).])
