"""Head-on (l = 0) Coulomb reflection: radial wave packet and classical orbit.

Units: lengths in the turning radius r_c, energies in the mean packet energy
E (so V(r) = 1/r and V(r_c) = E), hbar = 1. The reduced mass then follows from
the Sommerfeld parameter eta = g m/(hbar^2 k): hbar^2/(2 m) = 1/(4 eta^2),
k = 2 eta/r_c and r_c = 2 eta lambdabar. The radial function u(r) = r R(r)
obeys i du/dt = -(1/(4 eta^2)) u'' + u/r with u(0) = 0 (and u(R) = 0 far
outside the plotted range). The finite-difference Hamiltonian is diagonalized
once, so the evolution is exact in the discrete space and unitary.
"""

import numpy as np

ETA = 2.0          # D-T at E = E_G/(4 pi^2 eta^2) = 7.5 keV
SIGMA = 2.0        # rms width of |u|^2 at t = 0, in r_c
R0 = 16.0          # initial packet centre, in r_c
R_MAX = 30.0       # outer wall, in r_c
N = 2000           # interior grid points

# D-T in the centre-of-mass frame (atomic masses in u): the head-on positions
# along the collision axis are x_D = -(m_T/M) r and x_T = +(m_D/M) r.
M_D = 2.01410178
M_T = 3.01604928
MU_C2_EV = M_D * M_T / (M_D + M_T) * 931.49410e6    # reduced mass, eV
ALPHA = 1 / 137.035999
HBAR_EV_S = 6.582119569e-16


def grid(n=N, r_max=R_MAX):
    dr = r_max / (n + 1)
    return np.arange(1, n + 1) * dr, dr


def hamiltonian(r, dr, eta=ETA):
    """Three-point Laplacian with u(0) = u(R) = 0 plus the Coulomb term."""
    c = 1.0 / (4 * eta**2 * dr**2)
    h = np.diag(2 * c + 1.0 / r) - c * (np.eye(len(r), k=1) + np.eye(len(r), k=-1))
    return h


def packet(r, dr, k0, sigma=SIGMA, r0=R0):
    """Incoming Gaussian (|u|^2 rms width sigma), unit norm."""
    u = np.exp(-((r - r0) ** 2) / (4 * sigma**2) - 1j * k0 * r)
    return u / np.sqrt(np.sum(np.abs(u) ** 2) * dr)


class RadialPacket:
    """Eigen-decomposed propagator and the packet with mean energy 1."""

    def __init__(self, eta=ETA, sigma=SIGMA, r0=R0, n=N, r_max=R_MAX):
        self.eta = eta
        self.r, self.dr = grid(n, r_max)
        self.levels, self.modes = np.linalg.eigh(hamiltonian(self.r, self.dr, eta))
        # Newton on k0 so that <H> = 1 (= E) in the discrete space;
        # d<H>/dk0 = k0/(2 eta^2) for a plane-wave factor.
        k = 2 * eta
        for _ in range(50):
            energy = self.energy(packet(self.r, self.dr, k, sigma, r0))
            if abs(energy - 1.0) < 1e-13:
                break
            k -= (energy - 1.0) / (k / (2 * eta**2))
        self.k0 = k
        self.u0 = packet(self.r, self.dr, k, sigma, r0)
        self.coeff = self.modes.T @ self.u0

    def energy(self, u):
        c = self.modes.T @ u
        return float(np.sum(self.levels * np.abs(c) ** 2) / np.sum(np.abs(c) ** 2))

    def at(self, t):
        return self.modes @ (np.exp(-1j * self.levels * t) * self.coeff)

    @property
    def mass(self):
        return 2 * self.eta**2      # hbar^2/(2 m) = 1/(4 eta^2)


def classical_orbit(t, r0=R0, eta=ETA, energy=1.0):
    """Head-on orbit r(t) at energy E in V = 1/r: incoming from r0 at t = 0.

    Uses the closed form t(r) measured from the turning point r_c = 1/E,
    t(r) = sqrt(m/(2E)) [sqrt(r (r - r_c)) + r_c ln((sqrt(r) + sqrt(r - r_c))/sqrt(r_c))].
    """
    m = 2 * eta**2
    rc = 1.0 / energy

    def from_turning(r):
        return np.sqrt(m / (2 * energy)) * (
            np.sqrt(r * (r - rc)) + rc * np.log((np.sqrt(r) + np.sqrt(r - rc)) / np.sqrt(rc)))

    t_turn = from_turning(r0)
    tau = np.abs(np.asarray(t, float) - t_turn)
    # Invert t(r) by bisection (monotone in r >= r_c).
    lo, hi = np.full_like(tau, rc), np.full_like(tau, rc + 50.0)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        below = from_turning(mid) < tau
        lo, hi = np.where(below, mid, lo), np.where(below, hi, mid)
    return 0.5 * (lo + hi), t_turn


def wkb_exponent(r, eta=ETA):
    """2 int_r^{r_c} kappa dr' with kappa = 2 eta sqrt(1/r' - 1) (r_c = 1, E = 1)."""
    r = np.asarray(r, float)
    # int_r^1 sqrt((1 - s)/s) ds = arccos(sqrt r) - sqrt(r (1 - r))
    return 2 * 2 * eta * (np.arccos(np.sqrt(r)) - np.sqrt(r * (1 - r)))


def energy_ev(eta=ETA):
    """E = E_G/(4 pi^2 eta^2) = m c^2 alpha^2/(2 eta^2) for D-T (Z_1 = Z_2 = 1)."""
    return MU_C2_EV * ALPHA**2 / (2 * eta**2)


def time_unit_s(eta=ETA):
    """The model time unit hbar/E in seconds."""
    return HBAR_EV_S / energy_ev(eta)


def cm_positions(r, m1=M_D, m2=M_T):
    """Head-on positions (x_1, x_2) with x_2 - x_1 = r and m1 x_1 + m2 x_2 = 0."""
    r = np.asarray(r, float)
    total = m1 + m2
    return -(m2 / total) * r, (m1 / total) * r


def marginal_densities(x, r, density, m1=M_D, m2=M_T):
    """Densities of x_1 and x_2 on the collision axis from the radial |u(r)|^2.

    With x_1 = -(m2/M) r the change of variables gives
    rho_1(x) = (M/m2) |u(-M x/m2)|^2 for x < 0 and zero for x > 0; likewise
    rho_2(x) = (M/m1) |u(M x/m1)|^2 for x > 0. Each integrates to the norm of u.
    Also returns the separations r_1(x), r_2(x) that each point stands for.
    """
    x = np.asarray(x, float)
    total = m1 + m2
    r1 = -total * x / m2
    r2 = total * x / m1
    rho1 = (total / m2) * np.interp(r1, r, density, left=0.0, right=0.0)
    rho2 = (total / m1) * np.interp(r2, r, density, left=0.0, right=0.0)
    return rho1, rho2, r1, r2
