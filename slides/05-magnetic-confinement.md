# Magnetic confinement — live route

Chapter 5. Canonical source: `slides/05-magnetic-confinement.typ`.
Course structure: `Nextcloud/lv/fusion/PLAN.md`.

Route (decided 2026-11-17): the fluid and the particle picture in turn. Fluid:
magnetic pressure, beta <= 1 and the pinch. Particles: gyration, mirror, end
losses, toroidal drift and E x B, which need a twist with q not too large. Fluid
again: sausage and kink, q not too small. Then ZETA, tokamak and stellarator,
and last the limits of a real machine (pages moved from Chapter 4).

## Pages

| Page | Content | Lecturer cue |
|---|---|---|
| 1 | Title | — |
| 2 | 5.1 Fluid and particle pictures | Recap p tau_E >= 10 bar s at 15 keV, p = 4.8 bar at 1e20 m^-3. Two models: fluid (j x B - grad p) and particles (Lorentz force). |
| 3 | 5.2 Magnetic pressure and beta | 3D theta-pinch: coil current I_c, axial B_ext, compressed plasma. j x B = pressure + tension. Theta-pinch with straight B: p + B_in^2/2mu0 = B_ext^2/2mu0, so beta <= 1 with the external field (local beta can be infinite where B = 0). 5.3 T: 112 bar; beta = 2.5 % gives tau_E >= 3.6 s. |
| 4 | 5.2 Z-pinch | 3D Z-pinch: current I from anode to cathode, B_theta rings, inward j x B. dp/dr = -j_z B_theta, Ampere, Bennett mu0 I^2/8pi = N k_B (T_e + T_i), <p> = B_theta(a)^2/2mu0 (beta_p = 1, held by tension). 0.45 MA for 1e20 m^-3, 10 cm, 10 keV. |
| 5 | 5.2 Screw pinch | 3D picture: axial current plus coil field B_z gives helical field lines; pitch q = 2 pi a B_z/(L B_theta), the same q as Kruskal-Shafranov later. |
| 6 | 5.3 Gyration and magnetic mirror | 3D mirror: two coils, field lines pinched under the coils. rho = 4 mm for D at 10 keV, 5 T. mu conserved, reflection sin^2 theta > 1/R_m, loss cone 13 % at R_m = 4; collisions refill it, so bend into a torus. |
| 7 | 5.4 Torus with a toroidal field | B_phi ~ 1/R; grad-B and curvature drift vertical with the sign of q; charge separation E_z; E x B outward for all species. Twist the field lines. |
| 8 | 5.4 Twisted field lines | Unrolled torus, q = r B_phi/(R B_theta). Drift during half a poloidal turn: Delta ~ q rho, trapped q rho/sqrt(eps); alphas at 5 T: 0.3 m. Particles: q not too large. |
| 9 | 5.5 Sausage and kink | Sausage: B_theta ~ 1/r, the neck pinches further; kink: B_theta crowds inside the bend. Axial field: sausage stable for B_z^2 > B_theta^2/2, Kruskal-Shafranov q(a) > 1. Fluid: q not too small. |
| 10 | 5.5 Window for the twist | Particles bound q from above, fluid from below: 1 < q(a) << a sqrt(eps)/rho; tokamak q95 ~ 3. |
| 11 | 5.5 Stability and losses | Table: Z-pinch unstable (kink always, sausage unless the pressure profile is gentle, Kadomtsev); theta-pinch ideal-MHD stable but end losses; screw pinch stable for q(a) > 1, end losses; mirror interchange-unstable unless minimum-B, loss cone refilled by collisions; torus with only B_phi has no equilibrium (drift, E x B); tokamak 1 < q(a) <~ 3. Z-pinch at Lawson n, T would need tau_E = 3 s but lives microseconds. |
| 12 | 5.6 Toroidal pinch on a transformer | 3D schematic at ZETA size: iron-core transformer with primary on the central limb, plasma torus with strong I, few weak B_phi coils, field line with q(a) = 0.25. |
| 13 | 5.6 Toroidal pinch and ZETA | Strong I, weak B_phi: q(a) << 1, kinks. ZETA 1957, neutrons claimed January 1958, Rose et al.: beam-like spectrum, not thermonuclear. Quiet phase = reversed-field pinch (Taylor 1974). |
| 14 | 5.6 Tokamak: ITER coil set | 3D: CS (6 modules), 18 TF coils with front sector cut away, 6 PF coils, plasma, field line q = 3, I_p and I_TF directions. CS/PF positions from M3D-C1 ITER device data, plasma shape ITER Physics Basis, TF D schematic. |
| 15 | 5.6 Tokamak | B_phi from coils, B_theta from I_p; q(a) = 2 pi a^2 B_phi/(mu0 R I_p) >= 2-3 gives the current limit (ITER 15 MA with elongation). T-3, 1 keV, Culham Thomson scattering 1969. |
| 16 | Widget `tokamak-exb` | Same widget as the Plasma deck: torus with only B_phi, ion up and electron down by grad-B and curvature drift, charges pile up, a vertical E pushes both outward by E x B. Twist toggle and q slider: helical field lines average the vertical drift out, orbit width ~ q rho; at q >~ 5 the scaled ion reaches the wall (rho exaggerated). |
| 17 | 5.6 Stellarator: NCSX modular coils | 3D: 12 of the 18 NCSX modular coils (front ones removed), VMEC boundary, one field line from theta + lambda = theta_0 + iota phi (iota = 0.65). Data: STELLOPT benchmark. |
| 18 | 5.6 Stellarator | Twist from 3D coils, no current: no current-driven kink, no disruptions, steady state; orbits need 3D optimisation. Model C -> ST 1970, W7-AS, W7-X. |
| 19 | 5.7 Pressure and density limits | Opening question: Chapter 4 placed the reactor in the Lawson landscape; what decides where a machine can sit is how high it can go in pressure and density. Pressure, not density, is what the magnet holds: p = 2nk_BT, so p_fus ∝ p²⟨σv⟩/T² — the 13.5 keV optimum of section 2.20 is a fixed-pressure optimum. With β: P_fus ∝ β²B⁴V, doubling B gives 16 times the power density. Density limit as one line (Greenwald, empirical); scaling laws come with transport. |
| 20 | Widget `limits` | Fixed τ_E: colour = τ_E needed for Q; density line n_max, pressure line p_max = β_max B²/2μ₀. Optimum = crossing T× = p_max/2n_max clamped to [13.5, 25.7] keV; stellarator toggle drops the density limit → 13.5 keV. Defaults B = 6 T, β = 4.5 %, n_max = 10²⁰: 20 keV, 1.55 s. |
| 21 | Limits and confinement scaling | Tokamak T× ≈ 0.39 β_N a B/f_GW keV (I_p cancels): ITER 8.8 keV, EU-DEMO 13.8 keV. IPB98(y,2) and ISS04 with coefficients; τ_E falls with heating power, so at the β limit τ_E ∝ T^−1.3 and the optimum moves to 6–9 keV. |
| 22 | Widget `popcon` | 0-D operating space with parabolic profiles, pure D-T 50:50 and no radiation (both not yet taught), tau_E = H IPB98 or H ISS04 solved with P = W/tau_E. Presets ITER, SPARC, ARC, W7-X, HELIAS 5-B; B and H sliders. Best point sits on a limit. Without radiation and dilution the model is optimistic: ITER ignites at H = 1 (1.4 GW at 10 keV on the Greenwald line) and still at H = 0.85; H = 0.8 gives Q of about 80. Say that radiation and impurities lower this and come later. |
| 23 | Widget `machines` | Wurzel & Hsu records in n–T, n–τ_E, T–τ_E and the Lawson plane; no present machine reaches the reactor window in all three at once; ITER and SPARC design points. Q bands are in peak values like the data (Wurzel & Hsu Eq. 45: peaked T, broad n, Z_eff 1.5–3.4, fixed 2026-11-09 after Lecture 4): the JET 1991 and JT-60U records fall below Q = 1, not above; the ITER and SPARC design points lie in the Q ≈ 10 to ignition band. |
