#import "theme.typ": *
#show: deck.with(chapter: 2, title: [Fusion reactions])

#slide(title: [Main fusion reactions])[
  #let r(name, f) = ([#text(fill: muted, name)], f)
  #at(1, 12, y: 6mm, grid(columns: (auto, 1fr), column-gutter: 14mm, row-gutter: 13mm,
    align: (right + horizon, left + horizon),
    ..r([D–T], $"D" + "T" -> ""^4"He" (3.5 "MeV") + "n" (14.1 "MeV")$),
    ..r([D–D], $"D" + "D" -> "T" (1.01 "MeV") + "p" (3.02 "MeV")$),
    ..r([], $"D" + "D" -> ""^3"He" (0.82 "MeV") + "n" (2.45 "MeV")$),
    ..r([D–#super[3]He], $"D" + ""^3"He" -> ""^4"He" (3.6 "MeV") + "p" (14.7 "MeV")$),
    ..r([p–#super[11]B], $"p" + ""^11"B" -> 3 thin ""^4"He" quad (8.7 "MeV")$),
    ..r([p–p (Sun)], $"p" + "p" -> "D" + "e"^+ + nu_e quad (0.42 "MeV")$),
  ))
]

#slide(title: [Two-body Coulomb problem])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #show math.equation.where(block: true): set align(left)
  #at(1, 7, y: 0mm)[
    $ H = (p_1^2)/(2 m_1) + (p_2^2)/(2 m_2) + (Z_1 Z_2 e^2)/(4 pi epsilon_0 |bold(r)_1 - bold(r)_2|) $
    #v(3mm)
    $ M = m_1 + m_2, quad m = (m_1 m_2)/(m_1 + m_2) $
    $ bold(R) = (m_1 bold(r)_1 + m_2 bold(r)_2)/M, quad bold(r) = bold(r)_1 - bold(r)_2 $
    $ bold(P) = bold(p)_1 + bold(p)_2, quad bold(p) = (m_2 bold(p)_1 - m_1 bold(p)_2)/M $
    #v(3mm)
    $ H = P^2/(2 M) + p^2/(2 m) + (Z_1 Z_2 e^2)/(4 pi epsilon_0 r) $
  ]
  #at(8, 5, y: 10mm, canvas(length: 10mm, {
    import draw: *
    let arrow = (end: "stealth", fill: ink)
    let p1 = (2.2, 4.2)
    let p2 = (5.6, 1.4)
    let c = (4.47, 2.33)
    line((0, 0), p1, stroke: 0.8pt + ink, mark: arrow)
    line((0, 0), p2, stroke: 0.8pt + ink, mark: arrow)
    line(p2, p1, stroke: 1.2pt + plot-orange, mark: (end: "stealth", fill: plot-orange))
    line((0, 0), c, stroke: (paint: muted, thickness: 0.8pt, dash: "dashed"), mark: (end: "stealth", fill: muted))
    circle(p1, radius: 0.32, fill: plot-blue, stroke: none)
    circle(p2, radius: 0.45, fill: plot-blue, stroke: none)
    circle(c, radius: 0.08, fill: muted, stroke: none)
    content((0, 0), anchor: "north-east", padding: 0.15, [$O$])
    content(p1, anchor: "south", padding: 0.4, [$m_1, Z_1$])
    content(p2, anchor: "west", padding: 0.55, [$m_2, Z_2$])
    content((0.75, 2.5), [$bold(r)_1$])
    content((3.2, 0.4), [$bold(r)_2$])
    content((4.5, 3.2), text(fill: plot-orange)[$bold(r)$])
    content((2.3, 1.65), text(fill: muted)[$bold(R)$])
  }))
]

#slide(title: [Head-on collision])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #show math.equation.where(block: true): set align(left)
  #at(1, 5, y: 10mm, canvas(length: 16mm, {
    import draw: *
    let arrow(c) = (end: "stealth", fill: c)
    // incoming: both move towards each other
    circle((0, 3), radius: 0.3, fill: plot-blue, stroke: none)
    circle((6, 3), radius: 0.4, fill: plot-blue, stroke: none)
    line((0.5, 3), (1.6, 3), stroke: 1pt + ink, mark: arrow(ink))
    line((5.4, 3), (4.3, 3), stroke: 1pt + ink, mark: arrow(ink))
    line((0, 2.2), (6, 2.2), stroke: 0.7pt + plot-orange, mark: (start: "stealth", end: "stealth", fill: plot-orange))
    content((3, 1.85), text(fill: plot-orange)[$r$])
    content((0, 3.6), [$Z_1$])
    content((6, 3.7), [$Z_2$])
    // turning point: momentarily at rest
    circle((2, 0), radius: 0.3, fill: plot-blue, stroke: none)
    circle((4, 0), radius: 0.4, fill: plot-blue, stroke: none)
    line((2, -0.8), (4, -0.8), stroke: 0.7pt + plot-orange, mark: (start: "stealth", end: "stealth", fill: plot-orange))
    content((3, -1.15), text(fill: plot-orange)[$r_c$])
    content((3, 0.75), text(fill: muted, size: 14pt)[$dot(r) = 0$])
  }))
  #at(7, 6, y: 0mm)[
    $ dot(bold(P)) = -(partial H)/(partial bold(R)) = 0 quad => quad bold(P) = 0 $
    #text(fill: muted)[centre-of-mass frame; head-on: $ell = 0$]
    $ E = m/2 dot(r)^2 + V(r) = "const" $
    $ V(r) = (Z_1 Z_2 e^2)/(4 pi epsilon_0 r) $
    #v(2mm)
    $ V(r_c) = E quad => quad r_c = (Z_1 Z_2 e^2)/(4 pi epsilon_0 E) $
    #v(2mm)
    $ |t| = sqrt(m/2) integral_(r_c)^r (dif r')/sqrt(E - V(r')) $
  ]
]

#slide(title: [Rutherford scattering])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #show math.equation.where(block: true): set align(left)
  #at(1, 7, y: 6mm, canvas(length: 15mm, {
    import draw: *
    let d = 1.0
    let rmax = 5.0
    // repulsive Coulomb orbit: 1/r = sin(phi)/b + d/(2 b^2) (cos(phi) - 1)
    let orbit(b) = {
      let u(phi) = calc.sin(phi) / b + d / (2 * b * b) * (calc.cos(phi) - 1)
      range(1, 600).map(k => k * calc.pi / 600).filter(phi => u(phi) > 1 / rmax)
        .map(phi => { let r = 1 / u(phi); (r * calc.cos(phi), r * calc.sin(phi)) })
    }
    for b in (0.25, 0.5, 0.9, 1.5, 2.4) {
      line(..orbit(b), stroke: 0.9pt + plot-blue)
    }
    // head-on: reflected at r_c
    line((rmax, 0), (d, 0), stroke: 0.9pt + plot-blue)
    circle((d, 0), radius: 0.07, fill: plot-blue, stroke: none)
    // incoming direction
    line((5.3, 2.4), (4.6, 2.4), stroke: 0.8pt + ink, mark: (end: "stealth", fill: ink))
    content((5.6, 2.75), text(size: 14pt)[$alpha$, $E$])
    // nucleus and turning distance
    circle((0, 0), radius: 0.18, fill: plot-orange, stroke: none)
    content((0, -0.45), text(fill: plot-orange)[$R$])
    line((0, -0.9), (d, -0.9), stroke: 0.6pt + ink, mark: (start: "stealth", end: "stealth", fill: ink))
    content((d / 2, -1.25), [$r_c$])
    line((2.3, 0), (2.3, 0.9), stroke: 0.6pt + muted, mark: (start: "stealth", end: "stealth", fill: muted))
    content((2.55, 0.45), text(fill: muted, size: 14pt)[$b$])
  }))
  #at(8, 5, y: 4mm)[
    $ r_c = (Z_alpha Z e^2)/(4 pi epsilon_0 E) $
    #v(6mm)
    #grid(columns: 5, column-gutter: 6mm, row-gutter: 5mm, align: left + horizon,
      [], [$Z$], [$E$], [$r_c$], [],
      [Au], [$79$], [$5 "MeV"$], [$45 "fm"$], [Coulomb],
      [Al], [$13$], [$7.7 "MeV"$], [$5 "fm"$], [deviation],
    )
    #v(6mm)
    $ r_c approx R quad => quad R tilde 10^(-15) "m" $
  ]
  #at(1, 12, y: 136mm, text(size: 12pt)[
    #link("https://doi.org/10.1098/rspa.1909.0054")[Geiger & Marsden · Proc. R. Soc. A 82, 495 (1909)] ·
    #link("https://doi.org/10.1080/14786440508637080")[Rutherford · Phil. Mag. 21, 669 (1911)] \
    #link("https://doi.org/10.1098/rspa.1924.0029")[Bieler · Proc. R. Soc. A 105, 434 (1924)] ·
    #link("https://doi.org/10.1080/14786442508628535")[Rutherford & Chadwick · Phil. Mag. 50, 889 (1925)]])
]

#slide(title: [Classical turning point])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #show math.equation.where(block: true): set align(left)
  #at(1, 7, y: 8mm, canvas(length: 15mm, {
    import draw: *
    let e = 1.0
    let rc = 3.0
    // axes
    line((0, 0), (8.5, 0), stroke: 0.7pt + ink, mark: (end: "stealth", fill: ink))
    line((0, 0), (0, 4.4), stroke: 0.7pt + ink, mark: (end: "stealth", fill: ink))
    content((8.5, -0.35), [$r$])
    content((-0.4, 4.3), [$V$])
    // Coulomb barrier V = E r_c / r
    line(..range(0, 81).map(k => { let r = 0.7 + k * 0.1; (r, e * rc / r) }), stroke: 1pt + ink)
    content((1.35, 3.6), [$V(r)$])
    // energy level and turning point
    line((0, e), (8.2, e), stroke: (paint: muted, thickness: 0.6pt, dash: "dashed"))
    content((8.5, e), [$E$])
    line((rc, 0), (rc, e), stroke: (paint: plot-orange, thickness: 0.6pt, dash: "dotted"))
    content((rc, -0.35), text(fill: plot-orange)[$r_c$])
    // classical particle: comes in, reflected at r_c
    circle((6.5, e), radius: 0.16, fill: plot-blue, stroke: none)
    line((5.6, 1.6), (4.4, 1.6), stroke: 0.8pt + ink, mark: (end: "stealth", fill: ink))
    line((4.4, 0.4), (5.6, 0.4), stroke: 0.8pt + ink, mark: (end: "stealth", fill: ink))
    content((rc + 0.1, 1.45), text(fill: muted, size: 14pt)[$dot(r) = 0$])
  }))
  #at(1, 7, y: 100mm)[$ r_c lt.tilde R approx 3 "fm" quad => quad E gt.tilde (e^2)/(4 pi epsilon_0 R) approx 0.5 "MeV" $]
]

#slide(title: [Classical cross section])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #at(1, 12, y: 0mm, align(center, canvas(length: 12mm, {
    import draw: *
    let d = 1.0
    let R = 1.5
    let rmax = 5.0
    let bmax = R * calc.sqrt(1 - d / R)
    let blue = plot-blue
    // repulsive Coulomb orbit with head-on turning distance d, cut where it touches R
    let orbit(b, s) = {
      let u(phi) = calc.sin(phi) / b + d / (2 * b * b) * (calc.cos(phi) - 1)
      let pts = ()
      for k in range(1, 600) {
        let phi = k * calc.pi / 600
        if u(phi) > 1 / rmax {
          let r = 1 / u(phi)
          let x = r * calc.cos(phi)
          let y = r * calc.sin(phi)
          if x < -2.0 or y > 3.0 { break }
          pts.push((x, s * y))
          if r <= R { break }
        }
      }
      pts
    }
    // side view
    circle((0, 0), radius: R, fill: plot-orange.lighten(85%), stroke: (paint: plot-orange, dash: "dashed"))
    circle((0, 0), radius: 0.12, fill: plot-orange, stroke: none)
    for s in (1, -1) {
      for bb in (0.35, 1.4, 2.0) { line(..orbit(bb, s), stroke: 0.8pt + muted) }
      line(..orbit(bmax, s), stroke: 1.3pt + ink)
    }
    // the cross section seen edge-on: a line of length 2 b_max
    line((5.3, -bmax), (5.3, bmax), stroke: 3pt + blue)
    line((5.75, 0), (5.75, bmax), stroke: 0.6pt + ink, mark: (start: "stealth", end: "stealth", fill: ink))
    content((5.9, bmax / 2), anchor: "west", [$b_"max"$])
    line((0, 0), (R * calc.cos(-50deg), R * calc.sin(-50deg)), stroke: 0.6pt + plot-orange)
    content((0.55, -0.95), text(fill: plot-orange)[$R$])
    // beam direction
    line((5.6, 3.3), (4.4, 3.3), stroke: 0.8pt + ink, mark: (end: "stealth", fill: ink))
    // front view: what the beam sees
    let cx = 10.0
    line((5.3, bmax), (cx, bmax), stroke: (paint: muted, thickness: 0.4pt, dash: "dotted"))
    line((5.3, -bmax), (cx, -bmax), stroke: (paint: muted, thickness: 0.4pt, dash: "dotted"))
    circle((cx, 0), radius: R, stroke: (paint: plot-orange, dash: "dashed"))
    circle((cx, 0), radius: bmax, fill: blue.lighten(55%), stroke: 1.2pt + blue)
    circle((cx, 0), radius: 0.12, fill: plot-orange, stroke: none)
    content((cx, -R - 0.45), text(fill: blue)[$sigma_"cl" = pi b_"max"^2$])
  })))
  #at(1, 12, y: 96mm, align(center, grid(columns: 3, column-gutter: 10mm, row-gutter: 8mm,
    align: left + horizon,
    $r_"min" (b) <= R$, $=>$, $b^2 <= R^2 (1 - V(R)/E)$,
    $sigma_"cl" = pi R^2 (1 - V(R)/E)$, [], $sigma_"cl" = 0 quad (E < V(R))$,
  )))
]

#slide(title: [Classical cross sections])[
  #at(1, 12, y: 0mm, deck-fig("cross_section_classical", columns: 12))
  #at(1, 5, y: 92mm)[
    $ sigma_"cl" = pi R^2 (1 - V(R)/E) $
    $ R = r_0 (A_1^(1\/3) + A_2^(1\/3)), quad r_0 approx 1.2 "fm" $]
  #at(6, 7, y: 92mm, grid(columns: 5, column-gutter: 7mm, row-gutter: 4mm, align: left + horizon,
    [], [$A_1, A_2$], [$R$], [$V(R)$], [$pi R^2$],
    [D–T], [$2, 3$], [$3.2 "fm"$], [$440 "keV"$], [$0.33 "b"$],
    [D–D], [$2, 2$], [$3.0 "fm"$], [$480 "keV"$], [$0.29 "b"$],
    [p–p], [$1, 1$], [$2.4 "fm"$], [$600 "keV"$], [$0.18 "b"$],
  ))
]

#animation-page("coulomb-collision", "coulomb_collision", loop: false)

#slide(title: [Quantum ballpark])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #show math.equation.where(block: true): set align(left)
  #at(1, 7, y: 8mm, canvas(length: 15mm, {
    import draw: *
    let e = 1.0
    let rc = 3.0
    // axes
    line((0, 0), (8.5, 0), stroke: 0.7pt + ink, mark: (end: "stealth", fill: ink))
    line((0, 0), (0, 4.4), stroke: 0.7pt + ink, mark: (end: "stealth", fill: ink))
    content((8.5, -0.35), [$r$])
    content((-0.4, 4.3), [$V$])
    // Coulomb barrier V = E r_c / r
    line(..range(0, 81).map(k => { let r = 0.7 + k * 0.1; (r, e * rc / r) }), stroke: 1pt + ink)
    content((1.35, 3.6), [$V(r)$])
    // energy level and turning point
    line((0, e), (8.2, e), stroke: (paint: muted, thickness: 0.6pt, dash: "dashed"))
    content((8.5, e), [$E$])
    line((rc, 0), (rc, e), stroke: (paint: plot-orange, thickness: 0.6pt, dash: "dotted"))
    content((rc, -0.35), text(fill: plot-orange)[$r_c$])
    // relative wave: oscillating outside, decaying tail inside r_c
    let amp = 0.38
    let lam = rc
    line(..range(0, 155).map(k => { let r = 0.3 + k * 0.05; (r, e + amp * calc.cos(2 * calc.pi * (r - rc) / lam)) }),
      stroke: 1.2pt + plot-blue)
    // wavelength marker
    line((4.6, 2.3), (4.6 + lam, 2.3), stroke: 0.6pt + plot-blue, mark: (start: "stealth", end: "stealth", fill: plot-blue))
    content((4.6 + lam / 2, 2.65), text(fill: plot-blue)[$lambda$])
    line((5.6, 1.6), (4.4, 1.6), stroke: 0.8pt + ink, mark: (end: "stealth", fill: ink))
  }))
  #at(8, 5, y: 4mm)[
    $ ƛ = lambda/(2 pi) = ħ/p = ħ/sqrt(2 m E) $
    #v(2mm)
    $ ƛ approx r_c quad => quad E approx 2 m c^2 (alpha Z_1 Z_2)^2 $
    #text(fill: muted)[D–T: $E approx 120 "keV"$]
    #v(4mm)
    $ r_c/ƛ = alpha Z_1 Z_2 c sqrt((2 m)/E) prop E^(-1\/2) $
  ]
]

#slide(title: [Barrier in slices])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #show math.equation.where(block: true): set align(left)
  #at(1, 7, y: 8mm, canvas(length: 15mm, {
    import draw: *
    let e = 1.0
    let rc = 3.0
    let dr = 0.4
    // axes
    line((0, 0), (8.5, 0), stroke: 0.7pt + ink, mark: (end: "stealth", fill: ink))
    line((0, 0), (0, 4.4), stroke: 0.7pt + ink, mark: (end: "stealth", fill: ink))
    content((8.5, -0.35), [$r$])
    content((-0.4, 4.3), [$V$])
    // slices: rectangles of height V(r_i) - E
    for i in range(5) {
      let r = 1.0 + i * dr
      let v = e * rc / (r + dr / 2)
      rect((r, e), (r + dr, v), fill: plot-orange.lighten(75%), stroke: 0.5pt + plot-orange)
    }
    content((2.0, 0.65), text(fill: plot-orange)[$kappa_i, Delta r$])
    // Coulomb barrier V = E r_c / r
    line(..range(0, 81).map(k => { let r = 0.7 + k * 0.1; (r, e * rc / r) }), stroke: 1pt + ink)
    content((1.35, 3.6), [$V(r)$])
    // energy level and turning point
    line((0, e), (8.2, e), stroke: (paint: muted, thickness: 0.6pt, dash: "dashed"))
    content((8.5, e), [$E$])
    line((rc, 0), (rc, e), stroke: (paint: plot-orange, thickness: 0.6pt, dash: "dotted"))
    content((rc, -0.35), text(fill: plot-orange)[$r_c$])
    // relative wave: oscillating outside, decaying tail inside r_c
    let amp = 0.38
    let lam = rc
    line(..range(0, 101).map(k => { let r = rc + k * 0.05; (r, e + amp * calc.cos(2 * calc.pi * (r - rc) / lam)) }),
      stroke: 1.2pt + plot-blue)
    line(..range(0, 46).map(k => { let r = rc - k * 0.05; (r, e + amp * calc.exp(-1.2 * (rc - r))) }),
      stroke: 1.2pt + plot-blue)
    // wavelength marker
    line((4.6, 2.3), (4.6 + lam, 2.3), stroke: 0.6pt + plot-blue, mark: (start: "stealth", end: "stealth", fill: plot-blue))
    content((4.6 + lam / 2, 2.65), text(fill: plot-blue)[$lambda$])
    line((5.6, 1.6), (4.4, 1.6), stroke: 0.8pt + ink, mark: (end: "stealth", fill: ink))
  }))
  #at(8, 5, y: 4mm)[
    #text(fill: muted)[one slice:]
    $ P_i approx e^(-2 kappa_i Delta r), quad kappa_i = sqrt(2 m (V(r_i) - E))/ħ $
    #v(4mm)
    #text(fill: muted)[all slices:]
    $ P approx product_i P_i = exp(-2 sum_i kappa_i Delta r) $
    $ -> exp(-2 integral_0^(r_c) kappa(r) dif r) $
  ]
]

#slide(title: [Gamow tunnelling])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #show math.equation.where(block: true): set align(left)
  #at(1, 7, y: 8mm, canvas(length: 15mm, {
    import draw: *
    let e = 1.0
    let rc = 3.0
    // axes
    line((0, 0), (8.5, 0), stroke: 0.7pt + ink, mark: (end: "stealth", fill: ink))
    line((0, 0), (0, 4.4), stroke: 0.7pt + ink, mark: (end: "stealth", fill: ink))
    content((8.5, -0.35), [$r$])
    content((-0.4, 4.3), [$V$])
    // Coulomb barrier V = E r_c / r
    line(..range(0, 81).map(k => { let r = 0.7 + k * 0.1; (r, e * rc / r) }), stroke: 1pt + ink)
    content((1.35, 3.6), [$V(r)$])
    // energy level and turning point
    line((0, e), (8.2, e), stroke: (paint: muted, thickness: 0.6pt, dash: "dashed"))
    content((8.5, e), [$E$])
    line((rc, 0), (rc, e), stroke: (paint: plot-orange, thickness: 0.6pt, dash: "dotted"))
    content((rc, -0.35), text(fill: plot-orange)[$r_c$])
    // relative wave: oscillating outside, decaying tail inside r_c
    let amp = 0.38
    let lam = rc
    line(..range(0, 101).map(k => { let r = rc + k * 0.05; (r, e + amp * calc.cos(2 * calc.pi * (r - rc) / lam)) }),
      stroke: 1.2pt + plot-blue)
    line(..range(0, 46).map(k => { let r = rc - k * 0.05; (r, e + amp * calc.exp(-1.2 * (rc - r))) }),
      stroke: 1.2pt + plot-blue)
    // wavelength marker
    line((4.6, 2.3), (4.6 + lam, 2.3), stroke: 0.6pt + plot-blue, mark: (start: "stealth", end: "stealth", fill: plot-blue))
    content((4.6 + lam / 2, 2.65), text(fill: plot-blue)[$lambda$])
    line((5.6, 1.6), (4.4, 1.6), stroke: 0.8pt + ink, mark: (end: "stealth", fill: ink))
  }))
  #at(8, 5, y: 4mm)[
    $ V(r) = E r_c/r quad => quad kappa(r) = 1/ƛ sqrt(r_c/r - 1) $
    #v(2mm)
    $ 2 integral_0^(r_c) kappa dif r = (2 r_c)/ƛ integral_0^1 sqrt(1/x - 1) dif x = pi r_c/ƛ $
    #v(2mm)
    $ P approx exp(-pi r_c/ƛ) = exp(-sqrt(E_G/E)) $
    #v(2mm)
    $ E_G = 2 m c^2 (pi alpha Z_1 Z_2)^2 $
  ]
  #at(1, 12, y: 136mm, text(size: 12pt)[
    #link("https://doi.org/10.1007/BF01343196")[Gamow · Z. Phys. 51, 204 (1928)] ·
    #link("https://doi.org/10.1038/122439a0")[Gurney & Condon · Nature 122, 439 (1928)] \
    #link("https://doi.org/10.1007/BF01341595")[Atkinson & Houtermans · Z. Phys. 54, 656 (1929)]])
]

#slide(title: [Measuring a cross section])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #at(1, 6, y: 2mm, canvas(length: 12mm, {
    import draw: *
    let arrow(c) = (end: "stealth", fill: c)
    // side view: beam through a thin target
    for y in (0.8, 1.6, 2.4, 3.2) {
      line((0, y), (2.8, y), stroke: 1pt + plot-blue, mark: arrow(plot-blue))
      if y != 2.4 { line((3.6, y), (6.0, y), stroke: 1pt + plot-blue, mark: arrow(plot-blue)) }
    }
    content((1.2, 3.75), text(fill: plot-blue)[$N_"beam"$])
    rect((3.0, 0.2), (3.4, 3.8), fill: plot-orange.lighten(80%), stroke: 0.8pt + plot-orange)
    content((3.2, -0.25), [$Delta x$])
    content((3.2, 4.15), text(fill: plot-orange)[$n$])
    circle((3.2, 2.4), radius: 0.12, fill: plot-orange, stroke: none)
    line((3.3, 2.5), (5.2, 3.9), stroke: 0.8pt + ink, mark: arrow(ink))
    rect((5.2, 3.7), (6.2, 4.4), stroke: 0.8pt + ink)
    content((5.7, 4.75), [$N_"react"$])
    // face-on view: discs of area sigma
    rect((1.2, -5.0), (4.8, -1.4), fill: plot-orange.lighten(80%), stroke: 0.8pt + plot-orange)
    for (x, y) in ((1.7, -2.1), (2.6, -4.2), (3.5, -2.6), (4.2, -4.4), (2.1, -3.2), (4.1, -1.9), (3.1, -3.5), (1.8, -4.6)) {
      circle((x, y), radius: 0.2, fill: plot-orange.lighten(30%), stroke: none)
    }
    line((3.5, -2.6), (4.15, -2.95), stroke: 0.6pt + ink)
    content((4.35, -3.1), [$sigma$])
    content((5.2, -1.6), anchor: "west", [$A$])
  }))
  #let r(name, f) = ([#text(fill: muted, name)], f)
  #at(7, 6, y: 4mm, grid(columns: (auto, 1fr), rows: 22mm, column-gutter: 8mm,
    align: (right + horizon, left + horizon),
    ..r([nuclei], $N_T = n A Delta x$),
    ..r([covered fraction], $P = (N_T sigma)/A = (n Delta x) thin sigma$),
    ..r([reactions], $N_"react" = N_"beam" thin P$),
    ..r([measured], $sigma = N_"react"/N_"beam" thin 1/(n Delta x)$),
    ..r([unit], $1 "b" = 10^(-28) "m"^2$),
  ))
]

#slide(title: [Cross section])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #show math.equation.where(block: true): set align(left)
  #at(1, 5, y: 10mm, canvas(length: 15mm, {
    import draw: *
    let R = 2.0
    circle((0, 0), radius: R, fill: plot-blue.lighten(85%), stroke: 1pt + plot-blue)
    // one wavelength across the diameter
    line(..range(0, 81).map(k => { let x = -R + k * 2 * R / 80; (x, 0.45 * calc.sin(calc.pi * (x + R) / R)) }),
      stroke: 1.2pt + plot-blue)
    line((-R, -2.5), (R, -2.5), stroke: 0.6pt + ink, mark: (start: "stealth", end: "stealth", fill: ink))
    content((0, -2.9), [$lambda$])
    line((0, 0), (R * calc.cos(50deg), R * calc.sin(50deg)), stroke: 0.7pt + ink, mark: (end: "stealth", fill: ink))
    content((0.15, 1.1), [$tilde ƛ$])
  }))
  #at(7, 6, y: 10mm)[
    $ sigma_"geo" tilde pi ƛ^2 = (pi ħ^2)/(2 m E) prop 1/E $
    #v(10mm)
    $ sigma(E) = S(E)/E exp(-sqrt(E_G/E)) $
  ]
]

#slide(title: [Tunnelling alone])[
  #at(1, 7, y: 0mm, deck-fig("cross_section_shape", columns: 7))
  #at(8, 5, y: 10mm)[
    $ sigma = 1/E exp(-sqrt(E_G/E)), quad S = 1 "keV b" $
    #v(6mm)
    #grid(columns: 2, column-gutter: 8mm, row-gutter: 5mm,
      [], [$E_G$],
      [D–T], [$1.18 "MeV"$],
      [D–D], [$0.99 "MeV"$],
      [p–p], [$0.49 "MeV"$],
    )
  ]
]

#slide(title: [Actual cross sections])[
  #at(1, 7, y: 0mm, deck-fig("cross_section_actual", columns: 7))
  #at(8, 5, y: 10mm)[
    $ sigma = S(E)/E exp(-sqrt(E_G/E)) $
    #v(6mm)
    #grid(columns: 2, column-gutter: 8mm, row-gutter: 5mm,
      [], [$S(0)$],
      [D–T], [$approx 10^4 "keV b"$],
      [D–D], [$approx 10^2 "keV b"$],
      [p–p], [$4 times 10^(-22) "keV b"$],
    )
  ]
  #at(1, 12, y: 136mm, text(size: 12pt)[
    #link("https://doi.org/10.1088/0029-5515/32/4/I07")[Bosch & Hale · Nucl. Fusion 32, 611 (1992)] ·
    #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. · Rev. Mod. Phys. 83, 195 (2011)]])
]

#slide(title: [S-factor from experiment])[
  #at(1, 8, y: 0mm, deck-fig("s_factor_data", columns: 8))
  #at(9, 4, y: 10mm)[ $ S_i = sigma_i E_i exp(sqrt(E_G/E_i)) $ ]
  #at(1, 12, y: 136mm, text(size: 12pt)[ #link("https://doi.org/10.1103/PhysRev.93.483")[Arnold · Phys. Rev. 93, 483 (1954)] · #link("https://doi.org/10.1103/PhysRev.107.1616")[Bame · Phys. Rev. 107, 1616 (1957)] · #link("https://doi.org/10.1103/PhysRevC.29.2031")[Jarmie · Phys. Rev. C 29, 2031 (1984)] · #link("https://doi.org/10.1103/PhysRevC.35.1999")[Brown · Phys. Rev. C 35, 1999 (1987)] · #link("https://doi.org/10.1098/rspa.1954.0249")[Preston · Proc. R. Soc. A 226, 206 (1954)] · #link("https://doi.org/10.1007/BF01292792")[Greife · Z. Phys. A 351, 107 (1995)] · #link("https://doi.org/10.1103/PhysRevC.73.045801")[Leonard · Phys. Rev. C 73, 045801 (2006)] · #link("https://doi.org/10.1088/0029-5515/32/4/I07")[Bosch & Hale · Nucl. Fusion 32, 611 (1992)] · #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. · Rev. Mod. Phys. 83, 195 (2011)] ])
]

#slide(title: [#super[5]He resonance])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #at(1, 7, y: 4mm, canvas(length: 14mm, {
    import draw: *
    let er = 4.7
    let w = 0.25
    // levels (gap between D+T and 5He* exaggerated)
    line((0, 0), (4, 0), stroke: 1.5pt + ink)
    content((4.2, 0), anchor: "west", [$""^4"He" + "n"$])
    line((0, 4), (4, 4), stroke: (paint: ink, thickness: 1pt, dash: "dashed"))
    content((4.2, 4), anchor: "west", [$"D" + "T"$])
    line((0, er), (4, er), stroke: 1.5pt + plot-orange)
    content((4.2, er), anchor: "west", text(fill: plot-orange)[$""^5"He"^*$])
    // sideways Lorentzian: the level has a width
    line(..range(0, 81).map(k => { let y = er - 1.0 + k * 0.025; (-0.3 - 1.6 / (1 + calc.pow((y - er) / w, 2)), y) }),
      stroke: 1.2pt + plot-orange)
    line((-1.1, er - w), (-1.1, er + w), stroke: 0.6pt + ink, mark: (start: "stealth", end: "stealth", fill: ink))
    content((-2.1, er), anchor: "east", [$Gamma$])
    line((-0.3, er - 1.0), (-0.3, er + 1.0), stroke: 0.6pt + muted)
    // resonance energy above threshold
    line((1.0, 4), (1.0, er), stroke: 0.6pt + ink, mark: (start: "stealth", end: "stealth", fill: ink))
    content((1.15, (4 + er) / 2), anchor: "west", [$E_r$])
    // decay
    line((3.0, er), (3.0, 0.1), stroke: 1pt + ink, mark: (end: "stealth", fill: ink))
    content((3.15, 2.2), anchor: "west", [$17.6 "MeV"$])
  }))
  #at(8, 5, y: 24mm)[
    $ S(E) prop 1/((E - E_r)^2 + Gamma^2\/4) $
    #v(10mm)
    $ tau = ħ/Gamma $
  ]
]

#slide(title: [Which force?])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #at(1, 12, y: 2mm, align(center, canvas(length: 12mm, {
    import draw: *
    let nuc(x, y, f) = {
      let c = if f == "p" { plot-orange } else { plot-blue }
      circle((x, y), radius: 0.34, fill: c.lighten(55%), stroke: 1pt + c)
      content((x, y), [$#f$])
    }
    let group(x, y, fs, name) = {
      let w = fs.len() * 0.8
      rect((x - 0.5, y - 0.5), (x + w - 0.3, y + 0.5), radius: 0.5, stroke: 0.8pt + muted)
      for (k, f) in fs.enumerate() { nuc(x + k * 0.8, y, f) }
      content((x + w / 2 - 0.4, y + 0.85), [$#name$])
    }
    let arrow(x, y) = line((x, y), (x + 1.4, y), stroke: 1pt + ink, mark: (end: "stealth", fill: ink))
    // D + T -> 4He + n: the nucleons only regroup
    group(0, 6.2, ("p", "n"), "D")
    content((1.75, 6.2), [$+$])
    group(2.7, 6.2, ("p", "n", "n"), "T")
    arrow(5.3, 6.2)
    group(7.3, 6.2, ("p", "p", "n", "n"), [$""^4"He"$])
    content((10.7, 6.2), [$+$])
    group(11.7, 6.2, ("n",), "n")
    content((14.0, 6.2), anchor: "west", [#text(fill: muted)[strong] \ $P tilde 1$])
    content((6.0, 4.85), text(size: 14pt, fill: muted)[also D–D, D–#super[3]He, p–#super[11]B])
    // D + p -> 3He + gamma: regroup, excess energy leaves as a photon
    group(0, 2.7, ("p", "n"), "D")
    content((1.75, 2.7), [$+$])
    group(2.7, 2.7, ("p",), "p")
    arrow(4.1, 2.7)
    group(6.1, 2.7, ("p", "p", "n"), [$""^3"He"$])
    line(..range(0, 41).map(k => { let x = 8.6 + k * 0.04; (x, 2.7 + 0.15 * calc.sin(k * calc.pi / 5)) }),
      stroke: 1pt + ink)
    content((10.4, 2.7), anchor: "west", [$gamma$])
    content((14.0, 2.7), anchor: "west", [#text(fill: muted)[electromagnetic] \ $P tilde 10^(-5)$])
    // p + p -> D: one proton must turn into a neutron
    group(0, -0.3, ("p",), "p")
    content((0.95, -0.3), [$+$])
    group(1.9, -0.3, ("p",), "p")
    arrow(3.3, -0.3)
    group(5.3, -0.3, ("p", "n"), "D")
    line((6.1, -0.65), (6.9, -1.7), stroke: (paint: ink, thickness: 1pt, dash: "dashed"))
    content((6.35, -1.35), anchor: "east", [$W^+$])
    line((6.9, -1.7), (8.0, -1.2), stroke: 1pt + ink, mark: (end: "stealth", fill: ink))
    line((6.9, -1.7), (8.0, -2.2), stroke: 1pt + ink, mark: (end: "stealth", fill: ink))
    content((8.15, -1.2), anchor: "west", [$"e"^+$])
    content((8.15, -2.2), anchor: "west", [$nu_e$])
    content((14.0, -0.3), anchor: "west", [#text(fill: muted)[weak] \ $P tilde 10^(-22)$])
  })))
  #at(1, 12, y: 136mm, text(size: 12pt)[
    #link("https://doi.org/10.1088/0029-5515/32/4/I07")[Bosch & Hale · Nucl. Fusion 32, 611 (1992)] ·
    #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. · Rev. Mod. Phys. 83, 195 (2011)] \
    #link("https://doi.org/10.1103/RevModPhys.97.025002")[CODATA 2022 · Rev. Mod. Phys. 97, 025002 (2025)]])
]

#slide(title: [S and R])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #at(1, 12, y: 6mm, align(center, canvas(length: 13mm, {
    import draw: *
    let R = 1.0
    let rc = 6.0
    rect((0, 0), (R, 1.2), fill: plot-orange.lighten(70%), stroke: none)
    rect((R, 0), (rc, 1.2), fill: plot-blue.lighten(85%), stroke: none)
    line((0, 0), (11, 0), stroke: 0.8pt + ink, mark: (end: "stealth", fill: ink))
    content((11.3, 0), [$r$])
    for (x, l) in ((0, $0$), (R, $R$), (rc, $r_c$)) {
      line((x, -0.12), (x, 0.12), stroke: 0.8pt + ink)
      content((x, -0.45), l)
    }
    content((R / 2, 0.6), text(fill: plot-orange)[$S$])
    content(((R + rc) / 2, 0.6), text(fill: plot-blue)[$e^(-sqrt(E_G\/E))$])
    content(((rc + 11) / 2, 0.6), text(fill: muted)[free])
  })))
  #at(1, 12, y: 52mm, align(center)[
    $display(sigma = S/E e^(-sqrt(E_G \/ E)))$
  ])
]

#slide(title: [Range of the forces])[
  #show math.equation.where(block: true): set align(left)
  #at(1, 6, y: 6mm, deck-fig("force_ranges", columns: 6))
  #at(7, 6, y: 6mm)[
    $ lambda = ħ/(m c) $
    #v(10mm)
    #text(fill: muted)[Fermi's golden rule]
    $ P prop abs(integral psi_f^* thin V thin psi_i dif^3 r)^2 $
    #v(2mm)
    $ tilde cases(
      1 & quad "strong",
      alpha (R \/ lambda_gamma)^2 approx 10^(-5) & quad "electromagnetic",
      alpha_W^2 (lambda_W \/ lambda_(e nu))^4 approx 10^(-22) & quad "weak",
    ) $
  ]
]

#slide(title: [Computing S])[
  #at(1, 12, y: 6mm, align(center, $display(S prop e^(4 sqrt(R \/ a)) dot P)$ + h(14mm) + text(size: 16pt)[$a = (4 pi epsilon_0 ħ^2)/(2 m Z_1 Z_2 e^2)$]))
  #let r(name, how, f) = ([#text(fill: muted, name)], how, f)
  #at(1, 12, y: 36mm, grid(columns: (auto, auto, 1fr), column-gutter: 10mm, row-gutter: 11mm,
    align: (right + horizon, left + horizon, left + horizon),
    ..r([p–p], [weak interaction], $S prop G_F^2 g_A^2 abs(chevron.l "d" mid(|) "pp" chevron.r)^2$),
    ..r([D–T], [R-matrix], [$E_r, Gamma$ fitted $=>$ Breit–Wigner]),
    ..r([D–T], [ab initio], [five nucleons, realistic forces]),
  ))
  #at(1, 12, y: 136mm, text(size: 12pt)[
    #link("https://doi.org/10.1103/RevModPhys.30.257")[Lane & Thomas · Rev. Mod. Phys. 30, 257 (1958)] ·
    #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. · Rev. Mod. Phys. 83, 195 (2011)] \
    #link("https://doi.org/10.1103/PhysRevLett.108.042503")[Navrátil & Quaglioni · Phys. Rev. Lett. 108, 042503 (2012)]])
]

#slide(title: [p–p fusion from wave functions])[
  #at(1, 6, y: 0mm, deck-fig("pp_fusion_waves", columns: 6))
  #let step(name, f) = ([#text(fill: muted, name)], f)
  #at(7, 6, y: 0mm, grid(columns: (auto, 1fr), column-gutter: 6mm, row-gutter: 8mm,
    align: (right + horizon, left + horizon),
    [], $H_0 = -ħ^2/(2 m) (dif^2)/(dif r^2)$,
    ..step([deuteron], $(H_0 + V_d) thin u_d = -B_d thin u_d$),
    ..step([p–p], $(H_0 + V_(p p) + V_C) u_(p p) = E u_(p p)$),
    ..step([overlap], $Lambda prop display(integral_0^infinity) u_d thin u_(p p) dif r$),
    ..step([rate], $S_(p p)(0) prop G_V^2 g_A^2 thin f_(p p) thin Lambda^2$),
  ))
  #at(7, 6, y: 98mm, text(size: 14pt, fill: muted)[
    $V_d$: S–D coupled by tensor force \
    $u_(p p)$: $E -> 0$, matched to Coulomb waves, Gamow factor divided out \
    $V$: Reid potential, fitted to nucleon–nucleon scattering \
    $f_(p p)$: phase space of e⁺ and ν])
  #at(1, 12, y: 136mm, text(size: 12pt)[
    #link("https://doi.org/10.1016/0003-4916(68)90126-7")[Reid · Ann. Phys. 50, 411 (1968)] ·
    #link("https://doi.org/10.1103/PhysRevC.58.1263")[Schiavilla et al. · Phys. Rev. C 58, 1263 (1998)]])
]

#slide(title: [Pionless effective field theory])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #at(1, 12, y: 2mm, align(center, canvas(length: 11mm, {
    import draw: *
    let R = 1.4
    let gi = 4.32
    let a = 7.8
    rect((0, 0), (R, 3.2), fill: muted.lighten(80%), stroke: none)
    content((R / 2, 3.6), text(fill: muted, size: 14pt)[unresolved])
    // deuteron tail e^{-gamma r}
    line(..range(0, 141).map(k => { let r = R + k * 0.1; (r, 2.8 * calc.exp(-(r - R) / gi)) }),
      stroke: 1.5pt + plot-blue)
    content((6.5, 1.6), text(fill: plot-blue)[$u_d prop e^(-gamma r)$])
    line((0, 0), (16, 0), stroke: 0.8pt + ink, mark: (end: "stealth", fill: ink))
    content((16.4, 0), [$r$])
    for (x, l, y) in ((R, [$R_pi approx 1.4 "fm"$], -0.6), (gi, [$1\/gamma approx 4.3 "fm"$], -1.3), (a, [$|a_(p p)| approx 7.8 "fm"$], -0.6)) {
      line((x, -0.12), (x, 0.12), stroke: 0.8pt + ink)
      content((x, y), l)
    }
  })))
  #let step(name, f) = ([#text(fill: muted, name)], f)
  #at(2, 10, y: 76mm, grid(columns: (auto, 1fr), column-gutter: 8mm, row-gutter: 9mm,
    align: (right + horizon, left + horizon),
    ..step([scale separation], $R_pi = ħ/(m_pi c) quad << quad 1/gamma, |a_(p p)|$),
    ..step([deuteron], $gamma = sqrt(m_N B_d)/ħ$),
    ..step([p–p], $k cot delta = -1/a_(p p) + r_(p p)/2 k^2 + dots$),
    ..step([short range], [one constant $L_(1,A)$ #text(fill: muted)[from lattice QCD]]),
  ))
]

#slide(title: [p–p: computed vs reference])[
  #let r(name, a, e, ref) = ([#text(fill: muted, name)], a, e, ref)
  #let inp = text(fill: muted)[input]
  #at(1, 12, y: 4mm, grid(columns: 4, column-gutter: 10mm, row-gutter: 8mm,
    align: (right + horizon, left + horizon, left + horizon, left + horizon),
    [], text(fill: muted)[potential model], text(fill: muted)[pionless EFT], text(fill: muted)[reference],
    ..r([deuteron binding], $2.2246 "MeV"$, inp, $2.2246 "MeV"$),
    ..r([D-state fraction], $6.5 %$, [–], $tilde 5 "–" 7 %$),
    ..r([$a_(p p)$], $-7.75 "fm"$, inp, $-7.81 "fm"$),
    ..r([$Lambda^2$], $6.91$, $7.02$, $approx 7.0$),
    ..r([$S_(p p)(0) thin [10^(-25) "MeV b"]$], $3.95$, $4.01 plus.minus 0.27$, $4.01 plus.minus 0.04$),
  ))
  #at(1, 12, y: 84mm, align(center)[
    #text(fill: muted)[EFT order by order:] $quad 3.60 quad -> quad 3.82 quad -> quad 4.01$])
  #at(1, 12, y: 130mm, text(size: 12pt)[
    #link("https://doi.org/10.1016/S0370-2693(01)01152-2")[Butler & Chen · Phys. Lett. B 520, 87 (2001)] ·
    #link("https://doi.org/10.1103/PhysRevLett.119.062002")[Savage et al. · Phys. Rev. Lett. 119, 062002 (2017)] \
    #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. · Rev. Mod. Phys. 83, 195 (2011)]])
]

#slide(title: [From classical to nuclear])[
  #import "@preview/fletcher:0.5.8": diagram, node, edge
  #let n(pos, title, f, c) = node(pos, align(center)[#text(fill: c)[#title] \ #v(2mm) #f],
    stroke: 1pt + c, inset: 5mm, corner-radius: 3mm, width: 57mm, height: 46mm)
  #at(1, 12, y: 8mm, align(center, diagram(spacing: (9mm, 32mm), edge-stroke: 1pt + ink,
    n((0, 0), [classical], $r_c = (Z_1 Z_2 e^2)/(4 pi epsilon_0 E)$, ink),
    edge((0, 0), (1, 0), "-|>"),
    n((1, 0), [classical $sigma$], [$sigma_"cl" = 0$ \ $E < V(R)$], ink),
    edge((1, 0), (2, 0), "-|>"),
    n((2, 0), [quantum], [$ƛ = ħ/sqrt(2 m E)$ \ #v(1mm) $ƛ approx r_c$], plot-blue),
    edge((2, 0), (3, 0), "-|>"),
    n((3, 0), [tunnelling], $e^(-sqrt(E_G \/ E))$, plot-blue),
    edge((3, 0), (3, 1), "-|>"),
    n((3, 1), [wave area], $pi ƛ^2 prop 1/E$, plot-blue),
    edge((3, 1), (2, 1), "-|>"),
    n((2, 1), [cross section], $sigma = S/E e^(-sqrt(E_G \/ E))$, plot-blue),
    edge((2, 1), (1, 1), "-|>"),
    n((1, 1), [nuclear physics], [$S$: $R$, force, #super[5]He#super[\*]], plot-orange),
    edge((1, 1), (0, 1), "-|>"),
    n((0, 1), [$S$ [keV b]], [D–T $10^4$ \ D–D $10^2$ \ p–p $10^(-22)$], plot-orange),
  )))
]

#slide(section: "reaction-rate", title: [From cross section to rate])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #at(1, 5, y: 6mm, canvas(length: 12mm, {
    import draw: *
    let arrow(c) = (end: "stealth", fill: c)
    rect((2.6, 0), (6.4, 4.2), fill: plot-orange.lighten(85%), stroke: 0.8pt + plot-orange)
    for (x, y) in ((3.1, 0.6), (4.4, 1.1), (5.7, 0.5), (3.6, 2.0), (5.1, 2.4), (6.0, 3.4), (3.0, 3.5), (4.4, 3.7)) {
      circle((x, y), radius: 0.16, fill: plot-orange, stroke: none)
    }
    content((4.5, 4.65), text(fill: plot-orange)[$n_2$])
    for y in (0.8, 1.7, 2.6, 3.5) {
      line((0, y), (2.2, y), stroke: 1pt + plot-blue, mark: arrow(plot-blue))
    }
    content((1.0, 4.25), text(fill: plot-blue)[$n_1, v$])
    line((2.6, -0.5), (6.4, -0.5), stroke: 0.6pt + ink, mark: (start: "stealth", end: "stealth", fill: ink))
    content((4.5, -0.9), [$v thin Delta t$])
  }))
  #let r(name, f) = ([#text(fill: muted, name)], f)
  #at(5, 8, y: 4mm, grid(columns: (auto, 1fr), column-gutter: 7mm, row-gutter: 10mm,
    align: (right + horizon, left + horizon),
    ..r([beam on target], $R = n_1 n_2 thin sigma(v) thin v$),
    ..r([thermal plasma], $R = n_1 n_2 chevron.l sigma v chevron.r$),
    ..r([], $chevron.l sigma v chevron.r = integral.double f_1(bold(v)_1) f_2(bold(v)_2) thin sigma(g) thin g dif^3 v_1 dif^3 v_2$),
    ..r([identical], $N(N - 1)\/2 approx N^2\/2 "pairs"$),
  ))
  #at(4, 6, y: 90mm, result-box($R = (n_1 n_2)/(1 + delta_(12)) chevron.l sigma v chevron.r$, none))
  #at(1, 12, y: 124mm, text(size: 14pt, fill: muted)[
    $R$: reactions per volume and time #h(6mm) $n_1, n_2$: densities #h(6mm)
    $f_1, f_2$: velocity distributions, $integral f dif^3 v = 1$ #h(6mm)
    $g = |bold(v)_1 - bold(v)_2|$ #h(6mm) $delta_(12) = 1$ for identical nuclei (D–D), else $0$])
]

#slide(section: "reaction-rate", title: [Relative velocity])[
  #let r(name, f) = ([#text(fill: muted, name)], f)
  #at(1, 12, y: 0mm, grid(columns: (auto, 1fr), column-gutter: 8mm, row-gutter: 8mm,
    align: (right + horizon, left + horizon),
    ..r([Maxwellian], $F_mu (bold(w)) = (mu/(2 pi k_B T))^(3\/2) e^(-mu w^2\/(2 k_B T)), quad f_1 = F_(m_1), quad f_2 = F_(m_2)$),
    ..r([centre of mass], $bold(V) = (m_1 bold(v)_1 + m_2 bold(v)_2)/M, quad bold(g) = bold(v)_1 - bold(v)_2$),
    ..r([no mixed term], $m_1 v_1^2 + m_2 v_2^2 = M V^2 + m g^2, quad dif^3 v_1 dif^3 v_2 = dif^3 V dif^3 g$),
    ..r([], $f_1 (bold(v)_1) thin f_2 (bold(v)_2) = F_M (bold(V)) thin F_m (bold(g))$),
    ..r([convolution], $f_"rel" (bold(g)) = integral f_1 (bold(v)) thin f_2 (bold(v) - bold(g)) dif^3 v = F_m (bold(g))$),
    ..r([variances add], $(k_B T)/m_1 + (k_B T)/m_2 = (k_B T)/m$),
  ))
  #at(1, 12, y: 124mm, text(size: 14pt, fill: muted)[
    $M = m_1 + m_2$, #h(2mm) $m = m_1 m_2 \/ M$ #h(2mm) ($m_r$ in the animation) #h(8mm)
    $F_mu$: Maxwellian of mass $mu$ \
    no $bold(V) dot bold(g)$ term: no angles, Jacobian 1])
]

#animation-page("relative-velocity", "relative_velocity", section: "reaction-rate")

#slide(section: "reaction-rate", title: [Convolution and kernel smoothing])[
  #import "@preview/cetz:0.5.2": canvas, draw
  #let r(name, f) = ([#text(fill: muted, name)], f)
  #let note(body) = ([], text(size: 15pt, fill: muted, body))
  #at(1, 7, y: 0mm, grid(columns: (auto, 1fr), column-gutter: 6mm, row-gutter: 5mm,
    align: (right + horizon, left + horizon),
    ..r([convolution], $(f * K)(x) = integral f(x') thin K(x - x') dif x'$),
    ..note[$K$ shifted to $x$, multiplied with $f$, integrated],
    ..r([correlation], $integral f(x') thin K(x' - x) dif x'$),
    ..note[$K$ not flipped; the same for even $K$],
    ..r([smoothing], text(fill: muted)[$K$ of width $h$ removes structure narrower than $h$]),
  ))
  // Sketch: f with a narrow spike, the kernel at x_0, their product, and the smoothed f * K.
  #at(8, 5, y: 0mm, canvas(length: 10mm, {
    import draw: *
    let f(x) = 1.4 * calc.exp(-calc.pow((x - 3.5) / 1.3, 2)) + 2.2 * calc.exp(-calc.pow((x - 6.4) / 0.12, 2))
    let h = 0.7
    let k(x) = calc.exp(-calc.pow(x / h, 2) / 2) / (h * calc.sqrt(2 * calc.pi))
    let xs = range(0, 401).map(i => i * 0.025)
    let conv(x) = xs.map(t => f(t) * k(x - t) * 0.025).sum()
    let x0 = 5.6
    line((0, 3.2), (10, 3.2), stroke: 0.6pt + ink)
    line((0, 0), (10, 0), stroke: 0.6pt + ink)
    let prod = xs.map(t => (t, 3.2 + 2.2 * f(t) * k(x0 - t)))
    line(..prod, (10, 3.2), (0, 3.2), fill: plot-orange.lighten(55%), stroke: none)
    line(..xs.map(t => (t, 3.2 + f(t))), stroke: 1pt + ink)
    line(..xs.map(t => (t, 3.2 + 3.0 * k(x0 - t))), stroke: (paint: plot-blue, thickness: 1pt, dash: "dashed"))
    content((1.1, 4.6), [$f$])
    content((x0 + 1.5, 4.1), text(fill: plot-blue)[$K$])
    line(..xs.map(t => (t, 2.2 * conv(t))), stroke: 1.2pt + plot-orange)
    circle((x0, 2.2 * conv(x0)), radius: 0.1, fill: plot-orange, stroke: none)
    line((x0, 0), (x0, 3.2), stroke: (paint: muted, thickness: 0.5pt, dash: "dotted"))
    content((x0, -0.4), [$x$])
    content((1.3, 1.3), text(fill: plot-orange)[$f * K$])
  }))
  #at(1, 12, y: 86mm, grid(columns: (auto, 1fr), column-gutter: 6mm, row-gutter: 6mm,
    align: (right + horizon, left + horizon),
    ..r([relative velocity], [$f_"rel" (bold(g)) = integral f_1 (bold(v)) thin f_2 (bold(v) - bold(g)) dif^3 v = F_m (bold(g))$ #h(4mm) #text(fill: muted)[convolution in $bold(v)$]]),
    ..r([reactivity], [$chevron.l sigma v chevron.r (T) = integral sigma v(u) thin K(u - s) dif u$ #h(4mm) #text(fill: muted)[correlation in $ln E$]]),
    ..note[$u = ln E, quad s = ln k_B T, quad K(x) = 2/sqrt(pi) e^(3x\/2) exp(-e^x)$],
    ..note[$T$ only shifts $K$, which smooths the #super[5]He resonance],
  ))
  #at(1, 12, y: 140mm, text(size: 12pt)[
    see also #link("https://krystophny.github.io/plasma-skript/animations/kernel-smoothing.html")[kernel smoothing · Plasma Physics animation]])
]

#slide(section: "reaction-rate", title: [Maxwell average])[
  #let r(name, f) = ([#text(fill: muted, name)], f)
  #at(1, 12, y: 0mm, grid(columns: (auto, 1fr), column-gutter: 8mm, row-gutter: 8mm,
    align: (right + horizon, left + horizon),
    ..r([relative motion], $chevron.l sigma v chevron.r = integral F_m (bold(g)) thin sigma(g) thin g dif^3 g = 4 pi integral_0^infinity F_m (g) thin sigma(g) thin g^3 dif g$),
    ..r([$E = m g^2 \/ 2$], $g^3 dif g = (2 E)/m^2 dif E$),
  ))
  #at(1, 12, y: 36mm, result-box($chevron.l sigma v chevron.r = (8/(pi m))^(1\/2) (k_B T)^(-3\/2) integral_0^infinity sigma(E) thin E thin e^(-E\/k_B T) dif E$, none))
  #at(1, 12, y: 86mm, grid(columns: (auto, 1fr), column-gutter: 8mm, row-gutter: 8mm,
    align: (right + horizon, left + horizon),
    ..r([in $ln E$], $f_M (E) dif E = 2/sqrt(pi) (E/(k_B T))^(3\/2) e^(-E\/k_B T) dif ln E = K(u - s) dif u$),
    ..r([], [$chevron.l sigma v chevron.r (T) = integral sigma v(u) thin K(u - s) dif u$ #h(5mm) #text(fill: muted)[$T$ shifts a fixed kernel]]),
  ))
  #at(1, 12, y: 130mm, text(size: 14pt, fill: muted)[
    $f_M (E) = 2/sqrt(pi) (k_B T)^(-3\/2) sqrt(E) e^(-E\/k_B T)$: energy distribution, maximum at $k_B T\/2$ #h(8mm)
    $u = ln E$, #h(2mm) $s = ln k_B T$])
]

#animation-page("maxwell-average", "maxwell_average", section: "reaction-rate")

#slide(section: "reaction-rate", title: [From cross section to reactivity])[
  #at(1, 12, y: 0mm, align(center, deck-fig("reaction_product", columns: 12)))
  #at(1, 12, y: 120mm, align(center)[
    $display(I_T(E) = sigma(E) thin v(E) thin f_M(E), quad chevron.l sigma v chevron.r = integral_0^infinity I_T(E) dif E)$
  ])
  #at(1, 12, y: 139mm, align(center, text(size: 14pt, fill: muted)[
    $f_M(E) prop sqrt(E) e^(-E\/(k_B T))$: shell factor $sqrt(E)$; relative speed $v(E) prop sqrt(E)$.
  ]))
]

#slide(section: "reaction-rate", title: [Gamow peak])[
  #let r(name, f) = ([#text(fill: muted, name)], f)
  #at(1, 12, y: 0mm, grid(columns: (auto, 1fr), column-gutter: 6mm, row-gutter: 7mm,
    align: (right + horizon, left + horizon),
    ..r([insert $sigma = S/E e^(-sqrt(E_G\/E))$], $chevron.l sigma v chevron.r = (8/(pi m))^(1\/2) (k_B T)^(-3\/2) integral_0^infinity S(E) thin e^(-F(E)) dif E$),
    ..r([exponent], $F(E) = E/(k_B T) + sqrt(E_G/E)$),
  ))
  #at(1, 6, y: 48mm, grid(columns: (auto, 1fr), column-gutter: 6mm, row-gutter: 7mm,
    align: (right + horizon, left + horizon),
    ..r([maximum $F' = 0$], $E_0 = (E_G (k_B T)^2 \/ 4)^(1\/3)$),
    ..r([depth], $F(E_0) = tau = 3 E_0 \/ k_B T$),
    ..r([curvature], $F''(E_0) = 3 \/ (2 E_0 k_B T)$),
    ..r([width], $Delta = 4 sqrt(E_0 k_B T \/ 3)$),
  ))
  #at(7, 6, y: 52mm, result-box($chevron.l sigma v chevron.r approx (8 sqrt(6))/27 S(E_0)/sqrt(m E_G) thin tau^2 e^(-tau)$, [Gaussian around $E_0$]))
  #at(1, 12, y: 108mm, grid(columns: (auto, 1fr), column-gutter: 6mm, row-gutter: 6mm,
    align: (right + horizon, left + horizon),
    ..r([$tau prop (k_B T)^(-1\/3)$], $chevron.l sigma v chevron.r prop (k_B T)^(-2\/3) exp(-3 (E_G\/4)^(1\/3) (k_B T)^(-1\/3))$),
    ..r([D–T, $k_B T = 10 "keV"$], $E_0 approx 31 "keV", quad Delta approx 41 "keV", quad tau approx 9.3$),
  ))
  #at(1, 12, y: 140mm, text(size: 14pt, fill: muted)[
    $Delta$: full width at $1\/e$ #h(8mm) $S(E) approx S(E_0)$ across the peak])
]

#slide(section: "reaction-rate", title: [Gamow window])[
  #at(1, 12, y: 0mm, align(center, deck-fig("gamow_peak", columns: 11)))
]

#animation-page("gamow-sweep", "gamow_sweep", section: "reaction-rate")

#slide(section: "reaction-rate", title: [Only the tail fuses])[
  #at(1, 12, y: 0mm, align(center, deck-fig("tail_fuses", columns: 9)))
  #at(1, 12, y: 102mm, align(center, text(fill: muted)[D–T at $chevron.l sigma v chevron.r = 1.1 times 10^(-22) "m"^3\/"s"$ #h(4mm) (the value at $k_B T = 10 "keV"$)]))
  #at(1, 12, y: 114mm, align(center, grid(columns: 3, column-gutter: 14mm, row-gutter: 4mm,
    align: (right, left, left),
    text(fill: muted)[$k_B T$ needed for], text(fill: muted)[all pairs at $E = 3\/2 thin k_B T$], text(fill: muted)[Maxwellian],
    text(fill: muted)[classical $sigma_"cl"$], $450 "keV" approx 5 times 10^9 "K"$, $440 "keV" approx 5 times 10^9 "K"$,
    text(fill: muted)[tunnelling $sigma$], $15 "keV" approx 1.7 times 10^8 "K"$, $10 "keV" approx 1.2 times 10^8 "K"$,
  )))
]

#slide(section: "reaction-rate", title: [Reactivity])[
  #at(1, 12, y: 0mm, align(center, deck-fig("reactivity", columns: 11)))
  #at(1, 12, y: 118mm, align(center)[
    D–T, $k_B T = 10 "keV"$: $chevron.l sigma v chevron.r = 1.1 times 10^(-22) "m"^3\/"s"$ #h(10mm)
    #text(fill: muted)[Lawson (Chapter 4):] $n T tau_E prop T^2 \/ chevron.l sigma v chevron.r$])
  #at(1, 12, y: 136mm, text(size: 12pt)[
    #link("https://doi.org/10.1088/0029-5515/32/4/I07")[Bosch & Hale · Nucl. Fusion 32, 611 (1992)] ·
    #link("https://doi.org/10.1088/0029-5515/40/4/310")[Nevins & Swain · Nucl. Fusion 40, 865 (2000)] ·
    #link("https://krystophny.github.io/fusion-skript/notebooks/reactivity.html")[notebook: reactivity and Gamow peak]])
]

#slide(section: "reaction-rate", title: [Reaction rate: summary])[
  #context {
    let assumptions = (([Maxwellians], [both species at one $T$]), ([$S(E)$], [slowly varying near $E_0$]))
    let derivation = (
      ([rate], $R = n_1 n_2 chevron.l sigma v chevron.r \/ (1 + delta_(12))$),
      ([relative motion], [Maxwellian with $m$]),
      ([average], $chevron.l sigma v chevron.r prop (k_B T)^(-3\/2) integral sigma E e^(-E\/k_B T) dif E$),
      ([in $ln E$], [$T$ shifts a fixed kernel]),
      ([Gamow peak], $E_0 = (E_G (k_B T)^2 \/ 4)^(1\/3)$),
    )
    let lw = label-width(assumptions, derivation)
    at(1, 7)[
      #labelled[Assumptions][#rows(assumptions, lw, gap: 5mm)]
      #v(10mm, weak: true)
      #labelled[Derivation][#rows(derivation, lw, gap: 6mm)]
    ]
  }
  #at(8, 5)[
    #labelled[Result][#result-box($chevron.l sigma v chevron.r prop tau^2 e^(-tau)$, [$tau = 3 E_0 \/ k_B T$])]
    #v(8mm)
    #text(fill: muted)[D–T, $k_B T = 10 "keV"$:] \
    $chevron.l sigma v chevron.r = 1.1 times 10^(-22) "m"^3\/"s"$ \
    #text(fill: muted)[$chevron.l sigma v chevron.r \/ T^2$ maximal at] $13.5 "keV"$
  ]
]

#slide(section: "reaction-rate", title: [Solar core])[
  #at(1, 12, y: 0mm, align(center, deck-fig("gamow_peak_pp", columns: 10)))
  #at(1, 12, y: 134mm, align(center)[
    p–p: #h(3mm) $E_G = 0.49 "MeV", quad k_B T approx 1.3 "keV" quad => quad E_0 approx 6 "keV" approx 4.6 thin k_B T$])
]
