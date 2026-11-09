// Shared runtime of the slide widgets (slide-*.html, MIT): plain ES modules,
// no build step. Libraries come from jsDelivr, the only origin the Slopshell
// widget frame allows besides inlined data.
import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6.16/+esm";
import * as Inputs from "https://cdn.jsdelivr.net/npm/@observablehq/inputs@0.12.0/+esm";
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7.9.0/+esm";
import {html} from "https://cdn.jsdelivr.net/npm/htl@0.3.1/+esm";
import {INK} from "./plotting.js";

export {Plot, Inputs, d3, html};

export const font = {fontFamily: "'STIX Two Text', serif", fontSize: "16px", color: INK, background: "transparent"};

// Plot labels write x_E and x^2; render them as sub- and superscripts.
export function sub(svg) {
  for (const t of svg.querySelectorAll("text")) {
    if (!/[_^]/.test(t.textContent)) continue;
    t.innerHTML = t.textContent
      .replace(/_(\w+)/g, '<tspan baseline-shift="sub" font-size="72%">$1</tspan>')
      .replace(/\^(\S+)/g, '<tspan baseline-shift="super" font-size="72%">$1</tspan>');
  }
  return svg;
}

// Log-axis tick label: 1, 10, 10², 10⁻³ ...
export function pow(d) {
  const e = Math.round(Math.log10(d));
  return e === 0 ? "1" : e === 1 ? "10" : "10" + String(e).replace("-", "⁻").replace(/\d/g, (c) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[c]);
}

// Formatted value shown right of a range slider (its number box is hidden).
export function readout(input, text) {
  const div = input.querySelector("div");
  const out = div.querySelector("output") ?? div.appendChild(document.createElement("output"));
  out.textContent = text;
}

// Mount the inputs, then redraw the figure whenever one of them changes.
export function run(inputs, draw) {
  document.querySelector("#inputs").replaceChildren(...Object.values(inputs));
  const update = () => {
    const values = Object.fromEntries(Object.entries(inputs).map(([k, v]) => [k, v.value]));
    document.querySelector("#figure").replaceChildren(draw(values, inputs));
  };
  for (const input of Object.values(inputs)) input.addEventListener("input", update);
  update();
}

// Inside a deck (presenter or Slopshell) the page-turning keys always belong
// to the deck, also on a focused slider, radio, select or checkbox; only text
// fields keep every key and sliders and selects keep ArrowUp/ArrowDown, so the
// figure stays keyboard-usable without trapping the presenter.
addEventListener("keydown", (e) => {
  if (parent === window) return;
  const t = e.target;
  const text = t && t.matches && (t.isContentEditable || t.matches("textarea, " +
    "input:not([type=range], [type=checkbox], [type=radio], [type=button], " +
    "[type=submit], [type=reset], [type=color], [type=file], [type=image])"));
  if (text) return;
  const adjusts = t && t.matches && t.matches("input[type=range], select") &&
    /^Arrow(Up|Down)$/.test(e.key);
  if (adjusts) return;
  parent.postMessage({type: "slide-widget-key", key: e.key, shiftKey: e.shiftKey,
    altKey: e.altKey, ctrlKey: e.ctrlKey, metaKey: e.metaKey}, "*");
  if (/^(Arrow|Page)|^ $|^Home$|^End$/.test(e.key)) e.preventDefault();
}, true);
