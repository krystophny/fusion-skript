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

#animation("animations/coulomb_collision.mp4",
  "Head-on D-T collision at eta = 2 seen from above in the centre-of-mass frame, classical on the left and quantum on the right, on the same clock. Left: the deuteron (small dot) and the triton (large dot) approach along a line, slow down, turn at separation r_c and fly apart. Right: each nucleus is a probability cloud; the clouds approach, show interference fringes while they are reflected, and a small part reaches separations below r_c, drawn in yellow.",
  poster: "../media/coulomb-collision.png",
  caption: [Head-on D–T collision ($ell = 0$) at $eta = 2$
  ($E = 7.5 thin "keV"$), seen from above in the centre-of-mass frame, same
  energy and same clock in both panels. With separation $r$ the nuclei sit at
  $x_"D" = -(m_"T" \/ M) r$ and $x_"T" = (m_"D" \/ M) r$, $M = m_"D" + m_"T"$;
  the bar marks $r_c$ between the turning positions. Left: point particles on
  the classical orbit $r(t)$ at energy $E$, reflected at $r_c$. Right: the
  densities of $x_"D"$ and $x_"T"$ obtained from the $ell = 0$ wave
  packet $|u(r, t)|^2$ (12 % energy spread) by the same relations. Incoming
  and reflected waves interfere into fringes, and a few per cent of the
  probability reaches $r < r_c$ (yellow, brightened), where tunnelling starts.
  The width across the collision axis is illustrative only.])
]
