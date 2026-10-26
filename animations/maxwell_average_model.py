"""Numerics for the Maxwell-average scenes (maxwell_average.py), numpy only.

D-T cross section from the Bosch-Hale (1992) S factor, Table IV: the same
coefficients as data/ch02/cross-sections.json (E <= 550 keV) and
data/ch02/reactivity.json (550-4700 keV). E is the centre-of-mass energy in keV.

    <sigma v>(T) = int sigma(E) v(E) f_M(E; T) dE,
    v(E) = c sqrt(2 E / m_r c^2),  f_M = (2/sqrt(pi)) T^(-3/2) sqrt(E) exp(-E/T).

On a logarithmic energy axis the integrand per d(ln E) is sigma v times the
kernel K(E/T) = E f_M = (2/sqrt(pi)) (E/T)^(3/2) exp(-E/T), whose shape depends
on E/T only: in E a T-dependent weight (a moment of sigma v), not a
translation-invariant convolution; in ln E a fixed kernel shifted by ln T.
"""
import numpy as np

C = 299792458.0                 # m/s
MRC2_DT = 1124656.0             # keV, Bosch-Hale Table VII
B_G = 34.3827                   # keV^(1/2)
LOW = ([6.927e4, 7.454e8, 2.050e6, 5.2002e4, 0.0], [6.38e1, -9.95e-1, 6.981e-5, 1.728e-4])
HIGH = ([-1.4714e6, 0.0, 0.0, 0.0, 0.0], [-8.4127e-3, 4.7983e-6, -1.0748e-9, 8.5184e-14])
KERNEL_MAX = 2 / np.sqrt(np.pi) * 1.5**1.5 * np.exp(-1.5)   # max of K at E = 1.5 T


def _pade(e, coeff):
    a, b = coeff
    num = a[0] + e * (a[1] + e * (a[2] + e * (a[3] + e * a[4])))
    return num / (1 + e * (b[0] + e * (b[1] + e * (b[2] + e * b[3]))))


def sigma(e):
    """D-T cross section in m^2 (S in keV mb -> 1e-31 m^2 keV)."""
    e = np.asarray(e, float)
    s = np.where(e <= 550, _pade(e, LOW), _pade(np.minimum(e, 4700), HIGH))
    return s / e * np.exp(-B_G / np.sqrt(e)) * 1e-31


def speed(e):
    return C * np.sqrt(2 * np.asarray(e, float) / MRC2_DT)


def sigma_v(e):
    return sigma(e) * speed(e)


def kernel(e, t):
    """K = E f_M(E; T), dimensionless weight per d(ln E)."""
    x = np.asarray(e, float) / t
    return 2 / np.sqrt(np.pi) * x**1.5 * np.exp(-x)


def average(t, n=6000):
    """<sigma v>(T) in m^3/s as int sigma v K d(ln E)."""
    ln_e = np.linspace(np.log(0.05), np.log(5000.0), n)
    e = np.exp(ln_e)
    return float(np.trapezoid(sigma_v(e) * kernel(e, t), ln_e))


def bosch_hale(t):
    """Bosch-Hale (1992) Table VII D-T reactivity in m^3/s, for comparison."""
    c1, c2, c3, c4, c5, c6, c7 = (1.17302e-9, 1.51361e-2, 7.51886e-2, 4.60643e-3, 1.35e-2,
                                  -1.0675e-4, 1.366e-5)
    theta = t / (1 - t * (c2 + t * (c4 + t * c6)) / (1 + t * (c3 + t * (c5 + t * c7))))
    xi = (B_G**2 / (4 * theta)) ** (1 / 3)
    return c1 * theta * np.sqrt(xi / (MRC2_DT * t**3)) * np.exp(-3 * xi) * 1e-6


# --- 1D relative-velocity convolution (RelativeVelocity scene) -----------------------
MC2_D, MC2_T = 1875612.945, 2808921.137    # keV, CODATA


def gauss(v, s):
    return np.exp(-0.5 * (v / s) ** 2) / (np.sqrt(2 * np.pi) * s)


def thermal_width(t, mc2):
    """1D Maxwellian standard deviation sqrt(k_B T/m) in units of 10^6 m/s."""
    return np.sqrt(t / mc2) * C / 1e6


def relative_density(g, v, s1, s2):
    """f_rel(g) = int f_1(v) f_2(v - g) dv by quadrature on the grid v."""
    return np.array([np.trapezoid(gauss(v, s1) * gauss(v - gg, s2), v) for gg in np.atleast_1d(g)])
