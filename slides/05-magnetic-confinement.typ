#import "theme.typ": *
#show: deck.with(chapter: 5)

// Route (2026-11-17): fluid and particle pictures, pinch, mirror, torus,
// kink and sausage, then the concepts and the limits of a real machine.
#let r(name, f) = ([#text(fill: muted, name)], f)
#let steps(..items, gap: 8mm) = grid(columns: (auto, 1fr), column-gutter: 7mm, row-gutter: gap,
  align: (right + horizon, left + horizon), ..items.pos().flatten())
#let cite-line(body) = text(size: 12pt, body)
#let sv = $chevron.l sigma v chevron.r$
#import "@preview/cetz:0.5.2": canvas, draw

#let lbl(body) = text(size: 14pt, body)
#let note(body) = text(size: 14pt, fill: muted, body)
#let soft = plot-orange.lighten(82%)
#let pane(body) = canvas(length: 1mm, body)

// -------------------------------------------- 5.1 Fluid and particle pictures

#slide(section: "two-pictures", title: [Fluid and particle pictures])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([Lawson], [$p tau_E >= 10 "bar s"$ #h(4mm) at #h(1mm) $k_B T approx 15 "keV"$]),
    r([pressure], [$p = 2 n k_B T = 4.8 "bar"$ #h(4mm) #text(fill: muted)[$n = 10^20 "m"^(-3)$]]),
  ))
  #at(1, 12, y: 44mm, table(columns: (52mm, 1fr, 1fr), inset: (x: 4mm, y: 4mm), stroke: none,
    align: (right + horizon, left + horizon, left + horizon),
    table.hline(stroke: 0.6pt + rule),
    [], text(fill: muted)[fluid], text(fill: muted)[particles],
    table.hline(stroke: 0.6pt + rule),
    text(fill: muted)[model], $rho_m (dif bold(u))/(dif t) = bold(j) times bold(B) - nabla p$, $m (dif bold(v))/(dif t) = q (bold(E) + bold(v) times bold(B))$,
    table.hline(stroke: 0.6pt + rule),
  ))
  #at(1, 12, y: 140mm, note[$rho_m$ mass density, $bold(u)$ flow velocity, $bold(j)$ current density])
]

// --------------------------------------------- 5.2 Magnetic pressure, pinches

#slide(section: "magnetic-pressure", title: [Magnetic pressure and $beta$])[
  #at(1, 5, y: 0mm, deck-fig("theta_pinch", columns: 5))
  #at(6, 7, y: 0mm, steps(gap: 7mm,
    r([force], $bold(j) times bold(B) = underbrace(- nabla B^2/(2 mu_0), "pressure") + underbrace((bold(B) dot nabla) bold(B) \/ mu_0, "tension")$),
    r([straight $bold(B)$], $p + B_"in"^2/(2 mu_0) = B_"ext"^2/(2 mu_0)$),
    r([$beta$], $beta = (2 mu_0 p)/B_"ext"^2 <= 1$),
    r([$5.3 "T"$], $B^2 \/ (2 mu_0) = 112 "bar"$),
  ))
  #at(6, 7, y: 112mm, result-box($tau_E >= (10 "bar s")/(beta dot 112 "bar") = 3.6 "s"$, [$beta = 2.5 %$]))
]

#slide(section: "magnetic-pressure", title: [Z-pinch])[
  #at(1, 5, y: 0mm, deck-fig("z_pinch", columns: 5))
  #at(6, 7, y: 0mm, steps(gap: 7mm,
    r([force balance], $(dif p)/(dif r) = - j_z B_theta$),
    r([Ampère], $B_theta = (mu_0 I(r))/(2 pi r)$),
    r([Bennett], $(mu_0 I^2)/(8 pi) = N k_B (T_e + T_i)$),
    r([average], $chevron.l p chevron.r = B_theta (a)^2 \/ (2 mu_0)$),
  ))
  #at(1, 12, y: 86mm, result-box([$I = 0.45 "MA"$ #h(2mm) #text(size: 18pt)[axial current that holds the column]], [$n = 10^20 "m"^(-3)$, $a = 10 "cm"$, $k_B T = 10 "keV"$: #h(1mm) $B_theta (a) = 0.9 "T"$, #h(1mm) $B_theta^2 \/ 2 mu_0 = 3.2 "bar" = 2 n k_B T$]))
  #at(1, 12, y: 140mm, note[$N = n pi a^2$ ions per length, $a$ column radius])
  #at(1, 12, y: 150mm, cite-line[#link("https://doi.org/10.1103/PhysRev.45.890")[Bennett · Phys. Rev. 45, 890 (1934)]])
]

#slide(section: "magnetic-pressure", title: [Screw pinch])[
  #at(1, 12, y: 0mm, deck-fig("screw_pinch", columns: 12))
  #at(1, 12, y: 122mm, align(center, $q = (2 pi a B_z)/(L B_theta)$))
]

// ------------------------------------------------- 5.3 Gyration and mirrors

#slide(section: "mirrors", title: [Gyration and magnetic mirror])[
  #at(1, 6, y: 0mm, deck-fig("mirror_3d", columns: 6))
  #at(7, 6, y: 0mm, steps(gap: 7mm,
    r([gyration], [$rho = (m v_perp)/(abs(q) B)$ #h(3mm) #text(fill: muted)[D, 10 keV, 5 T: 4 mm]]),
    r([invariant], $mu = (m v_perp^2)/(2 B)$),
    r([reflection], $sin^2 theta > B_"min" \/ B_"max" = 1 \/ R_m$),
    r([loss cone], [$1 - sqrt(1 - 1\/R_m)$ #h(3mm) #text(fill: muted)[$R_m = 4$: 13 %]]),
  ))
  #at(1, 12, y: 104mm, result-box([$rho << a$ across $bold(B)$ #h(6mm) collisions refill the loss cone], [bend the column into a torus]))
  #at(1, 12, y: 146mm, note[$theta$ pitch angle at $B_"min"$, $R_m$ mirror ratio, $a$ plasma radius])
]

// ---------------------------------------------- 5.4 Torus and field-line twist

#slide(section: "torus", title: [Torus with a toroidal field])[
  #at(1, 5, y: 0mm, pane({
    import draw: *
    line((6, 4), (6, 100), stroke: (paint: muted, thickness: 0.8pt, dash: "dashed"))
    content((6, 102), anchor: "south", lbl[axis])
    line((6, 4), (104, 4), stroke: 0.6pt + muted, mark: (end: "stealth", fill: muted))
    content((104, 7), anchor: "south-east", lbl[$R$])
    circle((60, 52), radius: 30, fill: soft, stroke: 0.8pt + plot-orange)
    let crossb(p) = { circle(p, radius: 2, stroke: 0.6pt + ink)
      line((p.at(0) - 1.4, p.at(1) - 1.4), (p.at(0) + 1.4, p.at(1) + 1.4), stroke: 0.6pt + ink)
      line((p.at(0) - 1.4, p.at(1) + 1.4), (p.at(0) + 1.4, p.at(1) - 1.4), stroke: 0.6pt + ink) }
    for p in ((72, 52), (66, 40), (78, 64)) { crossb(p) }
    content((60, 75), text(size: 20pt)[$+ + +$])
    content((60, 29), text(size: 20pt)[$- - -$])
    line((46, 68), (46, 36), stroke: 1.4pt + plot-blue, mark: (end: "stealth", fill: plot-blue))
    content((43, 52), anchor: "east", lbl[$bold(E)$])
    line((92, 52), (104, 52), stroke: 1.8pt + plot-orange, mark: (end: "stealth", fill: plot-orange))
    content((98, 56), anchor: "south", lbl[$bold(E) times bold(B)$])
    content((60, 88), anchor: "south", lbl[ions $arrow.t$ #h(2mm) electrons $arrow.b$])
  }))
  #at(6, 7, y: 0mm, steps(gap: 7mm,
    r([coils], $B_phi = (mu_0 N_c I_c)/(2 pi R) prop 1/R$),
    r([$nabla B$ + curvature], $v_d = (m (v_parallel^2 + v_perp^2 \/ 2))/(q B R)$),
    r([separation], [$E_z$ grows #h(3mm) #text(fill: muted)[sign of $q$]]),
    r([$E times B$], [$v_E = E_z \/ B$ #h(3mm) #text(fill: muted)[outward, all species]]),
  ))
  #at(6, 7, y: 104mm, result-box([twist the field lines], [connect top and bottom]))
  #at(1, 12, y: 146mm, note[$bold(B)$ into the page · $N_c I_c$ total coil current · $v_parallel$, $v_perp$ along and across $bold(B)$])
]

#slide(section: "torus", title: [Twisted field lines])[
  #at(1, 6, y: 6mm, pane({
    import draw: *
    rect((10, 10), (120, 70), stroke: 0.8pt + ink)
    for k in range(3) {
      line((10, 10 + k * 20), (120, 30 + k * 20), stroke: 1.4pt + plot-orange)
    }
    content((65, 4), lbl[toroidal angle $phi: 0 dots 2 pi$])
    content((5, 40), angle: 90deg, lbl[poloidal angle $theta: 0 dots 2 pi$])
    content((65, 76), lbl[$q = 3$: three toroidal turns per poloidal turn])
  }))
  #at(7, 6, y: 0mm, steps(gap: 7mm,
    r([safety factor], $q = (Delta phi)/(2 pi) = (r B_phi)/(R B_theta)$),
    r([half turn], $Delta approx v_d (pi q R)/v_parallel tilde q rho$),
    r([trapped], [$Delta tilde q rho \/ sqrt(epsilon)$ #h(2mm) #text(fill: muted)[$epsilon = r\/R$]]),
    r([alphas, 5 T], [$rho_alpha = 5 "cm" => Delta approx 0.3 "m"$ #h(2mm) #text(fill: muted)[$q = 3$, $epsilon = 0.3$]]),
  ))
  #at(1, 12, y: 104mm, result-box($q rho \/ sqrt(epsilon) << a$, [particles: $q$ not too large]))
  #at(1, 12, y: 146mm, note[$Delta phi$ toroidal angle per poloidal turn, $Delta$ orbit width, $B_theta$ poloidal field])
]

// ------------------------------------------------------ 5.5 Sausage and kink

#slide(section: "kink-sausage", title: [Sausage and kink])[
  #at(1, 5, y: 0mm, canvas(length: 0.85mm, {
    import draw: *
    let n = 60
    let top = range(0, n + 1).map(i => { let x = 5 + i * 110 / n; (x, 70 + 9 + 4 * calc.cos(2 * calc.pi * (x - 5) / 36.7)) })
    let bot = range(0, n + 1).map(i => { let x = 5 + i * 110 / n; (x, 70 - 9 - 4 * calc.cos(2 * calc.pi * (x - 5) / 36.7)) })
    line(..top, stroke: 1pt + plot-orange); line(..bot, stroke: 1pt + plot-orange)
    for x0 in (23.35, 60.05, 96.75) {
      line((x0, 95), (x0, 81), stroke: 1.4pt + plot-blue, mark: (end: "stealth", fill: plot-blue))
      line((x0, 45), (x0, 59), stroke: 1.4pt + plot-blue, mark: (end: "stealth", fill: plot-blue))
    }
    content((60, 100), lbl[sausage, $m = 0$])
    let mid(x) = 22 + 7 * calc.sin(2 * calc.pi * (x - 5) / 110)
    line(..range(0, n + 1).map(i => { let x = 5 + i * 110 / n; (x, mid(x) + 7) }), stroke: 1pt + plot-orange)
    line(..range(0, n + 1).map(i => { let x = 5 + i * 110 / n; (x, mid(x) - 7) }), stroke: 1pt + plot-orange)
    line((32.5, 4), (32.5, 18), stroke: 1.4pt + plot-blue, mark: (end: "stealth", fill: plot-blue))
    line((87.5, 40), (87.5, 26), stroke: 1.4pt + plot-blue, mark: (end: "stealth", fill: plot-blue))
    content((60, 42), lbl[kink, $m = 1$])
  }))
  #at(6, 7, y: 0mm, steps(gap: 7mm,
    r([sausage], [$B_theta prop 1\/r$: #h(1mm) neck pinches further]),
    r([kink], [$B_theta$ crowds inside the bend]),
    r([axial $B_z$], [$B_z^2 > B_theta^2 \/ 2$ #h(2mm) #text(fill: muted)[sausage stable]]),
    r([Kruskal–Shafranov], $q(a) = (2 pi a B_z)/(L B_theta (a)) > 1$),
  ))
  #at(1, 12, y: 100mm, result-box([$q(a) > 1$ #h(4mm) #text(fill: muted)[torus: $L = 2 pi R$]], [fluid: $q$ not too small]))
  #at(1, 12, y: 140mm, note[blue arrows: magnetic pressure on the column · $m$ poloidal mode number · $L$ column length])
  #at(1, 12, y: 150mm, cite-line[#link("https://doi.org/10.1098/rspa.1954.0120")[Kruskal & Schwarzschild · Proc. R. Soc. A 223, 348 (1954)] · Shafranov · Sov. J. At. Energy 1, 709 (1956)])
]

#slide(section: "kink-sausage", title: [Window for the twist])[
  #at(1, 12, y: 4mm, table(columns: (52mm, 1fr, 1fr), inset: (x: 4mm, y: 5mm), stroke: none,
    align: (right + horizon, left + horizon, left + horizon),
    table.hline(stroke: 0.6pt + rule),
    [], text(fill: muted)[particles], text(fill: muted)[fluid],
    table.hline(stroke: 0.6pt + rule),
    text(fill: muted)[$q$ too small], [—], [kink: $q(a) < 1$],
    text(fill: muted)[$q$ too large], [orbits leave: $q rho \/ sqrt(epsilon) tilde a$], [—],
    table.hline(stroke: 0.6pt + rule),
  ))
  #at(2, 10, y: 76mm, result-box($1 < q(a) << a sqrt(epsilon) \/ rho$, [tokamak: $q_95 approx 3$]))
  #at(1, 12, y: 146mm, note[$q_95$: $q$ on the flux surface enclosing 95 % of the poloidal flux])
]

// ------------------------------------- 5.6 Toroidal pinch, tokamak, stellarator

#slide(section: "concepts", title: [Toroidal pinch and ZETA])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([toroidal pinch], [strong $I$, weak $B_phi$ #h(3mm) $=>$ #h(3mm) $q(a) << 1$]),
    r([ZETA, Harwell 1957], [$R = 1.5 "m"$, #h(1mm) $a = 0.5 "m"$ #h(3mm) neutrons reported January 1958]),
    r([neutron spectrum], [beam-like, direction-dependent: #h(1mm) not thermonuclear]),
    r([quiet phase], [$B_phi$ reverses at the edge: #h(1mm) reversed-field pinch]),
  ))
  #at(2, 10, y: 92mm, result-box([$q(a) << 1$: kinks], [the current must be weak, $B_phi$ strong]))
  #at(1, 12, y: 140mm, cite-line[
    #link("https://doi.org/10.1038/181217a0")[Thonemann et al. · Nature 181, 217 (1958)] ·
    #link("https://doi.org/10.1038/1811630a0")[Rose et al. · Nature 181, 1630 (1958)] ·
    #link("https://doi.org/10.1103/PhysRevLett.33.1139")[Taylor · Phys. Rev. Lett. 33, 1139 (1974)]])
]

#slide(section: "concepts", title: [Tokamak: ITER coil set])[
  #at(1, 12, y: 0mm, deck-fig("tokamak_3d", columns: 12))
  #at(1, 12, y: 140mm, cite-line[CS, PF: ITER, #link("https://github.com/PrincetonUniversity/M3DC1")[M3D-C1 device data] ·
    plasma $R_0 = 6.2 "m"$, $a = 2 "m"$, $kappa = 1.7$: #link("https://doi.org/10.1088/0029-5515/39/12/301")[ITER Physics Basis (1999)] · TF: schematic D, 18 coils])
]

#slide(section: "concepts", title: [Tokamak])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([fields], [$B_phi$ from coils, #h(1mm) $B_theta$ from the plasma current $I_p$ (transformer)]),
    r([safety factor], $q(a) = (2 pi a^2 B_phi)/(mu_0 R I_p) gt.tilde 2 dots 3$),
    r([current limit], [$I_p <= (2 pi a^2 B_phi)/(mu_0 R q_"min")$ #h(3mm) #text(fill: muted)[elongated cross section: higher, ITER 15 MA]]),
    r([T-3, Moscow], [$k_B T_e approx 1 "keV"$ #h(3mm) Thomson scattering by the Culham team, 1969]),
  ))
  #at(2, 10, y: 100mm, result-box($B_theta \/ B_phi = epsilon \/ q approx 0.1$, [strong $B_phi$, current inside the window]))
  #at(1, 12, y: 146mm, cite-line[#link("https://doi.org/10.1038/224488a0")[Peacock et al. · Nature 224, 488 (1969)]])
]

#slide(section: "concepts", title: [Stellarator: NCSX modular coils])[
  #at(1, 12, y: 0mm, deck-fig("stellarator_3d", columns: 12))
  #at(1, 12, y: 140mm, cite-line[NCSX modular coils and VMEC boundary: #link("https://github.com/PrincetonUniversity/STELLOPT")[STELLOPT benchmark data] · field line: $theta + lambda = theta_0 + iota phi$, $iota = 0.65$ · front coils removed])
]

#slide(section: "concepts", title: [Stellarator])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([twist], [from three-dimensional coils, #h(1mm) no plasma current #h(3mm) Spitzer, Princeton 1951]),
    r([no current], [no current-driven kink, no disruption, steady state]),
    r([orbits], [the vertical drift does not average out by itself #h(2mm) $=>$ optimised shape]),
    r([machines], [Model C → ST tokamak 1970 #h(3mm) W7-AS 1988 #h(3mm) W7-X 2015]),
  ))
  #at(2, 10, y: 100mm, result-box([twist from coils], [orbits need three-dimensional optimisation]))
  #at(1, 12, y: 146mm, cite-line[#link("https://doi.org/10.1063/1.1705883")[Spitzer · Phys. Fluids 1, 253 (1958)]])
]


#slide(section: "pressure-beta", title: [Pressure and density limits])[
  #at(1, 12, y: 0mm, steps(gap: 8mm,
    r([pressure], $p = 2 n k_B T, quad beta = (2 mu_0 p)/B^2 quad => quad p <= beta_max B^2 \/ 2 mu_0$),
    r([density], [$n <= n_G = I_p \/ (pi a^2)$ #h(3mm) #text(size: 14pt, fill: muted)[$10^20 "m"^(-3)$, MA, m]]),
  ))
  #at(2, 10, y: 62mm, result-box($p_"fus" prop sv/(k_B T)^2 thin beta^2 B^4$, [fixed $p$: optimum 13.5 keV #h(2mm) (4.4) #h(4mm) twice $B$: 16 times $p_"fus"$]))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0741-3335/44/8/201")[Greenwald · Plasma Phys. Control. Fusion 44, R27 (2002)]])
]

// ------------------------------------------------- 5.2 Where is the optimum? ---

#widget-page("limits", section: "optimum", title: [Density and pressure limits])

#slide(section: "optimum", title: [Limits and confinement scaling])[
  #at(1, 12, y: 0mm, steps(gap: 7mm,
    r([limits], $n <= n_G, quad p <= beta_max B^2 \/ 2 mu_0 quad => quad T_times = p_max \/ 2 n_max$),
    r([tokamak], [$T_times approx 0.39 thin beta_N a B \/ f_"GW" "keV"$ #h(4mm) #text(fill: muted)[ITER 8.8 keV]]),
    r([IPB98(y,2)], $tau_E prop I^0.93 R^1.97 overline(n)^0.41 P^(-0.69) dots$),
  ))
  #at(1, 12, y: 76mm, result-box([$tau_E$ falls with heating power #h(2mm) $=>$ #h(2mm) optimum #box[$approx 6$–$9 "keV"$]], none))
  #at(1, 12, y: 146mm, cite-line[
    #link("https://doi.org/10.1088/0029-5515/39/12/302")[ITER Physics Basis · Nucl. Fusion 39, 2175 (1999)] ·
    #link("https://doi.org/10.1088/0029-5515/45/12/024")[Yamada et al. · Nucl. Fusion 45, 1684 (2005)]])
]

#widget-page("popcon", section: "optimum", title: [Operating space of a device])

#widget-page("machines", section: "optimum", title: [Where present machines stand])
