#import "theme.typ": *
#show: deck.with(chapter: 3, title: [Fusion in stars])

#slide(title: [Proton–proton chain])[
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
