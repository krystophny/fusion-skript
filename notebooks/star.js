// Star widgets (slide-star, slide-sun; MIT): MIST v1.2 centre of a star against time.
import {Plot, Inputs, html, font, sub, pow, readout, run} from "./widget.js";
import {INK, MUTED, GREY} from "./plotting.js";
import mist from "./data/mist.json" with {type: "json"};
import stages from "./data/stages.json" with {type: "json"};

// MIST v1.2 tracks (Dotter 2016; Choi et al. 2016): centre of the star against time.
const COL = Object.fromEntries(mist.columns.map((c, i) => [c, i]));
const MASSES = mist.sets[0].tracks.map((t) => t.mass);
const SETS = mist.sets.map((s) => `Z = ${s.Z < 0.001 ? s.Z.toFixed(5) : s.Z.toFixed(3)}${s.feh === 0 ? " (Sun)" : ""}`);
const SPECIES = [
  ["H", "center_h1", "#56B4E9"], ["He", "center_he4", "#E69F00"], ["C", "center_c12", "#4D4D4D"],
  ["N", "center_n14", "#CC79A7"], ["O", "center_o16", "#0072B2"], ["Ne", "center_ne20", "#1B7F5B"],
  ["Mg", "center_mg24", "#B55000"], ["Si", "center_si28", "#C9B200"], ["other", "other", "#D9DDE2"]];
const CHANNELS = [["pp chain", "pp", "#B55000"], ["CNO cycle", "cno", "#1B7F5B"],
  ["triple alpha", "tri_alfa", "#0072B2"], ["carbon burning", "burn_c", "#4D4D4D"]];
const KB = 1.380649e-23, KEV = 1.602176634e-16, ME = 9.1093837e-31, HBAR = 1.054571817e-34, MU = 1.66053907e-27;
const YR = 3.15576e7;

function track(si, mi) {
  const t = mist.sets[si].tracks[mi];
  return t.star_age.map((age, i) => {
    const row = {i, age, left: t.log_t_left[i], phase: t.phase[i], mass: t.star_mass[i],
      logT: t.log_center_T[i], logRho: t.log_center_Rho[i] + 3, L: t.log_L[i]};
    let sum = 0;
    for (const [, c] of SPECIES.slice(0, -1)) sum += (row[c] = Math.max(t[c][i], 0));
    row.other = Math.max(1 - sum, 0);
    for (const [, c] of CHANNELS) row[c] = t[c][i];
    return row;
  });
}

function stage(r) {
  if (r.center_h1 > 1e-3) return "core hydrogen burning";
  const lH = Math.log10(10 ** r.pp + 10 ** r.cno), best = Math.max(lH, r.tri_alfa, r.burn_c);
  if (r.phase === 6) return r.L < 1 ? "white dwarf, cooling" : "envelope lost, hot core contracting";
  if (r.center_he4 > 1e-3) return best === r.tri_alfa && r.tri_alfa > -2 ? "core helium burning" : "hydrogen shell burning around an inert He core";
  if (r.center_c12 > 1e-3 && r.burn_c > r.tri_alfa && r.burn_c > 0) return "core carbon burning";
  return "shell burning around an inert core";
}

function ending(rows, m) {
  const last = rows[rows.length - 1];
  if (last.phase === 6) {
    const kind = last.center_he4 > 0.5 ? "helium" : last.center_ne20 > 0.2 ? "oxygen–neon" : "carbon–oxygen";
    return `${kind} white dwarf of ${last.mass.toFixed(2)} M☉`;
  }
  if (last.center_h1 > 1e-3) return `still burning hydrogen after ${(last.age / 1e9).toFixed(0)} Gyr (the universe is 13.8 Gyr old)`;
  if (last.center_c12 < 0.05 && last.center_he4 < 1e-3 && m >= 8)
    return "C exhausted; Ne, O, Si burn within about 2 years, the Fe core collapses: supernova, neutron star or black hole";
  return `track ends (${stage(last)}); MIST stops here`;
}

// Milestones of the Sun's life on its own track.
function milestones(rows) {
  const at = (i, name) => i >= 0 ? [{left: rows[i].left, name}] : [];
  let today = 0;
  rows.forEach((r, i) => { if (Math.abs(r.age - 4.57e9) < Math.abs(rows[today].age - 4.57e9)) today = i; });
  return [...at(today, "today"), ...at(rows.findIndex((r) => r.center_h1 < 1e-3), "core H gone"),
    ...at(rows.findIndex((r) => r.phase === 3), "He flash"), ...at(rows.findIndex((r) => r.phase >= 4), "AGB")];
}

const fmtAge = (y) => y >= 1e9 ? `${(y / 1e9).toFixed(2)} Gyr` : y >= 1e6 ? `${(y / 1e6).toFixed(2)} Myr` : y >= 1e3 ? `${(y / 1e3).toFixed(1)} kyr` : `${y.toFixed(1)} yr`;
const fmtLeft = (l) => fmtAge(10 ** l);

function draw({mass, set, time}, inputs, sun) {
  const si = SETS.indexOf(set), m = MASSES[mass];
  if (inputs.mass) readout(inputs.mass, `${m} M☉`);
  const all = track(si, mass);
  // Plot until burning ends: white-dwarf cooling (MIST phase 6) would dominate a log time axis.
  const cut = all.findIndex((r) => r.phase === 6);
  const rows = cut > 0 ? all.slice(0, cut + 1) : all;
  const k = Math.min(rows.length - 1, Math.round(time * (rows.length - 1)));
  const now = rows[k];
  readout(inputs.time, fmtAge(now.age));
  const xmax = Math.ceil(rows[0].left * 10) / 10, xmin = Math.floor(Math.min(...rows.map((r) => r.left)));
  const x = {type: "linear", domain: [xmax, xmin], label: null, ticks: [], axis: null};
  const comp = SPECIES.flatMap(([el, c, col]) => rows.map((r) => ({left: r.left, el, f: r[c]})));
  const top = Plot.plot({
    width: 600, height: 200, marginLeft: 66, marginRight: 20, marginTop: 8, marginBottom: 6, style: font, x,
    y: {domain: [0, 1], label: "core mass fraction", labelAnchor: "center", labelArrow: "none", labelOffset: 52, ticks: [0, 0.5, 1]},
    color: {domain: SPECIES.map((s) => s[0]), range: SPECIES.map((s) => s[2])},
    marks: [
      Plot.areaY(comp, {x: "left", y: "f", fill: "el", stroke: "el", strokeWidth: 0.6, order: SPECIES.map((s) => s[0])}),
      Plot.ruleX([now.left], {stroke: INK, strokeWidth: 2}),
      Plot.frame({stroke: GREY}),
    ],
  });
  const lum = CHANNELS.flatMap(([name, c]) => rows.map((r) => ({left: r.left, name, L: r[c]})));
  const bottom = sub(Plot.plot({
    width: 600, height: 205, marginLeft: 66, marginRight: 20, marginTop: 6, marginBottom: 44, style: font,
    x: {...x, axis: "bottom", ticks: [...Array(Math.floor(xmax) - xmin + 1).keys()].map((e) => Math.floor(xmax) - e),
      tickFormat: (e) => pow(10 ** e), label: "time until the end of nuclear burning [yr]", labelAnchor: "center", labelArrow: "none", labelOffset: 36},
    y: {domain: [-4, 7], label: "luminosity [L☉]", labelAnchor: "center", labelOffset: 52, labelArrow: "none", ticks: [-4, -2, 0, 2, 4, 6], tickFormat: (e) => pow(10 ** e)},
    color: {domain: CHANNELS.map((c) => c[0]), range: CHANNELS.map((c) => c[2])},
    marks: [
      Plot.line(rows, {x: "left", y: "L", stroke: GREY, strokeWidth: 1.5, strokeDasharray: "4,3"}),
      Plot.line(lum, {x: "left", y: "L", stroke: "name", strokeWidth: 2.2, clip: true}),
      Plot.ruleX([now.left], {stroke: INK, strokeWidth: 2}),
      sun ? Plot.ruleX(milestones(rows), {x: "left", stroke: MUTED, strokeDasharray: "2,3"}) : null,
      sun ? Plot.text(milestones(rows), {x: "left", y: 6.6, text: "name", rotate: -90, textAnchor: "end", dx: -5, fill: MUTED, fontSize: 12}) : null,
      Plot.frame({stroke: GREY}),
    ],
  }));
  // Centre in the rho-T plane; electron degeneracy (E_F = k_B T, mu_e = 2) for orientation.
  const deg = [6.5, 7, 7.5, 8, 8.5, 9, 9.5].map((lt) => ({lt, lr: Math.log10((2 * ME * KB * 10 ** lt) ** 1.5 / (3 * Math.PI ** 2 * HBAR ** 3) * 2 * MU)}));
  const rt = sub(Plot.plot({
    width: 340, height: 250, marginLeft: 58, marginRight: 10, marginTop: 10, marginBottom: 44, style: font,
    x: {domain: [2, 11], label: "ρ_c [kg m^−3]", labelAnchor: "center", labelArrow: "none", labelOffset: 36, ticks: [2, 4, 6, 8, 10], tickFormat: (e) => pow(10 ** e)},
    y: {domain: [6.4, 9.2], label: "T_c [K]", labelAnchor: "center", labelOffset: 46, labelArrow: "none", ticks: [7, 8, 9], tickFormat: (e) => pow(10 ** e)},
    marks: [
      Plot.line(deg, {x: "lr", y: "lt", stroke: GREY, strokeDasharray: "4,3"}),
      Plot.text([{x: 9.3, y: 6.75}], {x: "x", y: "y", text: () => "degenerate", fill: MUTED, fontSize: 13}),
      Plot.line(rows, {x: "logRho", y: "logT", stroke: INK, strokeWidth: 1.6}),
      Plot.dot([now], {x: "logRho", y: "logT", r: 6, fill: "white", stroke: INK, strokeWidth: 2.5}),
      Plot.frame({stroke: GREY}),
    ],
  }));
  const tc = 10 ** now.logT, rhoc = 10 ** now.logRho;
  const legend = (list) => html`<div style="display:flex;flex-wrap:wrap;gap:0 0.7rem;font-size:0.78rem">${list.map(([n, , c]) =>
    html`<span><span style="display:inline-block;width:0.8rem;height:0.8rem;background:${c};vertical-align:-0.1rem"></span> ${n}</span>`)}</div>`;
  const late = m >= 8 && all[all.length - 1].center_c12 < 0.05 && all[all.length - 1].center_he4 < 1e-3;
  return html`<div style="display:flex;gap:12px">
<div style="width:600px">${top}${bottom}</div>
<div style="width:350px;font-size:0.82rem;line-height:1.35;color:${INK}">
  ${rt}
  <div><b>${stage(now)}</b> · M = ${now.mass.toFixed(2)} M☉</div>
  <div><i>T</i><sub>c</sub> = ${(tc / 1e6).toFixed(tc < 1e8 ? 1 : 0)} MK = ${(KB * tc / KEV).toFixed(2)} keV, <i>ρ</i><sub>c</sub> = ${rhoc.toExponential(1).split("e+")[0]} × 10<sup>${rhoc.toExponential(1).split("e+")[1]}</sup> kg m<sup>−3</sup></div>
  ${sun ? html`<div>CNO share of hydrogen burning: ${(100 * 10 ** now.cno / (10 ** now.pp + 10 ** now.cno)).toFixed(1)} %</div>` : ""}
  <div style="color:${MUTED}">end: ${ending(all, m)}</div>
  ${late ? html`<div style="color:${MUTED};font-size:0.72rem">then (20 M☉ model): ${stages.stages.slice(3).map((s) => `${s.fuel} ${s.duration_yr < 0.1 ? (s.duration_yr * 365).toFixed(0) + " d" : s.duration_yr.toFixed(1) + " yr"}`).join(", ")}</div>` : ""}
  <div style="margin-top:0.3rem">${legend(SPECIES.slice(0, -1))}</div>
  <div style="margin-top:0.2rem">${legend(CHANNELS)}</div>
  <div style="color:${MUTED};font-size:0.66rem;margin-top:0.2rem">MIST v1.2 (MESA) tracks · Dotter 2016, Choi et al. 2016</div>
</div></div>`;
}

// opts.sun: 1 M☉ at solar metals only, starting at the present age of the Sun.
export function starWidget(opts = {}) {
  const sun = !!opts.sun;
  const presentSun = () => {
    const rows = track(2, MASSES.indexOf(1)), cut = rows.findIndex((r) => r.phase === 6);
    const n = cut > 0 ? cut + 1 : rows.length;
    let k = 0;
    for (let i = 0; i < n; i++) if (Math.abs(rows[i].age - 4.57e9) < Math.abs(rows[k].age - 4.57e9)) i && (k = i);
    return k / (n - 1);
  };
  const inputs = sun ? {
    time: Inputs.range([0, 1], {value: presentSun(), step: 0.001, label: "age"}),
    play: Inputs.toggle({label: "run", value: false}),
  } : {
    mass: Inputs.range([0, MASSES.length - 1], {value: MASSES.indexOf(15), step: 1, label: html`initial mass`}),
    set: Inputs.radio(SETS, {value: SETS[2], label: "metals"}),
    time: Inputs.range([0, 1], {value: 0.97, step: 0.001, label: "age"}),
    play: Inputs.toggle({label: "run", value: false}),
  };
  run(inputs, (v, inp) => draw(sun ? {...v, mass: MASSES.indexOf(1), set: SETS[2]} : v, inp, sun));
  // "run" advances the age slider along the track (equal time per phase) and stops at the end.
  let last = 0;
  function tick(ts) {
    if (inputs.play.value && ts - last > 60) {
      last = ts;
      inputs.time.value = inputs.time.value >= 1 ? 0 : Math.min(1, inputs.time.value + 0.004);
      inputs.time.dispatchEvent(new Event("input", {bubbles: true}));
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
