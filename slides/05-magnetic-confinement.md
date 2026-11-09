# Magnetic confinement — live route

Chapter 5. Canonical source: `slides/05-magnetic-confinement.typ`.
Course structure: `Nextcloud/lv/fusion/PLAN.md`.

Draft started 2026-11-09. The chapter opens with the question that ends
Chapter 4: which limits on density, pressure and confinement time decide where
a reactor sits in the Lawson landscape, and how a magnetic field reaches them.
The pages below moved here from Chapter 4; the magnetic physics (magnetic
pressure, gyration and Larmor radius, mirrors, torus, drifts, field-line twist)
follows.

## Pages

| Page | Content | Lecturer cue |
|---|---|---|
| 1 | Title | — |
| 2 | 5.1 Pressure and density limits | Opening question: Chapter 4 placed the reactor in the Lawson landscape; what decides where a machine can sit is how high it can go in pressure and density. Pressure, not density, is what the magnet holds: p = 2nk_BT, so p_fus ∝ p²⟨σv⟩/T² — the 13.5 keV optimum of section 2.20 is a fixed-pressure optimum. With β: P_fus ∝ β²B⁴V, doubling B gives 16 times the power density. Density limit as one line (Greenwald, empirical); scaling laws come with transport. |
| 3 | Widget `limits` | Fixed τ_E: colour = τ_E needed for Q; density line n_max, pressure line p_max = β_max B²/2μ₀. Optimum = crossing T× = p_max/2n_max clamped to [13.5, 25.7] keV; stellarator toggle drops the density limit → 13.5 keV. Defaults B = 6 T, β = 4.5 %, n_max = 10²⁰: 20 keV, 1.55 s. |
| 4 | Limits and confinement scaling | Tokamak T× ≈ 0.39 β_N a B/f_GW keV (I_p cancels): ITER 8.8 keV, EU-DEMO 13.8 keV. IPB98(y,2) and ISS04 with coefficients; τ_E falls with heating power, so at the β limit τ_E ∝ T^−1.3 and the optimum moves to 6–9 keV. |
| 5 | Widget `popcon` | 0-D operating space with parabolic profiles, 85 % fuel, bremsstrahlung, τ_E = H·IPB98 or H·ISS04 solved with P = W/τ_E. Presets ITER, SPARC, ARC, W7-X, HELIAS 5-B; B and H sliders. Best point sits on a limit near 6–9 keV; the region of high Q is broad. Without core radiation ITER comes out ignited at H = 1; H = 0.85 gives Q ≈ 15, H = 0.8 gives Q ≈ 9 (best point near 5–6 keV on the Greenwald line) — say this. |
| 6 | Widget `machines` | Wurzel & Hsu records in n–T, n–τ_E, T–τ_E and the Lawson plane; no present machine reaches the reactor window in all three at once; ITER and SPARC design points. Q bands are in peak values like the data (Wurzel & Hsu Eq. 45: peaked T, broad n, Z_eff 1.5–3.4, fixed 2026-11-09 after Lecture 4): the JET 1991 and JT-60U records fall below Q = 1, not above; the ITER and SPARC design points lie in the Q ≈ 10 to ignition band. |
