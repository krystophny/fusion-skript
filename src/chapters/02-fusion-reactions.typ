#import "../theme.typ": *

#let chapter = [
#page-title(number: 2)[Fusion reactions] <fusion-reactions>
#lead[Two nuclei must come within the range of the strong force, but their
Coulomb repulsion turns them around much earlier.]

#section-title[Head-on Coulomb encounter] <head-on-encounter>
Two nuclei with charges $Z_1 e$ and $Z_2 e$ and masses $m_1$, $m_2$ interact
only through their Coulomb potential. In centre-of-mass and relative
coordinates the total momentum is conserved, and the relative separation
$bold(r) = bold(r)_1 - bold(r)_2$ moves like one particle of reduced mass
$m = m_1 m_2 \/ (m_1 + m_2)$ in the potential
$ V(r) = (Z_1 Z_2 e^2)/(4 pi epsilon_0 r). $
For a head-on collision (no angular momentum) the energy
$E = m dot(r)^2\/2 + V(r)$ is constant. The relative particle comes in,
reaches $dot(r) = 0$ where $V(r_c) = E$ and is reflected there:
$ r_c = (Z_1 Z_2 e^2)/(4 pi epsilon_0 E). $
Classically the region $r < r_c$ is forbidden, because there $V(r) > E$
would require a negative kinetic energy.

Quantum mechanically the relative motion is a wave with reduced wavelength
$ƛ = ħ \/ (m v)$, where $v$ is the initial relative speed and
$E = m v^2 \/ 2$. Inserting $E$ gives
$ r_c = (Z_1 Z_2 e^2)/(4 pi epsilon_0) (2)/(m v^2)
  = 2 (Z_1 Z_2 e^2)/(4 pi epsilon_0 ħ v) (ħ)/(m v) = 2 eta ƛ, quad
  eta = (Z_1 Z_2 e^2)/(4 pi epsilon_0 ħ v). $
The Sommerfeld parameter $eta$ counts the turning distance in wavelengths. In
units of $ƛ$ the encounter depends only on $eta$ and the shape of the incoming
packet, so one simulation describes every pair at the same $eta$. For D–T,
$m = 2.0141 times 3.0160 \/ 5.0301 thin "u" = 1.2076 thin "u"$, and
$eta = 2$ corresponds to $E = 7.5 thin "keV"$ and
$r_c = 1.440 thin "MeV fm" \/ 7.5 thin "keV" = 0.19 thin "pm"$, still far
outside the nuclei (a few fm).

#animation("animations/coulomb_reflection.mp4",
  "Head-on Coulomb encounter at eta = 2 on one axis r over r_c: the potential V of r, the dashed energy line E and the turning point r_c. A classical particle (dot) moves in along the energy line, is reflected at r_c and moves out. The quantum probability density, drawn on the energy line, moves in, reflects and keeps a small tail inside r_c; a lower log-scale strip shows that tail.",
  poster: "../media/coulomb-reflection.png",
  caption: [Head-on encounter ($ell = 0$) at $eta = 2$ (D–T at
  $E = 7.5 thin "keV"$). Top: potential $V(r)$, energy $E$ and turning point
  $r_c$. The classical particle (dot) at energy $E$ is reflected at $r_c$.
  The quantum probability density $|u|^2$ of the relative motion, an incoming
  wave packet with 12 % energy spread, is drawn with the energy line as
  baseline; it is reflected at the same time but leaks into the classically
  forbidden region $r < r_c$. Bottom: $log_10 (|u|^2 r_c)$ on the same axis;
  inside $r_c$ the density decays like $exp(-2 integral_r^(r_c) kappa dif r')$
  with $kappa = sqrt(2 m (V - E)) \/ ħ$. This tail is where tunnelling
  starts.])
]
