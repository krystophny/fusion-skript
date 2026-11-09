"""The notebook model (notebooks/fusion.js) against the Python derivations.

Node evaluates the browser module with the same JSON coefficient files that
ch02_reactivity.py reads; every number is compared with the Python function
of the same name. The IPB98(y,2) presets are checked against the confinement
times published with their parameters.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "derivations/chapters"))
import ch02_reactivity as rx  # noqa: E402
import ch04_power_balance as pb  # noqa: E402

NODE = shutil.which("node")
TEMPS = [1.0, 2.0, 5.0, 10.0, 13.5, 20.0, 50.0, 100.0]
ENERGIES = [1.0, 5.0, 20.0, 64.0, 200.0, 600.0, 1000.0, 2000.0]

SCRIPT = """
import {readFileSync} from "node:fs";
const m = await import(process.argv[2]);
const rx = JSON.parse(readFileSync(process.argv[3]));
const cs = JSON.parse(readFileSync(process.argv[4]));
const presets = JSON.parse(readFileSync(process.argv[5]));
const T = %s, E = %s;
const out = {const: {E_FUS: m.E_FUS, E_ALPHA: m.E_ALPHA, C_B: m.C_B, KEV: m.KEV}};
for (const name of ["DT", "DDn", "DDp", "DHe3"]) {
  out["bh_" + name] = T.map(t => m.boschHale(rx.bosch_hale_reactivity.reactions[name], t));
}
for (const name of ["DT", "DDn", "DDp", "DHe3"]) {
  out["sigma_" + name] = E.map(e => m.sigma(cs, rx, name, e));
  out["avg_" + name] = T.map(t => m.maxwellAverage(cs, rx, name, t));
}
out.gamow10 = m.gamowPeak(m.gamowEnergy(rx, "DT"), 10);
out.estimate10 = m.gamowEstimate(cs, rx, "DT", 10);
out.ign = T.map(t => m.tripleProduct(rx, t));
out.ignBrems = T.map(t => m.tripleProduct(rx, t, Infinity, 1));
out.q5 = T.map(t => m.tripleProduct(rx, t, 5));
out.zeff2 = T.map(t => m.tripleProduct(rx, t, 10, 2));
out.he5 = T.map(t => m.ignitionDiluted(rx, t, [[2, 0.05]]));
out.peak = T.map(t => m.peakTripleProduct(rx, t));
{
  // The Lawson widget: minima of n T tau_E and n tau_E over its grid, without and with bremsstrahlung.
  const grid = Array.from({length: 4001}, (_, i) => 2 * 50 ** (i / 4000));
  const arg = (f) => grid.reduce((a, t) => (f(t) < f(a) ? t : a));
  out.lawsonMin = [0, 1].map(z => [arg(t => m.tripleProduct(rx, t, Infinity, z)), arg(t => m.tripleProduct(rx, t, Infinity, z) / t)]);
}
out.peakQ1 = T.map(t => m.peakTripleProduct(rx, t, 1, {zeff: 3.4}));
out.peakFlat = T.map(t => m.peakTripleProduct(rx, t, 5, {zeff: 1, zbar: 1, etaAbs: 1, nuN: 0, nuT: 0}));
out.lam = m.profileFactors(rx, 20, 1, 1);
out.w = m.dilution([[74, 1e-3]]);
out.cool = Object.fromEntries([4, 6, 7, 8, 74].map(z => [z, T.map(t => m.coolingRate(z, t))]));
out.impure = [[4, 0.02, true, true], [6, 0.01, true, false], [74, 3e-5, true, true], [8, 0.005, false, true]]
  .map(([z, c, b, l]) => T.map(t => m.ignitionImpure(rx, t, z, c, {brems: b, lines: l})));
out.fa = [1, 5, 10].map(m.fAlpha);
out.qeng = [m.qEng(5.25, 0.4, 0.4), m.qEng(11.5, 0.4, 0.4)];
out.tau = Object.fromEntries(Object.entries(presets).map(([k, p]) => [k, m.tauIPB98(p)]));
console.log(JSON.stringify(out));
""" % (json.dumps(TEMPS), json.dumps(ENERGIES))


@pytest.fixture(scope="module")
def js(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available")
    script = tmp_path_factory.mktemp("js") / "eval.mjs"
    script.write_text(SCRIPT)
    args = [NODE, str(script), (ROOT / "notebooks/fusion.js").as_uri(),
            str(ROOT / "data/ch02/reactivity.json"), str(ROOT / "data/ch02/cross-sections.json"),
            str(ROOT / "notebooks/presets.json")]
    return json.loads(subprocess.run(args, capture_output=True, text=True, check=True).stdout)


def arr(values):
    return np.array([np.inf if v is None else v for v in values], float)


def test_constants_match_python(js):
    c = js["const"]
    assert c["E_FUS"] == pytest.approx(pb.E_FUS, rel=1e-9)
    assert c["E_ALPHA"] == pytest.approx(pb.E_ALPHA, rel=1e-9)
    assert c["C_B"] == pytest.approx(pb.C_B, rel=1e-12)
    assert c["KEV"] == rx.KEV


@pytest.mark.parametrize("name", ["DT", "DDn", "DDp", "DHe3"])
def test_bosch_hale_reactivity(js, name):
    assert np.allclose(js["bh_" + name], rx.bosch_hale(name, np.array(TEMPS)), rtol=1e-12)


def test_dt_reference_values(js):
    assert js["bh_DT"][TEMPS.index(10.0)] == pytest.approx(1.136e-22, rel=5e-4)
    g = js["gamow10"]
    assert round(g["e0"]) == 31 and round(g["width"]) == 41


@pytest.mark.parametrize("name", ["DT", "DDn", "DDp", "DHe3"])
def test_cross_sections(js, name):
    assert np.allclose(js["sigma_" + name], rx.sigma(name, np.array(ENERGIES), "bh"), rtol=1e-12)


@pytest.mark.parametrize("name,tol", [("DT", 0.01), ("DDn", 0.025), ("DDp", 0.025), ("DHe3", 0.035)])
def test_quadrature_matches_parametrisation(js, name, tol):
    # Same tolerances as ch02_reactivity.checks() for the Bosch-Hale S(E) quadrature.
    ratio = np.array(js["avg_" + name]) / rx.bosch_hale(name, np.array(TEMPS))
    assert np.all(np.abs(ratio - 1) < tol), ratio


def test_saddle_point_estimate_close_to_quadrature(js):
    assert js["estimate10"] == pytest.approx(rx.bosch_hale("DT", 10.0), rel=0.1)


def test_power_balance(js):
    t = np.array(TEMPS)
    assert np.allclose(arr(js["ign"]), pb.triple_product(t), rtol=1e-12)
    assert np.allclose(arr(js["ignBrems"]), pb.triple_product(t, brems=True), rtol=1e-12)
    assert np.allclose(arr(js["q5"]), pb.triple_product(t, 5.0), rtol=1e-12)
    assert np.allclose(arr(js["he5"]), pb.ignition_diluted(t, [(2, 0.05)]), rtol=1e-12)
    # Z_eff only scales the bremsstrahlung term: independent restatement of the balance.
    sv = rx.bosch_hale("DT", t)
    net = sv * (pb.E_ALPHA + pb.E_FUS / 10) * rx.KEV - 8 * pb.C_B * np.sqrt(t)
    ref = np.where(net > 0, 12 * t**2 * rx.KEV / np.where(net > 0, net, 1), np.inf)
    assert np.allclose(arr(js["zeff2"]), ref, rtol=1e-12)


def test_peak_triple_product(js):
    t = np.array(TEMPS)
    finite = lambda v: np.array([np.inf if x is None else x for x in v], float)
    assert np.allclose(finite(js["peak"]), [pb.peak_triple_product(x) for x in t], rtol=1e-12)
    assert np.allclose(finite(js["peakQ1"]), [pb.peak_triple_product(x, 1.0, z_eff=3.4) for x in t],
                       rtol=1e-12)
    # Flat profiles, pure fuel, full absorption: Wurzel & Hsu Eq. (45) is the 0-D balance.
    assert np.allclose(finite(js["peakFlat"]), pb.triple_product(t, 5.0, brems=True), rtol=1e-12)
    # Parabolic profiles: closed forms of Eqs. (39)-(40).
    assert js["lam"]["kappa"] == pytest.approx(1 / 3) and js["lam"]["B"] == pytest.approx(2 / 7)


def test_lawson_widget_minima(js):
    """Fixed pressure: lowest n T tau_E at 13.5 keV; fixed density: lowest n tau_E at 25.7 keV."""
    (ntt, nt), (ntt_br, nt_br) = js["lawsonMin"]
    assert ntt == pytest.approx(13.5, abs=0.1) and nt == pytest.approx(25.7, abs=0.1)
    assert ntt_br == pytest.approx(14.2, abs=0.1) and nt_br == pytest.approx(26.0, abs=0.1)


def test_peak_values_put_record_shots_below_breakeven():
    """Peak-value records against flat-profile curves overstate the gain (Wurzel & Hsu 2022)."""
    jet_1991 = (18.6, 4.1e19 * 0.8 * 18.6)   # shot 26087: T_i0 [keV], n_i0 T_i0 tau_E* [keV s m^-3]
    assert jet_1991[1] > pb.triple_product(jet_1991[0], 1.0)
    assert jet_1991[1] < pb.peak_triple_product(jet_1991[0], 1.0)


def test_dilution_and_gain(js):
    fuel, ions, zeff = pb.dilution([(74, 1e-3)])
    assert js["w"]["fuel"] == pytest.approx(fuel) and js["w"]["zeff"] == pytest.approx(zeff)
    assert js["w"]["ions"] == pytest.approx(ions)
    assert js["fa"] == pytest.approx([1 / (1 + pb.E_FUS / pb.E_ALPHA), 5 / (5 + pb.E_FUS / pb.E_ALPHA),
                                      10 / (10 + pb.E_FUS / pb.E_ALPHA)])
    assert js["qeng"] == pytest.approx([0.0, 1.0], abs=1e-12)


def test_ipb98_presets_reproduce_published_times(js):
    presets = json.loads((ROOT / "notebooks/presets.json").read_text())
    for name, p in presets.items():
        if "tau_published_s" in p:
            assert js["tau"][name] == pytest.approx(p["tau_published_s"], rel=0.02), name


def test_impurity_radiation_matches_python(js):
    for z in (4, 6, 7, 8, 74):
        assert js["cool"][str(z)] == pytest.approx(list(pb.cooling_rate(z, TEMPS)), rel=1e-9)
    cases = [(4, 0.02, True, True), (6, 0.01, True, False), (74, 3e-5, True, True), (8, 0.005, False, True)]
    for got, (z, c, b, l) in zip(js["impure"], cases):
        want = pb.ignition_impure(np.array(TEMPS), z, c, brems=b, lines=l)
        assert [g if g is not None else np.inf for g in got] == pytest.approx(list(want), rel=1e-9)


def test_cooling_rates_approach_bremsstrahlung_of_stripped_light_ions():
    """At 20-50 keV Be, C, N and O are fully stripped: their coronal rate is nearly pure bremsstrahlung."""
    for z in (4, 6, 7, 8):
        for t in (20.0, 50.0):
            assert pb.cooling_rate(z, t) == pytest.approx(pb.C_B * z * z * np.sqrt(t), rel=0.3)
    # Tungsten keeps bound electrons: lines exceed its bremsstrahlung tenfold.
    assert pb.cooling_rate(74, 10.0) > 10 * pb.C_B * 74**2 * np.sqrt(10.0)


def test_no_impurity_reduces_to_pure_fuel():
    t = np.array(TEMPS)
    assert pb.ignition_impure(t, 74, 0.0, brems=False) == pytest.approx(pb.triple_product(t))
    assert pb.ignition_impure(t, 4, 0.0) == pytest.approx(pb.triple_product(t, brems=True))
