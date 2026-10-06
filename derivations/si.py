"""SI dimensional checks shared by chapter derivations (MIT).

Same small interface as plasma-skript/derivations/si.py; no plot styling.
Person, currency and counts are bookkeeping dimensions, stated in metadata.
"""
import sympy as sp
from sympy.physics import units as u
from sympy.physics.units import convert_to

BASE = [u.kilogram, u.meter, u.second, u.ampere, u.kelvin]


def si_unit(expression, units):
    missing = expression.free_symbols - units.keys()
    if missing:
        raise KeyError(f'Units missing: {missing}')
    return sp.simplify(convert_to(sp.simplify(expression.subs(units)), BASE))


def same_unit(actual, expected):
    ratio = sp.simplify(convert_to(actual / expected, BASE))
    return not ratio.atoms(u.Quantity) and not ratio.free_symbols


def check(derived, stated, unit, units):
    assert sp.simplify(derived - stated) == 0
    assert same_unit(si_unit(derived, units), unit)
