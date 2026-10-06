"""Independent dimensional and integrated-consumption checks."""
import importlib.util
from pathlib import Path
import numpy as np
import pytest

spec = importlib.util.spec_from_file_location("energy", Path(__file__).parents[1]/"derivations/energy.py")
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)

def test_one_person_one_kilowatt_year():
    joules = 1000 * 365 * 24 * 3600
    assert model.daily_energy(joules/1e12, 1) == pytest.approx(24)
    assert model.area_per_person(24, 10) == pytest.approx(100)

def test_growth_exhausts_stock_by_independent_quadrature():
    end = model.lifetime(100, .02)
    times = np.linspace(0, end, 10001)
    consumed = np.trapezoid(np.exp(.02 * times), times)
    assert consumed == pytest.approx(100, rel=1e-8)
    assert end < 100
    assert model.lifetime(100, 0) == 100

def test_sector_balance_from_source_totals():
    assert sum(model.DATA["sectors_TJ"].values()) == pytest.approx(model.DATA["final_TJ"], abs=.001)
