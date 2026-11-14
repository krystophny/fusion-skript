# MILCA in the browser

`milca_tokamak.mjs` is the teaching discharge model of
[MILCA](https://github.com/itpplasma/milca): `src/continuum/tokamak_discharge.f90`
with `src/mhd/cylinder_stability.f90` and `src/mhd/ballooning_s_alpha.f90`
([milca#432](https://github.com/itpplasma/milca/pull/432)), compiled to
WebAssembly by LFortran (lazy-fortran fork, 0.69.0-252-g652e56e133) and emscripten 6.0.13 and embedded in an ES module.
`slide-disruption.html` runs it. Model, surrogates and checks: MILCA
`docs/tokamak-limits-course.md`. Rebuild from a MILCA checkout:

    EMSDK_PATH=... LFORTRAN=... sh web/tokamak-limits/build.sh OUTDIR

MIT licence, as MILCA.
