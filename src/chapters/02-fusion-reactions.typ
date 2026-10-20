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
Classically, fusion requires the nuclei to touch, $r_c lt.tilde R$, with the
nuclear radius $R = r_0 A^(1\/3) approx 10^(-15) "m"$ and $r_0 approx 1.2 "fm"$.
For $Z_1 = Z_2 = 1$,
$ r_c lt.tilde R quad => quad E gt.tilde (e^2)/(4 pi epsilon_0 R) approx 1.4 "MeV". $ <ch02-classical-threshold>
This is more than a hundred times the thermal energy of a fusion plasma
($tilde 10 "keV"$). Classically such a plasma would hardly fuse at all.

#knowledge-check((
  (question: [How far below the classical threshold is a 10 keV plasma?], answer: [About a factor $1.4 "MeV" \/ 10 "keV" approx 140$ in energy.]),
))

#section-title[Classical cross section] <fusion-classical-cross-section>
Treat the nuclei as classical charged spheres that fuse whenever their
centres come within the contact distance
$R = r_0 (A_1^(1\/3) + A_2^(1\/3))$, the sum of the two nuclear radii. A
projectile with impact parameter $b$ has angular momentum
$L = b sqrt(2 m E)$; energy and angular-momentum conservation at the closest
approach $r_"min"$ give
$ E = V(r_"min") + L^2/(2 m r_"min"^2) = V(r_"min") + E b^2/r_"min"^2. $ <ch02-closest-approach>
It reaches contact, $r_"min" <= R$, if
$ b^2 <= R^2 (1 - V(R)/E), $ <ch02-bmax>
since $V(r) + E b^2 \/ r^2$ decreases outwards for a repulsive potential. All
projectiles inside the disc of radius $b_"max"$ fuse, so the classical
cross section is
$ sigma_"cl" = pi b_"max"^2 = pi R^2 (1 - V(R)/E), quad E >= V(R), $ <ch02-classical-cross-section>
and $sigma_"cl" = 0$ below the barrier top $V(R)$. The Coulomb repulsion
shrinks the geometric area $pi R^2$; far above the barrier
$sigma_"cl" -> pi R^2$.
#figure(table(columns: 5, align: left, stroke: none,
  [], [$A_1, A_2$], [$R$], [$V(R)$], [$pi R^2$],
  [D–T], [$2, 3$], [$3.2 "fm"$], [$440 "keV"$], [$0.33 "b"$],
  [D–D], [$2, 2$], [$3.0 "fm"$], [$480 "keV"$], [$0.29 "b"$],
  [p–p], [$1, 1$], [$2.4 "fm"$], [$600 "keV"$], [$0.18 "b"$],
), caption: [Contact distance, barrier height and geometric area with $r_0 = 1.2 "fm"$.]) <fusion-classical-table>
#deck-plot("cross_section_classical",
  "Log-log plot of the classical cross section sigma_cl in barn against E from 1 keV to 100 MeV for D-T, D-D and p-p. Each curve is zero below its barrier height of 440, 480 and 600 keV, rises steeply above it and approaches the geometric area pi R^2 of 0.33, 0.29 and 0.18 b.",
  [Classical cross sections $sigma_"cl" = pi R^2 (1 - V(R) \/ E)$; below
  $V(R)$ they vanish, so a 10 keV plasma would not fuse classically.])
#knowledge-check((
  (question: [Check $V(R)$ for D–T in the table.], answer: [$R = 1.2 (2^(1\/3) + 3^(1\/3)) "fm" = 3.24 "fm"$, $V(R) = 1.44 "MeV fm" \/ 3.24 "fm" = 0.44 "MeV"$.]),
  (question: [At which energy is $sigma_"cl"$ half the geometric area?], answer: [At $E = 2 V(R)$.]),
))


#section-title[Quantum ballpark] <fusion-quantum-ballpark>
Quantum mechanically the relative motion is a wave with the reduced de Broglie wavelength
$ ƛ = lambda/(2 pi) = ħ/p = ħ/sqrt(2 m E) = ħ/(m v), $ <ch02-wavelength>
where $v$ is the initial relative speed and $E = m v^2 \/ 2$. Inserting $E$
into the turning point gives
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
  (question: [What does $eta = 2$ mean geometrically?], answer: [The turning distance is two reduced wavelengths, $r_c = 4 ƛ$.]),
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

#section-title[Measuring a cross section] <fusion-measuring-cross-section>
A beam of $N_"beam"$ particles crosses a thin target of area $A$ and
thickness $Delta x$ with $n$ nuclei per unit volume. The target holds
$N_T = n A Delta x$ nuclei, and each presents the area $sigma$ to the beam. As
long as the target is thin enough that these discs do not shadow each other,
they cover the fraction
$ P = (N_T sigma)/A = n Delta x thin sigma $ <ch02-covered-fraction>
of the beam area. Each beam particle reacts with probability $P$, so
$N_"react" = N_"beam" P$ and the measured cross section is
$ sigma = N_"react"/(N_"beam" n Delta x). $ <ch02-measured-cross-section>
Nuclear cross sections are quoted in barn, $1 "b" = 10^(-28) "m"^2$, about the
geometric area of a heavy nucleus.
#knowledge-check((
  (question: [How many reactions do $10^12$ beam particles give for $sigma = 1 "b"$ and $n Delta x = 10^22 "m"^(-2)$?], answer: [$P = 10^(-28) times 10^22 = 10^(-6)$, so $10^6$ reactions.]),
  (question: [Why must the target be thin?], answer: [So that $P << 1$: the discs do not overlap and the beam is not depleted inside the target.]),
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
encounter.

#deck-plot("cross_section_actual",
  "Log-log plot of the measured-fit cross sections sigma(E) for D-T, D-D and p-p from 1 to 1000 keV on a broken vertical axis. D-T peaks near 5 b at about 64 keV; D-D lies about two orders lower; p-p lies some 24 decades lower on the lower panel.",
  [Actual cross sections from the Bosch–Hale fits for D–T and D–D
  #link("https://doi.org/10.1088/0029-5515/32/4/I07")[(Bosch and Hale 1992)]
  and the p–p $S$ factor of
  #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. (2011)]. The vertical axis is broken.])
#knowledge-check((
  (question: [What dominates $sigma(E)$ well below $E_G$?], answer: [The penetration factor $exp(-sqrt(E_G \/ E))$, which rises steeply with $E$.]),
  (question: [Why is the p–p cross section so much smaller than D–D at the same energy?], answer: [Its $S$ factor is about 24 orders of magnitude smaller, because the weak interaction is needed.]),
))

#section-title[S factor from experiment] <fusion-s-factor-data>
Dividing a measured cross section by the de Broglie area and the
penetration factor leaves the slowly varying nuclear part,
$ S_i = sigma_i E_i exp(sqrt(E_G/E_i)), $ <ch02-s-from-sigma>
with $E_i$ the centre-of-mass energy in keV and $sigma_i$ in barn. We converted the
EXFOR tables of
#link("https://doi.org/10.1103/PhysRev.93.483")[Arnold et al. (1954)],
#link("https://doi.org/10.1103/PhysRev.107.1616")[Bame and Perry (1957)],
#link("https://doi.org/10.1103/PhysRevC.29.2031")[Jarmie et al. (1984)] and
#link("https://doi.org/10.1103/PhysRevC.35.1999")[Brown et al. (1987)] for D–T, and of
#link("https://doi.org/10.1098/rspa.1954.0249")[Preston et al. (1954)],
#link("https://doi.org/10.1007/BF01292792")[Greife et al. (1995)] and
#link("https://doi.org/10.1103/PhysRevC.73.045801")[Leonard et al. (2006)] for D–D.
For each reaction we refitted three coefficients of the rational
Bosch–Hale form #link("https://doi.org/10.1088/0029-5515/32/4/I07")[(1992)]
by weighted least squares with the published error bars, keeping the others
at their Bosch–Hale values (script `derivations/chapters/ch02_s_factor_fit.py`;
reduced $chi^2 = 0.75$ for D–T, $0.59$ and $0.58$ for the two D–D branches).
Our D–T curve lies about 3 % below Bosch–Hale at 64 keV.

#deck-plot("s_factor_data",
  "Log plot of S in keV b against E from 1 to 1000 keV. Upper panel: D-T data points from four experiments rise from about 1e4 keV b to a maximum of about 2.7e4 keV b near 50 keV and fall to below 1e3 keV b at 450 keV, with our fit as a solid line and Bosch-Hale dashed. The two D-D branches lie nearly flat between 60 and 160 keV b. Lower panel, on a broken axis: the p-p S factor, about 4e-22 keV b and nearly constant.",
  [$S$ factors from EXFOR data (markers), our fit (solid) and Bosch–Hale
  (dashed) for D–T and both D–D branches; below the broken axis the p–p $S$ factor of
  #link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. (2011)].])
Unlike $sigma$, which varies over many decades, $S$ changes by less than a
factor of three below 100 keV. The D–D $S$ factors are nearly flat. The D–T
$S$ factor has a maximum of about $2.7 times 10^4 "keV b"$ near 50 keV; the
p–p $S$ factor has never been measured in the laboratory and comes from theory.
#knowledge-check((
  (question: [Why fit $S$ rather than $sigma$?], answer: [Dividing out $exp(-sqrt(E_G\/E))\/E$ removes the steep known energy dependence; the smooth remainder is easy to fit and extrapolate.]),
  (question: [What feature in the D–T data is not explained by tunnelling?], answer: [The maximum of $S$ near 50 keV, a nuclear resonance.]),
))

#section-title[#super[5]He resonance] <fusion-he5-resonance>
D and T first form the compound nucleus $""^5"He"^*$ in an excited state at
the resonance energy $E_r$ above the D–T threshold; it decays into
$""^4"He" + "n"$ and releases 17.6 MeV. A state that decays has an amplitude
$psi(t) prop e^(-i E_r t \/ ħ) e^(-Gamma t \/ (2 ħ))$ for $t > 0$, so its
occupation decays as $|psi|^2 prop e^(-t\/tau)$ with the lifetime
$ tau = ħ/Gamma. $ <ch02-lifetime>
Its energy content follows from the Fourier transform,
$ integral_0^infinity e^(i (E - E_r) t \/ ħ) e^(-Gamma t \/ (2 ħ)) dif t
  = (i ħ)/(E - E_r + i Gamma \/ 2), $ <ch02-resonance-fourier>
whose square gives the Breit–Wigner shape of the $S$ factor near the resonance,
$ S(E) prop 1/((E - E_r)^2 + Gamma^2\/4). $ <ch02-breit-wigner>
The width $Gamma$ is the full width at half maximum. A long-lived state is
sharp; a short-lived one is broad.
#knowledge-check((
  (question: [Which lifetime belongs to $Gamma = 100 "keV"$?], answer: [$tau = 6.58 times 10^(-22) "MeV s" \/ 0.1 "MeV" approx 6.6 times 10^(-21) "s"$.]),
  (question: [Show that $Gamma$ is the full width at half maximum.], answer: [$S$ halves when $(E - E_r)^2 = Gamma^2 \/ 4$, i.e. at $E = E_r plus.minus Gamma\/2$.]),
))

#section-title[Which force?] <fusion-which-force>
Once the nuclei touch, the force that completes the reaction decides how
likely it is. In D–T, D–D, D–#super[3]He and p–#super[11]B the nucleons only
regroup into new nuclei, and the light fragment carries away the energy. The
strong interaction does this with probability of order one. In
$"D" + "p" -> ""^3"He" + gamma$ the nucleons also regroup, but no fragment is
left to carry the energy; it leaves as a photon, an electromagnetic process
with probability of order $10^(-5)$. In
$"p" + "p" -> "D" + "e"^+ + nu_e$ one proton must turn into a neutron,
$"p" -> "n" + "e"^+ + nu_e$, through the weak interaction ($W^+$ exchange),
with probability of order $10^(-22)$
#link("https://doi.org/10.1088/0029-5515/32/4/I07")[(Bosch and Hale 1992;]
#link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. 2011;]
#link("https://doi.org/10.1103/RevModPhys.97.025002")[CODATA 2022)].
These ratios explain most of the spread of the measured $S$ factors.
#knowledge-check((
  (question: [Why does p–p fusion need the weak interaction?], answer: [The diproton is unbound; only the deuteron is, so one proton must become a neutron.]),
  (question: [Why is D + p slower than D + T after contact?], answer: [No fragment can carry the energy away, so a photon must be emitted electromagnetically.]),
))

#section-title[S and the nuclear radius] <fusion-s-and-r>
The Gamow factor integrates $kappa$ from $0$ to $r_c$, but the Coulomb barrier
ends at the contact distance $R$, where the strong force takes over. The
penetration probability to $R$ is
$ P(R) = exp(-2 integral_R^(r_c) kappa dif r)
  = exp(-sqrt(E_G/E)) exp(2 integral_0^R kappa dif r). $ <ch02-barrier-to-r>
For $R << r_c$ the kinetic energy is negligible inside $R$, $V >> E$, and
$kappa approx sqrt(2 m V) \/ ħ = 1 \/ sqrt(a r)$ with the length
$ a = (4 pi epsilon_0 ħ^2)/(2 m Z_1 Z_2 e^2), $ <ch02-bohr-length>
the Bohr radius of the pair. Then $2 integral_0^R kappa dif r approx 4 sqrt(R\/a)$
and
$ P(R) approx exp(-sqrt(E_G/E)) e^(4 sqrt(R \/ a)), quad
  sigma = S/E e^(-sqrt(E_G \/ E)), quad S prop e^(4 sqrt(R \/ a)) dot P_"nuc". $ <ch02-s-and-r>
The correction does not depend on $E$ and is absorbed in $S$, together with
the probability $P_"nuc"$ that the strong, electromagnetic or weak force
completes the reaction after contact. Thus $S$ carries the nuclear physics: the
nuclear radius, the force and resonances.
#knowledge-check((
  (question: [Evaluate $a$ and $e^(4 sqrt(R\/a))$ for D–T.], answer: [$a = (ħ c)^2 \/ (2 m c^2 times 1.44 "MeV fm") = 197.3^2 \/ (2 times 1125 times 1.44) "fm" approx 12 "fm"$; with $R = 3.2 "fm"$, $e^(4 sqrt(0.27)) approx 8$.]),
  (question: [Show that $r_c \/ ƛ^2 = 1\/a$.], answer: [$r_c \/ ƛ^2 = Z_1 Z_2 e^2 \/ (4 pi epsilon_0 E) dot 2 m E \/ ħ^2 = 1\/a$.]),
))

#section-title[Range of the forces] <fusion-force-range>
A force carried by a particle of mass $m$ has the range
$ lambda = ħ/(m c), $ <ch02-force-range>
the distance the particle travels during the time $ħ \/ (m c^2)$ for which
the energy $m c^2$ may be borrowed. The static field of a massive carrier
obeys $(nabla^2 - lambda^(-2)) phi = 0$ away from the source, which gives
the Yukawa potential $phi prop e^(-r\/lambda) \/ r$; the massless photon gives
the infinite-range Coulomb potential. The pion,
$m_pi c^2 = 139.6 "MeV"$, gives $lambda_pi = 1.41 "fm"$ for the strong force
between nucleons, and the $W$ boson, $M_W c^2 = 80.4 "GeV"$, gives
$lambda_W = 2.45 times 10^(-3) "fm"$ for the weak interaction.

#deck-plot("force_ranges",
  "Log-log plot of the magnitude of the potential |V| in MeV against r from 1e-3 to 1e3 fm. The Coulomb potential (black, repulsive) falls as 1/r. The attractive strong potential (orange) is larger inside and cuts off near hbar/m_pi c, crossing the Coulomb line at the contact radius R. The weak potential (purple) cuts off near hbar/M_W c. Dashed lines mark the photon and electron-neutrino wavelengths hbar c/E_gamma and hbar c/E_e nu, far outside R.",
  [Ranges of the forces: Coulomb, strong and weak potentials with the
  Yukawa ranges $ħ \/ (m_pi c)$ and $ħ \/ (M_W c)$, the contact distance $R$
  and the wavelengths $ħ c \/ E_gamma$ and $ħ c \/ E_(e nu)$ of the emitted particles.])
By Fermi's golden rule the transition probability is
$ P prop abs(integral psi_f^* thin V thin psi_i dif^3 r)^2. $ <ch02-golden-rule>
The overlap is limited by the region where all three factors are appreciable.
For the strong force $V$ and both nuclear states share the region $r lt.tilde R$, so
$P tilde 1$. A photon of energy $E_gamma$ has the wavelength
$lambda_gamma = ħ c \/ E_gamma >> R$; it overlaps the nucleus only weakly,
and $P tilde alpha (R \/ lambda_gamma)^2 approx 10^(-5)$. The weak force acts
only over $lambda_W << R$ and the leptons have wavelength
$lambda_(e nu) = ħ c \/ E_(e nu)$, giving
$P tilde alpha_W^2 (lambda_W \/ lambda_(e nu))^4 approx 10^(-22)$. These are
order-of-magnitude estimates; they reproduce the three classes of reactions
above.
#knowledge-check((
  (question: [Compute $lambda$ for the pion and the $W$ boson.], answer: [$197.3 "MeV fm" \/ 139.6 "MeV" = 1.41 "fm"$; $197.3 "MeV fm" \/ 80.4 "GeV" = 2.45 times 10^(-3) "fm"$.]),
  (question: [Why is the photon emission probability small although $alpha$ is not tiny?], answer: [The photon wavelength is much longer than the nucleus, so the factor $(R\/lambda_gamma)^2$ suppresses the overlap.]),
))

#section-title[Computing S] <fusion-computing-s>
Including the nuclear radius, $S prop e^(4 sqrt(R\/a)) P_"nuc"$, and
$P_"nuc"$ must be computed from the nuclear interaction. For p–p the weak
transition gives $S prop G_F^2 g_A^2 abs(chevron.l "d" mid(|) "pp" chevron.r)^2$,
with the Fermi constant $G_F$, the axial coupling $g_A$ and the overlap of
the deuteron with the p–p scattering state. For D–T the R-matrix theory
#link("https://doi.org/10.1103/RevModPhys.30.257")[(Lane and Thomas 1958)]
fits $E_r$ and $Gamma$ to data and yields the Breit–Wigner shape, while
ab initio calculations solve the five-nucleon problem with realistic forces
#link("https://doi.org/10.1103/PhysRevLett.108.042503")[(Navrátil and Quaglioni 2012)].
The p–p reference value is
#link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. (2011)].
#knowledge-check((
  (question: [Which nuclear inputs enter the p–p $S$ factor?], answer: [The deuteron and p–p wave functions through their overlap, and the weak couplings $G_F$ (or $G_V$) and $g_A$.]),
  (question: [What does an R-matrix fit determine for D–T?], answer: [The resonance energy $E_r$ and width $Gamma$ of $""^5"He"^*$.]),
))

#section-title[p–p fusion from wave functions] <fusion-pp-wave-functions>
With $H_0 = -ħ^2 \/ (2 m) dif^2 \/ dif r^2$ for the radial functions $u$,
we solve two problems with the Reid potential
#link("https://doi.org/10.1016/0003-4916(68)90126-7")[(Reid 1968)], fitted to
nucleon–nucleon scattering. The deuteron is bound,
$ (H_0 + V_d) thin u_d = -B_d thin u_d, $ <ch02-deuteron>
with S and D waves coupled by the tensor force. The p–p scattering state at
$E -> 0$,
$ (H_0 + V_(p p) + V_C) thin u_(p p) = E thin u_(p p), $ <ch02-pp-scattering>
is matched to Coulomb waves outside the force range, and the Gamow factor is
divided out. The overlap
$ Lambda prop integral_0^infinity u_d thin u_(p p) dif r $ <ch02-pp-overlap>
#link("https://doi.org/10.1103/PhysRevC.58.1263")[(Schiavilla et al. 1998)]
gives $S_(p p)(0) prop G_V^2 g_A^2 f_(p p)^R Lambda^2$, with the lepton phase-space
factor $f_(p p)^R$ and the normalisation of Adelberger et al. (2011).

#deck-plot("pp_fusion_waves",
  "Two panels against r from 0 to 15 fm. Top: the Reid p-p and deuteron potentials, strongly repulsive below 0.5 fm with attractive wells of about -95 and -40 MeV near 1 fm. Bottom: the deuteron radial function u_d peaks near 1.6 fm and decays slowly; the p-p function u_pp rises steadily outwards; their product, shaded, peaks near 2 fm and extends beyond 15 fm.",
  [Reid potentials (top) and the radial functions $u_d$, $u_(p p)$ and their
  product (shaded), whose integral is $Lambda$; computed with kin6d
  (data `derivations/chapters/data/pp_fusion_kin6d.json`).])
#knowledge-check((
  (question: [Why does the overlap extend far beyond the force range?], answer: [The deuteron is weakly bound, so $u_d$ decays slowly, as $e^(-gamma r)$ with $1\/gamma approx 4.3 "fm"$.]),
  (question: [Why is the Gamow factor divided out of $u_(p p)$?], answer: [It is already in $sigma = S\/E exp(-sqrt(E_G\/E))$; $S$ keeps only the nuclear part.]),
))

#section-title[Pionless effective field theory] <fusion-pionless-eft>
The overlap is dominated by distances beyond the pion range,
$ R_pi = ħ/(m_pi c) approx 1.4 "fm" quad << quad 1/gamma approx 4.3 "fm", quad |a_(p p)| approx 7.8 "fm", $ <ch02-eft-scales>
with the deuteron tail $u_d prop e^(-gamma r)$,
$ gamma = sqrt(m_N B_d)/ħ, $ <ch02-deuteron-gamma>
and the p–p scattering length $a_(p p)$ from the effective-range expansion
$ k cot delta = -1/a_(p p) + r_(p p)/2 k^2 + dots. $ <ch02-effective-range>
Pionless EFT does not resolve $r lt.tilde R_pi$. It expands in
$R_pi gamma$ and $R_pi \/ |a_(p p)|$, takes $B_d$, $a_(p p)$ and the effective
ranges as input and needs one short-range constant $L_(1,A)$, here from
lattice QCD
#link("https://doi.org/10.1016/S0370-2693(01)01152-2")[(Butler and Chen 2001;]
#link("https://doi.org/10.1103/PhysRevLett.119.062002")[Savage et al. 2017)].
#figure(table(columns: 4, align: (right, left, left, left), stroke: none,
  [], [potential model], [pionless EFT], [reference],
  [deuteron binding], [$2.2246 "MeV"$], [input], [$2.2246 "MeV"$],
  [D-state fraction], [$6.5 %$], [–], [$tilde 5 "–" 7 %$],
  [$a_(p p)$], [$-7.75 "fm"$], [input], [$-7.81 "fm"$],
  [$Lambda^2$], [$6.91$], [$7.02$], [$approx 7.0$],
  [$S_(p p)(0) thin [10^(-25) "MeV b"]$], [$3.95$], [$4.01 plus.minus 0.27$], [$4.01 plus.minus 0.04$],
), caption: [p–p fusion computed from the Reid potential and with pionless EFT
(kin6d; `derivations/chapters/data/pp_fusion_kin6d.json` and
`pp_fusion_eft.json`), against
#link("https://doi.org/10.1103/RevModPhys.83.195")[Adelberger et al. (2011)].
The EFT uncertainty is a truncation estimate.]) <fusion-pp-table>
Order by order the EFT gives $S_(p p)(0) = 3.60$, $3.82$ and
$4.01 times 10^(-25) "MeV b"$. Both calculations agree with the reference within
a few per cent; $S_(p p)(0) = 4.01 times 10^(-25) "MeV b" = 4.01 times 10^(-22) "keV b"$
is the p–p value in the $S$-factor figure.
#knowledge-check((
  (question: [Compute $1\/gamma$ from $B_d = 2.2246 "MeV"$ and $m_N c^2 approx 939 "MeV"$.], answer: [$ħ c \/ sqrt(m_N c^2 B_d) = 197.3 \/ sqrt(939 times 2.2246) "fm" approx 4.3 "fm"$.]),
  (question: [Why can pionless EFT ignore the details of the nuclear force?], answer: [The overlap comes mostly from $r >> R_pi$, where only $B_d$, $a_(p p)$ and the effective ranges matter.]),
))

#section-title[From classical to nuclear] <fusion-reactions-summary>
- Classical: the turning point $r_c = Z_1 Z_2 e^2 \/ (4 pi epsilon_0 E)$
  must reach the contact distance $R$; $sigma_"cl" = pi R^2 (1 - V(R)\/E)$
  vanishes below $V(R) approx 0.5 "MeV"$.
- Quantum: the wave of reduced wavelength $ƛ = ħ \/ sqrt(2 m E)$ reaches
  through the barrier once $ƛ approx r_c$.
- Tunnelling gives $e^(-sqrt(E_G\/E))$, the wave area $pi ƛ^2 prop 1\/E$, so
  $sigma = S\/E e^(-sqrt(E_G\/E))$.
- Nuclear physics sits in $S$: the radius ($e^(4 sqrt(R\/a))$), the force
  completing the reaction and the #super[5]He#super[\*] resonance.
- $S approx 10^4 "keV b"$ for D–T, $10^2 "keV b"$ for D–D and
  $4 times 10^(-22) "keV b"$ for p–p.
#knowledge-check((
  (question: [Which two factors set the energy dependence of $sigma(E)$, and which factor carries the nuclear physics?], answer: [$1\/E$ and $exp(-sqrt(E_G\/E))$; $S(E)$.]),
  (question: [Why is D–T the preferred reaction for a power plant?], answer: [At a Gamow energy close to that of D–D, the strong force and the #super[5]He resonance give it the largest $S$, about 100 times that of D–D.]),
))
]
