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
| 2 | 4.1 Alpha and neutron (`alpha_neutron_split`) | D + T almost at rest (k_BT ≈ 10 keV against 17.6 MeV): equal and opposite momenta, E = p²/2m, so the lighter particle takes the larger share. Let students give E_α before the box. 3.5 MeV, not 3.6 (2020 slip). 20 % stays in the plasma as α, 80 % leaves with the neutron into the blanket. Small print: relativistic 3.56/14.03 MeV. |
| 3 | 4.2 Fusion power density | Rate from section 2.20 with δ_DT = 0. Quasineutrality for Z = 1 fuel: n_e = n_D + n_T, so n_D n_T = n_e²/4 at 50:50, and x(1 − x) shows 50:50 is optimal. Do not drop the 1/4 (2021/22 slides did). Two-body process: ∝ n². Example: 1.7 MW/m³ at 10²⁰ m⁻³ and 14 keV. |
| 4 | 4.3 Stored energy and confinement time (`density_scaling`) | **Coffee cup:** hot coffee loses its heat in about 20 minutes; that is its τ_E, defined as stored energy over loss power, even while you keep reheating it. Plasma: about a second. Losses ∝ n at fixed τ_E, alpha heating ∝ n², so the curves cross: n τ_E is the combination that matters. |
| 5 | 4.4 Power balance with gain (`alpha_fraction`) | One balance, P_ext + P_α = P_loss, with P_ext = P_fus/Q gives every Q curve. Table: breakeven Q = 1 (f_α = 1/6), burning plasma Q = 5 (alphas supply half the heating), ignition Q → ∞. Plot: f_α saturates; at Q = 10 the alphas already supply two thirds of the heating. |
| 6 | Triple product | Board first (ignition balance → n τ_E = 12 k_BT/(⟨σv⟩E_α), times T). ⟨σv⟩ ∝ T² near 10–20 keV makes n T τ_E constant: ≈ 3·10²¹ keV s m⁻³ (exact minimum 2.7·10²¹ at 13.5 keV) = 4.8 bar s with the ion pressure n k_BT, ≈ 10 bar s with the full pressure p = 2n k_BT. The Q-dependence is on the Lawson plane, not on this page. |
| 7 | How good is ⟨σv⟩ ≈ cT²? (`reactivity`, shared with 2.20) | Before the widget: left ⟨σv⟩(T) for D–T, D–D, D–³He, p–¹¹B; right ⟨σv⟩/(cT²) with c the maximum of ⟨σv⟩/T² for each fuel, grey band ±20 %. Within 20 %: D–T 8–23 keV (peak 13.5), D–D 7.5–36 (16), D–³He 36–94 (59), p–¹¹B 91–218 (140). So n T τ_E ≈ const is a D–T statement near 10–20 keV; each fuel has its own window. Our D–D curve sits 6–12 % above Bosch–Hale (fit offset); does not change the window. |
| 8 | Widget `lawson`: n τ_E or n T τ_E? | Same ignition balance, two figures of merit, one panel per machine limit. Left, fixed density (Greenwald, τ_E = nτ_E/n): minimise n τ_E, minimum 25.7 keV. Right, fixed pressure (β limit, τ_E = 2 nTτ_E/p): minimise n T τ_E, minimum 13.5 keV. Solid exact Bosch–Hale, dashed ⟨σv⟩ ≈ cT² exact at the "fit T" slider (default 13.5 keV): in the approximation n T τ_E is flat and n τ_E falls as 1/T (slope −1, no minimum); the shaded gap is the error, ±12 % for 8–20 keV, factor 2 at 5 keV, 0.67 at 30 keV. The 25.7 keV minimum exists only because ⟨σv⟩ drops below T² above 20 keV. Spoken: bremsstrahlung moves the minima only to 14.2 and 26.0 keV; at 25.7 keV the triple product is 39 % above its minimum, at 13.5 keV n τ_E is 36 % above its; max P_fus at fixed n is at 66.7 keV. Switches for bremsstrahlung and "machine holds" removed 2026-11-09 (redundant). |
| 9 | Lawson plane (`lawson_plane`) | Minimum near 13.5 keV for every Q; bremsstrahlung wall at 4.3 keV (dashed). Right of the plot: n T τ_E ∝ Q/(Q + 5), so Q = 10 already needs 2/3 of the ignition value; same curve as f_α on page 5, so it is not drawn again. |
| 10 | 4.5 Lawson 1957 and self-heating | Same balance, two closures. Lawson: all output (fusion, bremsstrahlung, heat) through a converter with η = 1/3 and back as heating; useful when P_fus ≥ 2P_loss. Self-heating: the alphas stay inside, neutrons leave; ignition is P_α ≥ P_loss. The triple product is not "Lawson's criterion" in its 1957 form (2025 notebook). **Bank account** for Lawson's break-even, if time. Neutrons take the long path wall → turbine → heater: inefficient twice. Spoken, no page: with η_th = η_aux = 0.4, Q_eng = η_th η_aux (Q + 1) − 1, so net electricity needs Q > 5.25 and Q ≈ 10 gives Q_eng ≈ 1. |
| 11 | 4.6 Density and confinement time (`n_tau_plane`) | Same n τ_E, very different routes. Magnetic: 10²⁰ m⁻³ for about a second ("ultra-high vacuum in density, atmospheric in pressure"). Inertial: 10³⁰–10³¹ m⁻³ for 0.1 ns, held by its own inertia; the H-bomb is inertial too, driven by fission (no public data, not drawn). Sun: p–p, not D–T, and confined by gravity for ~10⁷ years. Lines are constant n τ only: whether a point is near Q = 1 depends on its temperature, which this plane hides (Alcator C: n τ ≈ 10²⁰ s m⁻³ at 1.5 keV, far below Q = 1); for that, go back to the Lawson plane. Points are measured peak values: compare orders of magnitude only. NIF's December 2022 shot reached target gain 1.5, not 10; JET's 1997 record was below Q = 1. |
| 12 | 4.7 Bremsstrahlung and ideal ignition (`alpha_brems`) | Electrons deflected by ions radiate; the plasma is transparent, so the power goes to the wall. ∝ n_e² like fusion, so n² cancels: below 4.3 keV no density helps (Lawson's first insight). Z_eff carries Z² per ion: impurities radiate more. Units trap: NRL 1.69·10⁻³² W cm³ eV^(−1/2) needs T in eV; with T in keV use 5.34·10⁻³⁷ W m³ keV^(−1/2). |
| 13 | Cyclotron radiation | Electrons gyrating at ω_ce radiate (Larmor); averaged over a Maxwellian, ⟨v⊥²⟩ = 2k_BT_e/m_e gives 6.2·10⁻¹⁷ n_e T_e B² W m⁻³ (NRL; `cyclotron_thin`). At 10²⁰ m⁻³, 10 keV, 5 T the emitted power (1.6 MW m⁻³) exceeds fusion (0.8) and is about 90 times bremsstrahlung (0.017) — but the plasma is optically thick at the low harmonics and the walls reflect, so little escapes. It grows with T_e and B and is a main loss for D–³He and p–¹¹B at 50–300 keV. Pairs: 2m_ec² = 1.02 MeV, suppressed like e^(−2m_ec²/k_BT), irrelevant below about 511 keV. |
| 14 | 4.8 Quasineutrality and dilution | Electrons neutralise every ion; the machine limits n_e (Greenwald) or p, not the fuel. At fixed n_e, p_fus ∝ (1 − Σ Z c_Z)²: one W ion takes 74 electrons' worth of fuel, 0.1 % W costs 14 %, 5 % He 19 %. Z_eff = 1 + Σ Z(Z − 1)c_Z enters bremsstrahlung. W is not fully ionised in the core and radiates lines: c_W = 3·10⁻⁵ already raises the minimum n T τ_E by 20 % (Pütterich et al. 2010). |
| 15 | Helium ash (`impurity_dilution`) | 5 % He raises the ignition triple product by about a quarter, 10 % by about 60 %. Right: one universal curve (1 − Zc)² for any impurity at fixed n_e. Helium has to leave within a few τ_E. |

Engineering gain, the Q = 10 power flow and "What is really optimised?"
were removed on 2026-11-09 because Lecture 4 (2026-11-03) never showed them.
The same day the pages were thinned to what the board does not already
carry: the derivations follow the Lecture 4 board route (power balance →
W = 3nk_BT → p_α → gain → x(1 − x) → Lawson → triple product → limits), the
pages keep results, plots and one line per step. Section 4.9 (now 4.7) became "Radiation
losses" with a cyclotron page, and quasineutral dilution returned to 4.10 (now 4.8) in
a slimmer form with line radiation. The Lawson widget (n τ_E against n T τ_E
with the T² approximation) followed the triple product the same day and took
over "Which temperature is optimal?". Removed content is in Git history.

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
- NRL Plasma Formulary, bremsstrahlung (1.69·10⁻³² W cm³ eV^(−1/2)) and
  cyclotron emission (6.21·10⁻²⁸ B² N_e T_e W cm⁻³, B in G, T_e in eV).
- T. Pütterich et al., Nucl. Fusion 50, 025012 (2010),
  doi:10.1088/0029-5515/50/2/025012: c_W = 3·10⁻⁵ raises the minimum nTτ_E by 20 %.
- M. Greenwald, Plasma Phys. Control. Fusion 44, R27 (2002), doi:10.1088/0741-3335/44/8/201.
- NIF target gain 1.5: H. Abu-Shawareb et al., Phys. Rev. Lett. 132, 065102 (2024),
  doi:10.1103/PhysRevLett.132.065102 (cue only).

No third-party figures are used; all plots and diagrams are drawn from the
code above.

On 2026-11-09 the duplicates were removed: "Momentum and energy" merged into
"Alpha and neutron"; the right panel of the Lawson plane (n T τ_E against Q,
the same curve as f_α) and the fixed-pressure figure (⟨σv⟩/T² against T, as on
pages 7 and 8) were dropped, as was the dilution table (its two values are the
points of the helium-ash curve). The limit pages (fixed pressure, limits widget,
limits and confinement scaling, operating space, machines) moved to Chapter 5,
`slides/05-magnetic-confinement.md`; sections 4.6–4.8 were renumbered.
