"""Focused SymPy 1.14/python-flint reproducer and independent Decimal oracle.

Original environment: python3 derivations/tool-repairs/reproduce_sympy.py
Patched checkout: PYTHONPATH=/tmp/fusion-ch00-sympy-repair python3 ...
This diagnostic intentionally exercises exact simplification, not slide data.
"""
from decimal import Decimal
import sympy as sp
from sympy.external.gmpy import GROUND_TYPES

expression = 1000*sp.log(sp.Rational(34369,31250))
expected = float((Decimal(34369)/Decimal(31250)).ln()*1000)
print('SymPy',sp.__version__,'ground types',GROUND_TYPES)
actual = float(sp.simplify(expression).evalf())
assert abs(actual-expected)<1e-9
print('Exact simplification agrees with independent Decimal logarithm:',actual)
