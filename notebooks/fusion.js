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
