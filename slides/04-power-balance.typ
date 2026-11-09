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
  #at(9, 4, y: 112mm, text(size: 14pt, fill: muted)[dashed: with bremsstrahlung (4.7)])
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

#widget-page("bremsstrahlung", section: "bremsstrahlung", title: [How bremsstrahlung arises])

#slide(section: "bremsstrahlung", title: [Bremsstrahlung from one pass])[
  #at(1, 12, y: 0mm, steps(gap: 6mm,
    r([Larmor], $P = (e^2 a^2)/(6 pi epsilon_0 c^3)$),
    r([Coulomb kick], [$a approx (Z e^2)/(4 pi epsilon_0 m_e b^2), quad Delta t approx (2 b)/v$]),
    r([one pass], $Delta E = P Delta t prop Z^2 / (b^3 v)$),
    r([passes], [$n_i v thin 2 pi b thin d b$ #h(3mm) per second, #h(2mm) $b >= b_"min" = ℏ \/ (m_e v)$]),
    r([one electron], $P_e = integral_(b_"min")^infinity Delta E thin n_i v thin 2 pi b thin d b prop Z^2 n_i / b_"min" prop Z^2 n_i v$),
  ))
  #at(2, 10, y: 98mm, result-box($p_"br" = C_B thin Z^2 n_e n_i sqrt(k_B T)$, [Maxwell: $chevron.l v chevron.r prop sqrt(T)$ #h(3mm) estimate $8.4$, exact $5.34 times 10^(-37) "W m"^3 "keV"^(-1\/2)$]))
  #at(1, 12, y: 146mm, cite-line[NRL Plasma Formulary · Jackson, Classical Electrodynamics, §15.2])
]

#slide(section: "bremsstrahlung", title: [Bremsstrahlung and ideal ignition])[
  #at(1, 6, y: 0mm, steps(gap: 7mm,
    r([electron–ion], $p_"br" = C_B n_e^2 Z_"eff" sqrt(k_B T)$),
    r([$p_alpha = p_"br"$], [$sv E_alpha = 4 C_B Z_"eff" sqrt(k_B T)$ #h(3mm) #text(fill: muted)[$n$ cancels]]),
  ))
  #at(1, 6, y: 50mm, result-box($k_B T_"ideal" = 4.3 "keV"$, [D–T, $Z_"eff" = 1$, any density]))
  #at(7, 6, y: -4mm, deck-fig("alpha_brems", columns: 6))
  #at(1, 12, y: 134mm, text(size: 14pt, fill: muted)[$C_B = 5.34 times 10^(-37) "W m"^3 "keV"^(-1\/2)$])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0370-1301/70/1/303")[Lawson · Proc. Phys. Soc. B 70, 6 (1957)] · NRL Plasma Formulary])
]

#slide(section: "bremsstrahlung", title: [Line radiation])[
  #at(1, 6, y: 0mm, steps(gap: 6mm,
    r([excite], [electron hits ion, bound electron jumps up]),
    r([decay], [photon $h nu = E_"upper" - E_"lower"$]),
    r([coronal], [every excitation ends in a photon]),
    r([power], $p_Z = n_e n_Z L_Z (T_e)$),
  ))
  #at(1, 6, y: 72mm, result-box([needs bound electrons], [light ions bare at 10 keV: $L_Z -> Z^2 C_B sqrt(T)$ #linebreak() W keeps electrons: $L_W approx 10^(-31) "W m"^3$]))
  #at(7, 6, y: -4mm, deck-fig("cooling_rates", columns: 6))
  #at(1, 12, y: 146mm, cite-line[Mavrin · Radiat. Eff. Defects Solids 173, 388 (2018) · Pütterich et al. · Nucl. Fusion 50, 025012 (2010)])
]

#widget-page("spectrum", section: "bremsstrahlung", title: [Where a plasma radiates])

#slide(section: "bremsstrahlung", title: [Cyclotron radiation])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([one electron], $P = (e^4 B^2 v_perp^2)/(6 pi epsilon_0 m_e^2 c^3)$),
    r([Maxwellian], $p_"cyc" approx 6.2 times 10^(-17) thin n_e thin k_B T_e thin B^2 thick "W m"^(-3)$),
  ))
  #at(1, 12, y: 46mm, text(fill: muted)[$10^20 "m"^(-3)$, $10 "keV"$, $5 "T"$ #h(2mm) [MW m#super[−3]]:])
  #at(3, 8, y: 56mm, data-table(
    ([$p_"fus"$], [$p_"br"$], [$p_"cyc"$ emitted]),
    (([0.8], [0.017], [1.6]),),
    align: (center, center, center),
  ))
  #at(2, 10, y: 86mm, result-box([optically thick: mostly reabsorbed, walls reflect],
    [grows with $T_e$ and $B$: a main loss for D–#super[3]He and p–#super[11]B]))
  #at(1, 12, y: 134mm, text(size: 14pt, fill: muted)[$n_e$ in m#super[−3], $k_B T_e$ in keV, $B$ in T #h(6mm) pairs need $2 m_e c^2 = 1.02 "MeV"$: negligible for $k_B T << 511 "keV"$])
  #at(1, 12, y: 146mm, cite-line[NRL Plasma Formulary])
]

#slide(section: "dilution", title: [Quasineutrality and dilution])[
  #at(1, 12, y: 0mm, steps(gap: 6mm,
    r([quasineutral], [$n_e = n_"D" + n_"T" + sum_Z Z n_Z$ #h(3mm) $c_Z = n_Z \/ n_e$]),
    r([fuel], [$f = (n_"D" + n_"T") \/ n_e = 1 - sum_Z Z c_Z$, #h(3mm) $p_"fus" prop f^2 n_e^2$]),
    r([stored], $W = 3/2 (n_e + n_i) k_B T$),
    r([losses], [$C_B f n_e^2 sqrt(T)$ (fuel) #h(2mm) $+ sum_Z n_e n_Z L_Z (T)$ (impurities)]),
  ))
  #at(1, 12, y: 66mm, result-box($n_e T tau_E = (3/2 (1 + n_i \/ n_e) T^2)/(f^2 sv E_alpha \/ 4 - C_B f sqrt(T) - sum_Z c_Z L_Z (T))$,
    [W: displaces 74 fuel ions and radiates; $c_W = 3 times 10^(-5)$: minimum +9 % (0-D, coronal)]))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0029-5515/50/2/025012")[Pütterich et al. · Nucl. Fusion 50, 025012 (2010)] · Mavrin · Radiat. Eff. Defects Solids 173, 388 (2018)])
]

#widget-page("impurities", section: "dilution", title: [Impurities: dilution and radiation])

#slide(section: "dilution", title: [Helium ash])[
  #at(1, 12, y: 0mm, align(center, deck-fig("impurity_dilution", columns: 12)))
  #at(1, 12, y: 130mm, align(center, text(fill: muted)[helium concentration $c$: #h(2mm) fuel $1 - 2c$, #h(2mm) $Z_"eff" = 1 + 2c$]))
  #at(1, 12, y: 146mm, cite-line[#link("https://krystophny.github.io/fusion-skript/notebooks/impurities.html")[notebook: impurities and fuel dilution]])
]
