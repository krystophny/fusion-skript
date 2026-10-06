# SymPy exact-log overflow repair

The system environment (SymPy 1.14.0 with python-flint) raises `OverflowError:
int too large to convert to float` for
`simplify(1000*log(Rational(34369,31250)))`. Exact growing-stock calculations
exposed it when simplification combined logarithms into large integer powers.
`_perfect_power` passed backend integers directly to `math.log`/`math.log2`;
their `__float__` conversion overflows, whereas Python's native integer path in
`math.log2` handles large integers.

The owning upstream checkout is `/tmp/fusion-ch00-sympy-repair`, frozen at
SymPy tag `sympy-1.14.0`, base commit
`16fa855354eb7bcabd3fe10993841e03b1382692`. The retained patch converts the
four logarithm arguments in `_perfect_power` to native Python integers and
adds a focused regression with an independent Decimal logarithm oracle.
`sympy-perfect-power.patch` reproduces the change; no commit or push was made.
The system installation was not edited.

Frozen patch SHA-256:
`6dc59e4b579fa0ab3813f654a0dbaa7703fdb34cc4690d09a8579bb93bc2fa1f`.

The focused upstream gate passed: **3 tests**, with python-flint active. Run:

```sh
PYTHONPATH=/tmp/fusion-ch00-sympy-repair uv run --no-project --python 3.14 \
  --with pytest --with hypothesis --with python-flint --with mpmath \
  python -m pytest -q \
  /tmp/fusion-ch00-sympy-repair/sympy/ntheory/tests/test_factor_.py \
  -k perfect_power
```

`reproduce_sympy.py` reproduces the defect on the original backend and verifies
the repair against Decimal in the patched checkout. The actual chapter
builder and original consumer tests were rechecked and pass. Numeric exports
evaluate SymPy quantities numerically; exact governing formulas remain exact.

A full optional run that aggressively simplifies every exact resource-curve
point also reaches Python's default 4300-digit integer-printing guard, and
with that guard temporarily disabled it **passed all 217 evaluations**, although
the run was slow. That is a separate
non-blocking symbolic-performance limitation; the numerical builder does not
need huge integer-power rewrites. Next action: review/submit the focused
upstream patch when requested; separately investigate large-log simplification
and integer printing at SymPy if that exact route is needed. No permanent
consumer monkeypatch or vendored SymPy replacement was introduced.
