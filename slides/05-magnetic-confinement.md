# Magnetic confinement — live route

Chapter 5. Canonical source: `slides/05-magnetic-confinement.typ`.
Course structure: `Nextcloud/lv/fusion/PLAN.md`.

Route (decided 2026-11-17, reordered the same day): linear devices first, then the torus, then tokamak and stellarator; fluid and particle picture in turn. Fluid:
magnetic pressure, beta <= 1 and the pinch. Particles: gyration, mirror, end
losses, toroidal drift and E x B, which need a twist with q not too large. Fluid
again: sausage and kink, q not too small. Then ZETA, tokamak and stellarator,
and last the limits of a real machine (pages moved from Chapter 4).

Extended 2026-11-21 for Lecture 7 (24 Nov), which starts at page 8 (torus):
principles of toroidal confinement (nested flux surfaces from force balance),
stability limits (beta: Troyon; density: Greenwald for tokamaks, Sudo for
stellarators; disruption), and section 5.8 with every main component seen once in
an exploded 3D build-up of an ITER-size tokamak (plasma, TF, CS, PF, vessel and
blanket, divertor, heating, cryostat), then magnets, plasma current and current
drive, heating, wall/blanket/divertor with a poloidal cross-section, the stellarator
differences and a one-page overview. Details follow in later lectures (heating and
current drive, exhaust, diagnostics, power plant). The confinement-scaling page and
the `popcon` widget left this deck; they return with transport in Chapter 7.

Lecture 6 (17 Nov) covered pages 2–7 on the board (fluid and particle model,
theta- and Z-pinch, sausage and kink, screw pinch with q, ZETA and the tokamak as
the toroidal screw pinch, mirror with mu, trapped–passing boundary and loss cone).

## Pages

| Page | Content | Lecturer cue |
|---|---|---|
| 1 | Title | — |
| 2 | 5.1 Fluid and particle pictures | Recap p tau_E >= 10 bar s at 15 keV, p = 4.8 bar at 1e20 m^-3. Two models: fluid (j x B - grad p) and particles (Lorentz force). |
| 3 | 5.2 Magnetic pressure and beta | 3D theta-pinch: coil current I_c, axial B_ext, compressed plasma. j x B = pressure + tension. Theta-pinch with straight B: p + B_in^2/2mu0 = B_ext^2/2mu0, so beta <= 1 with the external field (local beta can be infinite where B = 0). 5.3 T: 112 bar; beta = 2.5 % gives tau_E >= 3.6 s. |
| 4 | 5.2 Z-pinch | 3D Z-pinch: current I from anode to cathode, B_theta rings, inward j x B. dp/dr = -j_z B_theta, Ampere, Bennett mu0 I^2/8pi = N k_B (T_e + T_i), <p> = B_theta(a)^2/2mu0 (beta_p = 1, held by tension). 0.45 MA for 1e20 m^-3, 10 cm, 10 keV. |
| 5 | 5.2 Sausage and kink | Sausage: B_theta ~ 1/r, the neck pinches further; kink: B_theta crowds inside the bend. Pure Z-pinch unstable. |
| 6 | 5.2 Screw pinch | 3D: axial current plus coil field B_z, helical field lines. Axial B_z: sausage stable for B_z^2 > B_theta^2/2; field-line pitch q(a) = 2 pi a B_z/(L B_theta); Kruskal-Shafranov q(a) > 1 kink stable. Fluid: q not too small. |
| 7 | 5.3 Gyration and magnetic mirror | 3D mirror: two coils, field lines pinched under the coils. rho = 4 mm for D at 10 keV, 5 T. mu conserved, reflection sin^2 theta > 1/R_m, loss cone 13 % at R_m = 4; collisions refill it, so bend into a torus. |
| 8 | 5.4 Torus with a toroidal field | 3D: 12 TF coils around a torus, B_phi field lines (B_phi ~ 1/R), front sector cut open to show the cross-section used on the next page. |
| 9 | 5.4 Drift in a toroidal field | B_phi ~ 1/R; grad-B and curvature drift vertical with the sign of q; charge separation E_z; E x B outward for all species. Twist the field lines. |
| 10 | Widget `tokamak-exb` | Same widget as the Plasma deck: torus with only B_phi, ion up and electron down by grad-B and curvature drift, charges pile up, a vertical E pushes both outward by E x B. Twist toggle and q slider: helical field lines average the vertical drift out, orbit width ~ q rho; at q >~ 5 the scaled ion reaches the wall (rho exaggerated). |
| 11 | 5.4 Twisted field lines | Unrolled torus, q = r B_phi/(R B_theta). Drift during half a poloidal turn: Delta ~ q rho, trapped q rho/sqrt(eps); alphas at 5 T: 0.3 m. Particles: q not too large. |
| 12 | 5.4 Window for the twist | Particles bound q from above, fluid from below: 1 < q(a) << a sqrt(eps)/rho; tokamak q95 ~ 3. |
| 13 | 5.5 Toroidal pinch on a transformer | 3D schematic at ZETA size: iron-core transformer with primary on the central limb, plasma torus with strong I, few weak B_phi coils, field line with q(a) = 0.25. |
| 14 | 5.5 Toroidal pinch and ZETA | Strong I, weak B_phi: q(a) << 1, kinks. ZETA 1957, neutrons claimed January 1958, Rose et al.: beam-like spectrum, not thermonuclear. Quiet phase = reversed-field pinch (Taylor 1974). |
| 15 | 5.5 Tokamak: ITER coil set | 3D: CS (6 modules), 18 TF coils with front sector cut away, 6 PF coils, plasma, field line q = 3, I_p and I_TF directions. CS/PF positions from M3D-C1 ITER device data, plasma shape ITER Physics Basis, TF D schematic. |
| 16 | 5.5 Tokamak | B_phi from coils, B_theta from I_p; q(a) = 2 pi a^2 B_phi/(mu0 R I_p) >= 2-3 gives the current limit (ITER 15 MA with elongation). T-3, 1 keV, Culham Thomson scattering 1969. |
| 16a | 5.5 Classical stellarator: helical windings | 3D schematic: circular TF coils plus l = 2 helical windings with alternating current, 5 field periods; the plasma cross-section is an ellipse that turns with the windings; field line with iota = 0.4. Figure `classical_stellarator_3d`. |
| 17 | 5.5 Stellarator: NCSX modular coils | 3D: 12 of the 18 NCSX modular coils (front ones removed), VMEC boundary, one field line from theta + lambda = theta_0 + iota phi (iota = 0.65). Data: STELLOPT benchmark. |
| 18 | 5.5 Stellarator | Twist from 3D coils, no current: no current-driven kink, no disruptions, steady state; orbits need 3D optimisation. Model C -> ST 1970, W7-AS, W7-X. |
| 19 | 5.5 Stability and losses | Table: Z-pinch unstable (kink always, sausage unless the pressure profile is gentle, Kadomtsev); theta-pinch ideal-MHD stable but end losses; screw pinch stable for q(a) > 1, end losses; mirror interchange-unstable unless minimum-B, loss cone refilled by collisions; torus with only B_phi has no equilibrium (drift, E x B); tokamak 1 < q(a) <~ 3. Z-pinch at Lawson n, T would need tau_E = 3 s but lives microseconds. |
| 19a | 5.5 Principles of toroidal confinement | grad p = j x B, so B.grad p = 0 and j.grad p = 0: field lines and currents lie on surfaces p = const; twist covers each surface, closed lines, no ends. Result: nested flux surfaces, beta << 1. Figure: poloidal cross-section `tokamak_section` (same figure as on the divertor page). |
| 20 | 5.6 Pressure and density limits | p = 2 n k_B T, p <= beta_max B^2/2mu0; p_fus ~ <sigma v>/T^2 p^2 ~ beta^2 B^4: twice B gives 16 times p_fus. Question: what limits beta and n? |
| 21 | 5.6 Pressure limit: beta | Pressure-driven kink and ballooning (bad curvature outboard). Troyon beta_max[%] = beta_N I_p/(a B), beta_N ~ 2.8 (up to ~4 with wall and profile). ITER: 4 % limit, design 2.5 % (same 2.5 % as page 3). Stellarator: coils set equilibrium and stability, W7-X design <beta> ~ 5 %. |
| 22 | 5.6 Density limit: Greenwald and Sudo | n_G = I_p/(pi a^2): ITER 1.2e20, operation ~0.85 n_G. Mechanism: radiating edge shrinks the current channel, MHD, disruption. Sudo n_c = 0.25 sqrt(P B/(a^2 R)); W7-X 5 MW, 2.5 T: 0.7e20. Tokamak hard limit, stellarator soft. |
| 23 | 5.6 Disruption | Thermal quench ~1 ms (ITER W ~ 350 MJ), current quench tens of ms with forces, runaway electrons; avoid and mitigate (gas, pellets). Stellarator: none. |
| 23a | Widget `disruption` | MILCA in WebAssembly (`notebooks/wasm/milca_tokamak.mjs`): tokamak operating point against q, beta and density limits, and the disruption that follows when a start lies beyond a limit. |
| 24 | Widget `limits` | as before. |
| 25 | Widget `machines` | as before. |
| 26 | 5.8 Tokamak, built up | Eight build steps, one component group each in its assembled position: plasma, TF, CS, PF, vessel + blanket, divertor (54 cassettes), NBI + ICRH + ECRH, cryostat. Figure `figures_tokamak_parts.py`. |
| 27 | 5.8 Magnets | Table TF, CS, PF, correction, in-vessel: job and ITER number (iter.org magnets page). |
| 28 | 5.8 Plasma current | U_loop = -dPsi_CS/dt, pulsed: ITER 15 MA for 300–500 s; NBCD, ECCD, LHCD; bootstrap; steady state I_p = I_CD + I_bs. |
| 29 | 5.8 Heating | Ohmic (eta ~ T^-3/2), NBI (neutrals cross B; 2 x 16.5 MW, 1 MeV from negative ions), ECRH (28 GHz/T; 170 GHz, 40 → 67 MW in the 2024 baseline), ICRH (D 7.6 MHz/T; 40–55 MHz, 20 MW), alphas 100 MW. Resonance on a vertical line since B ~ 1/R. |
| 30 | 5.8 Wall, blanket and divertor | Separatrix, X-point, SOL, lambda_q ~ 1 mm (Eich 2013), targets 10 MW/m2, 440 blanket modules 736 MW. P_sep ~ 100 MW onto a few m2: radiate most. Figure `tokamak_section`. |
| 31 | 5.8 Stellarator: what changes | Table tokamak vs W7-X: twist, CS, current drive, exhaust (island divertor), heating (ECRH 140 GHz second harmonic at 2.5 T), limits. |
| 32 | 5.8 Components at a glance | Confine, drive current, shape, heat, exhaust, protect, keep cold. Outlook line: heating/CD, exhaust, diagnostics, power plant. |
