#import "theme.typ": *
#import "@preview/fletcher:0.5.8": diagram as fdiagram, node, edge
#show: deck.with(chapter: 3)

// Chapter 3 applies the reaction physics of Chapter 2 to stars. Numbers come
// from derivations/chapters/ch03_stars.py; data provenance in data/ch03/README.md.
// Slides build up step by step (`build`, `reveal`); the PDF shows the last step.
#let weak = rgb("#7B3294")
#let em = plot-blue
#let strong = plot-orange
#let force-colour = (weak: weak, electromagnetic: em, strong: strong)
#let legend = text(size: 14pt, stack(spacing: 2.5mm, text(fill: weak)[■ weak], text(fill: em)[■ electromagnetic], text(fill: strong)[■ strong]))
#let rr(k, name, f) = (reveal(k, text(fill: muted, name)), reveal(k, f))
#let steps(..items, gap: 8mm) = grid(columns: (auto, 1fr), column-gutter: 7mm, row-gutter: gap,
  align: (right + horizon, left + horizon), ..items.pos().flatten())
#let cite-line(body) = text(size: 12pt, body)
#let msun = $M_dot.o$
#let lab(c, body) = text(size: 14pt, fill: c, body)
// Diagram pieces that appear from step k on; hidden ones keep their place.
#let bn(k, pos, body, stroke: none, ..args) = node(pos, if shown(k) { body } else { hide(body) },
  stroke: if shown(k) { stroke } else { none }, ..args)
#let be(k, a, b, c, label, side: left) = edge(a, b, "-|>",
  stroke: if shown(k) { 1pt + c } else { none },
  label: if shown(k) { lab(c, label) } else { hide(lab(c, label)) }, label-side: side)

// ------------------------------------------------- 3.1 What powers the Sun ---

#photo-page("stars/sun-sdo-304.jpg", [NASA/SDO (AIA), public domain], "photo-sun",
  section: "sun-power", fit: "contain", title: [The Sun])

#build(5, slide(section: "sun-power", title: [Energy budget of the Sun])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    ..rr(1, [Sun], [$L_dot.o = 3.83 times 10^26 "W", quad M_dot.o = 1.99 times 10^30 "kg", quad R_dot.o = 6.96 times 10^8 "m"$]),
    ..rr(2, [gravity], $t_"KH" = (G M_dot.o^2)/(R_dot.o L_dot.o) approx 3 times 10^7 "yr"$),
    ..rr(3, [Earth], [$4.5 times 10^9 "yr"$ #h(3mm) #text(fill: muted)[(radiometric)]]),
    ..rr(4, [fusion], [$4 "p" -> ""^4"He": quad Delta m \/ m = 0.71 %, quad t_"nuc" = (0.1 dot 0.0071 thin M_dot.o c^2)/L_dot.o approx 1 times 10^10 "yr"$]),
  ))
  #at(2, 10, y: 92mm, reveal(5, result-box($t_"KH" << 4.5 "Gyr" < t_"nuc"$, [only nuclear energy lasts long enough])))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1038/106014a0")[Eddington · Nature 106, 14 (1920)] ·
    #link("https://doi.org/10.1103/PhysRev.55.434")[Bethe · Phys. Rev. 55, 434 (1939)]])
])

// How the inputs of the energy budget are measured: the Sun from experiments
// anyone can repeat, the age of the Earth from uranium and lead.
#let earth = $⊕$
#let sunpanel(k, title, drawing, formula, note) = reveal(k, block(width: cols(4))[
  #align(center, text(size: 16pt, weight: "bold", title))
  #v(1mm)
  #align(center, block(height: 84mm, drawing))
  #v(1mm)
  #align(center, text(size: 17pt, formula))
  #v(1.5mm)
  #align(center, text(size: 13pt, fill: muted, note))
])

#build(6, slide(section: "sun-power", title: [How heavy, how large, how bright?])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    ..rr(1, [angle], [$theta = 2 R_dot.o \/ d = 0.53 degree$ #h(3mm) #text(fill: muted)[gives $R_dot.o \/ d = 1\/215$, no unit]]),
    ..rr(2, [distance], [$d = 1.5 times 10^11 "m"$ #h(3mm) #text(fill: muted)[parallax gives $d = 23 thin 500 thin R_earth$, so $R_dot.o = 109 thin R_earth$]]),
    ..rr(3, [Kepler and $g$], [$G M_dot.o = (4 pi^2 d^3)/T^2, quad G M_earth = g R_earth^2 quad => quad M_dot.o \/ M_earth = 333 thin 000$ #h(2mm) #text(fill: muted)[(no $G$)]]),
    ..rr(4, [weighing the Earth], [$G$ from a torsion balance: #h(1mm) $M_earth = 6.0 times 10^24 "kg", quad M_dot.o = 2.0 times 10^30 "kg"$]),
    ..rr(5, [sunlight], [$S = 1361 "W"\/"m"^2$ at Earth: #h(1mm) $L_dot.o = 4 pi d^2 S = 3.8 times 10^26 "W"$]),
  ))
  #at(2, 10, y: 104mm, reveal(6, result-box($t_"KH" = (G M_dot.o^2)/(R_dot.o L_dot.o) = (8 pi^3 d^3)/(G theta S T^4)$, [$G$ enters once; the distance enters as $d^3$])))
])

#build(3, slide(section: "sun-power", title: [Measuring it at home: angle, Earth, gravity])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #let thin-ink = 0.8pt + ink
  #let lbl(body) = text(size: 14pt, body)
  #at(1, 4, y: 0mm, sunpanel(1, [pinhole camera], canvas(length: 1mm, {
    import draw: *
    circle((8, 45), radius: 8, fill: plot-orange, stroke: none)
    line((8, 53), (78, 27.5), stroke: 0.6pt + plot-orange)
    line((8, 37), (78, 62.5), stroke: 0.6pt + plot-orange)
    line((30, 14), (30, 44), stroke: 2.4pt + ink)
    line((30, 46), (30, 76), stroke: 2.4pt + ink)
    line((78, 12), (78, 78), stroke: thin-ink)
    line((78, 27.5), (78, 62.5), stroke: 3.5pt + plot-orange)
    line((30, 5), (78, 5), stroke: thin-ink, mark: (start: "stealth", end: "stealth", fill: ink))
    content((54, 5), anchor: "south", padding: 1.5, lbl[$ell$])
    content((76, 45), anchor: "east", padding: 1, lbl[$D$])
    content((30, 80), anchor: "south", lbl[card with a pinhole])
    content((8, 32), anchor: "north", lbl[Sun])
  }), $R_dot.o \/ d = D \/ (2 ell) = 1\/215$, [$ell = 2 "m"$ gives an image $D = 1.9 "cm"$ · not to scale]))
  #at(5, 4, y: 0mm, sunpanel(2, [double sunset], canvas(length: 1mm, {
    import draw: *
    arc((40, -60), start: 58deg, stop: 122deg, radius: 100, anchor: "origin", stroke: 1.4pt + ink)
    line((40, 40), (40, 18), stroke: (paint: muted, thickness: 0.6pt, dash: "dashed"))
    content((38, 22), anchor: "east", lbl[$R_earth$])
    line((40, 41), (40, 53), stroke: 1.8pt + ink)
    circle((40, 41), radius: 1.3, fill: ink, stroke: none)
    circle((40, 53), radius: 1.3, fill: ink, stroke: none)
    line((40, 41), (90, 41), stroke: 1pt + plot-orange, mark: (end: "stealth", fill: plot-orange))
    line((40, 53), (90, 28.1), stroke: 1pt + plot-orange, mark: (end: "stealth", fill: plot-orange))
    content((38, 47), anchor: "east", lbl[$h$])
    content((38, 41), anchor: "east", lbl[lying])
    content((38, 55), anchor: "east", lbl[standing])
    content((90, 44), anchor: "south-east", lbl[to the setting Sun])
  }), $R_earth = (2 h)/(omega thin Delta t cos phi)^2$, [lie down until the Sun sets, stand up, time the second sunset: $h = 1.7 "m"$, Graz at equinox $Delta t approx 15 "s"$ · Rawlins 1979]))
  #at(9, 4, y: 0mm, sunpanel(3, [pendulum], canvas(length: 1mm, {
    import draw: *
    line((22, 74), (58, 74), stroke: 2.4pt + ink)
    line((40, 74), (40, 12), stroke: (paint: muted, thickness: 0.6pt, dash: "dashed"))
    line((40, 74), (56, 18), stroke: 1pt + ink)
    circle((56, 18), radius: 5, fill: plot-blue, stroke: none)
    content((50, 48), anchor: "west", padding: 1.5, lbl[$ell$])
    arc((40, 74), start: -90deg, stop: -74deg, radius: 30, anchor: "origin", stroke: 0.6pt + muted, mark: (end: "stealth", fill: muted))
    content((40, 6), lbl[swing period $T$])
  }), $g = (4 pi^2 ell)/T^2$, [$ell = 1 "m"$ gives $T = 2.01 "s"$; with $R_earth$: $G M_earth = g R_earth^2$, no $G$ needed]))
])

#build(3, slide(section: "sun-power", title: [Measuring it at home: distance, $G$, sunlight])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #let thin-ink = 0.8pt + ink
  #let lbl(body) = text(size: 14pt, body)
  #at(1, 4, y: 0mm, sunpanel(1, [Io's eclipses and a microwave oven], canvas(length: 1mm, {
    import draw: *
    circle((20, 60), radius: 14, stroke: (paint: muted, thickness: 0.5pt, dash: "dashed"))
    circle((20, 60), radius: 3.5, fill: plot-orange, stroke: none)
    circle((34, 60), radius: 2, fill: plot-blue, stroke: none)
    circle((6.8, 64.8), radius: 2, fill: plot-blue, stroke: none)
    circle((78, 60), radius: 6, fill: muted, stroke: none)
    circle((70, 66), radius: 1.2, fill: ink, stroke: none)
    line((36, 60), (72, 60), stroke: 0.7pt + ink)
    line((8.8, 64.6), (72, 61.2), stroke: (paint: ink, thickness: 0.7pt, dash: "dashed"))
    content((34, 56), anchor: "north", lbl[near])
    content((6.8, 68), anchor: "south", lbl[far])
    content((78, 52), anchor: "north", lbl[Jupiter, Io])
    content((50, 44), lbl[eclipse seen 16.6 min later])
    rect((8, 6), (78, 20), fill: rgb("#6B4226"), stroke: none)
    for x in (17, 35, 53, 71) { circle((x, 13), radius: 3.5, fill: rgb("#C9A27A"), stroke: none) }
    line((17, 25), (35, 25), stroke: thin-ink, mark: (start: "stealth", end: "stealth", fill: ink))
    content((26, 26), anchor: "south", padding: 1, lbl[$Delta x = lambda\/2$])
    content((60, 30), lbl[melted spots])
  }), $c = 2 f Delta x, quad d = (c thin Delta t)/2$, [chocolate in a microwave oven without turntable, $f = 2.45 "GHz"$, $Delta x approx 6 "cm"$ · Rømer 1676; Stauffer 1997]))
  #at(5, 4, y: 0mm, sunpanel(2, [torsion balance, top view], canvas(length: 1mm, {
    import draw: *
    line((14, 45), (62, 45), stroke: 1.6pt + ink)
    circle((14, 45), radius: 3, fill: plot-blue, stroke: none)
    circle((62, 45), radius: 3, fill: plot-blue, stroke: none)
    circle((16, 60), radius: 8.5, fill: muted, stroke: none)
    circle((60, 30), radius: 8.5, fill: muted, stroke: none)
    rect((36.5, 42), (39.5, 48), fill: white, stroke: 0.7pt + ink)
    line((86, 40), (39.5, 45), stroke: 0.8pt + rgb("#D62728"))
    line((39.5, 45), (86, 56), stroke: 0.8pt + rgb("#D62728"))
    line((86, 20), (86, 76), stroke: thin-ink)
    content((28, 60), anchor: "west", lbl[$M$, lead])
    content((10, 40), anchor: "north", lbl[$m$])
    content((38, 38), anchor: "north", lbl[mirror])
    content((84, 74), anchor: "east", lbl[wall])
    content((64, 64), lbl[laser])
    content((40, 10), lbl[fibre twists by $theta$])
  }), $G = (2 pi^2 L r^2 theta)/(M T^2)$, [rod length $L$, swing period $T$, distance $r$ between $M$ and $m$ · Cavendish 1798]))
  #at(9, 4, y: 0mm, sunpanel(3, [water calorimeter], canvas(length: 1mm, {
    import draw: *
    for i in range(4) { line((4 + 12 * i, 78), (22 + 12 * i, 58), stroke: 1pt + plot-orange, mark: (end: "stealth", fill: plot-orange)) }
    rect((26, 10), (56, 50), fill: ink, stroke: none)
    rect((29, 13), (53, 42), fill: plot-blue.lighten(40%), stroke: none)
    line((48, 18), (48, 60), stroke: 1.4pt + muted)
    circle((48, 18), radius: 2, fill: rgb("#D62728"), stroke: none)
    content((60, 44), anchor: "west", lbl[black can])
    content((60, 36), anchor: "west", lbl[area $A$])
    content((60, 28), anchor: "west", lbl[water $m$])
    content((60, 52), anchor: "west", lbl[thermometer])
    content((40, 4), lbl[warms by $Delta T$ in $Delta t$])
  }), $S = (m c_w Delta T)/(A thin Delta t)$, [200 g of water, $A = 50 "cm"^2$: about 0.3 K per minute; add the 30 % absorbed by the air · Pouillet 1838]))
])

#widget-page("kelvin", section: "sun-power", title: [Weighing the Sun])

#build(5, slide(section: "sun-power", title: [Uranium clocks])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #at(1, 6, y: 0mm, text(size: 17pt, steps(gap: 6mm,
    ..rr(1, [$""^238"U"$ chain], [$-> ""^206"Pb" + 8 thin alpha + 6 thin "e"^- + 6 thin overline(nu)_e$ #linebreak() $Q = 51.7 "MeV"$, #h(1mm) $t_(1\/2) = 4.47 "Gyr"$]),
    ..rr(2, [$""^235"U"$ chain], [$-> ""^207"Pb" + 7 thin alpha + 4 thin "e"^- + 4 thin overline(nu)_e$ #linebreak() $Q = 46.4 "MeV"$, #h(1mm) $t_(1\/2) = 0.70 "Gyr"$]),
    ..rr(3, [two forces], [#text(fill: em)[$alpha$: tunnelling out through the Coulomb barrier, fusion in reverse (Gamow 1928)] #linebreak() #text(fill: weak)[$beta$: weak interaction]]),
    ..rr(4, [the clock], [$(""^207"Pb"^*)/(""^206"Pb"^*) = (e^(lambda_235 t) - 1)/(137.8 thin (e^(lambda_238 t) - 1))$ #linebreak() #text(fill: muted, size: 15pt)[\* made by decay; $""^204"Pb"$ is not and marks the lead present at the start]]),
  )))
  #at(7, 6, y: 0mm, reveal(1, align(right, canvas(length: 1mm, {
    import draw: *
    let chain = ((92, 238, "U"), (90, 234, "Th"), (91, 234, "Pa"), (92, 234, "U"), (90, 230, "Th"),
      (88, 226, "Ra"), (86, 222, "Rn"), (84, 218, "Po"), (82, 214, "Pb"), (83, 214, "Bi"), (84, 214, "Po"),
      (82, 210, "Pb"), (83, 210, "Bi"), (84, 210, "Po"), (82, 206, "Pb"))
    let pos(z, a) = ((z - 82) * 9.5, (a - 206) / 4 * 11)
    let r = 3.6
    for a in range(206, 239, step: 4) {
      content((-7, pos(82, a).at(1)), anchor: "east", text(size: 12pt, fill: muted, str(a)))
    }
    for z in range(82, 93, step: 2) {
      content((pos(z, 206).at(0), -8), text(size: 12pt, fill: muted, str(z)))
    }
    content((-7, 96), anchor: "east", text(size: 13pt, fill: muted)[$A$])
    content((103, -8), anchor: "west", text(size: 13pt, fill: muted)[$Z$])
    for i in range(chain.len() - 1) {
      let (z1, a1, _) = chain.at(i)
      let (z2, a2, _) = chain.at(i + 1)
      let c = if a1 == a2 { weak } else { em }
      let (x1, y1) = pos(z1, a1)
      let (x2, y2) = pos(z2, a2)
      let l = calc.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
      let (ux, uy) = ((x2 - x1) / l, (y2 - y1) / l)
      line((x1 + r * ux, y1 + r * uy), (x2 - r * ux, y2 - r * uy), stroke: 1.2pt + c, mark: (end: "stealth", fill: c, scale: 0.7))
    }
    for (z, a, el) in chain {
      let ends = (a == 238 or a == 206)
      circle(pos(z, a), radius: r, fill: if ends { plot-orange.lighten(70%) } else { white },
        stroke: (if ends { 1.2pt } else { 0.6pt }) + ink)
      content(pos(z, a), text(size: 10pt, el))
    }
    content((pos(92, 238).at(0) + 5, pos(92, 238).at(1)), anchor: "west", text(size: 12pt)[4.47 Gyr])
    content((pos(92, 234).at(0) + 5, pos(92, 234).at(1)), anchor: "west", text(size: 12pt, fill: muted)[0.25 Myr])
    content((pos(82, 206).at(0) + 5, pos(82, 206).at(1) - 1), anchor: "west", text(size: 12pt)[stable])
  }))))
  #at(1, 6, y: 104mm, reveal(5, result-box([lead ratio → age], [the amount of uranium drops out])))
  #at(7, 6, y: 120mm, reveal(1, align(right, text(size: 13pt, fill: muted)[#text(fill: em)[$alpha$]: $A - 4$, $Z - 2$ · #text(fill: weak)[$beta^-$]: $Z + 1$ · all steps after $""^238"U"$ are fast])))
  #at(1, 12, y: 146mm, cite-line[
    Q from AME2020 · #link("https://doi.org/10.1088/1674-1137/abddae")[NUBASE2020 half-lives] ·
    #link("https://doi.org/10.1103/PhysRevC.4.1889")[Jaffey et al. · Phys. Rev. C 4, 1889 (1971)]])
])

#widget-page("isochron", section: "sun-power", title: [The age of meteorites and the Earth])

#build(5, slide(section: "sun-power", title: [From meteorites to the Sun])[
  #at(1, 12, y: 0mm, steps(gap: 8mm,
    ..rr(1, [meteorites], [oldest solids of the Solar System: $4.567 "Gyr"$ #h(2mm) #text(fill: muted)[(unchanged since they formed)]]),
    ..rr(2, [Earth], [crust lead lies on the meteorite line: $4.54 plus.minus 0.05 "Gyr"$ #h(2mm) #text(fill: muted)[(oldest Earth mineral 4.40 Gyr: the crust is recycled)]]),
    ..rr(3, [Sun], [helioseismology, independent of lead: $4.57 plus.minus 0.11 "Gyr"$]),
    ..rr(4, [sunlight], [life on Earth for 3.4 Gyr: the Sun has shone for most of its age]),
  ))
  #at(2, 10, y: 96mm, reveal(5, result-box($t_"Sun" approx 150 thin t_"KH"$, [gravity cannot have powered the Sun; Kelvin's age was too short])))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1016/0016-7037(56)90036-9")[Patterson · GCA 10, 230 (1956)] ·
    #link("https://doi.org/10.1126/science.1226919")[Connelly et al. · Science 338, 651 (2012)] ·
    #link("https://doi.org/10.1144/GSL.SP.2001.190.01.14")[Dalrymple (2001)] ·
    #link("https://doi.org/10.1038/35051550")[Wilde et al. (2001)] ·
    #link("https://doi.org/10.1051/0004-6361:20020749")[Bonanno et al. (2002)] ·
    #link("https://doi.org/10.1038/nature04764")[Allwood et al. (2006)]])
])

#build(5, slide(section: "sun-power", title: [What heats the Earth?])[
  #at(1, 12, y: 0mm, steps(gap: 8mm,
    ..rr(1, [heat flow], [$47 plus.minus 2 "TW"$ out of the Earth #h(2mm) #text(fill: muted)[($0.09 "W"\/"m"^2$; sunlight: $340 "W"\/"m"^2$)]]),
    ..rr(2, [radioactivity], [decay chains of $""^238"U"$, $""^235"U"$, $""^232"Th"$ and #text(fill: weak)[$beta$ decay of $""^40"K"$] #h(2mm) #text(fill: muted)[(no fission, no fusion)]]),
    ..rr(3, [geoneutrinos], [#text(fill: weak)[$overline(nu)_e$ from the $beta$ decays]: U + Th give $20 plus.minus 9 "TW"$ (KamLAND), all radiogenic $38 plus.minus 13 "TW"$ (Borexino)]),
    ..rr(4, [the rest], [heat of accretion and core formation: gravitational energy, still flowing out]),
  ))
  #at(2, 10, y: 96mm, reveal(5, result-box([nuclear decay is the missing heat source], [Kelvin's Earth and Sun ages failed for want of nuclear physics])))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.5194/se-1-5-2010")[Davies & Davies · Solid Earth 1, 5 (2010)] ·
    #link("https://doi.org/10.1038/ngeo1205")[KamLAND · Nature Geosci. 4, 647 (2011)] ·
    #link("https://doi.org/10.1103/PhysRevD.101.012009")[Borexino · Phys. Rev. D 101, 012009 (2020)]])
])

// -------------------------------------------- 3.2 Gravitational confinement ---

#build(5, slide(section: "gravity", title: [Hydrostatic equilibrium and virial theorem])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    ..rr(1, [force balance], $(dif p)/(dif r) = -(G m(r) rho)/r^2$),
    ..rr(2, [virial theorem], [$2 K + U = 0, quad K = 3/2 N k_B overline(T), quad U approx -3/5 (G M^2)/R$]),
    ..rr(3, [mean temperature], [$k_B overline(T) = (G M mu m_u)/(5 R) approx 0.25 "keV"$ #h(3mm) #text(fill: muted)[($mu = 0.62$)]]),
    ..rr(4, [total energy], $E = K + U = -K quad => quad (dif K)/(dif E) = -1$),
  ))
  #at(2, 10, y: 100mm, reveal(5, result-box([losing energy heats the star], [too much fusion: expands and cools · a thermostat])))
])

#slide(section: "gravity", title: [Inside the Sun])[
  #at(1, 12, y: 0mm, align(center, deck-fig("sun_profile", columns: 12)))
  #at(1, 12, y: 128mm, align(center)[centre: $p_"fus" = 262 "W"\/"m"^3$ #h(3mm) #text(fill: muted)[(a human body: about $1 "kW"\/"m"^3$)]])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1126/science.272.5266.1286")[Model S · Christensen-Dalsgaard et al. · Science 272, 1286 (1996)]])
]

#build(7, slide(section: "gravity", title: [The Sun and a tokamak])[
  #let row(k, a, b, c) = (reveal(k, a), reveal(k, b), reveal(k, c))
  #at(2, 10, y: 4mm, data-table(
    ([], [Sun, centre], [tokamak (ITER)]),
    (
      row(1, [$k_B T$], [1.35 keV], [10–20 keV]),
      row(2, [$n$], [$4.6 times 10^31 "m"^(-3)$], [$10^20 "m"^(-3)$]),
      row(3, [fuel], [p–p (weak interaction)], [D–T (strong)]),
      row(4, [$p_"fus"$], [$262 "W"\/"m"^3$], [$0.6 "MW"\/"m"^3$]),
      row(5, [$tau_E = W_"th" \/ L$], [$2 times 10^7 "yr"$], [3.7 s]),
      row(6, [$n T tau_E$], [$5 times 10^46 "keV s m"^(-3)$], [needs $3 times 10^21 "keV s m"^(-3)$]),
    ),
  ))
  #at(2, 10, y: 112mm, reveal(7, result-box([the Sun wins by confinement time], [not by reaction rate or power density])))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0029-5515/39/12/301")[ITER Physics Basis · Nucl. Fusion 39, 2137 (1999)]])
])

// ---------------------------------------------------- 3.3 Burning hydrogen ---

#build(6, slide(section: "hydrogen", title: [Proton–proton chain])[
  #at(1, 8, y: 0mm, align(center, context fdiagram(spacing: (27mm, 11mm), node-inset: 3mm,
    node-stroke: none, edge-stroke: 1pt + ink,
    bn(1, (1, 0), $"p" + "p"$),
    be(1, (1, 0), (1, 1), weak, [$"e"^+ + nu_e$, 0.42 MeV]),
    bn(1, (1, 1), $"D"$),
    be(2, (1, 1), (1, 2), em, [$+ "p"$, $gamma$, 5.49 MeV]),
    bn(2, (1, 2), $""^3"He"$),
    be(3, (1, 2), (0, 3), strong, [$+ ""^3"He"$, 12.86 MeV], side: right),
    bn(3, (0, 3), $""^4"He" + 2 "p"$, stroke: 0.8pt + strong),
    be(4, (1, 2), (2, 3), em, [$+ ""^4"He", gamma$]),
    bn(4, (2, 3), $""^7"Be"$),
    be(4, (2, 3), (1.4, 4), weak, [$+ "e"^-$, $nu_e$ 0.86 MeV], side: right),
    bn(4, (1.4, 4), $""^7"Li"$),
    be(4, (1.4, 4), (1.4, 5), strong, [$+ "p"$], side: right),
    bn(4, (1.4, 5), $2 thin ""^4"He"$, stroke: 0.8pt + strong),
    be(5, (2, 3), (2.6, 4), em, [$+ "p", gamma$]),
    bn(5, (2.6, 4), $""^8"B"$),
    be(5, (2.6, 4), (2.6, 5), weak, [$"e"^+ + nu_e$ ≤ 15 MeV]),
    bn(5, (2.6, 5), $""^8"Be"^* -> 2 thin ""^4"He"$, stroke: 0.8pt + strong),
    bn(3, (0, 5.7), text(fill: muted)[pp I · 84.8 %]),
    bn(4, (1.4, 5.7), text(fill: muted)[pp II · 15.2 %]),
    bn(5, (2.6, 5.7), text(fill: muted)[pp III · 0.017 %]),
  )))
  #at(9, 4, y: 2mm, legend)
  #at(9, 4, y: 30mm, reveal(6, text(size: 16pt)[
    $4 "p" -> ""^4"He" + 2 "e"^+ + 2 nu_e$ \ 26.7 MeV #v(8mm)
    #text(fill: muted)[branch shares from neutrino fluxes:] \
    $Phi(""^7"Be")\/Phi("pp") = f\/(2 - f)$]))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. · Rev. Mod. Phys. 83, 195 (2011)] ·
    #link("https://doi.org/10.3847/1538-4357/835/2/202")[Vinyoles et al. · ApJ 835, 202 (2017)]])
])

#build(4, slide(section: "hydrogen", title: [Which force sets the rate?])[
  #let sf = json("/data/ch03/s-factors.json")
  #let step-of = (weak: 1, electromagnetic: 2, strong: 3)
  #let fmt(s) = if s >= 100 { str(int(s)) } else if s >= 0.01 { str(s) } else {
    let e = calc.floor(calc.log(s, base: 10))
    $#calc.round(s / calc.pow(10.0, e), digits: 2) times 10^#e$ }
  #at(2, 10, y: 0mm, data-table(
    ([reaction], [force], [$S(0)$ [keV b]]),
    sf.reactions.map(r => {
      let k = step-of.at(r.force)
      let c = force-colour.at(r.force)
      (reveal(k, r.reaction), reveal(k, text(fill: c, r.force)), reveal(k, fmt(r.S0_keV_b)))
    }),
  ))
  #at(2, 10, y: 92mm, reveal(4, result-box([$nu$ out: weak · $gamma$ out: electromagnetic · only nuclei: strong],
    [the force sets $S$; the Coulomb barrier sets the temperature (Chapter 2)])))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. · Rev. Mod. Phys. 83, 195 (2011)], recommended $S(0)$])
])

#build(7, slide(section: "hydrogen", title: [CNO cycle])[
  #at(1, 6, y: 4mm, align(center, context fdiagram(spacing: (22mm, 16mm), node-inset: 3mm,
    node-stroke: none, edge-stroke: 1pt + ink,
    bn(1, (1, 0), $""^12"C"$),
    be(1, (1, 0), (2, 1), em, [$("p", gamma)$]),
    bn(1, (2, 1), $""^13"N"$),
    be(2, (2, 1), (2, 2), weak, [$beta^+$ 10 min]),
    bn(2, (2, 2), $""^13"C"$),
    be(3, (2, 2), (1, 3), em, [$("p", gamma)$]),
    bn(3, (1, 3), $""^14"N"$, stroke: 0.8pt + em),
    be(4, (1, 3), (0, 2), em, [$("p", gamma)$ slowest]),
    bn(4, (0, 2), $""^15"O"$),
    be(5, (0, 2), (0, 1), weak, [$beta^+$ 2 min]),
    bn(5, (0, 1), $""^15"N"$),
    be(6, (0, 1), (1, 0), strong, [$("p", alpha)$]),
  )))
  #at(7, 6, y: 6mm, legend)
  #at(7, 6, y: 30mm, steps(gap: 9mm,
    ..rr(4, [bottleneck], [$""^14"N" + "p": Z_1 Z_2 = 7$]),
    ..rr(7, [net], $4 "p" -> ""^4"He" + 2 "e"^+ + 2 nu_e$),
    ..rr(7, [energy], [26.7 MeV, 25.0 MeV stays]),
    ..rr(7, [catalyst], [C, N, O are not used up]),
  ))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/PhysRev.55.434")[Bethe · Phys. Rev. 55, 434 (1939)] ·
    #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. · Rev. Mod. Phys. 83, 195 (2011)]])
])

#widget-page("gamow", section: "hydrogen", title: [Gamow window of stellar fuels])

#widget-page("neutrinos", section: "hydrogen", title: [Solar neutrinos])

#widget-page("sun", section: "hydrogen", title: [The life of the Sun])

// --------------------------------------------- 3.4 Primordial nucleosynthesis ---

#photo-page("stars/cmb-wmap-9yr.jpg", [NASA / WMAP Science Team, public domain], "photo-cmb",
  section: "bbn", fit: "contain", title: [Cosmic microwave background])

#build(5, slide(section: "bbn", title: [Neutrons decide the helium])[
  #at(1, 12, y: 0mm, text(size: 16pt, steps(gap: 8mm,
    ..rr(1, [freeze-out], [$"n" + nu_e arrows.rl "p" + "e"^-$ #text(fill: weak)[(weak)]: $n\/p = e^(-Q\/k_B T_f), quad Q = 1.293 "MeV", quad k_B T_f approx 0.8 "MeV" => 0.20$]),
    ..rr(2, [bottleneck], [$"n" + "p" -> "D" + gamma$ #text(fill: em)[(e.m.)]: $n_"D"\/n_"n" approx 3/4 eta (2 zeta(3))/pi^2 ((4 pi k_B T)/(m c^2))^(3\/2) e^(B_"D"\/k_B T) = 1 => k_B T_"D" = 0.066 "MeV"$]),
    ..rr(3, [decay], [$n\/p = 0.20 thin e^(-Delta t \/ tau_n) = 0.14 quad (tau_n = 878 "s", thin t_"D" approx 300 "s")$]),
    ..rr(4, [helium], $Y_p = (2 n\/p)/(1 + n\/p) = 0.25$),
  )))
  #at(2, 10, y: 98mm, reveal(5, result-box($Y_p = 0.247$, [network (LINX) · observed $0.245 plus.minus 0.004$])))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/PhysRev.73.803")[Alpher, Bethe & Gamow · Phys. Rev. 73, 803 (1948)] ·
    #link("https://doi.org/10.1103/f3tj-r882")[LINX · Phys. Rev. D 112, 063531 (2025)] ·
    #link("https://doi.org/10.1088/1475-7516/2015/07/011")[Aver et al. · JCAP 07, 011 (2015)]])
])

#widget-page("bbn", section: "bbn", title: [Primordial nucleosynthesis])

#build(4, slide(section: "bbn", title: [Why it stops at lithium])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    ..rr(1, [no stable $A = 5, 8$], [$""^5"He", ""^5"Li": 10^(-21) "s", quad ""^8"Be": 8 times 10^(-17) "s"$]),
    ..rr(2, [dilute], [$rho_b approx 10^(-2) "kg"\/"m"^3$ at $k_B T = 0.07 "MeV"$ #h(3mm) #text(fill: muted)[(Sun: $1.5 times 10^5$)]]),
    ..rr(3, [fast], [expansion: $T prop t^(-1\/2)$, over after about 20 min]),
  ))
  #at(2, 10, y: 84mm, reveal(4, result-box([#super[7]Li/H: predicted $5 times 10^(-10)$, observed $1.6 times 10^(-10)$], [the lithium problem])))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.3847/1538-4357/aaab53")[Cooke et al. · ApJ 855, 102 (2018)] · PDG BBN review (2024)])
])

// ---------------------------------- 3.5 Helium burning and heavier elements ---

#photo-page("stars/carina-nebula-eta-carinae-hubble.jpg",
  [NASA, ESA, N. Smith (UC Berkeley), Hubble Heritage Team (STScI/AURA), CC BY 4.0], "photo-carina",
  section: "heavier", title: [Carina Nebula])

#build(4, slide(section: "heavier", title: [Triple alpha and the Hoyle state])[
  #at(1, 12, y: 0mm, align(center, deck-fig("hoyle", columns: 11)))
  #at(1, 12, y: 118mm, align(center, grid(columns: 4, column-gutter: 9mm,
    reveal(1, [$""^4"He" + ""^4"He" arrows.rl ""^8"Be"$ #lab(strong)[strong]]),
    reveal(2, [$""^8"Be" + ""^4"He" -> ""^12"C"^*$ #lab(strong)[resonance]]),
    reveal(3, [$""^12"C"^* -> ""^12"C" + gamma$ #lab(em)[e.m.]]),
    reveal(4, [$""^12"C" + ""^4"He" -> ""^16"O" + gamma$ #lab(em)[e.m.]]),
  )))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1086/190005")[Hoyle · ApJS 1, 121 (1954)] ·
    #link("https://doi.org/10.1103/PhysRev.107.508")[Cook, Fowler, Lauritsen & Lauritsen · Phys. Rev. 107, 508 (1957)] · AME2020])
])

#widget-page("binding", section: "heavier", title: [Energy per nucleon])

#build(7, slide(section: "heavier", title: [Burning stages of a massive star])[
  #let row(k, ..c) = c.pos().map(x => reveal(k, x))
  #at(1, 7, y: 0mm, text(size: 16pt, data-table(
    ([fuel], [ash], [$T$ [GK]], [$k_B T$ [keV]], [duration]),
    (
      row(1, [H], [He], [0.037], [3], [8.1 Myr]),
      row(2, [He], [C, O], [0.19], [16], [1.2 Myr]),
      row(3, [C], [Ne, Mg], [0.87], [75], [980 yr]),
      row(4, [Ne], [O, Mg], [1.6], [140], [0.6 yr]),
      row(5, [O], [Si, S], [2.0], [170], [1.3 yr]),
      row(6, [Si], [Fe, Ni], [3.3], [280], [11 d]),
    ),
  )))
  #at(1, 7, y: 112mm, reveal(4, text(fill: muted)[20 #msun; after helium: neutrino losses $prop T^9$]))
  #at(8, 5, y: 0mm, reveal(7, image("/slides/build/fig/onion.svg", width: cols(5))))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://arxiv.org/abs/astro-ph/0211062")[Heger, Woosley, Fryer & Langer · Massive star evolution through the ages (2003), Table 1] · shells not to scale])
])

#widget-page("star", section: "heavier", title: [Build a star])

// --------------------------------------- 3.6 Endpoints and extreme conditions ---

#photo-page("stars/ring-nebula-webb.jpg", [ESA/Webb, NASA, CSA, M. Barlow, N. Cox, R. Wesson, CC BY 4.0], "photo-ring",
  section: "endpoints", title: [Ring Nebula])

#build(5, slide(section: "endpoints", title: [Degeneracy ends the burning])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    ..rr(1, [degenerate], [$E_F > k_B T$: pressure no longer depends on $T$, no thermostat]),
    ..rr(2, [lightest star], [$0.075 msun$: degeneracy stops the contraction before p–p ignites]),
    ..rr(3, [brown dwarf], [$0.013 msun approx 13 M_"Jupiter"$: deuterium burning only]),
    ..rr(4, [Chandrasekhar], [$M_"Ch" = sqrt(3 pi)/2 thin omega_3 ((ħ c)/G)^(3\/2) 1/(mu_e m_u)^2 = 1.46 msun quad (mu_e = 2)$]),
    ..rr(5, [neutron star], [$1.4 msun$, $R approx 12 "km"$, nuclear density]),
  ))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1086/143324")[Chandrasekhar · ApJ 74, 81 (1931)] ·
    #link("https://doi.org/10.1146/annurev.astro.38.1.337")[Chabrier & Baraffe · ARA&A 38, 337 (2000)] ·
    #link("https://doi.org/10.1088/0004-637X/727/1/57")[Spiegel et al. · ApJ 727, 57 (2011)]])
])

#widget-page("whitedwarf", section: "endpoints", title: [White dwarfs])

#widget-page("extremes", section: "endpoints", title: [Where fusion happens])

#photo-page("stars/tycho-snr-chandra.jpg", [Tycho's supernova remnant: NASA/CXC/Rutgers/J. Warren & J. Hughes et al., public domain], "photo-tycho",
  section: "endpoints", fit: "contain", title: [Tycho's supernova, 1572])

#build(5, slide(section: "endpoints", title: [Type Ia supernova: a carbon bomb])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    ..rr(1, [progenitor], [C/O white dwarf grows towards $M_"Ch"$]),
    ..rr(2, [ignition], [#super[12]C + #super[12]C #text(fill: strong)[(strong)] at $rho_c approx 2 times 10^12 "kg"\/"m"^3$: degenerate, runs away]),
    ..rr(3, [energy], [C, O $-> ""^56"Ni"$: $0.81 "MeV"$ per nucleon $times 1.4 msun = 2 times 10^44 "J"$ #h(2mm) #text(fill: muted)[> binding]]),
    ..rr(4, [light], [$""^56"Ni" ->^(6.1 "d") ""^56"Co" ->^(77 "d") ""^56"Fe"$ #text(fill: weak)[(weak)]]),
  ))
  #at(2, 10, y: 100mm, reveal(5, result-box([fusion unbinds the whole star], [no remnant · about 0.6 $msun$ of #super[56]Ni])))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1146/annurev.astro.38.1.191")[Hillebrandt & Niemeyer · ARA&A 38, 191 (2000)]])
])

#photo-page("stars/crab-nebula-webb.jpg", [Crab Nebula: NASA, ESA, CSA, STScI, T. Temim (Princeton University), CC BY 4.0], "photo-crab",
  section: "endpoints", fit: "contain", title: [Crab Nebula, supernova of 1054])

#build(5, slide(section: "endpoints", title: [Core collapse: gravity, not fusion])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    ..rr(1, [iron core], [no fusion energy left: $B\/A$ is maximal]),
    ..rr(2, [collapse], [photodisintegration, electron capture #text(fill: weak)[(weak)]; bounce at nuclear density]),
    ..rr(3, [energy], [$3/5 (G M^2)/R = 3 times 10^46 "J"$ #h(2mm) #text(fill: muted)[(1.4 $msun$, 12 km), 99 % neutrinos]]),
    ..rr(4, [SN 1987A], [24 neutrinos in Kamiokande-II, IMB, Baksan; $0.07 msun$ of #super[56]Ni]),
  ))
  #at(2, 10, y: 100mm, reveal(5, result-box([fusion builds the core and burns the ejecta], [explosive Si and O burning])))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/PhysRevLett.58.1490")[Hirata et al. · PRL 58, 1490 (1987)] ·
    #link("https://doi.org/10.1103/PhysRevLett.58.1494")[Bionta et al. · PRL 58, 1494 (1987)] ·
    #link("https://doi.org/10.1146/annurev.aa.27.090189.003213")[Arnett et al. · ARA&A 27, 629 (1989)] ·
    #link("https://doi.org/10.1016/j.physrep.2007.02.002")[Janka et al. · Phys. Rep. 442, 38 (2007)]])
])

#photo-page("stars/neutron-star-merger-eso-illustration.jpg", [Illustration: ESO/L. Calçada/M. Kornmesser, CC BY 4.0], "photo-merger",
  section: "endpoints", title: [Neutron-star merger (illustration)])

#build(4, slide(section: "endpoints", title: [Neutron stars: bursts, crusts, mergers])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    ..rr(1, [X-ray burst], [accreted H, He ignite: He flash, rapid proton capture #text(fill: em)[(e.m.)] up to Sn–Te in seconds]),
    ..rr(2, [crust], [pycnonuclear fusion: zero-point motion in a lattice, density instead of temperature]),
    ..rr(3, [merger], [GW170817: neutron capture (r process), kilonova · not fusion]),
    ..rr(4, [on Earth], [muon-catalysed fusion is fusion by density too (Chapter 9)]),
  ))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/PhysRevLett.86.3471")[Schatz et al. · PRL 86, 3471 (2001)] ·
    Haensel & Zdunik · A&A 227, 431 (1990) ·
    #link("https://doi.org/10.1103/PhysRevLett.119.161101")[LIGO/Virgo · PRL 119, 161101 (2017)]])
])

#slide(section: "endpoints", title: [Where the elements come from])[
  #at(1, 12, y: 0mm, align(center, deck-fig("abundances", columns: 12)))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1051/0004-6361/202140445")[Asplund, Amarsi & Grevesse · A&A 653, A141 (2021), CC BY 4.0] ·
    #link("https://doi.org/10.1103/RevModPhys.29.547")[Burbidge, Burbidge, Fowler & Hoyle · Rev. Mod. Phys. 29, 547 (1957)]])
]

#credits-page((
  ("photo-sun", [NASA/SDO (AIA), the Sun, public domain], "sdo.gsfc.nasa.gov"),
  ("photo-cmb", [NASA/WMAP Science Team, nine-year sky, public domain], "commons.wikimedia.org"),
  ("photo-carina", [NASA, ESA, N. Smith, Hubble Heritage Team, CC BY 4.0], "esahubble.org"),
  ("photo-ring", [ESA/Webb, NASA, CSA, M. Barlow, N. Cox, R. Wesson, CC BY 4.0], "esawebb.org"),
  ("photo-tycho", [NASA/CXC/Rutgers/J. Warren & J. Hughes et al., public domain], "chandra.harvard.edu"),
  ("photo-crab", [NASA, ESA, CSA, STScI, T. Temim, CC BY 4.0], "esawebb.org/images/weic2326a"),
  ("photo-merger", [ESO/L. Calçada/M. Kornmesser, illustration, CC BY 4.0], "eso.org"),
), [Data: MIST (Dotter 2016; Choi et al. 2016), LINX/PRIMAT, Model S, AME2020, Asplund et al. 2021, B16, Adelberger et al. 2011, Bond et al. 2017, Heger et al. 2003, Patterson 1956, KamLAND 2011, Borexino 2020. Drawings, plots, widgets, calculations: Christopher Albert, CC BY 4.0.])
