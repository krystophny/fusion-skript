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
reduced mass m_r.

## Pages

| Pages | Content | Lecturer cue |
|---|---|---|
| 1–2 | Title; main reactions and energy release | — |
| 3–9 | Two-body problem, head-on collision, Rutherford, classical turning point and cross section; Coulomb-collision animation | Open Lecture 4 with the contact-distance correction (PLAN.md) |
| 10–16 | Quantum ballpark, WKB slices, Gamow tunnelling, measuring σ, S factor, tunnelling alone, actual σ | — |
| 17–26 | Measured S, ⁵He resonance, which force, S and R, force ranges, computing S, p–p from wave functions, pionless EFT, comparison, summary diagram | Taught in Lecture 3. The p–p chain page moved to Chapter 3 (`03-fusion-in-stars`) on 2026-11-10. |
| 27 | 2.20 Reactivity (plot `reactivity`) | D–T two orders above the others at 10 keV; ⟨σv⟩/T² maximal at 13.5 keV; right panel ⟨σv⟩/(cT²) per fuel with a ±20 % band (discussed in 4.4). Lawson curve n T τ_E ∝ T²/⟨σv⟩ is this curve upside down (Chapter 4). Hotter is not safer below about 70 keV. |
| 28 | Reaction rate: summary | Five steps and the τ²e^(−τ) result. |

Section 2.20 is derived on the board (reaction rate per beam particle,
Maxwell average, reactivity) and the deck keeps only its three result pages.
Its eleven derivation pages (rate, relative velocity, kernel smoothing,
Maxwell average, Gamow peak and window, tail) and their three animations were
removed on 2026-11-09 after Lecture 4 (2026-11-03), where they proved too
detailed for the live route; they remain in Git history.

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
