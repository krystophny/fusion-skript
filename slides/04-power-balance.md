# Power balance and Lawson — live route

Chapter 4. Canonical source: `slides/04-power-balance.typ`.
Course structure: `Nextcloud/lv/fusion/PLAN.md` (chapter structure, next
route decided 2026-10-26: cross section → reactivity → power balance →
Lawson and Q). Use the existing Typst theme, build and presenter.

The deck is the board plan: each topic has one derivation page with the
formulas the lecturer develops by hand, short muted step labels and one
result box, next to its plot or on the page before it. No prose, no speaker
notes and no blank writing pages; the lecturer writes on paper or in a
separate notebook. All pages are light; the chapter has no animation yet.

## Notation

0-D model: 50:50 D–T, n_e = n_i = n, T_e = T_i = T, flat profiles, steady
state. Lower-case p are powers per volume, capital P totals. k_BT is written
in formulas; T alone means k_BT in keV. E_fus = Q_DT = 17.6 MeV per reaction,
E_α = 3.5 MeV (3.56 MeV relativistic, used in the plots), E_n = 14.1 MeV.
W = 3nk_BT is the thermal energy per volume, τ_E = W/p_loss the energy
confinement time; p_loss is everything not counted separately (conduction,
convection; radiation where it is not written out). P_ext is the external
heating, Q = P_fus/P_ext the plasma (scientific) gain, Q_DT the reaction
energy, Q_eng the engineering gain. f_α = P_α/(P_α + P_ext) is the self-heating
fraction. C_B is the bremsstrahlung constant for T in keV, Z_eff = Σ n_j Z_j²/n_e,
c_Z = n_Z/n_e an impurity concentration, β = 2μ₀p/B². τ_L (2020 notes) and
P_heat or P_aux (older decks) are not used.

## Pages

| Page | Content | Lecturer cue |
|---|---|---|
| 1 | Title | — |
| 2 | 4.1 Momentum and energy | D + T almost at rest (k_BT ≈ 10 keV against 17.6 MeV): equal and opposite momenta, E = p²/2m, so the lighter particle takes the larger share. Let students give E_α before the box. 3.5 MeV, not 3.6 (2020 slip). |
| 3 | Alpha and neutron (`alpha_neutron_split`) | 20 % stays in the plasma as α, 80 % leaves with the neutron into the blanket. Small print: relativistic 3.56/14.03 MeV. |
| 4 | 4.2 Fusion power density | Rate from section 2.20 with δ_DT = 0. Quasineutrality for Z = 1 fuel: n_e = n_D + n_T, so n_D n_T = n_e²/4 at 50:50, and x(1 − x) shows 50:50 is optimal. Do not drop the 1/4 (2021/22 slides did). Two-body process: ∝ n². Example: 1.7 MW/m³ at 10²⁰ m⁻³ and 14 keV. |
| 5 | 4.3 Stored energy and confinement time (`density_scaling`) | **Coffee cup:** hot coffee loses its heat in about 20 minutes; that is its τ_E, defined as stored energy over loss power, even while you keep reheating it. Plasma: about a second. Losses ∝ n at fixed τ_E, alpha heating ∝ n², so the curves cross: n τ_E is the combination that matters. |
| 6 | 4.4 Bremsstrahlung and ideal ignition (`alpha_brems`) | Electrons deflected by ions radiate; unavoidable. ∝ n_e² like fusion, so n² cancels: below 4.3 keV no density helps. Lawson's first insight. Units trap: the NRL constant 1.69·10⁻³² W cm³ eV^(−1/2) needs T in eV; with T in keV use 5.34·10⁻³⁷ W m³ keV^(−1/2) (2025 notes mixed them). |
| 7 | 4.5 Power balance with gain (`alpha_fraction`) | One balance, P_ext + P_α = P_loss, with P_ext = P_fus/Q gives every Q curve. Table: breakeven Q = 1 (f_α = 1/6), burning plasma Q = 5 (alphas supply half the heating), ignition Q → ∞. Plot: f_α saturates; at Q = 10 the alphas already supply two thirds of the heating. |
| 8 | Triple product | Multiply by T; ⟨σv⟩ ≈ 1.1·10⁻²⁴ T² m³/s near 10–20 keV makes n T τ_E independent of T: 3.1·10²¹, exact minimum 2.7·10²¹ keV s m⁻³ at 13.5 keV. Factor 2: n k_BT τ_E = 4.4·10⁵ Pa s, while pτ_E = 2nk_BTτ_E ≈ 9 bar s; quote bar·s only with pτ_E. |
| 9 | Lawson plane (`lawson_plane`) | Minimum near 14 keV for every Q; bremsstrahlung wall at 4.3 keV; right panel: Q = 10 already needs two thirds of the ignition value. |
| 10 | 4.6 Lawson 1957 and self-heating | Same balance, two closures. Lawson: all output (fusion, bremsstrahlung, heat) through a converter with η = 1/3 and back as heating; useful when P_fus ≥ 2P_loss. Self-heating: the alphas stay inside, neutrons leave; ignition is P_α ≥ P_loss. The triple product is not "Lawson's criterion" in its 1957 form (2025 notebook). **Bank account** for Lawson's break-even, if time. Neutrons take the long path wall → turbine → heater: inefficient twice. |
| 11 | Engineering gain (`q_eng`) | Bookkeeping: heat P_fus + P_ext at η_th, heating bought at η_aux. Net electricity only above Q = 5.25 (0.4 × 0.4); Q ≈ 11.5 gives Q_eng = 1, half the gross power recirculated. So Q ≈ 10 is the minimum for a plant, not "technical breakeven". Wurzel & Hsu: Q η_aux ≳ 10, i.e. Q ≳ 20 for magnetic plants. |
| 12 | Power flow at Q = 10 (`power_flow`) | 500 MW fusion, 50 MW heating, 101 MW alphas, 399 MW neutrons; f_α = 2/3. Exercise: Q_eng for this plant. |
| 13 | 4.7 Quasineutrality and dilution | Draw one W nucleus taking 74 electrons: at fixed n_e (density limit) it displaces 74 fuel ions. 0.1 % W: 7.4 % fewer fuel ions, 14 % less fusion power (not "74 %"). Tungsten in a reactor core is only partly ionised and line radiation dominates its loss; say this, no formula. **Ash stove:** helium is the ash of the burn; like ash in a wood stove it chokes the fire unless removed. Same mechanism with Z = 2. |
| 14 | Helium ash (`impurity_dilution`) | 5 % He raises the ignition triple product by about a quarter, 10 % by about 60 %. Right: one universal curve (1 − Zc)² for any impurity at fixed n_e. |
| 15 | 4.8 Fixed pressure (`fixed_pressure`) | Pressure, not density, is what the magnet holds: p = 2nk_BT, so p_fus ∝ p²⟨σv⟩/T² — the 13.5 keV optimum of section 2.20 is a fixed-pressure optimum. With β: P_fus ∝ β²B⁴V, doubling B gives 16 times the power density. Density limit as one line (Greenwald, empirical); scaling laws come with transport. |
| 16 | 4.9 Density and confinement time (`n_tau_plane`) | Same n τ_E, very different routes. Magnetic: 10²⁰ m⁻³ for about a second ("ultra-high vacuum in density, atmospheric in pressure"). Inertial: 10³⁰–10³¹ m⁻³ for 0.1 ns, held by its own inertia; the H-bomb is inertial too, driven by fission (no public data, not drawn). Sun: p–p, not D–T, and confined by gravity for ~10⁷ years, so the D–T lines do not apply to it. Points are measured peak values, lines uniform 0-D: compare orders of magnitude only. NIF's December 2022 shot reached target gain 1.5, not 10; JET's 1997 record was below Q = 1. |

## Sources and checks

Derivation checks: `derivations/chapters/ch04_power_balance.py`
(`symbolic_checks`: momentum split, 50:50 optimum, W = 3nk_BT, n² cancelling in
p_α = p_br, n τ_E(Q) with and without bremsstrahlung, f_α and its values at
Q = 1 and 5, T-independence for ⟨σv⟩ ∝ T², Lawson's η loop, Q_eng and its two
thresholds, quasineutral dilution and Z_eff, the diluted ignition formula,
fixed-pressure and β forms; `checks`: all numbers on the pages). Tests:
`tests/test_reactivity_power_balance.py`. Figures: `slides/figures_power_balance.py`,
described in `slides/04-power-balance-visuals.md`.

- J. D. Lawson, Proc. Phys. Soc. B 70, 6 (1957), doi:10.1088/0370-1301/70/1/303.
- S. E. Wurzel and S. C. Hsu, Phys. Plasmas 29, 062103 (2022),
  doi:10.1063/5.0083990, CC BY 4.0: Lawson's two insights, Q_eng, measured
  points (Tables 6–8 via `data/ch04/wurzel_hsu_2022.csv`).
- H.-S. Bosch and G. M. Hale, Nucl. Fusion 32, 611 (1992), doi:10.1088/0029-5515/32/4/I07.
- NRL Plasma Formulary, bremsstrahlung (1.69·10⁻³² W cm³ eV^(−1/2)).
- M. Greenwald, Plasma Phys. Control. Fusion 44, R27 (2002), doi:10.1088/0741-3335/44/8/201.
- NIF target gain 1.5: H. Abu-Shawareb et al., Phys. Rev. Lett. 132, 065102 (2024),
  doi:10.1103/PhysRevLett.132.065102 (cue only).

No third-party figures are used; all plots and diagrams are drawn from the
code above.
