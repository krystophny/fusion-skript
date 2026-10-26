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
out.w = m.dilution([[74, 1e-3]]);
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
