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
), [Data: MIST (Dotter 2016; Choi et al. 2016), LINX/PRIMAT, Model S, AME2020, Asplund et al. 2021, B16, Adelberger et al. 2011, Bond et al. 2017, Heger et al. 2003. Plots, widgets, calculations: Christopher Albert, CC BY 4.0.])
