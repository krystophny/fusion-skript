#import "theme.typ": *
#show: deck.with(chapter: 4)

// A formula row: muted step label, then the formula (as in deck 02).
#let r(name, f) = ([#text(fill: muted, name)], f)
#let steps(..items, gap: 8mm) = grid(columns: (auto, 1fr), column-gutter: 7mm, row-gutter: gap,
  align: (right + horizon, left + horizon), ..items.pos().flatten())
#let cite-line(body) = text(size: 12pt, body)
#let sv = $chevron.l sigma v chevron.r$

#slide(section: "alpha-neutron", title: [Alpha and neutron])[
  #at(1, 12, y: 0mm, align(center, deck-fig("alpha_neutron_split", columns: 11)))
  #at(3, 8, y: 112mm, result-box($E_alpha = 3.5 "MeV", quad E_n = 14.1 "MeV"$, [$alpha$ heats the plasma, $n$ the blanket]))
]

#slide(section: "fusion-power", title: [Fusion power density])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([fuel], $n_"D" + n_"T" = n, quad n_"D" n_"T" = n^2 x (1 - x)$),
    r([optimum], $x = 1\/2$),
  ))
  #at(3, 8, y: 46mm, result-box($p_alpha = n^2/4 sv E_alpha, quad p_"fus" = n^2/4 sv E_"fus"$, none))
  #at(1, 12, y: 100mm, align(center)[$n = 10^20 "m"^(-3)$, $14 "keV"$: #h(3mm) $p_"fus" = 1.7 "MW"\/"m"^3$])
]

#slide(section: "confinement-time", title: [Stored energy and confinement time])[
  #at(1, 6, y: 0mm, steps(gap: 7mm,
    r([quasineutral], $n_e = n_"D" + n_"T" = n$),
    r([stored], $W = 3 n k_B T$),
    r([losses], $p_"loss" = W \/ tau_E$),
  ))
  #at(1, 6, y: 70mm, result-box($p_"ext" + p_alpha = W \/ tau_E$, [steady state]))
  #at(7, 6, y: -4mm, deck-fig("density_scaling", columns: 6))
]

#slide(section: "power-balance", title: [Power balance with gain])[
  #at(1, 6, y: 0mm, steps(gap: 7mm,
    r([gain], $Q = p_"fus" \/ p_"ext"$),
    r([$E_"fus" approx 5 E_alpha$], $f_alpha = p_alpha / (p_alpha + p_"ext") = Q/(Q + 5)$),
  ))
  #at(1, 6, y: 54mm, data-table(
    ([$Q$], [], [$f_alpha$]),
    (
      ([$1$], [break-even], [$1\/6$]),
      ([$5$], [burning plasma], [$1\/2$]),
      ([$infinity$], [ignition], [$1$]),
    ),
    align: (right, left, right),
  ))
  #at(7, 6, y: -4mm, deck-fig("alpha_fraction", columns: 6))
]

#slide(section: "power-balance", title: [Triple product])[
  #at(1, 12, y: 0mm, steps(gap: 8mm,
    r([ignition], $n^2/4 sv E_alpha = (3 n k_B T)/tau_E$),
    r([10–20 keV], [$sv prop T^2$ #h(4mm) #text(fill: muted)[so $n T tau_E$ is constant]]),
  ))
  #at(2, 10, y: 50mm, result-box($n k_B T tau_E = (12 (k_B T)^2)/(sv E_alpha) approx 3 times 10^21 "keV s m"^(-3)$,
    [$= 5 "bar s"$ ion pressure, #h(2mm) $10 "bar s"$ ion + electron pressure]))
]

#slide(section: "power-balance", title: [How good is $sv approx c T^2$?])[
  #at(1, 12, y: 0mm, align(center, deck-fig("reactivity", columns: 11)))
  #at(1, 12, y: 116mm, align(center, text(size: 16pt)[within 20 %: #h(2mm) *D–T 8–23 keV* #h(3mm) D–D 7.5–36 keV #h(3mm) D–#super[3]He 36–94 keV #h(3mm) p–#super[11]B 91–218 keV]))
  #at(1, 12, y: 128mm, align(center, text(size: 14pt, fill: muted)[$c$: maximum of $sv \/ T^2$ for each fuel (grey band)]))
  #at(1, 12, y: 140mm, cite-line[
    #link("https://doi.org/10.1088/0029-5515/32/4/I07")[Bosch & Hale · Nucl. Fusion 32, 611 (1992)] ·
    #link("https://doi.org/10.1088/0029-5515/40/4/310")[Nevins & Swain · Nucl. Fusion 40, 865 (2000)]])
]

#widget-page("lawson", section: "power-balance", title: [$n tau_E$ or $n T tau_E$?])

#slide(section: "power-balance", title: [Lawson plane])[
  #at(1, 8, y: 0mm, deck-fig("lawson_plane", columns: 8))
  #at(9, 4, y: 30mm, steps(gap: 7mm,
    r([gain $Q$], $n T tau_E prop Q / (Q + 5)$),
  ))
  #at(9, 4, y: 58mm, result-box([$Q = 10$: #h(1mm) $2\/3$], [of the ignition value; #linebreak() minimum near 13.5 keV]))
  #at(1, 12, y: 142mm, cite-line[
    #link("https://doi.org/10.1088/0029-5515/32/4/I07")[Bosch & Hale · Nucl. Fusion 32, 611 (1992)] · #link("https://krystophny.github.io/fusion-skript/notebooks/lawson.html")[notebook: Lawson criterion]])
]

// Two closures of one balance: Lawson's loop through a converter, and alphas kept in the plasma.
#let loop-node(pos, body, color: ink) = node(pos, body, stroke: 0.8pt + color, corner-radius: 1.5mm,
  inset: 5mm, width: 42mm)
#slide(section: "plant-gain", title: [Lawson 1957 and self-heating])[
  #set text(size: 17pt)
  #at(1, 6, y: 0mm)[
    #block-label[Lawson 1957]
    #v(4mm)
    #align(center, fletcher.diagram(spacing: (34mm, 16mm), edge-stroke: 0.8pt + ink,
      loop-node((0, 0), [plasma], color: ink),
      loop-node((1, 0), [converter $eta$], color: plot-blue),
      edge((0, 0), (1, 0), "-|>", text(fill: muted, $P_"fus" + P_"loss"$), bend: 40deg, label-sep: 2mm),
      edge((1, 0), (0, 0), "-|>", text(fill: plot-blue)[heating $P_"loss"$], bend: 40deg, label-sep: 2mm,
        stroke: 0.8pt + plot-blue),
      edge((1, 0), (1, 1.4), "-|>", text(fill: muted)[net], label-side: left),
      node((1, 1.4), []),
    ))
  ]
  #at(7, 6, y: 0mm)[
    #block-label[Self-heating]
    #v(4mm)
    #align(center, fletcher.diagram(spacing: (16mm, 20mm), edge-stroke: 0.8pt + ink,
      edge((-1, 0), (0, 0), "-|>", text(fill: muted, $P_"ext"$)),
      loop-node((0, 0), [plasma], color: plot-orange),
      edge((0, 0), (0, 0), "-|>", text(fill: plot-orange, $P_alpha$), bend: 130deg, loop-angle: 90deg, stroke: 0.8pt + plot-orange),
      edge((0, 0), (1, 0), "-|>", text(fill: muted, $P_"loss"$)),
      edge((0, 0), (0, 1), "-|>", text(fill: muted, $P_n$), label-side: left),
      node((0, 1), text(fill: muted)[blanket]),
    ))
  ]
  #set text(size: body-size)
  #at(1, 6, y: 92mm, align(center)[$P_"fus" >= 2 P_"loss"$ #h(3mm) #text(fill: muted)[($eta = 1\/3$)]])
  #at(7, 6, y: 92mm, align(center)[$P_alpha >= P_"loss"$ #h(3mm) #text(fill: muted)[(ignition)]])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0370-1301/70/1/303")[Lawson · Proc. Phys. Soc. B 70, 6 (1957)] ·
    #link("https://doi.org/10.1063/5.0083990")[Wurzel & Hsu · Phys. Plasmas 29, 062103 (2022)]])
]

#slide(section: "confinement-routes", title: [Density and confinement time])[
  #at(1, 12, y: -2mm, align(center, deck-fig("n_tau_plane", columns: 12)))
  #at(1, 12, y: 146mm, cite-line[
    Data: #link("https://doi.org/10.1063/5.0083990")[Wurzel & Hsu · Phys. Plasmas 29, 062103 (2022)], Tables 6–8, CC BY 4.0])
]
