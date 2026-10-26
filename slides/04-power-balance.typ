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
    r([D + T at rest], [$bold(p)_"D" + bold(p)_"T" approx 0$ #h(5mm) #text(fill: muted)[$k_B T approx 10 "keV" << Q_"DT"$]]),
    r([momentum], $bold(p)_alpha + bold(p)_n = 0 quad => quad |bold(p)_alpha| = |bold(p)_n| = p$),
    r([energy], $E_alpha + E_n = Q_"DT" = 17.6 "MeV"$),
    r([$E = p^2 \/ 2m$], $E_alpha / E_n = (p^2 \/ 2 m_alpha)/(p^2 \/ 2 m_n) = m_n / m_alpha approx 1/4$),
    r([], $E_alpha = Q_"DT" m_n/(m_n + m_alpha), quad E_n = Q_"DT" m_alpha/(m_n + m_alpha)$),
  ))
  #at(3, 8, y: 92mm, result-box($E_alpha = 3.5 "MeV", quad E_n = 14.1 "MeV"$,
    [the lighter particle takes the larger energy]))
]

#slide(section: "alpha-neutron", title: [Alpha and neutron])[
  #at(1, 12, y: 0mm, align(center, deck-fig("alpha_neutron_split", columns: 11)))
]

#slide(section: "fusion-power", title: [Fusion power density])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([rate], $R = n_"D" n_"T" sv$ + [#h(5mm) #text(fill: muted)[section 2.20, $delta_"DT" = 0$]]),
    r([power], $p_"fus" = n_"D" n_"T" sv E_"fus", quad E_"fus" = 17.6 "MeV"$),
    r([quasineutral], $n_e = n_"D" + n_"T", quad n_"D" = x n_e, quad n_"T" = (1 - x) n_e$),
    r([mixture], [$n_"D" n_"T" = x (1 - x) n_e^2$ #h(5mm) #text(fill: muted)[maximal at] $x = 1\/2$]),
  ))
  #at(3, 8, y: 56mm, result-box($p_"fus" = n_e^2/4 sv E_"fus"$, [two-body: $prop n^2$]))
  #at(1, 12, y: 114mm, steps(gap: 6mm,
    r([alpha, neutron], $p_alpha = E_alpha/E_"fus" thin p_"fus" approx p_"fus" \/ 5, quad p_n approx 4/5 thin p_"fus"$),
    r([$n_e = 10^20 "m"^(-3)$, $14 "keV"$], [$sv = 2.4 times 10^(-22) "m"^3\/"s", quad p_"fus" = 1.7 "MW"\/"m"^3$]),
  ))
]

#slide(section: "confinement-time", title: [Stored energy and confinement time])[
  #at(1, 6, y: 0mm, steps(gap: 7mm,
    r([thermal energy], $W = 3/2 n_e k_B T + 3/2 n_i k_B T$),
    r([$n_e = n_i = n$], $W = 3 n k_B T$),
    r([definition], $tau_E = W \/ p_"loss"$),
    r([loss], $p_"loss" = 3 n k_B T \/ tau_E prop n$),
    r([alpha heating], $p_alpha = n^2/4 sv E_alpha prop n^2$),
  ))
  #at(1, 6, y: 86mm, result-box($n tau_E >= (12 k_B T)/(sv E_alpha)$, [$p_alpha >= p_"loss"$, no radiation]))
  #at(7, 6, y: -4mm, deck-fig("density_scaling", columns: 6))
  #at(1, 12, y: 140mm, text(size: 14pt, fill: muted)[$W$, $p$: per volume #h(5mm) $T_e = T_i = T$ #h(5mm) $tau_E$: all losses not counted separately])
  #at(1, 12, y: 150mm, cite-line[#link("https://krystophny.github.io/fusion-skript/notebooks/scaling.html")[notebook: confinement scaling IPB98(y,2)]])
]

#slide(section: "bremsstrahlung", title: [Bremsstrahlung and ideal ignition])[
  #at(1, 6, y: 0mm, steps(gap: 7mm,
    r([electron–ion], $p_"br" = C_B n_e^2 Z_"eff" sqrt(k_B T)$),
    r([charge], $Z_"eff" = sum_j n_j Z_j^2 \/ n_e$),
    r([alpha heating], $p_alpha = n_e^2/4 sv E_alpha$),
    r([$p_alpha = p_"br"$], $sv E_alpha = 4 C_B Z_"eff" sqrt(k_B T)$),
  ))
  #at(1, 6, y: 74mm, result-box($k_B T_"ideal" = 4.3 "keV"$, [D–T, $Z_"eff" = 1$, any $n$]))
  #at(7, 6, y: -4mm, deck-fig("alpha_brems", columns: 6))
  #at(1, 12, y: 114mm, steps(gap: 5mm,
    r([$k_B T$ in keV], [$C_B = 5.34 times 10^(-37) "W m"^3 "keV"^(-1\/2)$]),
    r([$k_B T$ in eV], [$C_B = 1.69 times 10^(-38) "W m"^3 "eV"^(-1\/2)$ #h(4mm) #text(fill: muted)[factor $sqrt(1000)$]]),
  ))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0370-1301/70/1/303")[Lawson · Proc. Phys. Soc. B 70, 6 (1957)] ·
    NRL Plasma Formulary · #link("https://doi.org/10.1063/5.0083990")[Wurzel & Hsu · Phys. Plasmas 29, 062103 (2022)]])
]

#slide(section: "power-balance", title: [Power balance with gain])[
  #at(1, 7, y: 0mm, steps(gap: 7mm,
    r([steady state], $p_"ext" + p_alpha = p_"loss" = 3 n k_B T \/ tau_E$),
    r([gain], $Q = P_"fus" \/ P_"ext" quad => quad p_"ext" = p_"fus" \/ Q$),
    r([insert], $n^2/4 sv (E_alpha + E_"fus"/Q) = (3 n k_B T)/tau_E$),
  ))
  #at(1, 7, y: 62mm, result-box($n tau_E = (12 k_B T)/(sv (E_alpha + E_"fus" \/ Q))$, none))
  #at(1, 12, y: 112mm, steps(
    r([self-heating], $f_alpha = P_alpha/(P_alpha + P_"ext") = Q/(Q + E_"fus" \/ E_alpha) approx Q/(Q + 5)$),
  ))
  #at(8, 5, y: 2mm, data-table(
    ([$Q$], [], [$f_alpha$]),
    (
      ([$1$], [breakeven], [$1\/6$]),
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
    r([times $T$], $n T tau_E = (12 T^2)/(sv (E_alpha + E_"fus" \/ Q))$),
    r([10–20 keV], [$sv approx 1.1 times 10^(-24) "m"^3"s"^(-1) T^2$ #h(4mm) #text(fill: muted)[$T$ in keV]]),
    r([ignition], [$n T tau_E approx 12 \/ (1.1 times 10^(-24) dot 3.5 times 10^3) = 3.1 times 10^21 "keV s m"^(-3)$ #h(4mm) #text(fill: muted)[no $T$]]),
  ))
  #at(1, 12, y: 62mm, result-box($n T tau_E >= 2.7 times 10^21 "keV s m"^(-3)$,
    [ignition, minimum at $13.5 "keV"$ #h(4mm) with bremsstrahlung: $2.9 times 10^21$ at $14 "keV"$]))
  #at(1, 12, y: 116mm, steps(gap: 6mm,
    r([pressure units], [$n k_B T tau_E = 4.4 times 10^5 "Pa s", quad p tau_E = 2 n k_B T tau_E approx 9 "bar s"$]),
    r([$Q = 1, 10$], [$n T tau_E = 0.46 times 10^21, quad 1.8 times 10^21 "keV s m"^(-3)$]),
  ))
]

#slide(section: "power-balance", title: [Lawson plane])[
  #at(1, 12, y: 0mm, align(center, deck-fig("lawson_plane", columns: 12)))
  #at(1, 12, y: 128mm, align(center, text(fill: muted)[
    $n T tau_E = 12 T^2 \/ (sv (E_alpha + E_"fus" \/ Q) - 4 C_B sqrt(T))$ #h(4mm) (dashed; solid: $C_B = 0$)]))
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
    r([], $eta (P_"fus" + P_"loss") >= P_"loss"$),
    r([$eta = 1\/3$], $P_"fus" >= 2 P_"loss"$),
    r([], $n tau_E >= (12 k_B T)/(sv E_"fus" thin eta \/ (1 - eta))$),
  ))
  #at(7, 6, y: 86mm, steps(gap: 6mm,
    r([], $P_alpha >= P_"loss"$),
    r([$Q -> infinity$], $P_"ext" = 0$),
    r([], $n tau_E >= (12 k_B T)/(sv E_alpha)$),
  ))
  #at(1, 12, y: 134mm, text(size: 14pt, fill: muted)[
    $E_"fus" thin eta\/(1 - eta) = 8.8 "MeV"$ against $E_alpha = 3.5 "MeV"$ #h(5mm) steady-state form; Lawson treated a heated pulse])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0370-1301/70/1/303")[Lawson · Proc. Phys. Soc. B 70, 6 (1957)] ·
    #link("https://doi.org/10.1063/5.0083990")[Wurzel & Hsu · Phys. Plasmas 29, 062103 (2022)]])
]

#slide(section: "plant-gain", title: [Engineering gain])[
  #at(1, 6, y: 0mm, steps(gap: 7mm,
    r([heat], $P_"th" = P_"fus" + P_"ext"$),
    r([electric], $P_"gross" = eta_"th" P_"th"$),
    r([heating], $P_"recirc" = P_"ext" \/ eta_"aux"$),
    r([definition], $Q_"eng" = (P_"gross" - P_"recirc")/P_"recirc"$),
  ))
  #at(1, 6, y: 72mm, result-box($Q_"eng" = eta_"th" eta_"aux" (Q + 1) - 1$, none))
  #at(1, 6, y: 108mm, steps(gap: 6mm,
    r([$Q_"eng" = 0$], $Q = 1\/(eta_"th" eta_"aux") - 1 = 5.25$),
    r([$Q_"eng" = 1$], $Q = 2\/(eta_"th" eta_"aux") - 1 = 11.5$),
  ))
  #at(7, 6, y: -4mm, deck-fig("q_eng", columns: 6))
  #at(1, 12, y: 134mm, text(size: 14pt, fill: muted)[
    $eta_"th" = eta_"aux" = 0.4$ #h(5mm) other plant loads (magnets, pumps, cryogenics) neglected #h(5mm)
    rule of thumb for a plant: $Q eta_"aux" >= 10$])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1063/5.0083990")[Wurzel & Hsu · Phys. Plasmas 29, 062103 (2022)]])
]

#slide(section: "plant-gain", title: [Power flow at $Q = 10$])[
  #at(1, 12, y: 0mm, align(center, deck-fig("power_flow", columns: 11)))
]

#slide(section: "dilution", title: [Quasineutrality and dilution])[
  #at(1, 7, y: 0mm, steps(gap: 7mm,
    r([quasineutral], $n_e = n_"D" + n_"T" + sum_Z Z n_Z$),
    r([concentration], $c_Z = n_Z \/ n_e$),
    r([fuel], $(n_"D" + n_"T") \/ n_e = 1 - sum_Z Z c_Z$),
    r([fixed $n_e$], $p_"fus" prop (1 - sum_Z Z c_Z)^2$),
    r([radiation], $Z_"eff" = 1 - sum_Z Z c_Z + sum_Z Z^2 c_Z$),
  ))
  #at(8, 5, y: 2mm, data-table(
    ([], [$Z c$], [fuel], [$p_"fus"$]),
    (
      ([0.1 % W], [$0.074$], [$0.926$], [$0.86$]),
      ([5 % He], [$0.10$], [$0.90$], [$0.81$]),
    ),
    align: (left, right, right, right),
  ))
  #at(8, 5, y: 48mm, text(fill: muted)[tungsten: line radiation dominates])
  #at(1, 12, y: 76mm, result-box($p_"fus" \/ p_"fus" (c = 0) = (1 - sum_Z Z c_Z)^2$,
    [one W ion displaces 74 fuel ions: $7.4 thin %$ less fuel, $14 thin %$ less fusion power]))
  #at(1, 12, y: 124mm, steps(
    r([helium ash], [$Z = 2$, produced by the burn itself]),
  ))
]

#slide(section: "dilution", title: [Helium ash])[
  #at(1, 12, y: 0mm, align(center, deck-fig("impurity_dilution", columns: 12)))
  #at(1, 12, y: 128mm, align(center, text(fill: muted)[
    $n_e T tau_E = 3/2 (1 + n_i \/ n_e) T^2 \/ ((1 - 2c)^2 sv E_alpha \/ 4 - C_B Z_"eff" sqrt(T))$ #h(4mm) $Z_"eff" = 1 + 2c$]))
  #at(1, 12, y: 146mm, cite-line[#link("https://krystophny.github.io/fusion-skript/notebooks/impurities.html")[notebook: impurities and fuel dilution]])
]

#slide(section: "pressure-beta", title: [Fixed pressure])[
  #at(1, 6, y: 0mm, steps(gap: 7mm,
    r([pressure], $p = (n_e + n_i) k_B T = 2 n k_B T$),
    r([$n = p \/ 2 k_B T$], $p_"fus" = p^2/16 sv/(k_B T)^2 E_"fus"$),
    r([beta], $beta = (2 mu_0 p)/B^2$),
  ))
  #at(1, 6, y: 62mm, result-box($P_"fus" = E_"fus"/(64 mu_0^2) sv/(k_B T)^2 beta^2 B^4 V$, none))
  #at(1, 6, y: 108mm, steps(gap: 6mm,
    r([density limit], $n_G = I_p \/ (pi a^2)$),
  ))
  #at(7, 6, y: -4mm, deck-fig("fixed_pressure", columns: 6))
  #at(1, 12, y: 134mm, text(size: 14pt, fill: muted)[
    $sv\/T^2$: section 2.20 #h(5mm) $n_G$ in $10^20 "m"^(-3)$, plasma current $I_p$ in MA, minor radius $a$ in m #h(5mm) $V$: plasma volume])
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0741-3335/44/8/201")[Greenwald · Plasma Phys. Control. Fusion 44, R27 (2002)]])
]

#slide(section: "confinement-routes", title: [Density and confinement time])[
  #at(1, 12, y: -2mm, align(center, deck-fig("n_tau_plane", columns: 12)))
  #at(1, 12, y: 132mm, text(size: 14pt, fill: muted)[
    magnetic: peak ion density $n_(i 0)$ and $tau_E^*$ #h(4mm) inertial: $n = n tau \/ tau_"stag"$ #h(4mm)
    Sun: $tau = G M^2 \/ (R L) approx 3 times 10^7 "yr"$, mean to core density])
  #at(1, 12, y: 146mm, cite-line[
    Data: #link("https://doi.org/10.1063/5.0083990")[Wurzel & Hsu · Phys. Plasmas 29, 062103 (2022)], Tables 6–8, CC BY 4.0])
]
