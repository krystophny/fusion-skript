"""Deck figures for Chapter 5: three-dimensional sketches of the confinement devices.

Pinches and mirror are schematic. Tokamak: ITER PF and CS coil positions and sizes
from data/ch05/iter-coils.json, TF coils and plasma as D shapes of ITER size.
Stellarator: NCSX modular coils and VMEC boundary from data/ch05/ncsx.json.
Provenance in data/ch05/README.md.
Run:  python3 slides/figures_devices.py
      -> slides/build/fig/{theta_pinch,z_pinch,screw_pinch,mirror_3d,zeta_3d,torus_tf_3d,tokamak_3d,stellarator_3d}.{svg,png}

Rendering: every surface, coil, field line and arrow becomes shaded quadrilaterals,
which are depth-sorted together (painter's algorithm) and drawn in an orthographic view.
"""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import to_rgb

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figures import BLUE, GREEN, GREY, INK, MM, MUTED, ORANGE, ROOT, save, style  # noqa: E402

DATA = ROOT / "data/ch05"
COPPER = "#B87333"
STEEL = "#8C96A0"
GLASS = "#9AA5B1"
LABEL = 18


# ------------------------------------------------------------------ geometry

def unit(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def grid_quads(p):
    """(n, m, 3) grid of points -> ((n-1)(m-1), 4, 3) quadrilaterals."""
    return np.stack([p[:-1, :-1], p[1:, :-1], p[1:, 1:], p[:-1, 1:]], axis=2).reshape(-1, 4, 3)


def frames(path, closed=False):
    """Parallel-transport normals along a curve."""
    t = np.gradient(path, axis=0)
    if closed:
        t[0] = t[-1] = path[1] - path[-2]
    t = unit(t)
    a = np.array([0.0, 0.0, 1.0]) if abs(t[0, 2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    n = np.empty_like(path)
    n[0] = unit(a - (a @ t[0]) * t[0])
    for i in range(1, len(path)):
        v = n[i - 1] - (n[i - 1] @ t[i]) * t[i]
        n[i] = v / np.linalg.norm(v)
    return t, n, np.cross(t, n)


def tube(path, r, sides=12, closed=False):
    t, n, b = frames(path, closed)
    a = np.linspace(0, 2 * np.pi, sides + 1)
    p = path[:, None] + r * (np.cos(a)[None, :, None] * n[:, None] + np.sin(a)[None, :, None] * b[:, None])
    return grid_quads(p)


def sweep_rect(path, u, v, du, dv):
    """Rectangular cross-section du x dv along a path with frame vectors u, v (n, 3)."""
    c = np.array([(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]) * 0.5
    p = path[:, None] + du * c[None, :, 0, None] * u[:, None] + dv * c[None, :, 1, None] * v[:, None]
    return grid_quads(p)


def cone(base, direction, length, radius, sides=16):
    d = unit(np.asarray(direction, float))
    a = np.array([0.0, 0.0, 1.0]) if abs(d[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    n = unit(a - (a @ d) * d)
    b = np.cross(d, n)
    th = np.linspace(0, 2 * np.pi, sides + 1)
    ring = base + radius * (np.cos(th)[:, None] * n + np.sin(th)[:, None] * b)
    apex = base + length * d
    side = np.stack([ring[:-1], ring[1:], np.broadcast_to(apex, ring[1:].shape),
                     np.broadcast_to(apex, ring[1:].shape)], axis=1)
    cap = np.stack([ring[:-1], ring[1:], np.broadcast_to(base, ring[1:].shape),
                    np.broadcast_to(base, ring[1:].shape)], axis=1)
    return np.concatenate([side, cap])


def path_arrow(path, r, head_len, head_r):
    """Tube along a path that ends in a cone, tip at the last point."""
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))])
    keep = s <= s[-1] - head_len
    shaft = path[keep]
    d = path[-1] - shaft[-1]
    return np.concatenate([tube(shaft, r, sides=10), cone(shaft[-1], d, np.linalg.norm(d), head_r)])


def straight_arrow(p0, p1, r, head_len, head_r):
    return path_arrow(np.linspace(p0, p1, 12), r, head_len, head_r)


def revolve_x(profile, a0=0.0, a1=2 * np.pi, n=96):
    """Surface of revolution about the x axis from an (x, r) profile."""
    a = np.linspace(a0, a1, n)
    x, r = np.asarray(profile, float).T
    p = np.stack([np.broadcast_to(x, (n, len(x))), r[None] * np.cos(a)[:, None], r[None] * np.sin(a)[:, None]], -1)
    return grid_quads(p)


def revolve_z(profile, a0=0.0, a1=2 * np.pi, n=160):
    """Surface of revolution about the z axis from an (R, Z) profile."""
    a = np.linspace(a0, a1, n)
    rr, z = np.asarray(profile, float).T
    p = np.stack([rr[None] * np.cos(a)[:, None], rr[None] * np.sin(a)[:, None], np.broadcast_to(z, (n, len(z)))], -1)
    return grid_quads(p)


def rect_profile(r, z, dr, dz):
    return [(r - dr / 2, z - dz / 2), (r + dr / 2, z - dz / 2), (r + dr / 2, z + dz / 2),
            (r - dr / 2, z + dz / 2), (r - dr / 2, z - dz / 2)]


def ring_z(r, z, dr, dz, a0=0.0, a1=2 * np.pi, n=160):
    """Coil of rectangular cross-section about the z axis, with end caps if cut."""
    q = [revolve_z(rect_profile(r, z, dr, dz), a0, a1, n)]
    if a1 - a0 < 2 * np.pi - 1e-9:
        for a in (a0, a1):
            c = np.array(rect_profile(r, z, dr, dz)[:4])
            q.append(np.stack([c[:, 0] * np.cos(a), c[:, 0] * np.sin(a), c[:, 1]], -1)[None])
    return np.concatenate(q)


def ring_x(x, r, dx, dr, n=96):
    return revolve_x([(xx, rr) for rr, xx in rect_profile(r, x, dr, dx)], n=n)


# ------------------------------------------------------------------ rendering

class Scene:
    def __init__(self, elev, azim, axis_up=False):
        # axis_up maps the device axis x onto the vertical z (cyclic permutation, a rotation)
        self.rot = np.array([[0.0, 1, 0], [0, 0, 1], [1, 0, 0]]) if axis_up else np.eye(3)
        e, a = np.radians(elev), np.radians(azim)
        self.c = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
        self.e1 = np.array([-np.sin(a), np.cos(a), 0.0])
        self.e2 = np.cross(self.c, self.e1)
        self.light = unit(self.c + 0.7 * self.e2 - 0.4 * self.e1)
        self.quads, self.rgba, self.edge = [], [], []

    def add(self, quads, color, alpha=1.0, ambient=0.45, spec=0.25):
        quads = np.asarray(quads, float) @ self.rot.T
        n = np.cross(quads[:, 2] - quads[:, 0], quads[:, 3] - quads[:, 1])
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        lam = np.abs(n @ self.light)
        h = unit(self.light + self.c)
        shade = ambient + (1 - ambient) * lam
        rgb = np.clip(np.array(to_rgb(color))[None] * shade[:, None] + spec * np.abs(n @ h)[:, None] ** 30, 0, 1)
        self.quads.append(quads)
        self.rgba.append(np.column_stack([rgb, np.full(len(quads), alpha)]))
        self.edge.append(np.full(len(quads), alpha >= 1))

    def proj(self, p):
        return np.stack([p @ self.e1, p @ self.e2], -1)

    def screen(self, p):
        return self.proj(np.asarray(p, float) @ self.rot.T)

    def figure(self, width_mm, height_mm, pad=(0.02, 0.02, 0.02, 0.02)):
        q = np.concatenate(self.quads)
        rgba = np.concatenate(self.rgba)
        edge = np.concatenate(self.edge)
        order = np.argsort(q.mean(axis=1) @ self.c)
        xy = self.proj(q)[order]
        rgba, edge = rgba[order], edge[order]
        fig = plt.figure(figsize=(width_mm * MM, height_mm * MM), dpi=250)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        # Antialiased translucent faces share edge pixels by coverage, so they leave no seams;
        # opaque faces get a hairline edge of their own colour to close the antialiasing gaps.
        ec = rgba.copy()
        ec[~edge, 3] = 0
        ax.add_collection(PolyCollection(xy, facecolors=rgba, edgecolors=ec, linewidths=np.where(edge, 0.3, 0),
                                         antialiased=True, rasterized=True))
        lo, hi = xy.reshape(-1, 2).min(0), xy.reshape(-1, 2).max(0)
        span = hi - lo
        left, right, bottom, top = pad
        x0, x1 = lo[0] - left * span[0], hi[0] + right * span[0]
        y0, y1 = lo[1] - bottom * span[1], hi[1] + top * span[1]
        k = (width_mm / height_mm) / ((x1 - x0) / (y1 - y0))
        if k > 1:
            mid, w = (x0 + x1) / 2, (x1 - x0) * k
            x0, x1 = mid - w / 2, mid + w / 2
        else:
            mid, h = (y0 + y1) / 2, (y1 - y0) / k
            y0, y1 = mid - h / 2, mid + h / 2
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        return fig, ax

    def label(self, ax, text, at, dx=0, dy=0, color=INK, size=LABEL, leader=False, **kw):
        xy = self.screen(at)
        props = dict(arrowstyle="-", lw=0.8, color=MUTED, shrinkA=2, shrinkB=2) if leader else None
        ax.annotate(text, xy=xy, xytext=(dx, dy), textcoords="offset points", fontsize=size, color=color,
                    ha=kw.pop("ha", "center"), va=kw.pop("va", "center"), arrowprops=props, **kw)


def azimuthal_arrow_x(x, r, a0, a1, sign=1, rad=0.035, head=0.16, head_r=0.075):
    """Arrow along a circle about the x axis, right-handed about +x for sign > 0."""
    a = np.linspace(a0, a1, 40) if sign > 0 else np.linspace(a1, a0, 40)
    return path_arrow(np.stack([np.full_like(a, x), r * np.cos(a), r * np.sin(a)], -1), rad, head, head_r)


# ------------------------------------------------------------------ linear devices

def tube_and_electrodes(s, half, r_tube, r_el, with_electrodes=True):
    s.add(revolve_x([(-half, r_tube), (half, r_tube)]), GLASS, alpha=0.10, ambient=0.8, spec=0)
    if with_electrodes:
        for x0 in (-half, half):
            sgn = np.sign(x0)
            prof = [(x0 + sgn * 0.6, 0.0), (x0 + sgn * 0.6, 0.12), (x0 + sgn * 0.15, 0.12), (x0 + sgn * 0.15, r_el),
                    (x0, r_el), (x0, 0.0)]
            s.add(revolve_x(prof), STEEL)


def column(half, a, taper=0.25):
    x = np.linspace(-half, half, 60)
    r = a * np.clip((half - np.abs(x)) / taper, 0, 1) ** 0.35
    return revolve_x(np.column_stack([x, r]))


def z_pinch():
    s = Scene(elev=22, azim=-40)
    half, a = 2.0, 0.32
    tube_and_electrodes(s, half, 0.85, 0.7)
    s.add(column(half, a, 0.05), ORANGE, alpha=0.35, ambient=0.55, spec=0)
    s.add(straight_arrow([-1.0, 0, 0], [1.0, 0, 0], 0.05, 0.3, 0.13), INK)
    for x in (-1.3, 0.0, 1.3):
        th = np.linspace(0, 2 * np.pi, 120)
        s.add(tube(np.stack([np.full_like(th, x), 0.6 * np.cos(th), 0.6 * np.sin(th)], -1), 0.022, closed=True),
              BLUE, spec=0.1)
        s.add(azimuthal_arrow_x(x, 0.6, 2.0, 2.8, head=0.22, head_r=0.09, rad=0.022), BLUE)
    for ang in np.radians([90, 150, 210]):
        d = np.array([0, np.cos(ang), np.sin(ang)])
        s.add(straight_arrow(np.array([0.65, 0, 0]) + 0.8 * d, np.array([0.65, 0, 0]) + 0.34 * d,
                             0.035, 0.16, 0.085), ORANGE)
    fig, ax = s.figure(103, 82, pad=(0.02, 0.02, 0.06, 0.06))
    s.label(ax, "anode", [-half - 0.3, 0, -0.75], dy=-12)
    s.label(ax, "cathode", [half + 0.3, 0, -0.75], dy=-12)
    s.label(ax, "$I$", [0.8, 0, 0.0], dx=30, dy=-34, leader=True)
    s.label(ax, r"$B_\theta$", [1.3, 0, 0.6], dx=10, dy=12, color=BLUE)
    s.label(ax, r"$\mathbf{j}\times\mathbf{B}$", [0.65, 0, 0.8], dx=-6, dy=14, color=ORANGE)
    save(fig, "z_pinch")


def theta_pinch():
    s = Scene(elev=30, azim=-60, axis_up=True)
    half = 2.2
    tube_and_electrodes(s, half, 0.8, 0.0, with_electrodes=False)
    s.add(column(1.8, 0.25, 0.5), ORANGE, alpha=0.55, ambient=0.55, spec=0)
    for x in np.linspace(-1.5, 1.5, 5):
        s.add(ring_x(x, 0.98, 0.2, 0.1), COPPER)
    s.add(azimuthal_arrow_x(0.75, 1.13, 4.6, 5.6, head=0.2, head_r=0.08), INK)
    
    x = np.linspace(-2.8, 2.8, 120)
    flare = 1 + 0.55 * np.clip((np.abs(x) - 1.6) / 1.2, 0, 1) ** 2
    for ang in np.radians([30, 90, 150, 210, 270, 330]):
        r = 0.55 * flare
        p = np.stack([x, r * np.cos(ang), r * np.sin(ang)], -1)
        s.add(tube(p, 0.02), BLUE, spec=0.1)
        s.add(cone(p[-1], p[-1] - p[-3], 0.2, 0.07), BLUE)
    for ang in (np.pi / 2, -np.pi / 2):
        d = np.array([0, np.cos(ang), np.sin(ang)])
        s.add(straight_arrow(np.array([1.2, 0, 0]) + 0.5 * d, np.array([1.2, 0, 0]) + 0.27 * d, 0.025, 0.1, 0.06),
              ORANGE)
    fig, ax = s.figure(103, 140, pad=(0.15, 0.15, 0.02, 0.04))
    s.label(ax, "coil", [-0.75, 1.05 * np.cos(3.4), 1.05 * np.sin(3.4)], dx=-30, ha="right", leader=True)
    s.label(ax, r"$I_c$", [0.75, 1.13 * np.cos(5.6), 1.13 * np.sin(5.6)], dx=48, dy=-6, leader=True)
    s.label(ax, r"$B_{\rm ext}$", [2.8, 0, 0.9], dx=26, dy=4, color=BLUE)
    save(fig, "theta_pinch")


def screw_pinch():
    s = Scene(elev=18, azim=-65)
    half, a = 3.0, 0.45
    tube_and_electrodes(s, half, 1.0, 0.85)
    s.add(column(half, a, 0.05), ORANGE, alpha=0.32, ambient=0.55, spec=0)
    for x in np.linspace(-2.4, 2.4, 7):
        s.add(ring_x(x, 1.2, 0.2, 0.08), COPPER)
    s.add(azimuthal_arrow_x(1.6, 1.33, 1.9, 2.9, head=0.24, head_r=0.09), INK)
    s.add(straight_arrow([-1.4, 0, 0], [1.4, 0, 0], 0.05, 0.35, 0.14), INK)
    q = 1.25
    x = np.linspace(-half + 0.05, half - 0.05, 400)
    for k in range(3):
        th = 2 * np.pi * k / 3 + (x + half) / (2 * half) / q * 2 * np.pi
        p = np.stack([x, (a + 0.02) * np.cos(th), (a + 0.02) * np.sin(th)], -1)
        s.add(tube(p, 0.022), BLUE, spec=0.1)
        i = np.argmin(np.abs(x - (0.35 + 0.9 * k)))
        s.add(cone(p[i], p[i + 2] - p[i - 2], 0.22, 0.075), BLUE)
    fig, ax = s.figure(257, 112, pad=(0.12, 0.14, 0.2, 0.14))
    s.label(ax, "anode", [-half - 0.6, 0, 0], dx=-8, ha="right")
    s.label(ax, "cathode", [half + 0.6, 0, 0], dx=8, ha="left")
    s.label(ax, "$I$", [0.0, 0, 0.0], dy=-18)
    s.label(ax, r"$I_c$", [1.6, 1.33 * np.cos(1.9), 1.33 * np.sin(1.9)], dx=20, dy=16)
    s.label(ax, "coils", [-2.4, 0, 1.3], dy=16)
    s.label(ax, r"$\mathbf{B}$", [2.2, -0.3, a], dx=40, dy=50, color=BLUE, leader=True)
    s.label(ax, r"$L$", [0, 0, -1.6], dy=-14, color=MUTED)
    p0, p1 = s.screen([-half, 0, -1.6]), s.screen([half, 0, -1.6])
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="<->", mutation_scale=14, lw=1.0, color=MUTED))
    save(fig, "screw_pinch")


def mirror_3d():
    s = Scene(elev=20, azim=-62)
    xc, rc = 2.0, 1.0

    def bfield(x):
        return sum(1 / (1 + ((x - c) / rc) ** 2) ** 1.5 for c in (-xc, xc))

    b0 = bfield(0.0)
    for c in (-xc, xc):
        s.add(ring_x(c, rc, 0.35, 0.18), COPPER)
        s.add(azimuthal_arrow_x(c, rc + 0.14, 1.9, 2.8, head=0.2, head_r=0.08), INK)
    x = np.linspace(-3.3, 3.3, 200)
    rr = np.sqrt(b0 / bfield(x))
    xp = np.linspace(-1.95, 1.95, 80)
    rp = 0.42 * np.sqrt(b0 / bfield(xp)) * np.clip((1.95 - np.abs(xp)) / 0.5, 0, 1) ** 0.5
    s.add(revolve_x(np.column_stack([xp, rp])), ORANGE, alpha=0.4, ambient=0.55, spec=0)
    for ang in np.radians([95, 175, 255, 335]):
        r = 0.6 * rr
        p = np.stack([x, r * np.cos(ang), r * np.sin(ang)], -1)
        s.add(tube(p, 0.02), BLUE, spec=0.1)
        s.add(cone(p[-1], p[-1] - p[-3], 0.2, 0.07), BLUE)
    fig, ax = s.figure(124, 95, pad=(0.02, 0.02, 0.12, 0.14))
    s.label(ax, r"$B_{\rm max}$", [-xc, 0, rc + 0.2], dy=18)
    s.label(ax, r"$B_{\rm max}$", [xc, 0, rc + 0.2], dy=18)
    s.label(ax, r"$B_{\rm min}$", [0, 0, 0.6 * rr.max()], dy=18, color=BLUE)
    s.label(ax, "coil", [-xc, 0, -rc - 0.2], dy=-16)
    s.label(ax, "coil", [xc, 0, -rc - 0.2], dy=-16)
    save(fig, "mirror_3d")


# ------------------------------------------------------------------ toroidal devices

def d_shape(r0, a, kappa, delta, n=200):
    t = np.linspace(0, 2 * np.pi, n)
    return r0 + a * np.cos(t + np.arcsin(delta) * np.sin(t)), kappa * a * np.sin(t)


def in_cut(phi, centre, half):
    return np.abs((phi - centre + np.pi) % (2 * np.pi) - np.pi) < half


def tokamak_3d():
    itr = json.loads((DATA / "iter-coils.json").read_text())
    azim, cut = -58.0, np.radians(62)
    s = Scene(elev=24, azim=azim)
    front = np.radians(azim)
    for c in itr["cs"]:
        s.add(ring_z(c["R"], c["Z"], c["dR"], c["dZ"] * 0.97), MUTED)
    a0, a1 = front + cut, front - cut + 2 * np.pi
    for c in itr["pf"]:
        s.add(ring_z(c["R"], c["Z"], c["dR"], c["dZ"], a0, a1), GREEN)
    tf = itr["tf_schematic"]
    rr, zz = d_shape(tf["R_centre"], tf["half_width"], tf["kappa"], tf["delta"])
    rr, zz = rr[::-1], zz[::-1]  # clockwise in (R, Z): up the inner leg, so B_phi > 0
    for k in range(tf["n"]):
        phi = 2 * np.pi * k / tf["n"]
        if in_cut(phi, front, cut):
            continue
        path = np.stack([rr * np.cos(phi), rr * np.sin(phi), zz], -1)
        t = unit(np.gradient(path, axis=0))
        v = np.broadcast_to([-np.sin(phi), np.cos(phi), 0.0], path.shape)
        u = np.cross(t, v)
        s.add(sweep_rect(path, u, v, tf["radial"], tf["toroidal"]), GREY, spec=0.15)
    pl = itr["plasma"]
    pr, pz = d_shape(pl["R0"], pl["a"], pl["kappa"], pl["delta"], 90)
    s.add(revolve_z(np.column_stack([pr, pz]), n=180), ORANGE, alpha=0.3, ambient=0.55, spec=0)
    q = 3.0
    phi = np.linspace(0, 2 * np.pi * q, 1400)
    th = 0.6 - phi / q  # B_theta from I_p along +phi turns the line towards -theta
    rl = pl["R0"] + 1.01 * pl["a"] * np.cos(th + np.arcsin(pl["delta"]) * np.sin(th))
    zl = 1.01 * pl["kappa"] * pl["a"] * np.sin(th)
    line = np.stack([rl * np.cos(phi), rl * np.sin(phi), zl], -1)
    s.add(tube(line, 0.05), BLUE, spec=0.1)
    for f in (front - 0.25, front + 2 * np.pi + 0.35, front + 4 * np.pi - 0.1):
        i = np.argmin(np.abs(phi - (f % (6 * np.pi))))
        s.add(cone(line[i], line[i + 3] - line[i - 3], 0.55, 0.2), BLUE)
    ph = np.linspace(front - 0.45, front + 0.15, 40)
    r_ax = pl["R0"] + 0.2
    s.add(path_arrow(np.stack([r_ax * np.cos(ph), r_ax * np.sin(ph), np.zeros_like(ph)], -1), 0.09, 0.7, 0.28), INK)
    kept = [2 * np.pi * k / tf["n"] for k in range(tf["n"]) if not in_cut(2 * np.pi * k / tf["n"], front, cut)]
    phe = min(kept, key=lambda f: abs((f - front + cut + np.pi) % (2 * np.pi) - np.pi))
    zz_a = np.linspace(2.0, -2.0, 20)
    r_out = tf["R_centre"] + tf["half_width"] + 0.8
    s.add(path_arrow(np.stack([np.full(20, r_out * np.cos(phe)), np.full(20, r_out * np.sin(phe)), zz_a], -1),
                     0.08, 0.6, 0.24), INK)
    fig, ax = s.figure(257, 128, pad=(0.08, 0.08, 0.02, 0.04))
    s.label(ax, "CS", [0, 0, 5.6], dx=-290, dy=50, leader=True, color=MUTED)
    s.label(ax, "TF", [(r_out - 0.8) * np.cos(phe), (r_out - 0.8) * np.sin(phe), 3.5], dx=-60, dy=40, leader=True)
    s.label(ax, r"$I_{\rm TF}$", [r_out * np.cos(phe), r_out * np.sin(phe), 0], dx=24)
    pf3 = itr["pf"][2]
    s.label(ax, "PF", [pf3["R"] * np.cos(front + cut + 0.05), pf3["R"] * np.sin(front + cut + 0.05), pf3["Z"]], dx=60,
            dy=4, color=GREEN, leader=True)
    s.label(ax, "plasma", [(pl["R0"] + 1.2) * np.cos(front - 0.5), (pl["R0"] + 1.2) * np.sin(front - 0.5),
                           -0.6 * pl["kappa"] * pl["a"]], dx=-150, dy=-40, color=ORANGE, leader=True)
    s.label(ax, r"$I_p$", [r_ax * np.cos(front + 0.15), r_ax * np.sin(front + 0.15), 0], dx=16, dy=10)
    i = np.argmin(np.abs(phi - (front + 2 * np.pi + 0.8)))
    s.label(ax, "$q = 3$", line[i], dx=110, dy=-30, color=BLUE, leader=True)
    save(fig, "tokamak_3d")


def box(lo, hi, n=8):
    """Axis-aligned box from corner lo to corner hi, faces subdivided for depth sorting."""
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    t = np.linspace(0, 1, n + 1)
    faces = []
    for k in range(3):
        i, j = [m for m in range(3) if m != k]
        u, v = np.meshgrid(lo[i] + t * (hi[i] - lo[i]), lo[j] + t * (hi[j] - lo[j]), indexing="ij")
        for w in (lo[k], hi[k]):
            p = np.empty(u.shape + (3,))
            p[..., i], p[..., j], p[..., k] = u, v, w
            faces.append(grid_quads(p))
    return np.concatenate(faces)


def zeta_3d():
    """Toroidal pinch on an iron-core transformer, ZETA dimensions R = 1.5 m, a = 0.5 m."""
    r0, a, ap = 1.5, 0.5, 0.25
    s = Scene(elev=24, azim=-62)
    front = np.radians(-62)
    th = np.linspace(0, 2 * np.pi, 49)
    circ = lambda r: np.column_stack([r0 + r * np.cos(th), r * np.sin(th)])  # noqa: E731
    s.add(revolve_z(circ(a), n=160), GLASS, alpha=0.12, ambient=0.8, spec=0)
    s.add(revolve_z(circ(ap), n=160), ORANGE, alpha=0.45, ambient=0.55, spec=0)
    w, h = 0.36, 1.7
    s.add(box([-w, -w, -h - 0.5], [w, w, h + 0.5]), MUTED)
    ex = -3.4
    s.add(box([ex - w, -w, -h - 0.5], [ex + w, w, h + 0.5]), MUTED)
    s.add(box([ex + w, -w, h], [-w, w, h + 0.5]), MUTED)
    s.add(box([ex + w, -w, -h - 0.5], [-w, w, -h]), MUTED)
    for z in np.linspace(-0.6, 0.6, 5):
        s.add(ring_z(w * 1.5 + 0.05, z, 0.1, 0.18), COPPER)
    for k in range(10):
        ph = 2 * np.pi * k / 10 + 0.3
        loop = np.stack([(r0 + (a + 0.06) * np.cos(th)) * np.cos(ph), (r0 + (a + 0.06) * np.cos(th)) * np.sin(ph),
                         (a + 0.06) * np.sin(th)], -1)
        s.add(tube(loop, 0.02, closed=True), COPPER)
    q = 0.25
    phi = np.linspace(0, 2 * np.pi, 1600)
    tl = 0.4 - phi / q
    rl = r0 + 1.02 * ap * np.cos(tl)
    line = np.stack([rl * np.cos(phi), rl * np.sin(phi), 1.02 * ap * np.sin(tl)], -1)
    s.add(tube(line, 0.012), BLUE, spec=0.1)
    ph = np.linspace(front - 0.5, front + 0.1, 40)
    s.add(path_arrow(np.stack([r0 * np.cos(ph), r0 * np.sin(ph), np.zeros_like(ph)], -1), 0.03, 0.18, 0.075), INK)
    fig, ax = s.figure(257, 128, pad=(0.06, 0.06, 0.03, 0.05))
    s.label(ax, "iron core", [ex - w, 0, 0], dx=-12, ha="right")
    s.label(ax, "primary", [w * 1.5 * np.cos(front), w * 1.5 * np.sin(front), 0.6], dx=-90, dy=50, leader=True)
    s.label(ax, r"$B_\varphi$ coils, weak", [(r0 + a) * np.cos(front + 0.9), (r0 + a) * np.sin(front + 0.9), 0.3],
            dx=110, dy=50, leader=True)
    s.label(ax, "$I$", [r0 * np.cos(front + 0.1), r0 * np.sin(front + 0.1), 0], dx=40, dy=-62, leader=True)
    s.label(ax, r"$q(a) \ll 1$", line[200], dx=120, dy=-40, color=BLUE, leader=True)
    s.label(ax, "plasma", [r0 * np.cos(front + 0.5), r0 * np.sin(front + 0.5), -ap], dx=170, dy=-50, color=ORANGE,
            leader=True)
    save(fig, "zeta_3d")


def vmec_surface(b, theta, phi):
    m, n = np.array(b["xm"]), np.array(b["xn"])
    ang = theta[..., None] * m - phi[..., None] * n
    return (np.cos(ang) @ np.array(b["rmnc"]), np.sin(ang) @ np.array(b["zmns"]),
            np.sin(ang) @ np.array(b["lmns"]))


def field_line(b, theta0, phi):
    """theta* = theta + lambda(theta, phi) = theta0 + iota phi, solved for VMEC theta by Newton."""
    m, n = np.array(b["xm"]), np.array(b["xn"])
    target = theta0 + b["iota"] * phi
    th = target.copy()
    lm = np.array(b["lmns"])
    for _ in range(30):
        ang = m[None] * th[:, None] - n[None] * phi[:, None]
        f = th + np.sin(ang) @ lm - target
        th -= f / (1 + np.cos(ang) @ (m * lm))
    r, z, _ = vmec_surface(b, th, phi)
    return np.stack([r * np.cos(phi), r * np.sin(phi), z], -1)


def stellarator_3d():
    d = json.loads((DATA / "ncsx.json").read_text())
    b = d["boundary"]
    azim, cut = -60.0, np.radians(66)
    front = np.radians(azim)
    s = Scene(elev=24, azim=azim)
    th, ph = np.meshgrid(np.linspace(0, 2 * np.pi, 64), np.linspace(0, 2 * np.pi, 241), indexing="xy")
    r, z, _ = vmec_surface(b, th, ph)
    s.add(grid_quads(np.stack([r * np.cos(ph), r * np.sin(ph), z], -1)), ORANGE, alpha=0.4, ambient=0.55, spec=0)
    shown = []
    for c in d["modular_coils"]:
        p = np.array(c["xyz_m"])
        p = np.vstack([p, p[:1]])
        if in_cut(np.arctan2(p[:, 1].mean(), p[:, 0].mean()), front, cut):
            continue
        s.add(tube(p, 0.03, closed=True), GREY, spec=0.15)
        shown.append(p)
    line = field_line(b, 0.3, np.linspace(0, 2 * np.pi * 2, 1600))
    s.add(tube(line, 0.009), BLUE, spec=0.1)
    fig, ax = s.figure(257, 128, pad=(0.04, 0.04, 0.02, 0.04))
    phis = [np.arctan2(p[:, 1].mean(), p[:, 0].mean()) for p in shown]
    k = int(np.argmin([abs((f - front - cut - 0.3 + np.pi) % (2 * np.pi) - np.pi) for f in phis]))
    top = shown[k][np.argmax(shown[k][:, 2])]
    s.label(ax, "modular coils", top, dx=150, dy=10, leader=True)
    s.label(ax, "plasma", [1.45 * np.cos(front + 0.1), 1.45 * np.sin(front + 0.1), -0.25], dy=-30, color=ORANGE,
            leader=True)
    i = 1600 // 4 + 60
    s.label(ax, "field line", line[i], dx=-170, dy=-30, color=BLUE, leader=True)
    save(fig, "stellarator_3d")


def torus_tf_3d():
    """Torus with only toroidal-field coils: B_phi ~ 1/R, front wedge cut open."""
    r0, a, rc, n_tf = 3.0, 1.0, 1.45, 12
    azim, cut = -62.0, np.radians(38)
    s = Scene(elev=28, azim=azim)
    front = np.radians(azim)
    a0, a1 = front + cut, front - cut + 2 * np.pi
    s.add(straight_arrow([0, 0, -2.2], [0, 0, 2.4], 0.025, 0.3, 0.1), MUTED)
    tt = np.linspace(0, 2 * np.pi, 120)[::-1]  # clockwise in (R, Z): up the inner leg, B_phi > 0
    for k in range(n_tf):
        phi = 2 * np.pi * k / n_tf + 0.5 * np.pi / n_tf
        if in_cut(phi, front, cut + 0.06):
            continue
        rr, zz = r0 + rc * np.cos(tt), rc * np.sin(tt)
        path = np.stack([rr * np.cos(phi), rr * np.sin(phi), zz], -1)
        tg = unit(np.gradient(path, axis=0))
        v = np.broadcast_to([-np.sin(phi), np.cos(phi), 0.0], path.shape)
        s.add(sweep_rect(path, np.cross(tg, v), v, 0.14, 0.3), GREY, spec=0.15)
    th = np.linspace(0, 2 * np.pi, 60)
    prof = np.column_stack([r0 + a * np.cos(th), a * np.sin(th)])
    s.add(revolve_z(prof, a0, a1, 200), ORANGE, alpha=0.32, ambient=0.55, spec=0)
    rg, tg2 = np.meshgrid(np.linspace(0, a, 8), th, indexing="ij")
    for ang in (a0, a1):
        R = r0 + rg * np.cos(tg2)
        cap = np.stack([R * np.cos(ang), R * np.sin(ang), rg * np.sin(tg2)], -1)
        s.add(grid_quads(cap), ORANGE, alpha=0.75, ambient=0.6, spec=0)
    for rl in (r0 - 0.55, r0, r0 + 0.55):
        ph = np.linspace(a0 + 0.05, a1 - 0.05, 300)
        line = np.stack([rl * np.cos(ph), rl * np.sin(ph), np.full_like(ph, 0.02)], -1)
        s.add(tube(line[:-20], 0.035), BLUE, spec=0.1)
        s.add(cone(line[-20], line[-1] - line[-20], 0.35, 0.12), BLUE)
    kept = [2 * np.pi * k / n_tf + 0.5 * np.pi / n_tf for k in range(n_tf)]
    kept = [f for f in kept if not in_cut(f, front, cut + 0.06)]
    phc = min(kept, key=lambda f: abs((f - a0 - 0.55 + np.pi) % (2 * np.pi) - np.pi))
    arc = np.linspace(0.35, -0.35, 30)
    rr, zz = r0 + (rc + 0.32) * np.cos(arc), (rc + 0.32) * np.sin(arc)
    s.add(path_arrow(np.stack([rr * np.cos(phc), rr * np.sin(phc), zz], -1), 0.04, 0.3, 0.12), INK)
    fig, ax = s.figure(257, 128, pad=(0.12, 0.06, 0.1, 0.05))
    s.label(ax, "axis", [0, 0, 2.5], dx=28, dy=-6, color=MUTED)
    pht = min(kept, key=lambda f: abs((f - a1 + 0.5 + np.pi) % (2 * np.pi) - np.pi))
    s.label(ax, "TF coils", [r0 * np.cos(pht), r0 * np.sin(pht), rc + 0.07], dx=-70, dy=55, leader=True)
    s.label(ax, r"$I_{\rm TF}$", [(r0 + rc + 0.32) * np.cos(phc), (r0 + rc + 0.32) * np.sin(phc), 0], dx=34, dy=-10)
    s.label(ax, "plasma", [(r0 + 0.5) * np.cos(a0 + 0.4), (r0 + 0.5) * np.sin(a0 + 0.4), -0.85], dx=40, dy=-45,
            color=ORANGE, leader=True)
    s.label(ax, "cross-section", [r0 * np.cos(a1), r0 * np.sin(a1), -0.5], dx=-120, dy=-40, leader=True)
    s.label(ax, r"$B_\varphi \propto 1/R$", [r0 * np.cos(a1 - 0.45), r0 * np.sin(a1 - 0.45), 0],
            dx=-140, dy=60, color=BLUE, leader=True)
    save(fig, "torus_tf_3d")


if __name__ == "__main__":
    style()
    for f in sys.argv[1:] or ["z_pinch", "theta_pinch", "screw_pinch", "mirror_3d", "zeta_3d", "torus_tf_3d", "tokamak_3d", "stellarator_3d"]:
        globals()[f]()
