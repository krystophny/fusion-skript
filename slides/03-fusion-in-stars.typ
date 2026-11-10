#import "theme.typ": *
#show: deck.with(chapter: 3)

// Chapter 3 applies the reaction physics of Chapter 2 to stars. Numbers come
// from derivations/chapters/ch03_stars.py; data provenance in data/ch03/README.md.
#let r(name, f) = ([#text(fill: muted, name)], f)
#let steps(..items, gap: 8mm) = grid(columns: (auto, 1fr), column-gutter: 7mm, row-gutter: gap,
  align: (right + horizon, left + horizon), ..items.pos().flatten())
#let cite-line(body) = text(size: 12pt, body)
#let msun = $M_dot.o$
#let iso(a, el) = $""^#a #el$

// ------------------------------------------------- 3.1 What powers the Sun ---

#photo-page("stars/sun-sdo-304.jpg", [NASA/SDO (AIA), public domain], "photo-sun",
  section: "sun-power", fit: "contain", title: [The Sun])

#slide(section: "sun-power", title: [Energy budget of the Sun])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    r([Sun], [$L_dot.o = 3.83 times 10^26 "W", quad M_dot.o = 1.99 times 10^30 "kg", quad R_dot.o = 6.96 times 10^8 "m"$]),
    r([gravity], $t_"KH" = (G M_dot.o^2)/(R_dot.o L_dot.o) approx 3 times 10^7 "yr"$),
    r([fusion], [$4 "p" -> iso(4, "He"): quad Delta m \/ m = 0.71 %, quad t_"nuc" = (0.1 dot 0.0071 thin M_dot.o c^2)/L_dot.o approx 1 times 10^10 "yr"$]),
    r([Earth], [$4.5 times 10^9 "yr"$ #h(3mm) #text(fill: muted)[(radiometric)]]),
  ))
  #at(2, 10, y: 92mm, result-box($t_"KH" << 4.5 "Gyr" < t_"nuc"$, [only nuclear energy lasts long enough]))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1038/106014a0")[Eddington · Nature 106, 14 (1920)] ·
    #link("https://doi.org/10.1103/PhysRev.55.434")[Bethe · Phys. Rev. 55, 434 (1939)]])
]

// -------------------------------------------- 3.2 Gravitational confinement ---

#slide(section: "gravity", title: [Hydrostatic equilibrium and virial theorem])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    r([force balance], $(dif p)/(dif r) = -(G m(r) rho)/r^2$),
    r([virial theorem], [$2 K + U = 0, quad K = 3/2 N k_B overline(T), quad U approx -3/5 (G M^2)/R$]),
    r([mean temperature], [$k_B overline(T) = (G M mu m_u)/(5 R) approx 0.25 "keV"$ #h(3mm) #text(fill: muted)[($mu = 0.62$); centre 1.35 keV]]),
    r([total energy], $E = K + U = -K quad => quad (dif K)/(dif E) = -1$),
  ))
  #at(2, 10, y: 100mm, result-box([losing energy heats the star], [too much fusion: expands and cools · a thermostat]))
]

#slide(section: "gravity", title: [Inside the Sun])[
  #at(1, 12, y: 0mm, align(center, deck-fig("sun_profile", columns: 12)))
  #at(1, 12, y: 128mm, align(center)[
    centre: $k_B T = 1.35 "keV", quad rho = 1.5 times 10^5 "kg"\/"m"^3, quad p_"fus" = 262 "W"\/"m"^3$])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1126/science.272.5266.1286")[Model S · Christensen-Dalsgaard et al. · Science 272, 1286 (1996)]])
]

#slide(section: "gravity", title: [The Sun and a tokamak])[
  #at(2, 10, y: 4mm, data-table(
    ([], [Sun, centre], [tokamak (ITER)]),
    (
      ([$k_B T$], [1.35 keV], [10–20 keV]),
      ([$n$], [$4.6 times 10^31 "m"^(-3)$], [$10^20 "m"^(-3)$]),
      ([fuel], [p–p (weak interaction)], [D–T]),
      ([$p_"fus"$], [$262 "W"\/"m"^3$], [$0.6 "MW"\/"m"^3$]),
      ([$tau_E = W_"th" \/ L$], [$2 times 10^7 "yr"$], [3.7 s]),
      ([$n T tau_E$], [$5 times 10^46 "keV s m"^(-3)$], [needs $3 times 10^21 "keV s m"^(-3)$]),
    ),
  ))
  #at(2, 10, y: 116mm, text(fill: muted)[human body: about $1 "kW"\/"m"^3$ #h(6mm) Sun: fusion wins by $tau_E$, not by power density])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0029-5515/39/12/301")[ITER Physics Basis · Nucl. Fusion 39, 2137 (1999)]])
]

// ------------------------------------------------- 3.3 Proton–proton chain ---

#slide(section: "pp-chain", title: [Proton–proton chain])[
  #let lab(body) = text(size: 15pt, fill: muted, body)
  #let branch(x) = (
    node((x, 0), $"p" + "p"$),
    edge((x, 0), (x, 1), "-|>", label: lab[$"e"^+ + nu_e$, 0.42 MeV], label-side: if x < 1 { left } else { right }),
    node((x, 1), $"D" + "p"$),
    edge((x, 1), (x, 2), "-|>", label: lab[$gamma$, 5.49 MeV], label-side: if x < 1 { left } else { right }),
    node((x, 2), $""^3"He"$),
    edge((x, 2), (1, 3), "-|>"),
  )
  #at(2, 10, y: 0mm, align(center, diagram(spacing: (34mm, 15mm), node-inset: 4mm,
    node-stroke: none, edge-stroke: 0.9pt + ink,
    ..branch(0), ..branch(2),
    node((1, 3), $""^4"He" + 2 "p"$, stroke: 0.8pt + plot-orange, inset: 5mm),
    node((1, 2.55), lab[12.86 MeV]),
  )))
  #at(1, 12, y: 128mm, align(center)[
    $4 "p" -> ""^4"He" + 2 "e"^+ + 2 nu_e$ #h(10mm) #text(fill: muted)[26.7 MeV incl. $2 times$ e#super[+]e#super[−] annihilation]])
]

#slide(section: "pp-chain", title: [Three branches])[
  #import "@preview/fletcher:0.5.8": diagram, node, edge
  #let lab(body) = text(size: 15pt, fill: muted, body)
  #let box3(pos, body, c) = node(pos, body, stroke: 0.8pt + c, inset: 4mm, corner-radius: 2mm)
  #at(1, 12, y: 0mm, align(center, diagram(spacing: (24mm, 12mm), edge-stroke: 0.9pt + ink, node-stroke: none,
    node((1, 0), $""^3"He"$),
    edge((1, 0), (0, 1), "-|>", label: lab[$+ ""^3"He"$], label-side: right),
    edge((1, 0), (2, 1), "-|>", label: lab[$+ ""^4"He"$], label-side: left),
    box3((0, 1), [$""^4"He" + 2 "p"$], plot-orange),
    node((2, 1), $""^7"Be" + gamma$),
    edge((2, 1), (1.5, 2), "-|>", label: lab[$+ "e"^-$, $nu_e$ 0.86 MeV], label-side: right),
    edge((2, 1), (3, 2), "-|>", label: lab[$+ "p"$], label-side: left),
    node((1.5, 2), $""^7"Li"$),
    edge((1.5, 2), (1.5, 3), "-|>", label: lab[$+ "p"$], label-side: right),
    box3((1.5, 3), [$2 thin ""^4"He"$], plot-blue),
    node((3, 2), $""^8"B"$),
    edge((3, 2), (3, 3), "-|>", label: lab[$"e"^+ + nu_e$ ≤ 15 MeV], label-side: left),
    box3((3, 3), [$""^8"Be"^* -> 2 thin ""^4"He"$], rgb("#1B7F5B")),
    node((0, 3.7), text(fill: plot-orange)[pp I #h(2mm) 84.8 %]),
    node((1.5, 3.7), text(fill: plot-blue)[pp II #h(2mm) 15.2 %]),
    node((3, 3.7), text(fill: rgb("#1B7F5B"))[pp III #h(2mm) 0.017 %]),
  )))
  #at(1, 12, y: 128mm, align(center)[
    #text(fill: muted)[from neutrino fluxes (B16):] #h(3mm)
    $Phi(""^7"Be")\/Phi("pp") = f\/(2 - f), quad f = "pp II" + "pp III"$])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. · Rev. Mod. Phys. 83, 195 (2011)] ·
    #link("https://doi.org/10.3847/1538-4357/835/2/202")[Vinyoles et al. · ApJ 835, 202 (2017)]])
]

#slide(section: "pp-chain", title: [Solar core])[
  #at(1, 12, y: 0mm, align(center, deck-fig("gamow_peak_pp", columns: 10)))
  #at(1, 12, y: 134mm, align(center)[
    p–p: #h(3mm) $E_G = 0.49 "MeV", quad k_B T approx 1.3 "keV" quad => quad E_0 approx 6 "keV" approx 4.6 thin k_B T$])
]

#slide(section: "pp-chain", title: [Solar neutrinos])[
  #at(1, 12, y: 0mm, align(center, deck-fig("solar_neutrinos", columns: 12)))
  #at(1, 12, y: 128mm, align(center)[
    #text(fill: muted)[measured:] Cl 1968 · Ga 1990s · water 1996– · pp (Borexino 2014) · CNO (Borexino 2020)])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/PhysRevLett.20.1205")[Davis et al. · PRL 20, 1205 (1968)] ·
    #link("https://doi.org/10.1038/nature13702")[Borexino · Nature 512, 383 (2014)] ·
    #link("https://doi.org/10.1038/s41586-020-2934-0")[Borexino · Nature 587, 577 (2020)] ·
    fluxes B16-GS98])
]

// -------------------------------------------------------------- 3.4 CNO cycle ---

#slide(section: "cno", title: [CNO cycle])[
  #import "@preview/fletcher:0.5.8": diagram, node, edge
  #let lab(body) = text(size: 15pt, fill: muted, body)
  #at(1, 6, y: 4mm, align(center, diagram(spacing: (22mm, 16mm), edge-stroke: 0.9pt + ink, node-stroke: none,
    node((1, 0), $""^12"C"$),
    edge((1, 0), (2, 1), "-|>", label: lab[$("p", gamma)$], label-side: left),
    node((2, 1), $""^13"N"$),
    edge((2, 1), (2, 2), "-|>", label: lab[$beta^+$ 10 min], label-side: left),
    node((2, 2), $""^13"C"$),
    edge((2, 2), (1, 3), "-|>", label: lab[$("p", gamma)$], label-side: left),
    node((1, 3), $""^14"N"$, stroke: 0.8pt + plot-orange, inset: 3mm),
    edge((1, 3), (0, 2), "-|>", label: text(size: 15pt, fill: plot-orange)[$("p", gamma)$ slowest], label-side: left),
    node((0, 2), $""^15"O"$),
    edge((0, 2), (0, 1), "-|>", label: lab[$beta^+$ 2 min], label-side: left),
    node((0, 1), $""^15"N"$),
    edge((0, 1), (1, 0), "-|>", label: lab[$("p", alpha)$], label-side: left),
  )))
  #at(7, 6, y: 18mm, steps(gap: 9mm,
    r([net], $4 "p" -> ""^4"He" + 2 "e"^+ + 2 nu_e$),
    r([energy], [26.7 MeV, 25.0 MeV stays]),
    r([catalyst], [C, N, O are not used up]),
    r([bottleneck], [$""^14"N" + "p": Z_1 Z_2 = 7$]),
  ))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/PhysRev.55.434")[Bethe · Phys. Rev. 55, 434 (1939)] ·
    #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. · Rev. Mod. Phys. 83, 195 (2011)]])
]

#slide(section: "cno", title: [pp or CNO?])[
  #at(1, 12, y: 0mm, align(center, deck-fig("pp_cno", columns: 12)))
  #at(1, 12, y: 128mm, align(center)[
    $(dif ln chevron.l sigma v chevron.r)/(dif ln T) = (tau - 2)/3, quad tau = (3 E_0)/(k_B T)$ #h(8mm)
    #text(fill: muted)[equal at 19 MK · CNO wins above 1.5] $msun$])
  #at(1, 12, y: 146mm, cite-line[
    $S_"11" = 4.01 times 10^(-22) "keV b", S_"1,14" = 1.66 "keV b"$ (Adelberger et al. 2011) ·
    #link("https://doi.org/10.3847/0067-0049/222/1/8")[MIST · Dotter, ApJS 222, 8 (2016)]])
]

// --------------------------------------------- 3.5 Primordial nucleosynthesis ---

#photo-page("stars/cmb-wmap-9yr.jpg", [NASA / WMAP Science Team, public domain], "photo-cmb",
  section: "bbn", fit: "contain", title: [Cosmic microwave background])

#slide(section: "bbn", title: [Neutrons decide the helium])[
  #at(1, 12, y: 0mm, steps(gap: 8mm,
    r([freeze-out], [$n\/p = e^(-Q\/k_B T_f), quad Q = 1.293 "MeV", quad k_B T_f approx 0.8 "MeV" quad => quad 0.20$]),
    r([bottleneck], [$n_"D"\/n_"n" approx 3/4 eta (2 zeta(3))/pi^2 ((4 pi k_B T)/(m c^2))^(3\/2) e^(B_"D"\/k_B T) = 1 quad => quad k_B T_"D" = 0.066 "MeV"$]),
    r([decay], [$n\/p = 0.20 thin e^(-Delta t \/ tau_n) = 0.14 quad (tau_n = 878 "s", thin t_"D" approx 300 "s")$]),
    r([helium], $Y_p = (2 n\/p)/(1 + n\/p) = 0.25$),
  ))
  #at(2, 10, y: 98mm, result-box($Y_p = 0.247$, [network (LINX) · observed $0.245 plus.minus 0.004$]))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/PhysRev.73.803")[Alpher, Bethe & Gamow · Phys. Rev. 73, 803 (1948)] ·
    #link("https://doi.org/10.1103/f3tj-r882")[LINX · Phys. Rev. D 112, 063531 (2025)] ·
    #link("https://doi.org/10.1088/1475-7516/2015/07/011")[Aver et al. · JCAP 07, 011 (2015)]])
]

#widget-page("bbn", section: "bbn", title: [Primordial nucleosynthesis])

#slide(section: "bbn", title: [Why it stops at lithium])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    r([no stable $A = 5, 8$], [$""^5"He", ""^5"Li": 10^(-21) "s", quad ""^8"Be": 8 times 10^(-17) "s"$]),
    r([dilute], [$rho_b approx 10^(-2) "kg"\/"m"^3$ at $k_B T = 0.07 "MeV"$ #h(3mm) #text(fill: muted)[(Sun: $1.5 times 10^5$)]]),
    r([fast], [expansion: $T prop t^(-1\/2)$, over after about 20 min]),
    r([result], [H 75 %, #super[4]He 25 %, D/H $2.5 times 10^(-5)$, #super[7]Li/H $5 times 10^(-10)$]),
  ))
  #at(2, 10, y: 100mm, result-box([observed #super[7]Li/H $= 1.6 times 10^(-10)$], [the lithium problem]))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.3847/1538-4357/aaab53")[Cooke et al. · ApJ 855, 102 (2018)] · PDG BBN review (2024)])
]

// ---------------------------------- 3.6 Helium burning and heavier elements ---

#photo-page("stars/carina-nebula-eta-carinae-hubble.jpg",
  [NASA, ESA, N. Smith (UC Berkeley), Hubble Heritage Team (STScI/AURA), CC BY 4.0], "photo-carina",
  section: "heavier", title: [Carina Nebula])

#slide(section: "heavier", title: [Triple alpha and the Hoyle state])[
  #at(1, 12, y: 0mm, align(center, deck-fig("hoyle", columns: 12)))
  #at(1, 12, y: 126mm, align(center)[
    $""^4"He" + ""^4"He" arrows.rl ""^8"Be", quad ""^8"Be" + ""^4"He" -> ""^12"C"^* -> ""^12"C" + gamma, quad ""^12"C" + ""^4"He" -> ""^16"O" + gamma$])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1086/190005")[Hoyle · ApJS 1, 121 (1954)] ·
    #link("https://doi.org/10.1103/PhysRev.107.508")[Cook, Fowler, Lauritsen & Lauritsen · Phys. Rev. 107, 508 (1957)] · AME2020])
]

#slide(section: "heavier", title: [Binding energy per nucleon])[
  #at(1, 12, y: 0mm, align(center, deck-fig("binding", columns: 12)))
  #at(1, 12, y: 128mm, align(center)[
    most bound: $""^62"Ni"$ 8.795 MeV #h(3mm) $""^56"Fe"$ 8.790 MeV #h(3mm) $""^4"He"$ 7.074 MeV])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/1674-1137/abddaf")[AME2020 · Wang et al. · Chin. Phys. C 45, 030003 (2021)]])
]

#slide(section: "heavier", title: [Burning stages of a massive star])[
  #at(1, 7, y: 0mm, text(size: 16pt, data-table(
    ([fuel], [ash], [$T$ [GK]], [$k_B T$ [keV]], [duration]),
    (
      ([H], [He], [0.037], [3], [8.1 Myr]),
      ([He], [C, O], [0.19], [16], [1.2 Myr]),
      ([C], [Ne, Mg], [0.87], [75], [980 yr]),
      ([Ne], [O, Mg], [1.6], [140], [0.6 yr]),
      ([O], [Si, S], [2.0], [170], [1.3 yr]),
      ([Si], [Fe, Ni], [3.3], [280], [11 d]),
    ),
  )))
  #at(1, 7, y: 112mm, text(fill: muted)[20 #msun; after He: neutrino losses $prop T^9$])
  #at(8, 5, y: 0mm, image("/slides/build/fig/onion.svg", width: cols(5)))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://arxiv.org/abs/astro-ph/0211062")[Heger, Woosley, Fryer & Langer · Massive star evolution through the ages (2003), Table 1] · shells not to scale])
]

#widget-page("star", section: "heavier", title: [Build a star])

// ------------------------------------------------- 3.7 Degenerate endpoints ---

#photo-page("stars/ring-nebula-webb.jpg", [ESA/Webb, NASA, CSA, M. Barlow, N. Cox, R. Wesson, CC BY 4.0], "photo-ring",
  section: "remnants", title: [Ring Nebula])

#slide(section: "remnants", title: [Degeneracy ends the burning])[
  #at(1, 12, y: 0mm, steps(gap: 8mm,
    r([degenerate], [$E_F = k_B T$: pressure no longer depends on $T$, no thermostat]),
    r([lightest star], [$0.075 msun$: degeneracy stops the contraction before p–p ignites]),
    r([brown dwarf], [$0.013 msun approx 13 M_"Jupiter"$: deuterium burning only]),
    r([white dwarf], [$0.6 msun$: $rho_c = 3.5 times 10^9 "kg"\/"m"^3$, $R approx 8700 "km"$]),
    r([Chandrasekhar], [$M_"Ch" = sqrt(3 pi)/2 thin omega_3 ((ħ c)/G)^(3\/2) 1/(mu_e m_u)^2 = 1.46 msun quad (mu_e = 2)$]),
    r([neutron star], [$1.4 msun$, $R approx 12 "km"$, nuclear density]),
  ))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1086/143324")[Chandrasekhar · ApJ 74, 81 (1931)] ·
    #link("https://doi.org/10.1146/annurev.astro.38.1.337")[Chabrier & Baraffe · ARA&A 38, 337 (2000)] ·
    #link("https://doi.org/10.1088/0004-637X/727/1/57")[Spiegel et al. · ApJ 727, 57 (2011)]])
]

// -------------------------------------- 3.8 Fusion under extreme conditions ---

#widget-page("extremes", section: "extreme", title: [Where fusion happens])

#photo-page("stars/gk-per-chandra-xray.jpg", [GK Persei: NASA/CXC/RIKEN/D. Takei et al., public domain], "photo-nova",
  section: "extreme", fit: "contain", title: [GK Persei, nova of 1901])

#slide(section: "extreme", title: [Novae: hot CNO on a white dwarf])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    r([system], [white dwarf accretes hydrogen from a companion]),
    r([ignition], [degenerate layer: heating without expansion, runaway]),
    r([hot CNO], [$T approx 2 "–" 3 times 10^8 "K"$: capture faster than $beta^+$ decay of #super[14]O (71 s), #super[15]O (122 s)]),
    r([ejecta], [$10^(-5) "–" 10^(-4) msun$, rich in #super[13]C, #super[15]N, #super[17]O]),
  ))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1086/305244")[José & Hernanz · ApJ 494, 680 (1998)]])
]

#photo-page("stars/tycho-snr-chandra.jpg", [Tycho's supernova remnant: NASA/CXC/Rutgers/J. Warren & J. Hughes et al., public domain], "photo-tycho",
  section: "extreme", fit: "contain", title: [Tycho's supernova, 1572])

#slide(section: "extreme", title: [Type Ia supernova: a carbon bomb])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    r([progenitor], [C/O white dwarf grows towards $M_"Ch"$]),
    r([ignition], [$rho_c approx 2 times 10^12 "kg"\/"m"^3$, degenerate: no thermostat]),
    r([energy], [C, O $-> ""^56"Ni"$: $0.81 "MeV"$ per nucleon $times 1.4 msun = 2 times 10^44 "J"$ #h(2mm) #text(fill: muted)[> binding]]),
    r([light], [$""^56"Ni" ->^(6.1 "d") ""^56"Co" ->^(77 "d") ""^56"Fe"$]),
  ))
  #at(2, 10, y: 104mm, result-box([fusion unbinds the whole star], [no remnant · about 0.6 $msun$ of #super[56]Ni]))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1146/annurev.astro.38.1.191")[Hillebrandt & Niemeyer · ARA&A 38, 191 (2000)]])
]

#photo-page("stars/crab-nebula-webb.jpg", [Crab Nebula: NASA, ESA, CSA, STScI, T. Temim (Princeton University), CC BY 4.0], "photo-crab",
  section: "extreme", fit: "contain", title: [Crab Nebula, supernova of 1054])

#slide(section: "extreme", title: [Core collapse: gravity, not fusion])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    r([iron core], [no fusion energy left: $B\/A$ is maximal]),
    r([collapse], [photodisintegration, electron capture; bounce at nuclear density]),
    r([energy], [$3/5 (G M^2)/R = 3 times 10^46 "J"$ #h(2mm) #text(fill: muted)[(1.4 $msun$, 12 km), 99 % neutrinos]]),
    r([SN 1987A], [24 neutrinos in Kamiokande-II, IMB, Baksan; $0.07 msun$ of #super[56]Ni]),
  ))
  #at(2, 10, y: 104mm, result-box([fusion builds the core and burns the ejecta], [explosive Si and O burning]))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/PhysRevLett.58.1490")[Hirata et al. · PRL 58, 1490 (1987)] ·
    #link("https://doi.org/10.1103/PhysRevLett.58.1494")[Bionta et al. · PRL 58, 1494 (1987)] ·
    #link("https://doi.org/10.1146/annurev.aa.27.090189.003213")[Arnett et al. · ARA&A 27, 629 (1989)] ·
    #link("https://doi.org/10.1016/j.physrep.2007.02.002")[Janka et al. · Phys. Rep. 442, 38 (2007)]])
]

#photo-page("stars/neutron-star-merger-eso-illustration.jpg", [Illustration: ESO/L. Calçada/M. Kornmesser, CC BY 4.0], "photo-merger",
  section: "extreme", title: [Neutron-star merger (illustration)])

#slide(section: "extreme", title: [Neutron stars: bursts, crusts, mergers])[
  #at(1, 12, y: 0mm, steps(gap: 9mm,
    r([X-ray burst], [accreted H, He ignite: He flash, rapid proton capture up to Sn–Te in seconds]),
    r([crust], [pycnonuclear fusion: zero-point motion in a lattice, density instead of temperature]),
    r([merger], [GW170817: neutron capture (r process), kilonova · not fusion]),
    r([on Earth], [muon-catalysed fusion is fusion by density too (Chapter 9)]),
  ))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1103/PhysRevLett.86.3471")[Schatz et al. · PRL 86, 3471 (2001)] ·
    Haensel & Zdunik · A&A 227, 431 (1990) ·
    #link("https://doi.org/10.1103/PhysRevLett.119.161101")[LIGO/Virgo · PRL 119, 161101 (2017)]])
]

#slide(section: "extreme", title: [Where the elements come from])[
  #at(1, 12, y: 0mm, align(center, deck-fig("abundances", columns: 12)))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1051/0004-6361/202140445")[Asplund, Amarsi & Grevesse · A&A 653, A141 (2021), CC BY 4.0] ·
    #link("https://doi.org/10.1103/RevModPhys.29.547")[Burbidge, Burbidge, Fowler & Hoyle · Rev. Mod. Phys. 29, 547 (1957)]])
]

#slide(section: "extreme", title: [Stars and fusion on Earth])[
  #at(2, 10, y: 4mm, data-table(
    ([], [star], [reactor]),
    (
      ([confinement], [gravity, $tau_E tilde 10^7 "yr"$], [magnetic field, $tau_E tilde "s"$]),
      ([fuel], [p–p, $S tilde 10^(-22) "keV b"$], [D–T, $S tilde 10^4 "keV b"$]),
      ([temperature], [1.35 keV], [10–20 keV]),
      ([power density], [$262 "W"\/"m"^3$], [$tilde "MW"\/"m"^3$]),
      ([control], [negative heat capacity], [heating and feedback]),
    ),
  ))
]

#credits-page((
  ("photo-sun", [NASA/SDO (AIA), the Sun, public domain], "sdo.gsfc.nasa.gov"),
  ("photo-cmb", [NASA/WMAP Science Team, nine-year sky, public domain], "commons.wikimedia.org"),
  ("photo-carina", [NASA, ESA, N. Smith, Hubble Heritage Team, CC BY 4.0], "esahubble.org"),
  ("photo-ring", [ESA/Webb, NASA, CSA, M. Barlow, N. Cox, R. Wesson, CC BY 4.0], "esawebb.org"),
  ("photo-nova", [NASA/CXC/RIKEN/D. Takei et al., public domain], "chandra.harvard.edu/photo/2015/gkper"),
  ("photo-tycho", [NASA/CXC/Rutgers/J. Warren & J. Hughes et al., public domain], "chandra.harvard.edu"),
  ("photo-crab", [NASA, ESA, CSA, STScI, T. Temim, CC BY 4.0], "esawebb.org/images/weic2326a"),
  ("photo-merger", [ESO/L. Calçada/M. Kornmesser, illustration, CC BY 4.0], "eso.org"),
), [Data: MIST (Dotter 2016; Choi et al. 2016), LINX/PRIMAT, Model S, AME2020, Asplund et al. 2021, B16, Heger et al. 2003. Plots, widgets, calculations: Christopher Albert, CC BY 4.0.])
