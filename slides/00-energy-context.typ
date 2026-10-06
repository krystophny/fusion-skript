// Fusion Physics live deck, script chapter 0 (energy context). LOOK deck: photos,
// measured data and results; the estimates are derived live on the tablet.
// Figures: slides/figures.py (deck) from derivations/build/plotdata.
#import "theme.typ": *
#show: deck.with(chapter: 0)

#let named(formula, name) = align(center)[#formula #v(5mm) #text(fill: muted, name)]

// Dollar Street: the same object at four income levels.
#let stove(file, country, income) = block(width: 100%, height: 100%, clip: true,
  image("/slides/photos/" + file, width: 100%, height: 100%, fit: "cover"))
#let stove-page() = page(margin: 0mm, fill: rgb("#111418"), foreground: {
  place(top + right, dx: -4mm, dy: 3mm, block(inset: 1.5mm, fill: black, text(size: 8pt, fill: white)[
    Dollar Street, Gapminder: Z. Miller (Haiti, Bolivia), L. Carvalho (Brazil), O. Havana (Spain); CC BY 4.0]))
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

#slide(title: [Energy and income])[
  #at(1, 12, y: -2mm, deck-fig("energy_gdp"))
]
#stove-page()
#slide(title: [Two numbers to remember])[
  #at(1, 6, y: 16mm, named(text(size: result-size, $91.9 %$), [of humanity has electricity (2024)]))
  #at(7, 6, y: 16mm, named(text(size: result-size, $approx 50 times$), [energy per person: Austria vs Ethiopia]))
  #at(1, 12, y: 100mm, align(center, text(fill: muted)[monthly income in PPP dollars per adult (Dollar Street); World Bank WDI, EIA]))
]

#slide(section: "energy-normalization", title: [Numbers, not adjectives])[
  #at(1, 12, y: 18mm, align(center, text(size: result-size,
    $p = E/(N Delta t), quad 1 "kWh" slash ("person" dot "d") = 41.7 "W" slash "person"$)))
  #at(1, 12, y: 72mm, grid(columns: (1fr, 1fr, 1fr), align: center,
    named($E$, [energy in a period]), named($N$, [people]), named($Delta t$, [days])))
]
#slide(section: "energy-demand", title: [Micro and macro])[
  #at(1, 12, y: 0mm, deck-fig("micro_macro"))
  #at(1, 12, y: 128mm, align(center, text(fill: muted)[gross inland = primary; final = delivered to users; Austria 2025, Statistics Austria (preliminary)]))
]

#slide(section: "energy-resources", title: [How long do reserves last?])[
  #at(1, 12, y: 0mm, deck-fig("resources"))
  #at(1, 12, y: 128mm, align(center, text(fill: muted)[world 2024: BGR Energiestudie; IAEA/NEA Uranium 2024 (Red Book)]))
]
#slide(section: "energy-resources", title: [Lifetime with growth])[
  #at(1, 12, y: 14mm, align(center, text(size: result-size,
    $t_"static" = S/D_0, quad t_g = ln(1 + g S slash D_0)/g$)))
  #at(1, 12, y: 70mm, grid(columns: (1fr, 1fr, 1fr), align: center,
    named($S$, [reserve]), named($D_0$, [use per year today]), named($g$, [growth per year])))
  #at(1, 12, y: 118mm, align(center, text(fill: muted)[$S slash D_0 = 100 "a"$, $g = 2 %$: $t_g approx 55 "a"$]))
]

#slide(section: "energy-area", title: [Solar power per area in Graz])[
  #at(1, 12, y: 0mm, deck-fig("solar_chain"))
  #at(1, 12, y: 134mm, align(center, text(fill: muted)[PVGIS (EU JRC) for Graz; module at 20 % efficiency]))
]
#slide(section: "energy-area", title: [How big is a gigawatt?])[
  #at(1, 12, y: -4mm, deck-fig("true_scale"))
  #at(1, 12, y: 132mm, text(size: small-size, fill: muted)[Contains modified Copernicus Sentinel data 2025 (Sentinel-2A, 11 Sep 2025); Graz boundary: Stadt Graz, data.graz.gv.at, CC BY 4.0; park data: EnBW (2021), expected yield 180 GWh/a.])
]
#slide(section: "energy-area", title: [Solar became cheap])[
  #at(1, 12, y: 0mm, deck-fig("pv_prices"))
  #at(1, 12, y: 134mm, align(center, text(fill: muted)[module prices: Nemet (2009), Farmer & Lafond (2016), IRENA, via Our World in Data]))
]
#photo-page("wind-freilaenderalm.jpg", [Naturpuur, Wikimedia Commons, CC BY-SA 4.0], "photo-wind")
#slide(section: "energy-area", title: [Wind power per area])[
  #at(1, 12, y: 20mm, align(center, text(size: result-size,
    $P/A approx 1 "to" 2 "W"/"m"^2, quad "capacity factor" approx 23 %$)))
  #at(1, 12, y: 80mm, align(center, text(fill: muted)[turbines must stand about five rotor diameters apart; the wind, not the machine, sets the limit]))
]
#slide(section: "energy-area", title: [Land for Austria's energy])[
  #at(1, 12, y: 0mm, deck-fig("area_budget"))
]

#slide(section: "energy-deployment", title: [Fuel for one gigawatt-year])[
  #at(1, 12, y: 0mm, deck-fig("fuel_mass"))
  #at(1, 12, y: 126mm, align(center, text(fill: muted)[
    D + T → #super[4]He + n + 17.6 MeV; coal 24 MJ/kg; uranium once-through]))
]
#slide(section: "energy-deployment", title: [Building it])[
  #at(1, 6, y: 18mm, named(text(size: result-size, $37$), [1 GW reactors for Austria's final energy]))
  #at(7, 6, y: 18mm, named(text(size: result-size, $33 "/a"$), [world record of new grid connections]))
  #at(1, 12, y: 100mm, align(center, text(fill: muted)[fuel is not the limit: plants, materials and construction rate are]))
]
#photo-page("jet-vessel-interior.jpg", [EUROfusion, Wikimedia Commons, CC BY 4.0], "photo-jet")

#credits-page((
  ("photo-night", [NASA Earth Observatory, Black Marble 2016, public domain], "science.nasa.gov/earth/earth-observatory/earth-at-night"),
  ("photo-stoves", [Dollar Street, Gapminder, CC BY 4.0], "gapminder.org/dollar-street"),
  ("photo-wind", [Naturpuur, Windpark Freiländeralm, CC BY-SA 4.0], "commons.wikimedia.org"),
  ("photo-jet", [EUROfusion, JET vessel internal view, CC BY 4.0], "commons.wikimedia.org/wiki/File:JET_vessel_internal_view.jpg"),
), [Data: EIA (public domain); World Bank WDI (CC BY 4.0); Statistics Austria; BGR; IAEA/NEA (CC BY 4.0); PVGIS (EU JRC); Our World in Data (CC BY 4.0); Copernicus Sentinel-2; Stadt Graz OGD (CC BY 4.0). \ Plots and calculations: Christopher Albert, CC BY 4.0. Method after D. MacKay, Sustainable Energy — without the hot air (2009).])
