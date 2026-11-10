# Chapter 3 data: fusion in stars

All files are inputs to `derivations/chapters/ch03_stars.py`, `slides/figures_stars.py`
and the slide widgets `notebooks/slide-{star,bbn,extremes}.html`. Numerical data are
credited to their providers; our reductions, plots and widgets are CC BY 4.0.

| File | Content | Source and terms | Made by |
|---|---|---|---|
| `mist.json` | Core T, ρ, composition, burning luminosities (pp, CNO, 3α, C), L, T_eff, mass and phase against age for 20 initial masses at [Fe/H] = −2, −1, 0, +0.5 | MIST v1.2 EEP tracks, https://mist.science/ (computed with MESA); Dotter, ApJS 222, 8 (2016), doi:10.3847/0067-0049/222/1/8; Choi et al., ApJ 823, 102 (2016), doi:10.3847/0004-637X/823/2/102. Free to use with citation; no licence file. | `scripts/prepare-ch03-mist.py` (subsampled, all primary EEPs kept) |
| `bbn.json` | Abundances Y_i = n_i/n_b against time and photon temperature for 21 values of η, final abundances against η | Our runs of LINX (MIT), key network PRIMAT 2023; Giovanetti et al., Phys. Rev. D 112, 063531 (2025), doi:10.1103/f3tj-r882. Observed Y_p: Aver et al. (2015); D/H: Cooke et al. (2018); ⁷Li/H: PDG (2024) | `scripts/prepare-ch03-bbn.py` |
| `solar-model.json` | Radial profile of the present Sun: T, ρ, X, L_r, ε | Model S, Christensen-Dalsgaard et al., Science 272, 1286 (1996), doi:10.1126/science.272.5266.1286; file `fgong.l5bi.d.15`, https://users-phys.au.dk/jcd/solar_models/ | `scripts/prepare-ch03-solar-model.py` |
| `abundances.json` | Solar-system element abundances log ε | Asplund, Amarsi & Grevesse, A&A 653, A141 (2021), doi:10.1051/0004-6361/202140445, Table 2, CC BY 4.0 | `scripts/prepare-ch03-abundances.py` |
| `ame2020-mass_1.mas20` | Atomic mass evaluation 2020 (unchanged) | Wang et al., Chin. Phys. C 45, 030003 (2021), doi:10.1088/1674-1137/abddaf (CC BY 3.0), IAEA AMDC | copied |
| `neutrinos.json` | Solar neutrino fluxes, B16-GS98 | Vinyoles et al., ApJ 835, 202 (2017), doi:10.3847/1538-4357/835/2/202, Table 6 | typed from the table |
| `conditions.json` | Central density and temperature of objects in the ρ–T widget, with one reference per entry | references inside the file | typed |
| `stages.json` | Burning stages of a 20 M☉ star: temperature, duration, products | Heger, Woosley, Fryer & Langer, in *From Twilight to Highlight*, ESO Symposia (2003), arXiv:astro-ph/0211062, Table 1 | typed |

The B16, stage and condition values were typed from the cited tables on 2026-11-10.
Late burning stages (Ne, O, Si) have no published central density in the cited table;
the widget continues the MIST central track along ρ_c ∝ T_c³ (contraction of a
non-degenerate core) and marks this continuation as such.
