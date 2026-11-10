# Fusion in stars — live route

Chapter 3. Canonical source: `slides/03-fusion-in-stars.typ`.
Course structure: `Nextcloud/lv/fusion/PLAN.md`. Live lecture (decided
2026-11-10). The chapter applies the reaction physics of Chapter 2 (Gamow
peak, S factor, p–p from theory) to stars and to the early universe, and ends
by comparing gravitational with magnetic confinement. The p–p chain and solar
core pages moved here from deck 02.

All models use published data, not toy models: MIST v1.2 stellar tracks
(computed with MESA), the LINX nucleosynthesis network, Model S of the Sun,
AME2020 masses, Asplund et al. (2021) abundances and B16 neutrino fluxes.
Provenance: `data/ch03/README.md`; numbers and checks:
`derivations/chapters/ch03_stars.py`, `tests/test_stars.py`; images:
`slides/photos/stars/credits.md`.

## Notation

L☉, M☉, R☉ solar luminosity, mass, radius; t_KH Kelvin–Helmholtz time;
K, U thermal and gravitational energy; μ mean mass per particle in m_u;
η baryon-to-photon ratio; Y_p primordial helium mass fraction; Q = 1.293 MeV
neutron–proton mass difference; B_D = 2.224 MeV deuteron binding; τ_n neutron
lifetime; E_0 Gamow peak and τ = 3E_0/k_BT as in Chapter 2; ε heating per mass;
μ_e mass per electron in m_u; M_Ch Chandrasekhar mass.

## Pages

| Page | Content | Lecturer cue |
|---|---|---|
| 1 | Title | — |
| 2 | Photo: the Sun (SDO, 304 Å) | 3.1 What powers the Sun |
| 3 | Energy budget of the Sun | t_KH ≈ 3 × 10⁷ yr against 4.5 Gyr (Kelvin against the geologists); 4p → ⁴He frees 0.71 % of the mass, burning 10 % of the hydrogen gives 10¹⁰ yr. Eddington 1920 (Chapter 1), Bethe 1939. |
| 4 | Hydrostatic equilibrium and virial theorem | Board: virial theorem for a uniform sphere, k_B T̄ = GMμm_u/5R ≈ 0.25 keV; Model S centre 1.35 keV. E = −K: a star that loses energy heats up. Fusion runs at the rate the star loses heat — the thermostat a tokamak has to build. |
| 5 | Inside the Sun (Model S) | T, ρ, convective zone; 99 % of L made inside 0.26 R☉; hydrogen half used up at the centre. |
| 6 | The Sun and a tokamak | Sun core 262 W/m³, less than a human body; τ_E = W_th/L ≈ 2 × 10⁷ yr; n T τ_E exceeds the D–T requirement by 25 orders of magnitude, with the weakest reaction. Link to Chapter 4. |
| 7 | 3.3 Proton–proton chain (moved from deck 02) | Weak interaction in the first step (Chapter 2: p–p from theory). |
| 8 | Three branches | Branch shares from B16 neutrino fluxes: Φ(⁷Be)/Φ(pp) = f/(2 − f) gives pp I 84.8 %, pp II 15.2 %, pp III 0.017 %. Corrects the 2020 lecture (91/9/0.1 %). |
| 9 | Solar core (moved from deck 02, plot `gamow_peak_pp`) | k_BT ≈ 1.3 keV, E_0 ≈ 6 keV ≈ 4.6 k_BT. |
| 10 | Solar neutrinos (plot `solar_neutrinos`) | Neutrinos leave the core in 2 s; detectors by threshold; Davis 1968 deficit, oscillations; Borexino pp (2014) and CNO (2020) are direct evidence of fusion in the core. The ⁸B shape is the allowed β spectrum to the 3 MeV ⁸Be state (approximate). |
| 11 | 3.4 CNO cycle | Catalytic; ¹⁴N(p,γ) is the bottleneck (Z₁Z₂ = 7). |
| 12 | pp or CNO? (plot `pp_cno`) | Board: d ln⟨σv⟩/d ln T = (τ − 2)/3 from Chapter 2 gives T⁴ for pp at the solar centre and T¹⁸ for ¹⁴N + p; equal at 19 MK. MIST: CNO above 1.5 M☉, so massive stars have convective cores. |
| 13 | Photo: microwave sky (WMAP) | 3.5 Primordial nucleosynthesis; η from the CMB. |
| 14 | Neutrons decide the helium | Board: freeze-out n/p = e^(−Q/k_BT_f) ≈ 1/5; Saha deuterium bottleneck opens at 0.066 MeV, t ≈ 300 s; decay to n/p ≈ 1/7; Y_p = 2x/(1 + x) ≈ 0.25 against LINX 0.247 and observed 0.245. |
| 15 | Widget `bbn` | η slider: mass fractions against time (LINX histories for 21 values of η, interpolated) and final abundances against η with observed bands. D/H is the baryometer; ⁴He barely moves; ⁷Li is 3–4 times too high at the Planck η (lithium problem). |
| 16 | Why it stops at lithium | No stable A = 5, 8; density 10⁻² kg/m³; minutes. |
| 17 | Photo: Carina Nebula | 3.6 Helium burning and heavier elements. |
| 18 | Triple alpha and the Hoyle state (plot `hoyle`) | ⁸Be 92 keV above 2α; Hoyle state 288 keV above ⁸Be + α (corrects the 278–280 keV of 2020), from AME2020 masses. Predicted by Hoyle and found in 1953 (Dunbar et al.); Cook et al. (1957) showed that it forms ¹²C from ⁸Be + α. |
| 19 | Binding energy per nucleon (plot `binding`) | Each stage burns the ash of the previous one; ⁶²Ni is most bound, ⁵⁶Fe is made (as ⁵⁶Ni). First place in 2026 where B/A is shown. |
| 20 | Burning stages of a massive star | 20 M☉ table (Heger et al. 2003); after helium, neutrino losses ∝ T⁹ shorten the stages to years and days; onion schematic. |
| 21 | Widget `star` | MIST tracks: mass 0.1–100 M☉, four metallicities, age slider and run toggle. Show 1 M☉ (pp, He flash, thermal pulses, C/O white dwarf of 0.54 M☉), then 15 M☉ (CNO, He, C burning to an O–Ne core). Some very massive tracks end early (MIST); the widget says so. |
| 22 | Photo: Ring Nebula (Webb) | 3.7 Degenerate endpoints. |
| 23 | Degeneracy ends the burning | 0.075 M☉ minimum, brown dwarfs 13 M_J; our degenerate-electron solution: 0.6 M☉ white dwarf with ρ_c = 3.5 × 10⁹ kg/m³; M_Ch = 1.46 M☉. |
| 24 | Widget `extremes` | 3.8 Fusion under extreme conditions. ρ–T map with MIST centres, the Big Bang track, burning bands, degeneracy and radiation lines, tokamak and NIF; click a point for photo, values, process and reference. |
| 25 | Photo: GK Persei (X-ray) | Nova of 1901. |
| 26 | Novae: hot CNO | β⁺ half-lives cap the CNO rate. |
| 27 | Photo: Tycho's supernova remnant | Type Ia of 1572. |
| 28 | Type Ia: a carbon bomb | Degenerate ignition, no thermostat (contrast page 4); 0.81 MeV per nucleon × 1.4 M☉ = 2 × 10⁴⁴ J unbinds the star; ⁵⁶Ni → ⁵⁶Co → ⁵⁶Fe light curve. |
| 29 | Photo: Crab Nebula (Webb) | Supernova of 1054. |
| 30 | Core collapse: gravity, not fusion | 3/5 GM²/R = 3 × 10⁴⁶ J, 99 % neutrinos; SN 1987A neutrinos; fusion made the core and burns the ejecta. |
| 31 | Photo: neutron-star merger (illustration) | Labelled as illustration. |
| 32 | Neutron stars: bursts, crusts, mergers | rp process; pycnonuclear fusion by density, link to muon catalysis (Chapter 9); mergers make heavy elements by neutron capture, not fusion. |
| 33 | Where the elements come from (plot `abundances`) | Big Bang, stellar fusion up to the iron peak, neutron capture beyond. |
| 34 | Stars and fusion on Earth | Closing comparison; leads to Chapter 4 power balance. |
| 35 | Credits | — |

## Sources and checks

`derivations/chapters/ch03_stars.py` checks: virial temperature (SymPy), Kelvin–Helmholtz
and nuclear time scales, the Sun against Lawson, pp + CNO rates against Model S
(88 % of L without screening), pp/CNO crossover, pp branches from neutrino
fluxes, neutron freeze-out, Saha deuterium temperature and Y_p, Hoyle-state
energies from AME2020, most-bound nucleus, Chandrasekhar mass and a white-dwarf
solution, Type Ia and core-collapse energies. `tests/test_stars.py` compares
these against MIST, Model S and LINX. Data generators: `scripts/prepare-ch03-*.py`.

Open: Option of our own MESA runs to core collapse, which would replace the
ρ ∝ T³ continuation after carbon burning in the `extremes` widget.
