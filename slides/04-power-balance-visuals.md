# Visuals for reactivity and the start of power balance

Generated assets for the end of Chapter 2 (reaction rate in a thermal plasma),
the optional Chapter 3 (stars) and the opening of Chapter 4 (power balance).
The reactivity assets are used in deck 02, section 2.20; the power-balance ones in deck 04. Plots are light, A4-landscape slide size, English,
STIX Two, with direct labels and line styles in addition to colour.
Animations use the dark canvas of `animations/style.py`.

Build:

```sh
python3 derivations/chapters/ch02_reactivity.py     # checks, prints the numbers below
python3 derivations/chapters/ch04_power_balance.py
python3 slides/figures_reactivity.py                # -> slides/build/fig/*.svg, *.png
python3 slides/figures_power_balance.py
scripts/render-animations.sh                        # -> .cache/animations/<slug>.mp4, .png
```

`scripts/build-site.sh` and `scripts/build-slides.sh` run the figure scripts.
In a deck, use `/slides/build/fig/<name>.svg`.

Sources: H.-S. Bosch and G. M. Hale, Nucl. Fusion 32, 611 (1992),
doi:10.1088/0029-5515/32/4/I07 (D–T, D–D, D–³He S factors and reactivities);
W. M. Nevins and R. Swain, Nucl. Fusion 40, 865 (2000),
doi:10.1088/0029-5515/40/4/310 (p–¹¹B); NRL Plasma Formulary (2018), eq. (30),
p. 58 (bremsstrahlung); CODATA masses from `scipy.constants`; our EXFOR S-factor
fit `derivations/chapters/ch02_s_factor_fit.py`. Coefficients are in
`data/ch02/reactivity.json`.

## Reactivity

Symbols: E is the kinetic energy of the relative motion (centre-of-mass
energy), m_r = m₁m₂/(m₁ + m₂) the reduced mass, k_BT the ion temperature
(T in keV where written alone), σ(E) the cross section, ⟨σv⟩ the Maxwellian
reactivity, S(E) the astrophysical S factor, Z₁, Z₂ the charges, α the
fine-structure constant and E_G the Gamow energy. EXFOR is the IAEA database
of measured cross sections behind our S-factor fit.
⟨σv⟩ = √(8/(π m_r)) (k_BT)^(−3/2) ∫ σ(E) E e^(−E/k_BT) dE, with
σ(E) = (S/E) exp(−√(E_G/E)) and E_G = 2 m_r c² (π α Z₁Z₂)².

### `gamow_peak` (hero plot)

D–T at k_BT = 10 keV, E_G = 1182 keV. Top: the Maxwell factor e^(−E/k_BT)
(dashed), the tunnelling factor e^(−√(E_G/E)) (dotted) and their product
(solid), on a log scale. Bottom: the probability density of the relative energy
of all ion pairs, (2/√π)(k_BT)^(−3/2) √E e^(−E/k_BT), and of the pairs that fuse
for constant S, both normalised to unit area. Shaded: the Gamow window
E₀ ± Δ/2 with E₀ = (E_G (k_BT)²/4)^(1/3) = 30.9 keV and 1/e full width
Δ = 4√(E₀k_BT/3) = 40.6 keV.
The viewer should see that one factor falls and the other rises, so their
product has a broad maximum. The pair density peaks at k_BT/2 = 5 keV, while
the reacting pairs sit near 31 keV.
Axes: E [keV]; factor (dimensionless, log); density [keV⁻¹].
Check (of the arithmetic only): E₀ is the numerical maximum of
−E/k_BT − √(E_G/E) to 10⁻³ keV.

### `gamow_peak_pp` (stars, optional)

The same plot for p–p in the solar core, k_BT = 1.3 keV, E_G = 493 keV:
E₀ = 5.9 keV, Δ = 6.4 keV, against the expected ≈ 6 keV. The reacting pairs
have four to five times the thermal energy.

### `gamow-sweep` (animation, 16 s)

The top panel of `gamow_peak` while k_BT rises from 2 to 60 keV
geometrically (ln T linear in time, equal times are equal ratios). The Gamow window is shaded, E₀ and k_BT are read out, and the
path of the peak is traced. The peak moves from 10.6 to 102 keV and its value
exp(−3E₀/k_BT) grows from 1.2·10⁻⁷ to 6·10⁻³, so the tunnelling-weighted tail
gains almost five decades.
Axes: E [keV], 0–250; factor, 10⁻¹² to 1 (log).

### `reactivity`

Left: ⟨σv⟩(T) for D–T, D–D (³He + n and T + p, each branch), D–³He (Bosch–Hale
Table VII, drawn within its stated validity: 0.2–100 keV, D–³He to 190 keV)
and p–¹¹B (our numerical Maxwell average of the Nevins–Swain S(E), 20–500 keV).
The symbols are an independent comparison from measured data: our EXFOR
S-factor fit for D–T and D–D, Maxwell-averaged by quadrature at 2, 5, 10, 20,
50 and 100 keV. The p–¹¹B curve integrates the full Nevins–Swain S(E),
including the narrow 148 keV resonance; their stated S(E) uncertainty is
about 5 % plus 6 % normalisation. Right: D–T
⟨σv⟩/T² on a linear scale with its maximum at 13.5 keV. That maximum sets the
optimum temperature of the power balance: at fixed plasma pressure p ∝ nT,
the fusion power density p_fus ∝ n²⟨σv⟩ ∝ p²⟨σv⟩/T².
Axes: k_BT [keV] (log, 1–1000); ⟨σv⟩ [m³/s] (log); ⟨σv⟩/T² [10⁻²⁴ m³ s⁻¹ keV⁻²].
The viewer should see D–T more than two orders of magnitude above the other
reactions drawn at 10 keV (1.1·10⁻²² against 6·10⁻²⁵ for each D–D branch and 2·10⁻²⁵ for
D–³He), its broad maximum near 67 keV (the parametrisation is valid only up to
100 keV; a different maximum from the 13.5 keV of ⟨σv⟩/T²), D–³He overtaking
each D–D branch above 17 keV, and p–¹¹B overtaking them above about 67 keV.

Agreement printed by `ch02_reactivity.py` (numerical ⟨σv⟩ / Bosch–Hale − 1,
at 1, 2, 5, 10, 14, 20, 50, 100 keV):

| S(E) used in the quadrature | deviation [%] |
|---|---|
| Bosch–Hale S, D–T | +0.6, +0.7, +0.2, +0.5, +0.6, +0.8, +0.3, +0.1 |
| Bosch–Hale S, D–D n / p | within −1.5 … +1.9 |
| Bosch–Hale S, D–³He | within −3.2 … +0.6 |
| our EXFOR fit, D–T | −3.3, −2.6, −1.8, −1.3, −1.5, −1.9, −3.2, −3.5 |
| our EXFOR fit, D–D n | +10.2, +10.2, +9.7, +8.7, +8.0, +7.1, +4.8, +6.0 |

Bosch–Hale D–T at 10 keV: 1.136·10⁻²² m³/s, against the expected
≈ 1.1·10⁻²² from the course plan. The D–D difference follows the S factors:
our fitted D–D S lies 6–12 % above Bosch–Hale below 40 keV and 3–6 % above
at 100–300 keV. Below the lowest fitted point (14.8 keV) it is an
extrapolation; whether data or the extrapolation drive the difference has
not been tested. The table therefore compares two S factors, not a solved
discrepancy. For p–¹¹B, our quadrature agrees with Nevins–Swain eq. (13)
to within 2 % for 50–200 keV once their separate 148 keV resonance term is
excluded, but it lies 4–9 % above that fit at 300–500 keV, where the paper
quotes 0.22 %. That difference is unresolved, so the p–¹¹B curve is good to
about 10 % above 300 keV and to the S(E) uncertainty below.

### `tail_fuses` (Monte Carlo)

Two million D–T ion pairs at k_BT = 10 keV. Each ion's velocity is drawn from
its own 3D Maxwellian, and E = ½ m_r |v_D − v_T|². Histograms show all pairs and
the same pairs weighted by σ(E)v. σ comes from our EXFOR fit, including the
⁵He resonance. Thin dashed lines show the analytic densities f_M(E) and
σv f_M normalised, with the same σ. Shaded: the tail
E > 3k_BT, which holds 11 % of the pairs and 73 % of the reactions. The
reaction-weighted distribution peaks near 35 keV rather than at E₀ = 31 keV:
the fitted S(E) rises from 13.7 MeV b at 10 keV to 23 MeV b at the 64 keV
resonance, which shifts weight upwards.
Axes: E [keV], 0–150; density [keV⁻¹].
Check: the Monte Carlo mean of σv is 1.121·10⁻²² ± 0.002·10⁻²² m³/s, against
1.122·10⁻²² from the quadrature of the same σ, and the mean pair energy is
(3/2)k_BT.

### `maxwell-average` (animation, 18 s)

Left, over E (log axis, 0.3–1000 keV): D–T σv(E) with the ⁵He resonance
(Bosch–Hale S), the Maxwellian weight E f_M(E;T) (dashed) and their product
(shaded). The weight is the Maxwellian f_M per d(ln E),
(2/√π)(E/k_BT)^(3/2) e^(−E/k_BT); its maximum, at E = 1.5 k_BT, is the same at
every T. σv and the weight are each divided by a T-independent constant (their
maxima), and the product is drawn as the product of these scaled curves, so
the shaded area on the log axis is proportional to ⟨σv⟩(T). k_BT sweeps
1 → 100 keV geometrically (ln T linear in time). Right: ⟨σv⟩ computed
from that area and traced point by point over the dashed Bosch–Hale curve.
Axes: E [keV] (σv and weight scaled to unit maximum); k_BT [keV] (log, 1–100);
⟨σv⟩ [m³/s] (log, 10⁻²⁷ to 10⁻²¹).
The viewer should see the weight slide under the resonance: the shaded area
first grows from nothing, then the resonance is integrated away into a smooth
⟨σv⟩(T). On a linear energy axis the weight widens in proportion to T, so
⟨σv⟩(T) is a T-dependent weighted average (a moment) of σv, not a
translation-invariant convolution in E. Because the weight depends on E/T
only, it keeps its shape in ln E and merely shifts by ln T. In the variable
ln E the average is therefore a cross-correlation with one fixed kernel, which
is why the log axis shows a rigid window sliding along. The scene writes this on screen as
⟨σv⟩(T) = ∫ σv(u) K(u − s) du with u = ln E, s = ln k_BT and K = E f_M.
Check: the traced values are 1.142·10⁻²² (10 keV) and 8.674·10⁻²² m³/s
(50 keV), against Bosch–Hale 1.136·10⁻²² and 8.649·10⁻²²: +0.50 % and +0.29 %.

### `relative-velocity` (animation, 12 s, optional)

A genuine convolution, in one dimension at k_BT = 10 keV:
f_rel(g) = ∫ f_D(v) f_T(v − g) dv, the density of g = v_D − v_T. Written so it
is a cross-correlation; because f_T is even it equals the convolution
(f_D ∗ f_T)(g), and unlike the Maxwell average its kernel never changes shape. The tritium distribution slides across the
deuterium one, the overlap product f_D(v) f_T(v − g) is shaded, and its area
f_rel(g) is traced below over the dashed Maxwellian of the reduced mass
m_r = m_D m_T/(m_D + m_T). The variances add (k_BT/m_D + k_BT/m_T =
k_BT/m_r), and this is why ⟨σv⟩ uses the centre-of-mass energy with m_r.
Standard deviations √(k_BT/m): 0.69, 0.57 and 0.89·10⁶ m/s for D, T and the
relative velocity.
Axes: v, g [10⁶ m/s]; densities [10⁻⁶ s/m]. The 3D result is the same
Maxwellian in each component.
Check: the quadrature equals the reduced-mass Gaussian to a relative 10⁻⁹.

## Power balance

Zero-dimensional (0-D) model: 50:50 D–T with densities n_D = n_T = n/2,
electron density n_e = n, equal electron and ion temperatures T_e = T_i = T,
flat profiles, steady state, effective charge Z_eff = 1. Lower-case p are
powers per volume, capital P totals. W = 3nk_BT is the thermal energy per
volume (ions and electrons), τ_E the energy confinement time, so conduction
and convection lose W/τ_E. p_fus = n_D n_T ⟨σv⟩ E_fus with E_fus = 17.59 MeV
per reaction, of which the alpha particle keeps E_α = 3.56 MeV in the plasma.
P_ext is the external heating power, the gain is Q = P_fus/P_ext (not the
reaction energy Q_DT), and ignition means Q → ∞ (P_ext = 0). The power balance
uses the relativistic split (E_α/E_fus = 20.2 %).

### `alpha_neutron_split`

D + T at rest in the centre-of-mass frame → α + n with equal and opposite
momenta, so E_α/E_n = m_n/m_α. With Q_DT = 17.59 MeV from CODATA masses this
gives E_α = 3.54 MeV (20 %) and E_n = 14.05 MeV (80 %), drawn to scale as a bar.
Relativistic two-body kinematics give 3.56 and 14.03 MeV, quoted on the figure
in small print. The usual 3.5 and 14.1 MeV are rounded non-relativistic values.
Diagram; the bar is in MeV.

### `lawson_plane` (hero plot)

From 3nk_BT/τ_E + p_brems = (n²⟨σv⟩/4)(E_α + E_fus/Q):
nTτ_E = 12 T² / (⟨σv⟩(E_α + E_fus/Q) − 4C_B√T), with Bosch–Hale ⟨σv⟩.
Left: required nTτ_E against T for Q = 1, 5, 10 and ignition (Q = ∞) without
radiation, plus ignition with bremsstrahlung (dashed), whose power density is
p_brems = C_B n_e² √(k_BT) with C_B = 5.34·10⁻³⁷ W m³ keV^(−1/2) (NRL
1.69·10⁻³² W cm³ eV^(−1/2)). Right: nTτ_E against Q at the optimum
temperature 13.5 keV, without radiation, which approaches ignition as
Q/(Q + E_fus/E_α), E_fus/E_α = 4.94.
Axes: k_BT [keV] (log, 2–100); nTτ_E [keV s m⁻³] (log); Q (log);
nTτ_E [10²¹ keV s m⁻³].
The viewer should see a minimum at 13.5–14 keV for every Q, the wall that
bremsstrahlung builds below about 4.3 keV, and that, without radiation,
Q = 10 already needs two thirds of the ignition triple product.
Check: the ignition minimum is 2.74·10²¹ keV s m⁻³ at 13.5 keV (2.92·10²¹ at
14.2 keV with bremsstrahlung), against the lecture's ≈ 3·10²¹ at ≈ 14 keV:
−9 % (−3 %). The lecture value follows from the approximation
⟨σv⟩ ≈ 1.1·10⁻²⁴ T² m³/s (T in keV): 12/(1.1·10⁻²⁴ · 3561) = 3.1·10²¹. The
Bosch–Hale ⟨σv⟩/T² peaks at 1.23·10⁻²⁴, which gives the lower minimum.
Q = 1, 5 and 10 need 0.46, 1.38 and 1.84·10²¹. The ideal
ignition temperature (alpha heating = bremsstrahlung) is 4.28 keV. No machine
points are drawn, because no published values have been checked.

### `power_flow`

The 0-D steady state at Q = 10, scaled to P_fus = 500 MW. Arrow widths are
proportional to power: P_ext = 50 MW in, P_α = 101 MW from the fusion
reactions back into the plasma, P_loss = W/τ_E = P_ext + P_α = 151 MW to the
wall and divertor, and P_n = 399 MW to the blanket. Only Q and the
relativistic 20.2/79.8 % split set the ratios. The 500 MW scale is
illustrative. Here P_loss lumps all losses, radiation included, into W/τ_E,
unlike the bremsstrahlung curve of `lawson_plane`, where radiation is
separate.
Diagram; powers in MW.

### `density_scaling`

At k_BT = 14 keV: alpha heating p_α = (n²/4)⟨σv⟩E_α against the conduction loss
3nk_BT/τ_E for τ_E = 0.1, 1 and 10 s. Slopes 2 and 1 on log axes; the crossings
are at n = 12k_BT/(⟨σv⟩E_α τ_E) = 2·10²¹, 2·10²⁰ and 2·10¹⁹ m⁻³.
Axes: n [m⁻³] (log); power density [W m⁻³] (log).

### `alpha_brems`

p_α/n_e² = ⟨σv⟩E_α/4 and p_br/n_e² = C_B √(k_BT) (Z_eff = 1) against T; n_e²
cancels, so they cross at the ideal ignition temperature 4.28 keV for any density.
Axes: k_BT [keV] (log, 1–100); p/n_e² [W m³] (log).

### `q_eng`

Q_eng = η_th η_aux (Q + 1) − 1 against Q for η_th η_aux = 0.4 × 0.4 and 0.5 × 0.6.
Assumes all fusion and heating power become heat at η_th, no blanket energy gain
and no other recirculating loads. Q_eng = 0 at Q = 5.25 and Q_eng = 1 (half the
gross electricity recirculated) at Q = 11.5 for 0.4 × 0.4.

### `impurity_dilution`

Left: ignition n_eTτ_E(T) with bremsstrahlung for 0, 5, 10 and 15 % helium
(c = n_He/n_e), from n_eTτ_E = (3/2)(1 + n_i/n_e)T² / ((1 − 2c)²⟨σv⟩E_α/4 −
C_B Z_eff √T), Z_eff = 1 + 2c. Minima 2.9, 3.6, 4.6 and 6.1·10²¹ keV s m⁻³ near
14–15 keV. Right: p_fus/p_fus(c = 0) = (1 − Zc)² at fixed n_e, with 0.1 % W
(Zc = 0.074, 0.86) and 5 % He (Zc = 0.1, 0.81). Tungsten is drawn only on the
right: in a reactor core it is not fully ionised and line radiation, not
bremsstrahlung, dominates its loss, which this model omits.

### `fixed_pressure`

D–T p_fus at fixed density (∝ ⟨σv⟩) and at fixed pressure (∝ ⟨σv⟩/T²), each
divided by its maximum: maxima at 67 keV and 13.5 keV.
Axes: k_BT [keV] (log, 2–100); p_fus / maximum.

### `n_tau_plane`

Density against confinement time. Lines: n τ_E for D–T ignition and Q = 1 at
14 keV, uniform 0-D plasma (2.0·10²⁰ and 3.3·10¹⁹ s m⁻³). Points: measured
Lawson parameters from S. E. Wurzel and S. C. Hsu, Phys. Plasmas 29, 062103
(2022), doi:10.1063/5.0083990, CC BY 4.0, Tables 6–8, read from the arXiv
source (2105.10954v4) by `scripts/prepare-ch04-lawson-data.py` into
`data/ch04/wurzel_hsu_2022.csv`. Magnetic: peak ion density n_i0 and τ_E*;
inertial (laser ICF, MagLIF): n = nτ/τ_stag where τ_stag is reported. The
projected SPARC and ITER rows are excluded. Sun: τ = GM²/(RL) = 3.1·10⁷ yr
(IAU 2015 nominal values); electron density from the mean (1.41 g/cm³,
hydrogen mass fraction 0.7) to the core (150 g/cm³, X = 0.35, standard solar
model, not re-checked). The peak values of the points and the uniform-plasma
lines are not strictly comparable (Wurzel and Hsu correct for profile
factors); the plot compares orders of magnitude.
Axes: τ [s] (log, 10⁻¹²–10¹⁷); n [m⁻³] (log, 10¹⁷–10³⁴).
