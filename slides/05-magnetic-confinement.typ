#import "theme.typ": *
#show: deck.with(chapter: 5)

// Draft (2026-11-09): the limit pages moved here from Chapter 4. The chapter
// asks what limits n and p, and how a magnetic field reaches them.
#let r(name, f) = ([#text(fill: muted, name)], f)
#let steps(..items, gap: 8mm) = grid(columns: (auto, 1fr), column-gutter: 7mm, row-gutter: gap,
  align: (right + horizon, left + horizon), ..items.pos().flatten())
#let cite-line(body) = text(size: 12pt, body)
#let sv = $chevron.l sigma v chevron.r$

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
