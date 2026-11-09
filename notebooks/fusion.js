// Shared model functions for the Fusion Physics notebooks (MIT).
// Mirrors derivations/chapters/ch02_reactivity.py and ch04_power_balance.py;
// tests/test_notebooks.py evaluates both at the same points.
// Units: E, T in keV (k_B T written as T), sigma in m^2, <sigma v> in m^3/s.

export const KEV = 1.602176634e-16;            // J
export const C_LIGHT = 299792458;              // m/s
export const BARN = 1e-28;                     // m^2
// Relativistic two-body split of D + T at rest from CODATA masses (ch04_power_balance.two_body_split).
export const E_FUS = 17589.24794;              // keV
export const E_ALPHA = 3560.8535860879;           // keV
// NRL Plasma Formulary (2018) p. 58: 1.69e-32 W cm^3 eV^-1/2 in W m^3 keV^-1/2.
export const C_B = 1.69e-32 * 1e-6 * Math.sqrt(1e3);

export const REACTIONS = ["DT", "DD", "DHe3"];

// Bosch and Hale (1992) Table VII; r = reactivity.json bosch_hale_reactivity.reactions[name].
export function boschHale(r, t) {
  const [c1, c2, c3, c4, c5, c6, c7] = r.C;
  const theta = t / (1 - t * (c2 + t * (c4 + t * c6)) / (1 + t * (c3 + t * (c5 + t * c7))));
  const xi = Math.cbrt(r.B_G_sqrt_keV ** 2 / (4 * theta));
  return c1 * theta * Math.sqrt(xi / (r.mrc2_keV * t ** 3)) * Math.exp(-3 * xi) * 1e-6;
}

// Reactivity of a named channel; "DD" is the sum of both D-D branches.
export function reactivity(rx, name, t) {
  const r = rx.bosch_hale_reactivity.reactions;
  if (name === "DD") return boschHale(r.DDn, t) + boschHale(r.DDp, t);
  return boschHale(r[name], t);
}

function pade(e, a, b) {
  const num = a[0] + e * (a[1] + e * (a[2] + e * (a[3] + e * a[4])));
  return num / (1 + e * (b[0] + e * (b[1] + e * (b[2] + e * b[3]))));
}

// Bosch-Hale S(E) in keV b (Table IV), with the high-energy fits used by ch02_reactivity.s_factor(..., "bh").
export function sFactor(cs, rx, name, e) {
  const t4 = cs.bosch_hale.reactions;
  const extra = rx.bosch_hale_s_factor_extra;
  if (name === "DT") {
    if (e <= 550) return 1e-3 * pade(e, t4.DT.A, t4.DT.B);
    return 1e-3 * pade(Math.min(e, 4700), extra.DT_high.A, extra.DT_high.B);
  }
  if (name === "DHe3") {
    if (e <= 900) return 1e-3 * pade(e, extra.DHe3_low.A, extra.DHe3_low.B);
    return 1e-3 * pade(Math.min(e, 4800), extra.DHe3_high.A, extra.DHe3_high.B);
  }
  return 1e-3 * pade(e, t4[name].A, t4[name].B);
}

export function gamowEnergy(rx, name) {
  const r = rx.bosch_hale_reactivity.reactions[name === "DD" ? "DDn" : name];
  return r.B_G_sqrt_keV ** 2;
}

export function reducedMass(rx, name) {
  return rx.bosch_hale_reactivity.reactions[name === "DD" ? "DDn" : name].mrc2_keV;
}

// Cross section sigma = S/E exp(-sqrt(E_G/E)) in m^2; "DD" sums both branches.
export function sigma(cs, rx, name, e) {
  if (name === "DD") return sigma(cs, rx, "DDn", e) + sigma(cs, rx, "DDp", e);
  const bg = rx.bosch_hale_reactivity.reactions[name].B_G_sqrt_keV;
  return sFactor(cs, rx, name, e) / e * Math.exp(-bg / Math.sqrt(e)) * BARN;
}

// Gamow peak E_0 and 1/e full width Delta in keV.
export function gamowPeak(eG, t) {
  const e0 = Math.cbrt(eG * t * t / 4);
  return {e0, width: 4 * Math.sqrt(e0 * t / 3), tau: 3 * e0 / t};
}

// Log-energy kernel K(x) = (2/sqrt(pi)) e^(3x/2) exp(-e^x), x = ln(E/k_BT).
export function kernel(x) {
  return 2 / Math.sqrt(Math.PI) * Math.exp(1.5 * x - Math.exp(x));
}

// <sigma v> = c sqrt(8/(pi m c^2)) T^-3/2 int sigma E e^(-E/T) dE, trapezoid on a geometric grid.
export function maxwellAverage(cs, rx, name, t, n = 6000) {
  const {e0} = gamowPeak(gamowEnergy(rx, name), t);
  const lo = Math.log(1e-3), hi = Math.log(Math.max(60 * t, 12 * e0, 2000));
  let sum = 0, prev = null;
  for (let i = 0; i < n; i++) {
    const e = Math.exp(lo + (hi - lo) * i / (n - 1));
    const f = sigma(cs, rx, name, e) * e * Math.exp(-e / t);
    if (prev) sum += 0.5 * (f + prev.f) * (e - prev.e);
    prev = {e, f};
  }
  return C_LIGHT * Math.sqrt(8 / (Math.PI * reducedMass(rx, name))) * t ** -1.5 * sum;
}

// Saddle-point form (8 sqrt 6 / 27) S(E_0) / sqrt(m E_G) tau^2 e^-tau, m in keV/c^2.
export function gamowEstimate(cs, rx, name, t) {
  const eG = gamowEnergy(rx, name);
  const {e0, tau} = gamowPeak(eG, t);
  const s = name === "DD" ? sFactor(cs, rx, "DDn", e0) + sFactor(cs, rx, "DDp", e0)
                          : sFactor(cs, rx, name, e0);
  return 8 * Math.sqrt(6) / 27 * s * BARN * C_LIGHT / Math.sqrt(reducedMass(rx, name) * eG) * tau ** 2 * Math.exp(-tau);
}

// --- 0-D power balance, 50:50 D-T, n_e = n, T_e = T_i = T -----------------------------------
// Required n T tau_E (keV s m^-3) for gain Q (Infinity: ignition); bremsstrahlung C_B Z_eff n_e^2 sqrt(T)
// is included when zeff > 0.
export function tripleProduct(rx, t, q = Infinity, zeff = 0) {
  const sv = reactivity(rx, "DT", t);
  const heat = sv * (E_ALPHA + (Number.isFinite(q) ? E_FUS / q : 0)) * KEV;
  const net = heat - 4 * C_B * zeff * Math.sqrt(t);
  return net > 0 ? 12 * t * t * KEV / net : Infinity;
}

// Wurzel & Hsu (2022) Eqs. (38)-(40): profile factors for n, T ~ (1 - x^2)^nu; same
// midpoint rule in s = x^2 as ch04_power_balance.profile_factors.
export function profileFactors(rx, t0, nuN = 0.2, nuT = 3, points = 400) {
  let sum = 0;
  for (let i = 0; i < points; i++) {
    const s = (i + 0.5) / points, ts = t0 * (1 - s) ** nuT;
    if (ts >= 0.2) sum += (1 - s) ** (2 * nuN) * reactivity(rx, "DT", ts);
  }
  return {kappa: 1 / (1 + nuN + nuT), F: sum / points / reactivity(rx, "DT", t0), B: 2 / (4 * nuN + nuT + 2)};
}

// Wurzel & Hsu (2022) Eq. (45): n_i0 T_i0 tau_E for gain q in peak values, with the
// profiles and impurities of their magnetic-confinement contours.
export function peakTripleProduct(rx, t0, q = Infinity,
    {zeff = 1.5, zbar = 1.2, etaAbs = 0.9, nuN = 0.2, nuT = 3} = {}) {
  const lam = profileFactors(rx, t0, nuN, nuT);
  const gain = Number.isFinite(q) ? etaAbs * E_FUS / q : 0;
  const net = lam.F * reactivity(rx, "DT", t0) * (E_ALPHA + gain) / 4 * KEV
    - lam.B * C_B * zeff * zbar * zbar * Math.sqrt(t0);
  return net > 0 ? 1.5 * lam.kappa * (1 + zbar) * t0 * t0 * KEV / net : Infinity;
}

export function fAlpha(q) {
  return Number.isFinite(q) ? q / (q + E_FUS / E_ALPHA) : 1;
}

export function qEng(q, etaTh, etaAux) {
  return etaTh * etaAux * (q + 1) - 1;
}

// Quasineutral dilution for impurities [[Z, n_Z/n_e], ...]: fuel (n_D + n_T)/n_e, ions n_i/n_e, Z_eff.
export function dilution(impurities) {
  let fuel = 1, ions = 0, z2 = 0;
  for (const [z, c] of impurities) { fuel -= z * c; ions += c; z2 += z * z * c; }
  return {fuel, ions: fuel + ions, zeff: fuel + z2};
}

// Ignition n_e T tau_E (keV s m^-3) with dilution and bremsstrahlung of fully stripped ions.
export function ignitionDiluted(rx, t, impurities = []) {
  const {fuel, ions, zeff} = dilution(impurities);
  const net = fuel * fuel / 4 * reactivity(rx, "DT", t) * E_ALPHA * KEV - C_B * zeff * Math.sqrt(t);
  return net > 0 && fuel > 0 ? 1.5 * (1 + ions) * t * t * KEV / net : Infinity;
}

// Coronal radiative cooling rate L_Z (W m^3) of one impurity species, all radiation of
// its ions (lines, recombination, bremsstrahlung): p_Z = n_e n_Z L_Z(T_e). Fits of
// Mavrin, Radiat. Eff. Defects Solids 173, 388 (2018), valid 0.1-100 keV, as tabulated in
// cfspopcon (MIT): log10 L_Z = sum_k c_k (log10 T)^k on temperature bins (borders in keV).
export const MAVRIN = {
  4: {name: "Be", borders: [0, 100], c: [[-3.4765e1, 3.7270e-2, 3.8363e-1, -2.1384e-1, 4.1690e-2]]},
  6: {name: "C", borders: [0, 0.5, 100], c: [[-3.4738e1, -5.0085, -1.2788e1, -1.6637e1, -7.2904],
    [-3.4174e1, -3.6687e-1, 6.8856e-1, -2.9191e-1, 4.4470e-2]]},
  7: {name: "N", borders: [0, 0.5, 2, 100], c: [[-3.4065e1, -2.3614, -6.0605, -1.1570e1, -6.9621],
    [-3.3899e1, -5.9668e-1, 7.6272e-1, -1.7160e-1, 5.8770e-2],
    [-3.3913e1, -5.2628e-1, 7.0047e-1, -2.2790e-1, 2.8350e-2]]},
  8: {name: "O", borders: [0, 0.3, 100], c: [[-3.7257e1, -1.5635e1, -1.7141e1, -5.3765, 0],
    [-3.3640e1, -7.6211e-1, 7.9655e-1, -2.0850e-1, 1.4360e-2]]},
  74: {name: "W", borders: [0, 1.5, 4, 100], c: [[-3.0374e1, 3.8304e-1, -9.5126e-1, -1.0311, -1.0103e-1],
    [-3.0238e1, -2.9208, 2.2824e1, -6.3303e1, 5.1849e1],
    [-3.2153e1, 5.2499, -6.2740, 2.6627, -3.6759e-1]]},
};

export function coolingRate(z, t) {
  const {borders, c} = MAVRIN[z];
  const tt = Math.min(Math.max(t, 0.1), 100), x = Math.log10(tt);
  let i = 0;
  while (i < c.length - 1 && tt >= borders[i + 1]) i++;
  return 10 ** c[i].reduce((sum, ck, k) => sum + ck * x ** k, 0);
}

// Ignition n_e T tau_E (keV s m^-3) of 50:50 D-T with one impurity (charge z, n_Z/n_e = c):
// quasineutral fuel n_e (1 - z c), W = 3/2 (n_e + n_i) T, alpha heating against
// transport, fuel bremsstrahlung (Z = 1) and, if lines, the impurity's coronal radiation,
// else its bremsstrahlung as a fully stripped ion. brems = false drops all radiation.
export function ignitionImpure(rx, t, z, c, {brems = true, lines = true} = {}) {
  const fuel = 1 - z * c, ions = fuel + c;
  if (fuel <= 0) return Infinity;
  let loss = 0;
  if (brems) {
    loss = C_B * fuel * Math.sqrt(t);
    loss += lines ? c * coolingRate(z, t) : C_B * z * z * c * Math.sqrt(t);
  }
  const net = fuel * fuel / 4 * reactivity(rx, "DT", t) * E_ALPHA * KEV - loss;
  return net > 0 ? 1.5 * (1 + ions) * t * t * KEV / net : Infinity;
}

// --- IPB98(y,2) ELMy H-mode thermal energy confinement time, eq. (20) of the ITER Physics Basis (1999)
export const IPB98 = {C: 0.0562, I: 0.93, B: 0.15, n: 0.41, P: -0.69, R: 1.97, eps: 0.58, kappa: 0.78, M: 0.19};

export function ipb98Factors(p) {
  const eps = p.a / p.R;
  return [
    {key: "I", value: p.I ** IPB98.I}, {key: "B", value: p.B ** IPB98.B},
    {key: "n", value: p.n19 ** IPB98.n}, {key: "P", value: p.P ** IPB98.P},
    {key: "R", value: p.R ** IPB98.R}, {key: "eps", value: eps ** IPB98.eps},
    {key: "kappa", value: p.kappa ** IPB98.kappa}, {key: "M", value: p.M ** IPB98.M},
  ];
}

export function tauIPB98(p) {
  return (p.H ?? 1) * IPB98.C * ipb98Factors(p).reduce((acc, f) => acc * f.value, 1);
}
