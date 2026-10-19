#import "../theme.typ": *
#let deck-plot(name, alt, caption) = figure(
  image("/slides/build/fig/" + name + ".svg", width: 70%, alt: alt),
  caption: caption,
)

#let chapter = [
#page-title(number: 2)[Fusion reactions] <fusion-reactions>
#lead[Two nuclei must come within the range of the strong force, but their
Coulomb repulsion turns them around much earlier. Quantum tunnelling through
the barrier sets the energy dependence of every fusion cross section.]

#section-title[Main fusion reactions] <fusion-main-reactions>
The light-nucleus reactions relevant for power plants and stars release the
energy $Q$ as kinetic energy of the products, given in parentheses:
#figure(table(columns: 2, align: (right, left), stroke: none,
  [D–T], $"D" + "T" -> ""^4"He" (3.5 "MeV") + "n" (14.1 "MeV")$,
  [D–D], $"D" + "D" -> "T" (1.01 "MeV") + "p" (3.02 "MeV")$,
  [], $"D" + "D" -> ""^3"He" (0.82 "MeV") + "n" (2.45 "MeV")$,
  [D–#super[3]He], $"D" + ""^3"He" -> ""^4"He" (3.6 "MeV") + "p" (14.7 "MeV")$,
  [p–#super[11]B], $"p" + ""^11"B" -> 3 thin ""^4"He" quad (8.7 "MeV")$,
  [p–p (Sun)], $"p" + "p" -> "D" + "e"^+ + nu_e quad (0.42 "MeV")$,
), caption: [Main fusion reactions with product kinetic energies.]) <fusion-reaction-table>
D–T releases $Q = 17.6 "MeV"$, most of it carried by the neutron. All
reactants are positively charged, so every reaction first has to overcome
their Coulomb repulsion.
#knowledge-check((
  (question: [Why does the neutron carry about 4/5 of the D–T energy?], answer: [Equal and opposite momenta give kinetic energies inversely proportional to mass; $m_alpha \/ m_"n" approx 4$.]),
  (question: [What do all reactions in the table have in common before they can fuse?], answer: [Two positive nuclei must approach against their Coulomb repulsion.]),
))

#section-title[Two-body Coulomb problem] <fusion-two-body>
Two nuclei with charges $Z_1 e$, $Z_2 e$, masses $m_1$, $m_2$, positions
$bold(r)_1$, $bold(r)_2$ and momenta $bold(p)_1$, $bold(p)_2$ interact only
through their Coulomb potential:
$ H = (p_1^2)/(2 m_1) + (p_2^2)/(2 m_2) + (Z_1 Z_2 e^2)/(4 pi epsilon_0 |bold(r)_1 - bold(r)_2|). $ <ch02-hamiltonian>
With the total mass $M$ and the reduced mass $m$,
$ M = m_1 + m_2, quad m = (m_1 m_2)/(m_1 + m_2), $ <ch02-reduced-mass>
the centre-of-mass and relative coordinates and their conjugate momenta are
$ bold(R) = (m_1 bold(r)_1 + m_2 bold(r)_2)/M, quad bold(r) = bold(r)_1 - bold(r)_2, quad
  bold(P) = bold(p)_1 + bold(p)_2, quad bold(p) = (m_2 bold(p)_1 - m_1 bold(p)_2)/M. $ <ch02-cm-coordinates>
Inserting $bold(p)_1 = (m_1 \/ M) bold(P) + bold(p)$ and
$bold(p)_2 = (m_2 \/ M) bold(P) - bold(p)$ cancels the mixed terms
$plus.minus bold(P) dot bold(p) \/ M$ in the kinetic energy, so
$ H = P^2/(2 M) + p^2/(2 m) + (Z_1 Z_2 e^2)/(4 pi epsilon_0 r). $ <ch02-separated-hamiltonian>
The centre of mass moves freely; the relative separation moves like one
particle of mass $m$ in the potential
$ V(r) = (Z_1 Z_2 e^2)/(4 pi epsilon_0 r). $ <ch02-coulomb-potential>
#knowledge-check((
  (question: [Compute the D–T reduced mass from $m_"D" approx 2 "u"$ and $m_"T" approx 3 "u"$.], answer: [$m = 6\/5 "u" = 1.2 "u"$.]),
  (question: [Why does $H$ not depend on $bold(R)$?], answer: [The interaction depends only on the separation $bold(r)_1 - bold(r)_2$.]),
))

#section-title[Head-on Coulomb encounter] <head-on-encounter>
Because $H$ does not depend on $bold(R)$,
$dot(bold(P)) = -partial H \/ partial bold(R) = 0$; we work in the
centre-of-mass frame, $bold(P) = 0$. In a head-on collision the relative
angular momentum vanishes, $ell = 0$, and the relative motion is
one-dimensional with constant energy
$ E = m/2 dot(r)^2 + V(r). $ <ch02-radial-energy>
The relative particle comes in, reaches $dot(r) = 0$ where $V(r_c) = E$ and is
reflected there at the classical turning point
$ r_c = (Z_1 Z_2 e^2)/(4 pi epsilon_0 E). $ <ch02-turning-point>
Solving the energy relation for $dot(r) = plus.minus sqrt(2(E - V)\/m)$ and
separating variables gives the orbit by quadrature, with $t = 0$ at the turning
point:
$ |t| = sqrt(m/2) integral_(r_c)^r (dif r')/sqrt(E - V(r')). $ <ch02-quadrature>
Classically the region $r < r_c$ is forbidden, because there $V(r) > E$
would require a negative kinetic energy.
#knowledge-check((
  (question: [What fixes the turning point in a head-on collision?], answer: [$dot(r) = 0$, so the whole energy is potential, $V(r_c) = E$.]),
  (question: [How does $r_c$ change when the energy is doubled?], answer: [It halves, $r_c prop 1\/E$.]),
))

#section-title[Rutherford scattering and nuclear size] <fusion-rutherford>
Geiger and Marsden scattered $alpha$ particles of energy $E$ on gold foil
#link("https://doi.org/10.1098/rspa.1909.0054")[(1909)]. At impact parameter
$b$ the orbits are hyperbolae; head-on, $b = 0$, the $alpha$ particle of
charge $Z_alpha e$ turns at
$ r_c = (Z_alpha Z e^2)/(4 pi epsilon_0 E), $ <ch02-rutherford-rc>
the smallest distance reached for given $E$. Rutherford's pure Coulomb
scattering law #link("https://doi.org/10.1080/14786440508637080")[(1911)]
fits as long as $r_c$ stays outside the nucleus. With $Z_alpha = 2$ and
$e^2 \/ (4 pi epsilon_0) = 1.44 "MeV fm"$:
#figure(table(columns: 5, align: left, stroke: none,
  [], [$Z$], [$E$], [$r_c$], [],
  [Au], [$79$], [$5 "MeV"$], [$45 "fm"$], [Coulomb],
  [Al], [$13$], [$7.7 "MeV"$], [$5 "fm"$], [deviation],
), caption: [Head-on turning distance of $alpha$ particles.]) <fusion-rutherford-table>
Deviations from Rutherford's law appear for light targets, where $r_c$
reaches the nuclear surface
#link("https://doi.org/10.1098/rspa.1924.0029")[(Bieler 1924)],
#link("https://doi.org/10.1080/14786442508628535")[(Rutherford and Chadwick 1925)].
Hence $r_c approx R$ measures the nuclear radius, $R tilde 10^(-15) "m"$.
#knowledge-check((
  (question: [Why do light targets reveal the nuclear size first?], answer: [Small $Z$ gives small $r_c$ at the same $E$, so the $alpha$ particle reaches the nuclear force range.]),
  (question: [Check the Au entry of the table.], answer: [$2 times 79 times 1.44 "MeV fm" \/ 5 "MeV" = 45 "fm"$.]),
))

#section-title[Classical turning point] <fusion-classical-threshold>
Classically, fusion requires the nuclei to touch, $r_c lt.tilde r_0$ with
$r_0 approx 10^(-15) "m"$. For $Z_1 = Z_2 = 1$,
$ r_c lt.tilde r_0 quad => quad E gt.tilde (e^2)/(4 pi epsilon_0 r_0) approx 1.4 "MeV". $ <ch02-classical-threshold>
This is more than a hundred times the thermal energy of a fusion plasma
($tilde 10 "keV"$). Classically such a plasma would hardly fuse at all.

Quantum mechanically the relative motion is a wave with reduced wavelength
$ƛ = ħ \/ (m v)$, where $v$ is the initial relative speed and
$E = m v^2 \/ 2$. Inserting $E$ into the turning point gives
$ r_c = (Z_1 Z_2 e^2)/(4 pi epsilon_0) (2)/(m v^2)
  = 2 (Z_1 Z_2 e^2)/(4 pi epsilon_0 ħ v) (ħ)/(m v) = 2 eta ƛ, quad
  eta = (Z_1 Z_2 e^2)/(4 pi epsilon_0 ħ v). $ <ch02-sommerfeld>
The Sommerfeld parameter $eta$ counts the turning distance in wavelengths. In
units of $ƛ$ the encounter depends only on $eta$ and the shape of the incoming
packet, so one simulation describes every pair at the same $eta$. For D–T,
$m = 2.0141 times 3.0160 \/ 5.0301 thin "u" = 1.2076 thin "u"$, and
$eta = 2$ corresponds to $E = 7.5 thin "keV"$ and
$r_c = 1.440 thin "MeV fm" \/ 7.5 thin "keV" = 0.19 thin "pm"$, still far
outside the nuclei (a few fm).

#animation("animations/coulomb_collision.mp4",
  "Head-on D-T collision at eta = 2 seen from above in the centre-of-mass frame, shown in three parts on the same clock, axes and scale: the classical collision alone, the quantum collision alone, and both side by side. Classical: the deuteron (small dot) and the triton (larger dot) approach along a line, slow down, turn at separation r_c and fly apart. Quantum: each nucleus is a probability cloud; the clouds approach, show interference fringes while they are reflected, and a small part reaches separations below r_c, drawn in yellow.",
  poster: "../media/coulomb-collision.png",
  caption: [Head-on D–T collision ($ell = 0$) at $eta = 2$
  ($E = 7.5 thin "keV"$), seen from above in the centre-of-mass frame (the
  cross marks the centre of mass), shown three times on the same clock, axes
  and scale: classical alone, quantum alone, and both side by side. With
  separation $r$ the nuclei sit at
  $x_"D" = -(m_"T" \/ M) r$ and $x_"T" = (m_"D" \/ M) r$, $M = m_"D" + m_"T"$;
  the bar marks $r_c$ between the turning positions, and the shaded band is
  $r < r_c$. Classical: point particles on
  the orbit $r(t)$ at energy $E$, reflected at $r_c$. Quantum: the
  densities of $x_"D"$ and $x_"T"$ obtained from the $ell = 0$ wave
  packet $|u(r, t)|^2$ (12 % energy spread) by the same relations. Incoming
  and reflected waves interfere into fringes, and a few per cent of the
  probability reaches $r < r_c$ (yellow, brightened), where tunnelling starts.
  The width across the collision axis is illustrative only.])

#knowledge-check((
  (question: [How far below the classical threshold is a 10 keV plasma?], answer: [About a factor $1.4 "MeV" \/ 10 "keV" approx 140$ in energy.]),
  (question: [What does $eta = 2$ mean geometrically?], answer: [The turning distance is two reduced wavelengths, $r_c = 4 ƛ$.]),
))

#section-title[Quantum ballpark] <fusion-quantum-ballpark>
The relative wave has the reduced de Broglie wavelength
$ ƛ = lambda/(2 pi) = ħ/p = ħ/sqrt(2 m E). $ <ch02-wavelength>
A wave does not resolve structure smaller than $ƛ$, so the barrier stops being
an obstacle once it is no thicker than a wavelength. With
$e^2 \/ (4 pi epsilon_0) = alpha ħ c$ the turning point is
$r_c = alpha Z_1 Z_2 ħ c \/ E$, and
$ ƛ approx r_c quad => quad E approx 2 m c^2 (alpha Z_1 Z_2)^2. $ <ch02-ballpark>
For D–T ($m c^2 = 1.125 "GeV"$) this gives $E approx 120 "keV"$, an order of
magnitude below the classical estimate. The ratio
$ r_c/ƛ = alpha Z_1 Z_2 c sqrt((2 m)/E) prop E^(-1\/2) $ <ch02-thickness-ratio>
measures the barrier thickness in wavelengths; it grows slowly as $E$ drops.
#knowledge-check((
  (question: [Why is the quantum estimate lower than the classical one?], answer: [The wave reaches through a barrier of thickness up to about $ƛ$, so the nuclei need not touch classically.]),
  (question: [By which factor does $r_c \/ ƛ$ change when $E$ drops by 4?], answer: [It doubles.]),
))

#section-title[Tunnelling through the Coulomb barrier] <fusion-gamow>
Inside the barrier, $V(r) > E$, the wave decays with the local rate
$ kappa(r) = sqrt(2 m (V(r) - E))/ħ. $ <ch02-kappa-general>
Divide the forbidden region $0 < r < r_c$ into slices of width $Delta r$. Over
slice $i$ the amplitude falls by $e^(-kappa_i Delta r)$ and the probability by
$P_i approx e^(-2 kappa_i Delta r)$. The slices act in series, so their
transmissions multiply:
$ P approx product_i P_i = exp(-2 sum_i kappa_i Delta r) -> exp(-2 integral_0^(r_c) kappa(r) dif r). $ <ch02-wkb>
For the Coulomb barrier, $V(r) = E r_c \/ r$, and with $ƛ = ħ \/ sqrt(2 m E)$
$ kappa(r) = sqrt(2 m E)/ħ sqrt(r_c/r - 1) = 1/ƛ sqrt(r_c/r - 1). $ <ch02-kappa>
With $r = r_c x$ the exponent becomes a pure number times $r_c \/ ƛ$. The
substitution $x = sin^2 theta$, $dif x = 2 sin theta cos theta dif theta$,
turns the integrand into $2 cos^2 theta$:
$ 2 integral_0^(r_c) kappa dif r = (2 r_c)/ƛ integral_0^1 sqrt(1/x - 1) dif x
  = (2 r_c)/ƛ integral_0^(pi\/2) 2 cos^2 theta dif theta = pi r_c/ƛ. $ <ch02-gamow-integral>
Inserting $r_c \/ ƛ$ from the quantum ballpark gives the Gamow factor
#link("https://doi.org/10.1007/BF01343196")[(Gamow 1928)],
#link("https://doi.org/10.1038/122439a0")[(Gurney and Condon 1928)]
$ P approx exp(-pi r_c/ƛ) = exp(-sqrt(E_G/E)), quad E_G = 2 m c^2 (pi alpha Z_1 Z_2)^2. $ <ch02-gamow-energy>
The Gamow energy is the ballpark energy $2 m c^2 (alpha Z_1 Z_2)^2$ times $pi^2$. Atkinson and
Houtermans applied this tunnelling to fusion in stars
#link("https://doi.org/10.1007/BF01341595")[(1929)].
#knowledge-check((
  (question: [Evaluate $E_G$ for D–T.], answer: [$2 times 1.125 "GeV" times (pi \/ 137.036)^2 approx 1.18 "MeV"$.]),
  (question: [Why does p–p have the smallest $E_G$ despite equal charges to D–D?], answer: [Its reduced mass, $m_"p" \/ 2$, is half that of D–D.]),
))

#section-title[Cross section] <fusion-cross-section>
A wave of reduced wavelength $ƛ$ interacts with a target over an area of
order $pi ƛ^2$, the de Broglie area:
$ sigma_"geo" tilde pi ƛ^2 = (pi ħ^2)/(2 m E) prop 1/E. $ <ch02-geometric-cross-section>
Multiplying by the penetration probability $P$ and collecting
everything else in the astrophysical $S$ factor gives
$ sigma(E) = S(E)/E exp(-sqrt(E_G/E)). $ <ch02-cross-section>

#interpretation[Competing factors][
The $1\/E$ factor (de Broglie area) diverges at low $E$, but the Coulomb
penetration $exp(-sqrt(E_G \/ E))$ vanishes there. At high $E$ penetration
is easy, but $1\/E$ reduces $sigma$. This competition sets the shape of
$sigma(E)$; $S(E)$ carries the scale and the nuclear corrections.
]

#deck-plot("cross_section_shape",
  "Log-log plot of sigma = exp(-sqrt(E_G/E))/E with S = 1 keV b for D-T, D-D and p-p from 1 to 1000 keV. All three curves rise steeply at low energy and flatten towards 1/E at high energy; p-p, with the smallest Gamow energy, lies highest and D-T lowest.",
  [Tunnelling alone: $sigma = exp(-sqrt(E_G \/ E)) \/ E$ with $S = 1 "keV b"$,
  for $E_G = 1.18 "MeV"$ (D–T), $0.99 "MeV"$ (D–D) and $0.49 "MeV"$ (p–p).])

The actual cross sections differ mainly through $S$: $S(0) approx 10^4 "keV b"$
for D–T, $approx 10^2 "keV b"$ for D–D and $4 times 10^(-22) "keV b"$ for p–p,
where the weak interaction must convert a proton into a neutron during the
encounter. The next lecture discusses $S(E)$.

#deck-plot("cross_section_actual",
  "Log-log plot of the measured-fit cross sections sigma(E) for D-T, D-D and p-p from 1 to 1000 keV on a broken vertical axis. D-T peaks near 5 b at about 64 keV; D-D lies about two orders lower; p-p lies some 24 decades lower on the lower panel.",
  [Actual cross sections from the Bosch–Hale fits for D–T and D–D
  #link("https://doi.org/10.1088/0029-5515/32/4/I07")[(Bosch and Hale 1992)]
  and the p–p $S$ factor of
  #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. (2011)]. The vertical axis is broken.])
Measured cross sections give $S$ directly, $S_i = sigma_i E_i exp(sqrt(E_G \/ E_i))$
with $E_i$ the centre-of-mass energy in keV and $sigma_i$ in barn. We converted the
EXFOR tables of
#link("https://doi.org/10.1103/PhysRev.93.483")[Arnold et al. (1954)],
#link("https://doi.org/10.1103/PhysRev.107.1616")[Bame and Perry (1957)],
#link("https://doi.org/10.1103/PhysRevC.29.2031")[Jarmie et al. (1984)] and
#link("https://doi.org/10.1103/PhysRevC.35.1999")[Brown et al. (1987)] for D–T, and of
#link("https://doi.org/10.1098/rspa.1954.0249")[Preston et al. (1954)],
#link("https://doi.org/10.1007/BF01292792")[Greife et al. (1995)] and
#link("https://doi.org/10.1103/PhysRevC.73.045801")[Leonard et al. (2006)] for D–D,
and fitted the Bosch–Hale rational form by weighted least squares with the
published error bars (script `derivations/chapters/ch02_s_factor_fit.py`). Our D–T
curve lies about 3 % below Bosch–Hale at 64 keV.

#knowledge-check((
  (question: [What dominates $sigma(E)$ well below $E_G$?], answer: [The penetration factor $exp(-sqrt(E_G \/ E))$, which rises steeply with $E$.]),
  (question: [Why is the p–p cross section so much smaller than D–D at the same energy?], answer: [Its $S$ factor is about 24 orders of magnitude smaller, because the weak interaction is needed.]),
))

#section-title[Proton–proton chain] <fusion-pp-chain>
The Sun fuses hydrogen through the p–p chain. In its main branch, two
p–p reactions each produce a deuteron, a positron and a neutrino (0.42 MeV),
each deuteron captures a proton to $""^3"He"$ (5.49 MeV), and two $""^3"He"$
nuclei fuse to $""^4"He" + 2 "p"$ (12.86 MeV). In total
$ 4 "p" -> ""^4"He" + 2 "e"^+ + 2 nu_e, $ <ch02-pp-chain>
releasing 26.7 MeV including the annihilation of the two positrons. The slow
first step, set by the tiny p–p $S$ factor, makes the Sun burn for billions of
years.
#knowledge-check((
  (question: [Check the 26.7 MeV from the branch energies.], answer: [$2 times (0.42 + 5.49) + 12.86 = 24.68 "MeV"$, plus $2 times 1.022 "MeV"$ annihilation gives 26.7 MeV.]),
  (question: [Which step limits the rate of the chain?], answer: [The weak p–p reaction.]),
))
]
