#import "theme.typ": *
#import "@preview/fletcher:0.5.8": diagram, node, edge
#show: deck.with(chapter: 1, title: [Discovering fusion], background: "dark")

// Original FusionIntroSlides artwork; labels and equations stay native.
#let source(body) = at(1, 12, y: 146mm, text(size: 9pt, body))
#let flow(..items) = diagram(spacing: 8mm, node-inset: 5mm,
  node-stroke: 0.7pt + white, edge-stroke: 0.8pt + white, ..items)

#photo-page("discovering-fusion/sun-sdo-20260501.jpg", "NASA/SDO and AIA, EVE, HMI science teams · 1 May 2026 · public domain", "discovery-sun", fit: "contain", title: [The Sun])

#photo-page("discovering-fusion/original/potteries.jpeg", "Wellcome Collection · M0003525 · wellcomecollection.org/works/h3cuknsg", "discovery-industry", fit: "contain", title: [The Potteries])

#photo-page("discovering-fusion/original/aston-laboratory.jpeg", "F. W. Aston (1877–1945) · Cavendish Laboratory P42, c. 1937 · Cambridge University Library · CC BY-NC 4.0", "discovery-aston", fit: "contain", title: [Francis Aston])

#slide(title: [1913], background: "dark")[
  #at(1, 12)[
    #place(dx: 80mm, dy: 0mm, image("photos/discovering-fusion/original/neon-1913.png", height: 132mm, alt: "Historical neon isotope parabola photograph, as in FusionIntroSlides."))
  ]
  #source[#link("https://archive.org/details/isotopes00asto")[F. W. Aston · Isotopes (1922)] · #link("https://doi.org/10.1016/j.ijms.2013.03.009")[Historical discussion (2013)]]
]

#slide(title: [1922], background: "dark")[
  #at(1, 12)[
    #place(dx: 2mm, dy: 4mm, rotate(-90deg, reflow: true, box(width: 130mm, height: 253mm, clip: true)[#image("photos/discovering-fusion/original/aston-plates-1922.png", width: 174.17mm, height: 253mm, fit: "stretch", alt: "Aston, Isotopes, Plate III; original rotation and crop.")]))
  ]
  #source[#link("https://archive.org/details/isotopes00asto")[F. W. Aston · Isotopes (1922), Plate III]]
]

#slide(title: [Eddington · 1920], background: "dark")[
  #at(1, 12)[
    #place(dx: 12.49mm, dy: 4.60mm, box(width: 167.05mm, height: 70.92mm, clip: true)[#place(dx: -0.00mm, dy: -0.00mm, image("photos/discovering-fusion/original/eddington-header.png", width: 167.05mm, height: 80.07mm, fit: "stretch"))])
    #place(dx: 195.94mm, dy: 4.60mm, image("photos/discovering-fusion/original/eddington-portrait.jpeg", width: 48.57mm, height: 62.11mm, fit: "stretch", alt: "Eddington portrait"))
    #place(dx: 195.94mm, dy: 82.45mm, image("photos/discovering-fusion/original/einstein-sasse.jpeg", width: 48.67mm, height: 62.11mm, fit: "stretch", alt: "Einstein tongue portrait,1951"))
    #place(dx: 11mm, dy: 77mm, block(width: 167mm)[
      #set par(leading: 0.18em, spacing: 0.6em)
      #text(size: 12pt, style: "italic")[
        *Aston* has further shown conclusively that the mass of the helium atom is less than the
        sum of the masses of the four hydrogen atoms which enter into it and in this at least the
        chemists agree with him. There is a loss of mass in the synthesis amounting to 1 part in
        120, the atomic weight of *hydrogen being 1.008 and that of helium just 4.00*… Now
        mass cannot be annihilated and the deficit can only represent the *mass of the electrical
        energy* liberated when helium is made out of hydrogen. *If 5% of a star’s mass consists
        initially of hydrogen atoms*, which are gradually being combined to form more complex
        elements, the total heat liberated will more than suffice for our demands, and we need
        look no further for the source of a star’s energy.

        If, indeed, the subatomic energy in the stars is being freely used to maintain their
        furnaces, it seems to bring a little nearer to fulfillment our dream of controlling this
        latent *power for the well-being of the human race*—or for its suicide.
      ]
    ])
    #place(dx: 196mm, dy: 68mm, text(size: 10pt)[Arthur Eddington\ (1882–1944)])
  ]
  #source[#link("https://adsabs.harvard.edu/full/1920Obs....43..341E")[Eddington · The Observatory 43, 341 (1920)] · Einstein photograph: Arthur Sasse (1951) · portraits: FusionIntroSlides ]
]

#slide(title: [1927], background: "dark")[
  #at(1, 12)[
    #place(dx: 16.53mm, dy: 26.77mm, image("photos/discovering-fusion/original/packing-fraction.png", width: 217.06mm, height: 109.89mm, fit: "stretch", alt: "Historical packing-fraction/mass-number graph"))
    #place(dx: 27.87mm, dy: 16.44mm, image("photos/discovering-fusion/original/chalk-proton.png", width: 10.02mm, height: 9.62mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 16.53mm, dy: 10.42mm, text(size: 17pt)[$ ""^1 upright("H") $])
    #place(dx: 26.19mm, dy: 66.12mm, rotate(180.00000deg, origin: center + horizon, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 25.33mm, height: 24.71mm, fit: "stretch", alt: "Original-looking chalk physics drawing")))
    #place(dx: 26.36mm, dy: 61.69mm, box(width: 25.33mm, height: 13.46mm, clip: true)[#place(dx: -0.00mm, dy: -11.25mm, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 25.33mm, height: 24.71mm, fit: "stretch"))])
    #place(dx: 26.19mm, dy: 52.66mm, box(width: 25.33mm, height: 13.46mm, clip: true)[#place(dx: -0.00mm, dy: -11.25mm, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 25.33mm, height: 24.71mm, fit: "stretch"))])
    #place(dx: 26.03mm, dy: 43.27mm, box(width: 25.33mm, height: 13.46mm, clip: true)[#place(dx: -0.00mm, dy: -11.25mm, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 25.33mm, height: 24.71mm, fit: "stretch"))])
    #place(dx: 26.00mm, dy: 33.89mm, box(width: 25.33mm, height: 13.46mm, clip: true)[#place(dx: -0.00mm, dy: -11.25mm, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 25.33mm, height: 24.71mm, fit: "stretch"))])
    #place(dx: 25.96mm, dy: 27.42mm, box(width: 25.33mm, height: 7.06mm, clip: true)[#place(dx: -0.00mm, dy: -13.55mm, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 25.33mm, height: 24.71mm, fit: "stretch"))])
    #place(dx: 100.16mm, dy: 42.66mm, image("photos/discovering-fusion/original/doge-nuclear.png", width: 47.65mm, height: 56.75mm, fit: "stretch", alt: "Muscular Doge meme crop"))
    #place(dx: 199.17mm, dy: 94.79mm, rotate(351.03470deg, origin: center + horizon, scale(x: -100%, y: 100%, image("photos/discovering-fusion/original/chalk-arrow-right.png", width: 18.34mm, height: 13.96mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))))
    #place(dx: 204.55mm, dy: 6.96mm, image("photos/discovering-fusion/original/doge-chemical.png", width: 36.68mm, height: 51.13mm, fit: "stretch", alt: "Seated Doge meme crop"))
    #place(dx: 119mm, dy: 33mm, [MeV])
    #place(dx: 231mm, dy: 8mm, [eV])
    #place(dx: 120mm, dy: 66mm, text(size: 35pt)[☢])
  ]
  #source[Source: Christopher Albert · FusionIntroSlides, slide 11 · original annotations and composition]
]

#slide(title: [Atkinson and Houtermans · 1929], background: "dark")[
  #at(1, 12)[
    #place(dx: 40mm, dy: 15mm, block(width: 177mm, align(center)[
      #text(size: 19pt)[On the possibility of building up\ the elements in stars]
      #v(5mm)#text(size: 13pt)[R. d’E. Atkinson · F. G. Houtermans · 1929]
    ]))
    #place(dx: 202.65mm, dy: 114.93mm, image("photos/discovering-fusion/original/chalk-proton.png", width: 10.02mm, height: 9.62mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 174.49mm, dy: 58.46mm, image("photos/discovering-fusion/original/chalk-proton.png", width: 10.02mm, height: 9.62mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 190.57mm, dy: 99.38mm, rotate(59.37748deg, origin: center + horizon, scale(x: -100%, y: 100%, image("photos/discovering-fusion/original/chalk-arrow-right.png", width: 18.34mm, height: 13.96mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))))
    #place(dx: 158.92mm, dy: 76.94mm, image("photos/discovering-fusion/original/koralm.png", width: 81.65mm, height: 26.24mm, fit: "stretch", alt: "ARGE Koralm contractor logos photograph"))
    #place(dx: 178.38mm, dy: 66.56mm, image("photos/discovering-fusion/original/chalk-proton.png", width: 10.02mm, height: 9.62mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 20mm, dy: 57mm, block(width: 132mm)[
      #set par(leading: 0.18em, spacing: 0.55em)
      #text(size: 13pt, style: "italic")[
        The *quantum-mechanical* probability that a *proton penetrates an atomic nucleus*
        is calculated using *Gamow’s* method. It is found that, under the temperature
        and density conditions inside stars, *protons, but not α particles, penetrate*
        lighter elements sufficiently often to make the *building up of these elements*
        there appear probable. This makes it possible to explain the *energy production
        of stars through the mass defects* of the elements, while avoiding the assumption
        of six-particle collisions for helium formation. Some further hypothetical
        considerations on the building up of heavier elements follow.
      ]
    ])
  ]
  #source[#link("https://doi.org/10.1007/BF01341595")[Atkinson & Houtermans · Z. Phys. 54, 656–665 (1929)] · Title and full abstract translated from the original · Koralm image: FusionIntroSlides]
]

#slide(title: [1934], background: "dark")[
  #at(1, 12)[
    #place(dx: 14.24mm, dy: 14.50mm, image("photos/discovering-fusion/original/cockcroft-walton.png", width: 97.55mm, height: 130.07mm, fit: "stretch", alt: "Cambridge Cockcroft–Walton apparatus1932"))
    #place(dx: 116.24mm, dy: 12.17mm, box(width: 140.17mm, height: 33.25mm, clip: true)[#place(dx: -0.00mm, dy: -0.00mm, image("photos/discovering-fusion/original/oliphant-header.png", width: 140.17mm, height: 67.99mm, fit: "stretch"))])
    #place(dx: 134.93mm, dy: 36.48mm, box(width: 93.59mm, height: 108.08mm, clip: true)[#place(dx: -0.00mm, dy: -4.45mm, image("photos/discovering-fusion/original/oliphant-yield.png", width: 93.59mm, height: 112.53mm, fit: "stretch"))])
  ]
  #source[#link("https://cudl.lib.cam.ac.uk/view/PH-CAVENDISH-P-00514/1")[Cavendish P514 · Cambridge University Library · CC BY-NC 4.0] · #link("https://doi.org/10.1098/rspa.1934.0077")[Oliphant, Harteck & Rutherford (1934)]]
]

#slide(title: [D + D → T + p + 4.0 MeV], background: "dark")[
  #at(1, 12)[
    #place(dx: 18.54mm, dy: 17.39mm, image("photos/discovering-fusion/original/reaction-dd-proton.png", width: 227.79mm, height: 109.87mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 144.79mm, dy: 37.84mm, text(size: 17pt)[$ ""^2 upright("H") $])
    #place(dx: 139.32mm, dy: 96.37mm, text(size: 17pt)[$ ""^2 upright("H") $])
    #place(dx: 195.35mm, dy: 36.30mm, text(size: 17pt)[$ ""^3 upright("H") $])
    #place(dx: 206.23mm, dy: 94.03mm, text(size: 17pt)[$ p $])
  ]
  #source[Christopher Albert · original reaction drawing, FusionIntroSlides · D: deuterium; T: tritium; p: proton; n: neutron]
]

#slide(title: [D + D → T + p + 4.0 MeV], background: "dark")[
  #at(1, 12)[
    #place(dx: 18.72mm, dy: 17.44mm, image("photos/discovering-fusion/original/reaction-dd-neutron.png", width: 227.59mm, height: 109.78mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 144.79mm, dy: 37.84mm, text(size: 17pt)[$ ""^2 upright("H") $])
    #place(dx: 139.32mm, dy: 96.37mm, text(size: 17pt)[$ ""^2 upright("H") $])
    #place(dx: 193.98mm, dy: 36.30mm, text(size: 17pt)[$ ""^3 upright("He") $])
    #place(dx: 206.23mm, dy: 94.03mm, text(size: 17pt)[$ n $])
    #place(dx: 0mm, dy: 0mm, [D + D → ³He + n + 3.3 MeV])
  ]
  #source[Christopher Albert · original reaction drawing, FusionIntroSlides · D: deuterium; T: tritium; p: proton; n: neutron]
]

#slide(title: [D + D → T + p + 4.0 MeV], background: "dark")[
  #at(1, 12)[
    #place(dx: 18.73mm, dy: 17.58mm, box(width: 227.60mm, height: 109.40mm, clip: true)[#place(dx: -24.45mm, dy: -12.87mm, image("photos/discovering-fusion/original/reaction-dt.png", width: 272.90mm, height: 137.39mm, fit: "stretch"))])
    #place(dx: 144.79mm, dy: 37.84mm, text(size: 17pt)[$ ""^2 upright("H") $])
    #place(dx: 139.32mm, dy: 96.37mm, text(size: 17pt)[$ ""^3 upright("H") $])
    #place(dx: 193.98mm, dy: 36.30mm, text(size: 17pt)[$ ""^4 upright("He") $])
    #place(dx: 206.23mm, dy: 94.03mm, text(size: 17pt)[$ n $])
    #place(dx: 0mm, dy: 0mm, [D + D → ³He + n + 3.3 MeV])
    #place(dx: 0mm, dy: 10mm, [D + T → ⁴He + n + 17.6 MeV])
  ]
  #source[Christopher Albert · original reaction drawing, FusionIntroSlides · D: deuterium; T: tritium; p: proton; n: neutron]
]

#slide(title: [1943–1952], background: "dark")[
  #at(1, 12)[
    #place(dx: 34.92mm, dy: 10.82mm, image("photos/discovering-fusion/original/cross-sections-1943-1952.png", width: 181.58mm, height: 133.74mm, fit: "stretch", alt: "Historical D–T/D–D cross-sections Fig.2"))
  ]
  #source[#link("https://arxiv.org/abs/2302.04206")[M. B. Chadwick et al. (2023), Fig. 2 · Historical fusion cross-section measurements]]
]

#slide(title: [Lawson · 1955], background: "dark")[
  #at(1, 12)[
    #place(dx: 182mm, dy: 5mm, image("photos/discovering-fusion/original/lawson.jpeg",
      width: 67mm, height: 50mm, fit: "contain", alt: "John David Lawson."))
    #place(dx: 182mm, dy: 59mm, text(size: 12pt)[John David Lawson\ (1923–2008)])

    #place(dx: 57mm, dy: 38mm, text(size: 36pt)[$p$])
    #place(dx: 10mm, dy: 75mm, text(size: 36pt)[$n$])
    #place(dx: 36mm, dy: 75mm, text(size: 36pt)[$times$])
    #place(dx: 56mm, dy: 75mm, text(size: 36pt)[$k_B T$])
    #place(dx: 99mm, dy: 75mm, text(size: 36pt)[$times$])
    #place(dx: 120mm, dy: 75mm, text(size: 36pt)[$tau_E$])
    #place(dx: 158mm, dy: 40mm, text(size: 80pt)[☕])

    #place(dx: 21mm, dy: 47mm, rotate(40deg, origin: center + horizon,
      image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 25mm, height: 24mm)))
    #place(dx: 60mm, dy: 47mm, rotate(-28deg, origin: center + horizon,
      image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 25mm, height: 24mm)))
    #place(dx: 136mm, dy: 51mm, rotate(45deg, origin: center + horizon,
      image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 25mm, height: 24mm)))
    #place(dx: 62mm, dy: 94mm, rotate(215deg, origin: center + horizon,
      image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 23mm, height: 22mm)))
    #place(dx: 37mm, dy: 116mm, text(size: 30pt)[$lr(⟨ E ⟩)$])
    #place(dx: 102mm, dy: 123mm, text(size: 27pt)[$p tau_E > 3 times 10^5 "Pa s"$ (D–T)])
  ]
  #source[Original diagram and portrait: FusionIntroSlides · #link("https://doi.org/10.1088/0370-1301/70/1/303")[Lawson (1957)] · approximate D–T scale near optimal temperature]
]

#slide(title: [The Sun], background: "dark")[
  #at(1, 12)[
    #place(dx: 116mm, dy: -5mm, image("photos/discovering-fusion/sun-sdo-20260501.jpg",
      width: 141mm, height: 141mm, fit: "contain", alt: "NASA/SDO ultraviolet image of the Sun."))
    #place(dx: 0mm, dy: 10mm, block(width: 118mm)[
      $rho ~ 10^5 "kg/m"^3$ #v(7mm)
      $T ~ 10^7 "K"$ #v(7mm)
      $p ~ 10^16 "Pa"$ #v(7mm)
      $tau_E ~ 10^7 "years" ~ 3 times 10^14 "s"$
    ])
    #place(dx: 0mm, dy: 90mm, text(size: 23pt)[$p tau_E ~ 3 times 10^30 "Pa s"$])
    #place(dx: 0mm, dy: 110mm, text(size: 23pt)[$> 10^29 "Pa s"$ (p–p)])
    #place(dx: 0mm, dy: 132mm, text(size: 18pt)[$4 upright("H") arrow.r upright("He") + Q$])
  ]
  #source[FusionIntroSlides · #link("https://www.astro.princeton.edu/~burrows/classes/204/sun.interior.pdf")[Thermal time: solar stored energy / luminosity] · NASA/SDO and AIA, EVE, HMI science teams · public domain]
]

#slide(title: [Tokamak JET], background: "dark")[
  #at(1, 12)[
    #place(dx: 128.50mm, dy: 38.38mm, image("photos/discovering-fusion/original/jet-plasma.jpeg", width: 124.27mm, height: 100.23mm, fit: "stretch", alt: "JET interior/plasma composite"))
    #place(dx: 22.96mm, dy: 108.99mm, image("photos/discovering-fusion/original/chalk-deuterium.png", width: 16.17mm, height: 17.48mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 74.85mm, dy: 108.77mm, image("photos/discovering-fusion/original/chalk-tritium.png", width: 17.93mm, height: 17.93mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 22.96mm, dy: 127.36mm, text(size: 17pt)[$ ""^2 upright("H") $])
    #place(dx: 76.74mm, dy: 127.91mm, text(size: 17pt)[$ ""^3 upright("H") $])
    #place(dx: 217.26mm, dy: 77.21mm, rotate(270.00000deg, origin: center + horizon, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 16.17mm, height: 19.92mm, fit: "stretch", alt: "Original-looking chalk physics drawing")))
    #place(dx: 228.64mm, dy: 81.64mm, image("photos/discovering-fusion/original/chalk-arrow-right.png", width: 11.31mm, height: 11.25mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 217.45mm, dy: 72.28mm, text(size: 17pt)[$ r approx 1 "m" $])
    #place(dx: 40.97mm, dy: 110.13mm, rotate(270.00000deg, origin: center + horizon, scale(x: 100%, y: -100%, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 15.58mm, height: 15.21mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))))
    #place(dx: 57.82mm, dy: 110.19mm, rotate(90.00000deg, origin: center + horizon, scale(x: 100%, y: -100%, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 15.58mm, height: 15.21mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))))
    #place(dx: 0mm, dy: 15mm, block(width: 125mm)[
      $rho ~ 10^(-7) "kg/m"^3$ #v(8mm)
      $T ~ 2 times 10^8 "K"$ #v(8mm)
      $p ~ 10^5 "Pa"$ #v(8mm)
      $tau_E ~ 1 "s"$
    ])
    #place(dx: 10mm, dy: 90mm, text(size: 20pt)[$p tau_E ~ 10^5 "Pa s"$])
  ]
  #source[JET photograph: FusionIntroSlides, slide 21 · original annotations: Christopher Albert · approximate illustrative parameters]
]

#slide(title: [National Ignition Facility], background: "dark")[
  #at(1, 12)[
    #place(dx: 22.96mm, dy: 108.99mm, image("photos/discovering-fusion/original/chalk-deuterium.png", width: 16.17mm, height: 17.48mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 74.85mm, dy: 108.77mm, image("photos/discovering-fusion/original/chalk-tritium.png", width: 17.93mm, height: 17.93mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))
    #place(dx: 40.97mm, dy: 110.13mm, rotate(270.00000deg, origin: center + horizon, scale(x: 100%, y: -100%, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 15.58mm, height: 15.21mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))))
    #place(dx: 57.82mm, dy: 110.19mm, rotate(90.00000deg, origin: center + horizon, scale(x: 100%, y: -100%, image("photos/discovering-fusion/original/chalk-arrow-up.png", width: 15.58mm, height: 15.21mm, fit: "stretch", alt: "Original-looking chalk physics drawing"))))
    #place(dx: 127.01mm, dy: 32.42mm, box(width: 125.71mm, height: 107.18mm, clip: true)[#place(dx: -20.46mm, dy: -0.00mm, image("photos/discovering-fusion/original/nif-laser-bay.png", width: 163.84mm, height: 107.18mm, fit: "stretch"))])
    #place(dx: 22.96mm, dy: 127.36mm, text(size: 17pt)[$ ""^2 upright("H") $])
    #place(dx: 76.74mm, dy: 127.91mm, text(size: 17pt)[$ ""^3 upright("H") $])
    #place(dx: 0mm, dy: 15mm, block(width: 125mm)[
      $rho ~ 10^5 "kg/m"^3$ #v(8mm)
      $T ~ 10^8 "K"$ #v(8mm)
      $p ~ 5 times 10^16 "Pa"$ #v(8mm)
      $tau ~ 100 "ps"$
    ])
    #place(dx: 10mm, dy: 90mm, text(size: 20pt)[$p tau ~ 5 times 10^6 "Pa s"$])
  ]
  #source[NIF laser bay photograph and original annotations: FusionIntroSlides, slide 22 · LLNL/NIF · illustrative compressed-fuel parameters]
]

#slide(title: [A D-T fusion power plant], background: "dark")[
  #at(1, 12, y: 27mm)[#align(center, flow(
    node((0, 0), [D + T\ fuel], width: 35mm),
    edge("-|>"), node((1, 0), [Fusion\ plasma], width: 35mm),
    edge("-|>", [neutrons], label-side: left, label-sep: 20mm),
    node((2, 0), [Heat\ collection], width: 40mm),
    edge("-|>"), node((3, 0), [Turbine +\ generator], width: 40mm),
    edge("-|>"), node((4, 0), [Electricity], width: 35mm),
    node((1, 1), [Heating +\ plant systems], width: 45mm),
    node((3, 1), [Rejected\ heat], width: 40mm),
    edge((3, 0), (3, 1), "-|>"),
    edge((4, 0), (4, 1.9), (1, 1.9), (1, 1), "-|>"),
    edge((1, 1), (1, 0), "-|>"),
  ))]
  #source[Original concept diagram; cooling, exhaust and detailed power balance developed in Chapters 4 and 10.]
]

#slide(title: [Making the tritium fuel], background: "dark")[
  #at(1, 12, y: 7mm)[#align(center, text(size: result-size)[
    $n + ""^6upright("Li") arrow.r ""^4upright("He") + upright("T") + 4.8 "MeV"$
  ])]
  #at(1, 12, y: 45mm)[#align(center, flow(
    node((0, 0), [D-T plasma], width: 54mm),
    edge("-|>", [neutrons], label-side: left, label-sep: 20mm),
    node((1, 0), [Lithium-containing\ surrounding material], width: 76mm),
    edge((1, 0), (1, 1), "-|>"),
    node((1, 1), [Extract tritium], width: 76mm),
    edge((1, 1), (0, 1), "-|>"),
    node((0, 1), [Return fuel], width: 54mm),
    edge((0, 1), (0, 0), "-|>"),
  ))]
  #source[This surrounding heat-collecting, tritium-producing region is the breeding blanket. Details: Chapter 10.]
]

#slide(title: [Scientific sources], background: "dark")[
  #at(1, 12)[
    #link("https://www.nobelprize.org/uploads/2018/06/aston-lecture.pdf")[Aston · Nobel lecture (1922)]
    #v(6mm)#link("https://doi.org/10.1038/106014a0")[Eddington · The internal constitution of the stars (1920)]
    #v(6mm)#link("https://doi.org/10.1007/BF01341595")[Atkinson & Houtermans · Z. Phys. 54, 656–665 (1929)]
    #v(6mm)#link("https://doi.org/10.1098/rspa.1934.0077")[Oliphant, Harteck & Rutherford · Heavy-hydrogen reactions (1934)]
    #v(6mm)#link("https://doi.org/10.1088/0370-1301/70/1/303")[Lawson · Criteria for a power producing thermonuclear reactor (1957)]
    #v(6mm)#link("https://pml.nist.gov/cgi-bin/Compositions/stand_alone.pl?ascii=ascii")[NIST · Atomic weights and isotopic compositions]
    #v(6mm)#link("https://www.iaea.org/topics/energy/fusion/faqs")[IAEA · Fusion energy] #h(8mm)
    #link("https://lasers.llnl.gov/about/how-nif-works/target-chamber")[LLNL · NIF target chamber]
  ]
]

#slide(title: [Image sources and licences], background: "dark")[
  #at(1, 12)[
    #text(size: 15pt)[
      Christopher Albert · drawings and annotations from FusionIntroSlides
      #v(5mm)#link("https://commons.wikimedia.org/wiki/File:SDO_20260501_000906_4096_0304_(AIA).jpg")[Sun · NASA/SDO and AIA, EVE, HMI science teams · public domain]
      #v(5mm)#link("https://wellcomecollection.org/works/h3cuknsg")[Potteries · Wellcome Collection · M0003525]
      #v(5mm)#link("https://cudl.lib.cam.ac.uk/view/PH-CAVENDISH-P-00042/1")[Aston laboratory · Cambridge University Library, P42 · CC BY-NC 4.0]
      #v(5mm)#link("https://cudl.lib.cam.ac.uk/view/PH-CAVENDISH-P-00514/1")[1932 apparatus · Cambridge University Library, P514 · CC BY-NC 4.0]
      #v(5mm)#link("https://creativecommons.org/licenses/by-nc/4.0/")[CC BY-NC 4.0 licence]
      #v(5mm)#link("https://archive.org/details/isotopes00asto")[Aston plates · Isotopes (1922)]
      #v(5mm)Eddington, Einstein (Arthur Sasse, 1951), Lawson, JET, NIF, Doge, Koralm:\ original images from FusionIntroSlides; scientific figures cited on their slides.
      #v(6mm)Noncommercial university teaching · third-party images retain their own terms
    ]
    #v(5mm)#text(size: small-size, fill: rgb("#B8C2CC"), ai-line)
  ]
]
