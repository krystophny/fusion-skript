# Fusion in stars — live route

Chapter 3. Canonical source: `slides/03-fusion-in-stars.typ`.
Course structure: `Nextcloud/lv/fusion/PLAN.md`. Live lecture (decided
2026-11-10), redesigned the same day: no repeated pages, every text slide built
up step by step, interactive widgets wherever a parameter is worth varying, and
each reaction coloured by the interaction that sets its rate (weak purple,
electromagnetic blue, strong orange). The PDF is a handout with the final step
of each build; the presenter shows every step.

All models use published data: MIST v1.2 tracks (MESA), our LINX runs
(PRIMAT 2023 network, 2–5 neutrino species), Model S, AME2020, Asplund et al.
(2021) abundances, B16 neutrino fluxes, Adelberger et al. (2011) S factors,
Bond et al. (2017) white dwarfs. Provenance: `data/ch03/README.md`; numbers and
checks: `derivations/chapters/ch03_stars.py`, `tests/test_stars.py`; images:
`slides/photos/stars/credits.md`.

## Notation

L☉, M☉, R☉ solar luminosity, mass, radius; t_KH Kelvin–Helmholtz time;
K, U thermal and gravitational energy; μ mean mass per particle in m_u;
η baryon-to-photon ratio; Y_p primordial helium mass fraction; Q = 1.293 MeV;
B_D = 2.224 MeV; τ_n neutron lifetime; E_0 Gamow peak, τ = 3E_0/k_BT;
S(0) astrophysical S factor; μ_e mass per electron in m_u; M_Ch Chandrasekhar mass.

## Pages (handout numbering; build steps in brackets)

| Page | Content | Lecturer cue |
|---|---|---|
| 1 | Title | — |
| 2 | Photo: the Sun (SDO) | 3.1 What powers the Sun |
| 3 [5] | Energy budget | Sun's numbers → gravity lasts 3 × 10⁷ yr → Earth is 4.5 Gyr old → fusion lasts 10¹⁰ yr → result. Eddington 1920, Bethe 1939. |
| 4 [5] | Hydrostatic equilibrium and virial theorem | 3.2. Board: virial theorem, mean 0.25 keV (centre 1.35 keV on the next page); E = −K: the star heats when it loses energy, a thermostat. |
| 5 | Inside the Sun (Model S) | 99 % of L inside 0.26 R☉; 262 W/m³ at the centre, less than a human body. |
| 6 [7] | The Sun and a tokamak | Row by row; the Sun wins by τ_E, not by rate. |
| 7 [6] | Proton–proton chain | 3.3 Burning hydrogen. Step by step: p+p (weak, the slowest: Chapter 2), D+p (e.m.), ³He+³He (strong, pp I), pp II, pp III, net and the branch shares from neutrino fluxes (84.8/15.2/0.017 %). |
| 8 [4] | Which force sets the rate? | S(0) by force: weak 10⁻²² keV b, e.m. 10⁻⁴–1 keV b, strong 10³ keV b. ν out: weak, γ out: e.m., only nuclei: strong. The force sets S, the Coulomb barrier sets the temperature. |
| 9 [7] | CNO cycle | Around the cycle; ¹⁴N(p,γ) is the bottleneck (e.m. and Z₁Z₂ = 7); net, energy, catalyst. |
| 10 | Widget `gamow` | Fuel and T: Gamow window, E_0/k_BT and rate ∝ T^ν, force; pp against CNO heating, equal at 19 MK. Slide T up to 100 MK for He and 1 GK for C and O. |
| 11 | Widget `neutrinos` | Detector thresholds; shares are of the flux, not of the count rate (cross sections rise with energy, so Cl and water see mostly ⁷Be and ⁸B). Borexino measured pp (2014) and CNO (2020). |
| 12 | Widget `sun` | The Sun's own track: today 0.8 % CNO, end of core hydrogen 9.8 Gyr, red giant shell burning almost all CNO, He flash, AGB, C/O white dwarf of 0.54 M☉; carbon never ignites. |
| 13 | Photo: microwave sky (WMAP) | 3.4 Primordial nucleosynthesis. |
| 14 [5] | Neutrons decide the helium | Freeze-out (weak), deuterium bottleneck (e.m.), decay, Y_p ≈ 0.25 against LINX 0.247. |
| 15 | Widget `bbn` | η and the number of neutrino species: each extra species adds about 0.013 to Y_p; only three fit the observed 0.245. D/H measures η; lithium problem. |
| 16 [4] | Why it stops at lithium | No stable A = 5, 8; dilute; fast; lithium problem. |
| 17 | Photo: Carina Nebula | 3.5 Helium burning and heavier elements. |
| 18 [4] | Triple alpha and the Hoyle state | ⁸Be 92 keV, Hoyle state 288 keV above ⁸Be + α (AME2020); strong steps, e.m. stabilisation, ¹²C(α,γ)¹⁶O. |
| 19 | Widget `binding` | Pick a reaction: fuel and ash on the B/A curve, Q, energy per kg; D–T and ²³⁵U fission for comparison; ⁶²Ni most bound. |
| 20 [7] | Burning stages of a massive star | Row by row (20 M☉), neutrino losses ∝ T⁹, then the onion. |
| 21 | Widget `star` | Mass, metals and age: 15 M☉ to an O–Ne core; very massive MIST tracks may end early. |
| 22 | Photo: Ring Nebula | 3.6 Endpoints and extreme conditions. |
| 23 [5] | Degeneracy ends the burning | No thermostat; 0.075 M☉; brown dwarfs; M_Ch; neutron stars. |
| 24 | Widget `whitedwarf` | Central density moves the star along our cold-electron mass–radius curve; Procyon B, Sirius B, Stein 2051 B, 40 Eri B lie on it; radius → 0 at M_Ch. |
| 25 | Widget `extremes` | ρ–T map: click objects (Sun, white dwarf, nova, X-ray burst, Type Ia, bounce, crust, tokamak, NIF). Novae are only here. |
| 26 | Photo: Tycho's supernova remnant | — |
| 27 [5] | Type Ia: a carbon bomb | Degenerate ignition, no thermostat; 2 × 10⁴⁴ J; ⁵⁶Ni → ⁵⁶Co → ⁵⁶Fe (weak) light curve. |
| 28 | Photo: Crab Nebula (Webb) | — |
| 29 [5] | Core collapse: gravity, not fusion | 3 × 10⁴⁶ J, 99 % neutrinos; SN 1987A. |
| 30 | Photo: neutron-star merger (illustration) | — |
| 31 [4] | Neutron stars | rp process, pycnonuclear crust, r process is not fusion, muon catalysis (Chapter 9). |
| 32 | Where the elements come from | Big Bang, stellar fusion to the iron peak, neutron capture beyond. |
| 33 | Credits | — |

## Sources and checks

`derivations/chapters/ch03_stars.py` checks: virial temperature (SymPy), time
scales, the Sun against Lawson, pp + CNO rates against Model S (88 % of L without
screening), pp/CNO crossover, pp branches from neutrino fluxes, freeze-out, Saha
deuterium temperature and Y_p, Hoyle-state energies, most-bound nucleus,
Chandrasekhar mass and white-dwarf solutions, Type Ia and core-collapse energies,
reaction Q values for the binding widget. `tests/test_stars.py` compares against
MIST, Model S and LINX, including the helium count of neutrino species.

Open: our own MESA runs to core collapse would replace the ρ ∝ T³ continuation
after carbon burning in the `extremes` widget.
