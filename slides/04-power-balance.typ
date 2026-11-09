#import "theme.typ": *
#show: deck.with(chapter: 4)

// A formula row: muted step label, then the formula (as in deck 02).
#let r(name, f) = ([#text(fill: muted, name)], f)
#let steps(..items, gap: 8mm) = grid(columns: (auto, 1fr), column-gutter: 7mm, row-gutter: gap,
  align: (right + horizon, left + horizon), ..items.pos().flatten())
#let cite-line(body) = text(size: 12pt, body)
#let sv = $chevron.l sigma v chevron.r$

#slide(section: "alpha-neutron", title: [Momentum and energy])[
  #at(1, 12, y: 0mm, steps(
    r([fuel at rest], [$bold(p)_"D" + bold(p)_"T" approx 0$ #h(5mm) #text(fill: muted)[$k_B T approx 10 "keV" << E_"fus"$]]),
    r([momentum], $bold(p)_alpha = -bold(p)_n, quad |bold(p)_alpha| = |bold(p)_n| = p$),
    r([$E = p^2 \/ 2m$], $E_alpha / E_n = m_n / m_alpha approx 1/4$),
    r([$E_alpha + E_n = E_"fus"$], $E_alpha = E_"fus" m_n/(m_n + m_alpha) approx E_"fus" \/ 5$),
  ))
  #at(3, 8, y: 80mm, result-box($E_alpha = 3.5 "MeV", quad E_n = 14.1 "MeV"$, [$alpha$ heats the plasma, $n$ goes to the blanket]))
]

#slide(section: "alpha-neutron", title: [Alpha and neutron])[
  #at(1, 12, y: 0mm, align(center, deck-fig("alpha_neutron_split", columns: 11)))
]

#slide(section: "fusion-power", title: [Fusion power density])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([fuel], $n = n_"D" + n_"T", quad x = n_"D" \/ n$),
    r([rate], $cal(R) = n_"D" n_"T" sv = n^2 x (1 - x) sv$),
    r([maximum], $dif \/ dif x thin (x - x^2) = 0 quad => quad x = 1\/2$),
  ))
  #at(3, 8, y: 50mm, result-box($p_"fus" = n^2/4 sv E_"fus", quad p_alpha = n^2/4 sv E_alpha$, [$E_"fus" = 17.6 "MeV"$, $n_e = n$]))
  #at(1, 12, y: 112mm, steps(gap: 6mm,
    r([$n = 10^20 "m"^(-3)$, $14 "keV"$], [$sv = 2.4 times 10^(-22) "m"^3\/"s" quad => quad p_"fus" = 1.7 "MW"\/"m"^3$]),
  ))
]

#slide(section: "confinement-time", title: [Stored energy and confinement time])[
  #at(1, 6, y: 0mm, steps(gap: 7mm,
    r([per particle], $chevron.l m v^2 \/ 2 chevron.r = 3/2 k_B T$),
    r([$n_e + n_"D" + n_"T" = 2 n$], $W = 3 n k_B T$),
    r([confinement time], $p_"loss" = W \/ tau_E prop n$),
    r([alpha heating], $p_alpha = n^2/4 sv E_alpha prop n^2$),
  ))
  #at(1, 6, y: 90mm, result-box($p_"loss" = p_alpha + p_"ext"$, [steady state]))
  #at(7, 6, y: -4mm, deck-fig("density_scaling", columns: 6))
  #at(1, 12, y: 150mm, cite-line[#link("https://krystophny.github.io/fusion-skript/notebooks/scaling.html")[notebook: confinement scaling IPB98(y,2)]])
]

#slide(section: "power-balance", title: [Power balance with gain])[
  #at(1, 7, y: 0mm, steps(gap: 7mm,
    r([heating needed], $p_"ext" = (3 n k_B T)/tau_E - n^2/4 sv E_alpha$),
    r([gain], $Q = p_"fus" \/ p_"ext"$),
    r([$E_"fus" approx 5 E_alpha$], $p_"ext" = 5 p_alpha \/ Q$),
    r([], $p_"loss" = p_alpha (1 + 5\/Q)$),
    r([self-heating], $f_alpha = p_alpha \/ (p_alpha + p_"ext") = Q \/ (Q + 5)$),
  ))
  #at(8, 5, y: 2mm, data-table(
    ([$Q$], [], [$f_alpha$]),
    (
      ([$1$], [break-even], [$1\/6$]),
      ([$5$], [burning plasma], [$1\/2$]),
      ([$10$], [], [$2\/3$]),
      ([$infinity$], [ignition], [$1$]),
    ),
    align: (right, left, right),
  ))
  #at(8, 5, y: 64mm, deck-fig("alpha_fraction", columns: 5))
]

#slide(section: "power-balance", title: [Triple product])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([balance], $(3 n k_B T)/tau_E = n^2/4 sv E_alpha (1 + 5\/Q)$),
    r([$times k_B T$], $n k_B T tau_E = (12 (k_B T)^2)/(E_alpha sv (1 + 5\/Q))$),
    r([10–20 keV], [$sv approx 1.1 times 10^(-24) T^2 "m"^3"/s"$ #h(4mm) #text(fill: muted)[$T$ drops out]]),
  ))
  #at(1, 6, y: 76mm, result-box($n k_B T tau_E > 5 "bar s"$, [ignition: $3.1 times 10^21 "keV s m"^(-3)$ \ $p tau_E = 2 n k_B T tau_E > 10 "bar s"$]))
  #at(7, 6, y: 78mm, data-table(
    ([$Q$], [$p_"loss"$], [$n k_B T tau_E$], [$p tau_E$]),
    (
      ([$1$], [$6 p_alpha$], [0.8 bar s], [1.7 bar s]),
      ([$5$], [$2 p_alpha$], [2.5 bar s], [5 bar s]),
      ([$infinity$], [$p_alpha$], [5 bar s], [10 bar s]),
    ),
    align: (right, right, right, right),
  ))
  #at(7, 6, y: 128mm, text(size: 14pt, fill: muted)[exact $sv$: $2.7 times 10^21 "keV s m"^(-3)$ at 13.5 keV])
]

#slide(section: "power-balance", title: [Lawson plane])[
  #at(1, 12, y: 0mm, align(center, deck-fig("lawson_plane", columns: 12)))
  #at(1, 12, y: 130mm, align(center, text(fill: muted)[solid: no radiation #h(6mm) dashed: with bremsstrahlung (4.9)]))
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
  #at(1, 6, y: 86mm, steps(gap: 6mm,
    r([recycle], $eta (P_"fus" + P_"loss") >= P_"loss"$),
    r([$eta = 1\/3$], $P_"fus" >= 2 P_"loss"$),
  ))
  #at(7, 6, y: 86mm, steps(gap: 6mm,
    r([ignition], $P_alpha >= P_"loss"$),
    r([$Q -> infinity$], $P_"ext" = 0$),
  ))
  #at(1, 12, y: 128mm, text(fill: muted)[same triple product with $E_alpha -> E_"fus" eta \/ (1 - eta) = 8.8 "MeV"$])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0370-1301/70/1/303")[Lawson · Proc. Phys. Soc. B 70, 6 (1957)] ·
    #link("https://doi.org/10.1063/5.0083990")[Wurzel & Hsu · Phys. Plasmas 29, 062103 (2022)]])
]

#slide(section: "pressure-beta", title: [Fixed pressure])[
  #at(1, 6, y: 0mm, steps(gap: 7mm,
    r([pressure], $p = 2 n k_B T$),
    r([beta], $beta = (2 mu_0 p)/B^2$),
    r([$n = p \/ 2 k_B T$], $p_"fus" = p^2/16 sv/(k_B T)^2 E_"fus"$),
  ))
  #at(1, 6, y: 64mm, result-box($P_"fus" prop sv/(k_B T)^2 beta^2 B^4 V$, [maximum of $sv \/ T^2$: 13.5 keV]))
  #at(1, 6, y: 116mm, steps(gap: 6mm,
    r([density limit], $n_G = I_p \/ (pi a^2)$),
  ))
  #at(7, 6, y: -4mm, deck-fig("fixed_pressure", columns: 6))
  #at(1, 12, y: 136mm, text(size: 14pt, fill: muted)[$n_G$ in $10^20 "m"^(-3)$, $I_p$ in MA, $a$ in m])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0741-3335/44/8/201")[Greenwald · Plasma Phys. Control. Fusion 44, R27 (2002)]])
]

#slide(section: "confinement-routes", title: [Density and confinement time])[
  #at(1, 12, y: -2mm, align(center, deck-fig("n_tau_plane", columns: 12)))
  #at(1, 12, y: 134mm, text(size: 14pt, fill: muted)[magnetic: peak ion density, $tau_E^*$ #h(4mm) inertial: $n tau \/ tau_"stag"$ #h(4mm) Sun: $tau approx 3 times 10^7 "yr"$])
  #at(1, 12, y: 146mm, cite-line[
    Data: #link("https://doi.org/10.1063/5.0083990")[Wurzel & Hsu · Phys. Plasmas 29, 062103 (2022)], Tables 6–8, CC BY 4.0])
]

// ------------------------------------------------- 4.8 Where is the optimum? ---

#slide(section: "optimum", title: [Which temperature is optimal?])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([fixed $n, tau_E$], [max $sv \/ T$ #h(3mm) $=>$ #h(2mm) $25.7 "keV"$]),
    r([fixed $p, tau_E$], [max $sv \/ T^2$ #h(3mm) $=>$ #h(2mm) $13.5 "keV"$]),
    r([fixed $n$, max $P_"fus"$], [max $sv$ #h(3mm) $=>$ #h(2mm) $66.7 "keV"$]),
  ))
  #at(2, 10, y: 62mm, result-box([optimum depends on what is held fixed], none))
  #at(1, 12, y: 104mm, steps(gap: 7mm,
    r([$sv prop T^m$], $n k_B T tau_E prop T^(2 - m) quad => quad "minimum at" m = 2$),
    r([broad], [within 10 % of the minimum for 9.7–19 keV]),
  ))
]

#widget-page("limits", section: "optimum", title: [Density and pressure limits])

#slide(section: "optimum", title: [Limits and confinement scaling])[
  #at(1, 12, y: 0mm, steps(gap: 6mm,
    r([limits], $n <= n_max, quad p <= p_max = beta_max B^2 \/ 2 mu_0$),
    r([crossing], [$T_times = p_max \/ 2 n_max$ #h(4mm) #text(fill: muted)[optimum: $T_times$ clamped to 13.5–25.7 keV]]),
    r([tokamak], [$T_times approx 0.39 thin beta_N a B \/ f_"GW" "keV"$ #h(4mm) #text(fill: muted)[ITER 8.8 keV, EU-DEMO 13.8 keV]]),
    r([stellarator], [no Greenwald limit]),
  ))
  #at(1, 12, y: 70mm, steps(gap: 6mm,
    r([IPB98(y,2)], $tau_E = 0.0562 thin H thin I^0.93 B^0.15 overline(n)_19^0.41 P^(-0.69) R^1.97 epsilon^0.58 kappa^0.78 M^0.19$),
    r([ISS04], $tau_E = 0.134 thin H thin a^2.28 R^0.64 overline(n)_19^0.54 B^0.84 P^(-0.61) iota_(2\/3)^0.41$),
  ))
  #at(1, 12, y: 106mm, result-box([$tau_E prop P^(-0.7)$ #h(3mm) $=>$ #h(2mm) optimum $approx 6$–$9 "keV"$], none))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0029-5515/39/12/302")[ITER Physics Basis · Nucl. Fusion 39, 2175 (1999)] ·
    #link("https://doi.org/10.1088/0029-5515/45/12/024")[Yamada et al. · Nucl. Fusion 45, 1684 (2005)] ·
    #link("https://doi.org/10.1088/0741-3335/44/8/201")[Greenwald · PPCF 44, R27 (2002)]])
]

#widget-page("popcon", section: "optimum", title: [Operating space of a device])

#widget-page("machines", section: "optimum", title: [Where present machines stand])

#slide(section: "bremsstrahlung", title: [Bremsstrahlung and ideal ignition])[
  #at(1, 6, y: 0mm, steps(gap: 7mm,
    r([electron–ion], $p_"br" = C_B n_e^2 Z_"eff" sqrt(k_B T)$),
    r([charge], $Z_"eff" = sum_j n_j Z_j^2 \/ n_e$),
    r([$p_alpha = p_"br"$], $n^2/4 sv E_alpha = C_B n^2 Z_"eff" sqrt(k_B T)$),
    r([$n$ cancels], $sv E_alpha = 4 C_B Z_"eff" sqrt(k_B T)$),
  ))
  #at(1, 6, y: 74mm, result-box($k_B T_"ideal" = 4.3 "keV"$, [D–T, $Z_"eff" = 1$, any $n$]))
  #at(7, 6, y: -4mm, deck-fig("alpha_brems", columns: 6))
  #at(1, 12, y: 118mm, text(fill: muted)[$C_B = 5.34 times 10^(-37) "W m"^3 "keV"^(-1\/2)$ #h(5mm) $= 1.69 times 10^(-38) "W m"^3 "eV"^(-1\/2)$])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0370-1301/70/1/303")[Lawson · Proc. Phys. Soc. B 70, 6 (1957)] ·
    NRL Plasma Formulary · #link("https://doi.org/10.1063/5.0083990")[Wurzel & Hsu · Phys. Plasmas 29, 062103 (2022)]])
]

#slide(section: "dilution", title: [Helium ash])[
  #at(1, 12, y: 0mm, align(center, deck-fig("impurity_dilution", columns: 12)))
  #at(1, 12, y: 130mm, align(center, text(fill: muted)[helium concentration $c$: #h(2mm) fuel $1 - 2c$, #h(2mm) $Z_"eff" = 1 + 2c$]))
  #at(1, 12, y: 146mm, cite-line[#link("https://krystophny.github.io/fusion-skript/notebooks/impurities.html")[notebook: impurities and fuel dilution]])
]
