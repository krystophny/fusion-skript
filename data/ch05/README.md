# Chapter 5 data: magnetic confinement devices

Inputs to `slides/figures_devices.py`. Numerical data are credited to their providers; our
reductions and figures are CC BY 4.0.

| File | Content | Source and terms | Made by |
|---|---|---|---|
| `iter-coils.json` | ITER central-solenoid modules CS3U-CS3L and poloidal-field coils PF1-PF6: centre R, Z and cross-section ΔR, ΔZ in m (PF cross-sections as squares of equal area). Schematic TF D shape (18 coils) and plasma shape R0 = 6.2 m, a = 2.0 m, κ = 1.7, δ = 0.33 | Coil table: M3D-C1 device data `unstructured/device_data/ITER/coil.dat`, https://github.com/PrincetonUniversity/M3DC1. Plasma shape: ITER Physics Basis, Nucl. Fusion 39, 2137 (1999), doi:10.1088/0029-5515/39/12/301. TF D shape: our sketch, sized to clear the CS and PF coils | typed |
| `ncsx.json` | NCSX: the 18 modular coil filaments (every 4th point, m) with their currents, and the VMEC last closed flux surface (R, Z, λ Fourier coefficients, ι) of the reference plasma | STELLOPT benchmark `BENCHMARKS/FIELDLINES_TEST/{coils.NCSX,wout_NCSX_plasma.nc}`, https://github.com/PrincetonUniversity/STELLOPT | `scripts/prepare-ch05-ncsx.py` |
