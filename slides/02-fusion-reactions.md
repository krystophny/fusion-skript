# Fusion reactions — live route

Chapter 2. Canonical source: `slides/02-fusion-reactions.typ`.
Course structure: `Nextcloud/lv/fusion/PLAN.md` (chapter structure, next
route decided 2026-10-26). Use the existing Typst theme, build and presenter.

The deck is the board plan: derivation pages hold the formulas the lecturer
develops by hand, with muted step labels and no prose or speaker notes. The
deck has no blank writing pages; the lecturer writes on paper or in a
separate notebook. Light pages for mathematics and plots, dark full-slide
pages for animations, which carry no title; their route cues are below.

## Notation

E is the centre-of-mass energy, m = m₁m₂/(m₁ + m₂) the reduced mass and
M = m₁ + m₂ the total mass (page 3), σ(E) = (S/E) e^(−√(E_G/E)) with the
S factor S and the Gamow energy E_G = 2mc²(παZ₁Z₂)² (pages 12–16), k_BT the
ion temperature. The animations and `04-power-balance-visuals.md` write the
reduced mass m_r; page 28 names both. F_μ is the velocity Maxwellian of mass
μ, f_M(E) the energy distribution (maximum at k_BT/2), K the kernel per
d ln E, u = ln E and s = ln k_BT.

## Pages

| Pages | Content | Lecturer cue |
|---|---|---|
| 1–2 | Title; main reactions and energy release | — |
| 3–9 | Two-body problem, head-on collision, Rutherford, classical turning point and cross section; Coulomb-collision animation | Open Lecture 4 with the contact-distance correction (PLAN.md) |
| 10–16 | Quantum ballpark, WKB slices, Gamow tunnelling, measuring σ, S factor, tunnelling alone, actual σ | — |
| 17–26 | Measured S, ⁵He resonance, which force, S and R, force ranges, computing S, p–p from wave functions, pionless EFT, comparison, summary diagram | Taught in Lecture 3 |
| 27 | From cross section to rate (section 2.20 starts) | Beam on target: cylinder of length v Δt, R = n₁n₂σv. Plasma: average over both distributions. Identical particles: count pairs with four deuterons (D1 with 2, 3, 4; D2 with 3, 4; …): N(N−1)/2 ≈ N²/2, so 1/(1 + δ₁₂); forgetting it costs a factor 2 in a pure-D plasma. ⟨σv⟩ is an average of σ times v, not of σ times n. |
| 28 | Relative velocity | Same T for both species. Expand m₁v₁² + m₂v₂²: no mixed V·g term, so no angles; Jacobian 1. The relative velocity is Maxwellian with m: a convolution, variances add. |
| 29 | Animation `relative-velocity` | f_T slides across f_D, the overlap is shaded, its area f_rel(g) is traced over the reduced-mass Maxwellian. |
| 30 | Convolution and kernel smoothing | Define (f ∗ K)(x): shift, multiply, integrate; correlation = unflipped kernel. A kernel of width h removes structure narrower than h (sketch: spike smoothed). Two uses: (a) relative velocity, a true convolution in v; (b) reactivity, a correlation in ln E with a fixed kernel. Optional: Plasma kernel-smoothing animation (linked on the page). |
| 31 | Maxwell average | Integrate out V, then E = mg²/2; carry the prefactor through to (8/(πm))^(1/2)(k_BT)^(−3/2), which no earlier lecture reached. **Log-energy point:** per d ln E the weight (2/√π)(E/k_BT)^(3/2) e^(−E/k_BT) depends on ln E − ln k_BT only; T shifts one fixed kernel along the ln E axis. On a linear E axis the weight widens with T, so there it is a T-dependent average, not a convolution in E. |
| 33 | Animation `maxwell-average` | Kernel slides rigidly on the log axis under σv; the ⁵He resonance is integrated away into a smooth ⟨σv⟩(T). Left panel σv(E) is the mono-energetic beam value (delta distribution), right panel ⟨σv⟩(T) the Maxwellian one: compare the two curves at 10 keV and at their maxima. D–T ⟨σv⟩ peaks near 65–70 keV, not at a few hundred keV. |
| 33 | From cross section to reactivity (plot `reaction_product`) | D–T at 10 keV. Plot actual Bosch–Hale σ(E), Maxwell energy density f_M(E) (its √E comes from a spherical shell in 3D velocity space), and σ(E)v(E)f_M(E). The extra v ∝ √E is essential; the area under the third curve is ⟨σv⟩, not its height. f_M peaks at 5 keV, reaction contribution at about 35 keV (constant-S Gamow prediction 31 keV). |
| 34 | Gamow peak | Insert σ; F(E) = E/k_BT + √(E_G/E); maximum E₀, depth τ, curvature, 1/e width Δ; Gaussian integral gives τ²e^(−τ). Since τ ∝ (k_BT)^(−1/3), this is the low-temperature form (k_BT)^(−2/3) exp(−c (k_BT)^(−1/3)) of the NRL Plasma Formulary fits: the fitted constants follow from E_G. D–T at 10 keV: E₀ ≈ 31 keV, Δ ≈ 41 keV, τ ≈ 9.3. |
| 35 | Gamow window (plot `gamow_peak`) | One factor falls, one rises; pairs peak at k_BT/2 = 5 keV, reacting pairs near 31 keV. |
| 36 | Animation `gamow-sweep` | E₀ moves from 11 to 102 keV as k_BT rises from 2 to 60 keV; peak height grows by almost five decades. |
| 37 | Only the tail fuses (plot `tail_fuses`, ladder table) | 11 % of pairs, 73 % of reactions above 3k_BT. Let students compute the barrier temperature first: V(R) ≈ 0.44 MeV ≈ 5·10⁹ K. Table: k_BT needed for the D–T value 1.1·10⁻²² m³/s. Classical σ_cl: 450 keV with all pairs at 3/2 k_BT, 440 keV with a Maxwellian. Tunnelling σ: 15 keV and 10 keV. Tunnelling gains a factor of about 30 in temperature, the tail another 1.5. |
| 38 | Reactivity (plot `reactivity`) | D–T two orders above the others at 10 keV; ⟨σv⟩/T² maximal at 13.5 keV. Lawson curve n T τ_E ∝ T²/⟨σv⟩ is this curve upside down (Chapter 4). Hotter is not safer below about 70 keV. |
| 39 | Reaction rate: summary | Five steps and the τ²e^(−τ) result. |
| 40 | Solar core (plot `gamow_peak_pp`), optional | k_BT ≈ 1.3 keV, E₀ ≈ 6 keV ≈ 4.6 k_BT; bridge to Chapter 3, may be skipped. |

## Sources and checks

Derivation checks: `derivations/chapters/ch02_reactivity.py`
(`symbolic_checks`: rate counting, centre-of-mass identity and Jacobian,
reduced-mass convolution, Maxwell prefactor, f_M normalisation and mean,
log-energy kernel K and its normalisation, Gamow E₀, τ, curvature, Δ, the
τ²e^(−τ) coefficient 8√6/27 and the low-T form, the D–T numbers, the tail
fractions and the temperature ladder). Plot and animation descriptions:
`slides/04-power-balance-visuals.md`. Reactivity data: Bosch and Hale,
Nucl. Fusion 32, 611 (1992), doi:10.1088/0029-5515/32/4/I07; p–¹¹B: Nevins
and Swain, Nucl. Fusion 40, 865 (2000), doi:10.1088/0029-5515/40/4/310.
