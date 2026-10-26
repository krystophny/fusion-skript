// Presentation helpers shared by the notebooks (MIT). Colours follow slides/theme.typ.
export const INK = "#17202A", MUTED = "#526175", GREY = "#9AA5B1";
export const BLUE = "#0072B2", ORANGE = "#B55000", GREEN = "#1B7F5B", PURPLE = "#7B3294", SKY = "#56B4E9";

export function logspace(a, b, n) {
  return Array.from({length: n}, (_, i) => a * (b / a) ** (i / (n - 1)));
}

const SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹";
export function sup(n) {
  return String(n).replace("-", "⁻").replace(/\d/g, d => SUP[d]);
}

// Powers of ten between a and b, for log-axis ticks.
export function decades(a, b, step = 1) {
  const out = [];
  for (let e = Math.ceil(Math.log10(a)); e <= Math.floor(Math.log10(b)); e += step) out.push(10 ** e);
  return out;
}

export function pow10(x) {
  const e = Math.round(Math.log10(x));
  return e === 0 ? "1" : e === 1 ? "10" : `10${sup(e)}`;
}

export const ticks125 = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000];

// HTML number in scientific notation, d significant digits.
export function sci(x, d = 3) {
  if (!Number.isFinite(x)) return "∞";
  const [m, e] = x.toExponential(d - 1).split("e");
  return +e === 0 ? m : `${m} × 10<sup>${+e}</sup>`;
}

export function ticksIn(a, b) {
  return ticks125.filter(t => t >= a * 0.999 && t <= b * 1.001);
}
