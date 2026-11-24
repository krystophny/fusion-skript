"""Deck figures for Chapter 5: tokamak components.

tokamak_explode_<k> (k = 1..11): 3D build-up of an ITER-sized tokamak. Steps 1-8 add one component
group each in its assembled position: plasma, TF coils, central solenoid, PF coils, vacuum vessel with
blanket, divertor, heating systems, cryostat. Steps 9-11 explode it one group at a time: central
solenoid lifted, PF coils spread, heating systems pulled out. CS, PF and plasma from data/ch05/iter-coils.json (as in tokamak_3d);
vessel, blanket, divertor, heating and cryostat are schematic, sized after the ITER numbers
quoted on the slides. Exploded offsets are drawing choices, not positions.

tokamak_section: poloidal cross-section with a lower single-null separatrix. The flux function is
that of straight line currents in the (R, Z) plane: a distributed plasma current and a divertor
coil below it carrying current in the same direction produce the X-point between them. This is a
qualitative model (no toroidal correction, no free-boundary equilibrium).

Run:  python3 slides/figures_tokamak_parts.py
      -> slides/build/fig/{tokamak_explode_1..11,tokamak_section}.{svg,png}
"""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figures import BLUE, GREEN, GREY, INK, MM, MUTED, ORANGE, save, style  # noqa: E402
from figures_devices import (DATA, STEEL, Scene, box, cone, d_shape, grid_quads, in_cut,  # noqa: E402
                             revolve_z, ring_z, sweep_rect, tube, unit)

ITER = json.loads((DATA / "iter-coils.json").read_text())
PURPLE = "#7A4E9C"
VESSEL = "#B8C0C8"
BLANKET = "#C9A66B"
TUNGSTEN = "#5E6B78"
AZIM, ELEV = -58.0, 20.0
FRONT = np.radians(AZIM)
CUT = np.radians(62)
A0, A1 = FRONT + CUT, FRONT - CUT + 2 * np.pi

VV_SHAPE = (6.32, 3.0, 1.66, 0.38)  # R0, a, kappa, delta of the vacuum vessel [m]
FW_SHAPE = (6.25, 2.7, 1.62, 0.36)  # first wall (blanket surface)
# exploded offsets [m]
DZ_CS, DZ_PF_UP, DZ_PF_LO, DZ_DIV = 10.0, 2.5, -2.5, 0.0
DR_NBI, DR_ICRH, DZ_ECRH = 5.0, 4.0, 3.0
EX_CS, EX_PF, EX_HEAT = 9, 10, 11  # step at which each group moves to its exploded position
N_STEPS = 11


def shell(rr, zz, thick, a0=A0, a1=A1, n=200, keep=None):
    """Toroidal shell of an (R, Z) contour, thickness along the inward normal, cut ends capped."""
    rr, zz = np.asarray(rr), np.asarray(zz)
    if keep is not None:
        rr, zz = rr[keep], zz[keep]
    t = np.gradient(np.stack([rr, zz], -1), axis=0)
    nrm = np.stack([t[:, 1], -t[:, 0]], -1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True)
    # inward normal: towards the contour centre
    c = np.array([rr.mean(), zz.mean()])
    sgn = np.sign(((c - np.stack([rr, zz], -1)) * nrm).sum(1).mean())
    ri, zi = rr + sgn * thick * nrm[:, 0], zz + sgn * thick * nrm[:, 1]
    q = [revolve_z(np.column_stack([rr, zz]), a0, a1, n), revolve_z(np.column_stack([ri, zi]), a0, a1, n)]
    for a in (a0, a1):
        p = np.stack([np.stack([rr * np.cos(a), rr * np.sin(a), zz], -1),
                      np.stack([ri * np.cos(a), ri * np.sin(a), zi], -1)], 1)
        q.append(grid_quads(p))
    if keep is not None:  # close the open ends of a partial contour
        for j in (0, -1):
            prof = np.array([[rr[j], zz[j]], [ri[j], zi[j]]])
            q.append(revolve_z(prof, a0, a1, n))
    return np.concatenate(q)


def oriented_box(centre, ex, ey, ez, lx, ly, lz):
    """Box with edges lx, ly, lz along the orthonormal vectors ex, ey, ez."""
    b = box([-0.5, -0.5, -0.5], [0.5, 0.5, 0.5], n=4)
    m = np.stack([np.asarray(ex) * lx, np.asarray(ey) * ly, np.asarray(ez) * lz])
    return b @ m + np.asarray(centre)


def tokamak_parts():
    pl = ITER["plasma"]
    tf = ITER["tf_schematic"]
    parts = []  # (step, quads, colour, move, kwargs); move = (step, offset) or None

    def add(step, quads, colour, move=None, **kw):
        parts.append((step, np.asarray(quads, float), colour, move, kw))

    # 1 plasma
    pr, pz = d_shape(pl["R0"], pl["a"], pl["kappa"], pl["delta"], 90)
    add(1, revolve_z(np.column_stack([pr, pz]), n=180), ORANGE, alpha=0.35, ambient=0.55, spec=0)
    # 2 TF coils
    rr, zz = d_shape(tf["R_centre"], tf["half_width"], tf["kappa"], tf["delta"])
    for k in range(tf["n"]):
        phi = 2 * np.pi * k / tf["n"]
        if in_cut(phi, FRONT, CUT):
            continue
        path = np.stack([rr * np.cos(phi), rr * np.sin(phi), zz], -1)
        t = unit(np.gradient(path, axis=0))
        v = np.broadcast_to([-np.sin(phi), np.cos(phi), 0.0], path.shape)
        add(2, sweep_rect(path, np.cross(t, v), v, tf["radial"], tf["toroidal"]), GREY, spec=0.15)
    # 3 central solenoid, lifted
    for c in ITER["cs"]:
        add(3, ring_z(c["R"], c["Z"], c["dR"], c["dZ"] * 0.97), MUTED, move=(EX_CS, [0, 0, DZ_CS]))
    # 4 PF coils, upper ones lifted and lower ones lowered
    for c in ITER["pf"]:
        dz = DZ_PF_UP if c["Z"] > 4 else DZ_PF_LO if c["Z"] < -4 else 0.0
        add(4, ring_z(c["R"], c["Z"], c["dR"], c["dZ"], A0, A1), GREEN, move=(EX_PF, [0, 0, dz]) if dz else None)
    # 5 vacuum vessel and blanket (open at the bottom for the divertor)
    vr, vz = d_shape(*VV_SHAPE, 240)
    add(5, shell(vr, vz, 0.35), VESSEL, alpha=0.55, ambient=0.6, spec=0.05)
    th = np.linspace(0, 2 * np.pi, 240)
    br, bz = d_shape(*FW_SHAPE, 240)
    keep = np.abs(((th - 1.5 * np.pi) + np.pi) % (2 * np.pi) - np.pi) > 0.75
    add(5, shell(br, bz, 0.3, keep=keep), BLANKET, alpha=0.85, ambient=0.55, spec=0.05)
    # 6 divertor: 54 cassettes, lowered
    n_div = 54
    for k in range(n_div):
        a = 2 * np.pi * (k + 0.5) / n_div
        if in_cut(a, FRONT, CUT):
            continue
        da = 2 * np.pi / n_div * 0.42
        add(6, ring_z(5.55, -4.35 + DZ_DIV, 1.9, 0.6, a - da, a + da, n=6), TUNGSTEN, spec=0.3)
    # 7 heating systems
    # NBI: tangential, tangency radius 5.3 m, exits on the right
    rt = 5.3
    e_t = np.array([np.cos(FRONT), np.sin(FRONT), 0.0])
    d_b = np.array([-np.sin(FRONT), np.cos(FRONT), 0.0])
    s_port = np.sqrt(9.3 ** 2 - rt ** 2)
    nbi_out = (EX_HEAT, DR_NBI * d_b)
    p0 = rt * e_t + (s_port - 0.4) * d_b
    p1 = rt * e_t + (s_port + 3.5) * d_b
    add(7, tube(np.linspace(p0, p1, 10), 0.55, sides=16), BLUE, move=nbi_out, spec=0.2)
    add(7, oriented_box(rt * e_t + (s_port + 8.5) * d_b, d_b, np.cross([0, 0, 1], d_b), [0, 0, 1],
                        10.0, 3.2, 4.0), BLUE, move=nbi_out, ambient=0.5, spec=0.1)
    beam = np.linspace(rt * e_t + 1.5 * d_b, rt * e_t + (s_port - 0.6) * d_b, 20)
    add(7, tube(beam, 0.18, sides=10), BLUE, alpha=0.45, ambient=0.7, spec=0)
    # ICRH: equatorial port on the left, antenna pulled out radially
    a_ic = FRONT + np.pi + 0.95
    e_r = np.array([np.cos(a_ic), np.sin(a_ic), 0.0])
    e_p = np.array([-np.sin(a_ic), np.cos(a_ic), 0.0])
    icrh_out = (EX_HEAT, DR_ICRH * e_r)
    add(7, oriented_box(9.6 * e_r, e_r, e_p, [0, 0, 1], 2.6, 2.2, 2.4), PURPLE, move=icrh_out, spec=0.15)
    for k in (-0.6, 0.0, 0.6):
        a = 11.0 * e_r + k * e_p
        add(7, tube(np.linspace(a, a + 3.0 * e_r, 6), 0.16, sides=10), PURPLE, move=icrh_out)
    # ECRH: two upper launchers, lifted, with their beams
    for da in (0.55, 1.15):
        a = FRONT + np.pi + da
        er = np.array([np.cos(a), np.sin(a), 0.0])
        top = 7.6 * er + np.array([0, 0, 5.4])
        add(7, tube(np.linspace(top, top + np.array([0, 0, 2.8]) + 1.2 * er, 8), 0.45, sides=14), ORANGE,
            move=(EX_HEAT, [0, 0, DZ_ECRH]), spec=0.2)
        tgt = 6.4 * er + np.array([0, 0, 0.6])
        add(7, tube(np.linspace(7.4 * er + np.array([0, 0, 4.3]), tgt, 12), 0.1, sides=8), ORANGE, alpha=0.5,
            ambient=0.7, spec=0)
    # 8 cryostat: translucent cylinder and base, lid left off
    zc0, zc1, rc = -12.0, 10.5, 14.0
    add(8, revolve_z(np.array([[rc, zc0], [rc, zc1]]), A0, A1, 160), STEEL, alpha=0.12, ambient=0.7, spec=0)
    add(8, revolve_z(np.array([[0.0, zc0], [rc, zc0]]), A0, A1, 160), STEEL, alpha=0.18, ambient=0.7, spec=0)
    return parts


D_B = np.array([-np.sin(FRONT), np.cos(FRONT), 0.0])
A_ICRH, A_ECRH = FRONT + np.pi + 0.95, FRONT + np.pi + 0.55
E_ICRH = np.array([np.cos(A_ICRH), np.sin(A_ICRH), 0.0])
# (text, assembled anchor, label offset [pt], colour, (step, offset) at which the anchor moves, step shown)
LABELS = [
    ("plasma", [7.9 * np.cos(FRONT + 0.25), 7.9 * np.sin(FRONT + 0.25), -1.6], (170, -70), ORANGE, None, 1),
    ("TF coils", [10.8 * np.cos(FRONT + CUT + 0.18), 10.8 * np.sin(FRONT + CUT + 0.18), 3.0], (90, 40), INK,
     None, 2),
    ("central solenoid", [-0.9 * np.sin(FRONT), 0.9 * np.cos(FRONT), 4.0], (150, 10), MUTED,
     (EX_CS, [0, 0, DZ_CS]), 3),
    ("PF coils", [8.4 * np.cos(A0 + 0.05), 8.4 * np.sin(A0 + 0.05), 6.6], (110, 20), GREEN,
     (EX_PF, [0, 0, DZ_PF_UP]), 4),
    ("vessel, blanket", [8.9 * np.cos(A1), 8.9 * np.sin(A1), -1.0], (-40, -125), MUTED, None, 5),
    ("divertor", [6.5 * np.cos(A1 - 0.1), 6.5 * np.sin(A1 - 0.1), -3.9 + DZ_DIV], (-150, -10), TUNGSTEN, None, 6),
    ("NBI", list(5.3 * np.array([np.cos(FRONT), np.sin(FRONT), 0]) + (np.sqrt(9.3 ** 2 - 5.3 ** 2) + 12.0) * D_B
                 + np.array([0, 0, 2.4])), (20, 40), BLUE, (EX_HEAT, DR_NBI * D_B), 7),
    ("ICRH", list(12.0 * E_ICRH + np.array([0, 0, 1.4])), (-30, 40), PURPLE, (EX_HEAT, DR_ICRH * E_ICRH), 7),
    ("ECRH", [8.2 * np.cos(A_ECRH), 8.2 * np.sin(A_ECRH), 8.2], (-110, 10), ORANGE, (EX_HEAT, [0, 0, DZ_ECRH]), 7),
    ("cryostat", [14.0 * np.cos(A0 + 0.1), 14.0 * np.sin(A0 + 0.1), -5.0], (110, 0), MUTED, None, 8),
]


def placed(q, move, step):
    return q + np.asarray(move[1], float) if move and step >= move[0] else q


def tokamak_explode():
    parts = tokamak_parts()
    for step in range(1, N_STEPS + 1):
        s = Scene(elev=ELEV, azim=AZIM)
        for st, q, col, move, kw in parts:
            if st <= step:
                s.add(placed(q, move, step), col, **kw)
        # fix the frame to the fully exploded drawing so that the view does not jump between steps
        for st, q, col, move, kw in parts:
            s.add(placed(q, move, N_STEPS), "white", alpha=0.0)
        fig, ax = s.figure(257, 138, pad=(0.02, 0.02, 0.02, 0.02))
        for text, at, (dx, dy), col, move, shown in LABELS:
            if shown <= step:
                if text == "central solenoid" and step < EX_CS:
                    dx, dy = 120, 115  # in place, the exploded offset would land on the TF label
                s.label(ax, text, placed(np.asarray(at, float), move, step), dx=dx, dy=dy, color=col, leader=True)
        save(fig, f"tokamak_explode_{step}")


def tokamak_section():
    """Poloidal cross-section: coils, vessel, first wall, separatrix with X-point, divertor legs."""
    pl = ITER["plasma"]
    R0, a, kap = pl["R0"], pl["a"], pl["kappa"]
    # plasma current: filaments over an elliptic cross-section with a parabolic profile
    g = np.linspace(-1, 1, 25)
    fr, fz = np.meshgrid(g, g)
    inside = fr ** 2 + fz ** 2 < 1
    w = (1 - fr ** 2 - fz ** 2)[inside]
    w = w / w.sum()
    rf, zf = R0 + 0.86 * a * fr[inside], 0.86 * kap * a * fz[inside]
    # weights relative to I_p = 1: divertor coil below (same sign) makes the X-point, two upper coils
    # stretch the plasma upwards
    coils = [(5.6, -5.6, 0.5), (5.0, 6.0, 0.4), (9.5, 5.5, 0.24)]

    def psi(R, Z):
        p = np.zeros(np.broadcast(R, Z).shape)
        for r_, z_, w_ in list(zip(rf, zf, w)) + coils:
            p = p + w_ * np.log(np.hypot(R - r_, Z - z_) + 1e-12)
        return p

    def grad2(x):
        h = 1e-4
        gr = (psi(x[0] + h, x[1]) - psi(x[0] - h, x[1])) / (2 * h)
        gz = (psi(x[0], x[1] + h) - psi(x[0], x[1] - h)) / (2 * h)
        return float(gr ** 2 + gz ** 2)

    from scipy.optimize import minimize
    xp = minimize(grad2, [5.8, -4.0], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-16)).x
    psi_x, psi_ax = float(psi(*xp)), float(psi(R0, 0.0))
    R, Z = np.meshgrid(np.linspace(1.0, 13.0, 700), np.linspace(-8.8, 8.6, 900))
    P = psi(R, Z)

    fig = plt.figure(figsize=(118 * MM, 150 * MM), dpi=250)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_aspect("equal")
    ax.axis("off")
    for c in ITER["cs"]:
        ax.add_patch(plt.Rectangle((c["R"] - c["dR"] / 2, c["Z"] - c["dZ"] / 2), c["dR"], c["dZ"] * 0.97,
                                   fc=MUTED, ec="none"))
    for c in ITER["pf"]:
        ax.add_patch(plt.Rectangle((c["R"] - c["dR"] / 2, c["Z"] - c["dZ"] / 2), c["dR"], c["dZ"], fc=GREEN,
                                   ec="none"))
    tf = ITER["tf_schematic"]
    tr, tz = d_shape(tf["R_centre"], tf["half_width"], tf["kappa"], tf["delta"])
    ax.plot(tr, tz, color=GREY, lw=9, solid_capstyle="butt")
    vr, vz = d_shape(*VV_SHAPE, 240)
    ax.plot(vr, vz, color=VESSEL, lw=4)
    th = np.linspace(0, 2 * np.pi, 240)
    br, bz = d_shape(*FW_SHAPE, 240)
    keep = np.abs(((th - 1.5 * np.pi) + np.pi) % (2 * np.pi) - np.pi) > 0.75
    ax.plot(np.where(keep, br, np.nan), np.where(keep, bz, np.nan), color=BLANKET, lw=6, solid_capstyle="butt")
    # closed flux surfaces
    core = np.where((Z > xp[1]) & (np.hypot((R - R0) / 2.6, Z / 4.4) < 1.0), P, np.nan)
    ax.contourf(R, Z, core, levels=[psi_ax - 1, psi_x], colors=[ORANGE], alpha=0.18)
    ax.contour(R, Z, core, levels=list(psi_ax + (psi_x - psi_ax) * np.array([0.2, 0.4, 0.6, 0.8])),
               colors=[ORANGE], linewidths=0.8)
    # separatrix and one open surface of the scrape-off layer, legs ending on the targets
    z_t = xp[1] - 0.95
    open_ = np.where((Z > z_t) & (R > 3.8) & (R < 9.0) & (Z < 4.5), P, np.nan)
    cs = ax.contour(R, Z, open_, levels=[psi_x], colors=[INK], linewidths=1.4)
    ax.contour(R, Z, open_, levels=[psi_x + 0.03 * (psi_x - psi_ax)], colors=[BLUE], linewidths=0.9,
               linestyles="dashed")
    ax.plot(*xp, "x", color=INK, ms=9, mew=2)
    # targets: plates where the separatrix legs end
    legs = np.concatenate([seg for seg in cs.allsegs[0] if len(seg)])
    for side in (legs[:, 0] < xp[0] - 0.05, legs[:, 0] > xp[0] + 0.05):
        pts = legs[side & (legs[:, 1] < xp[1] - 0.3)]
        if len(pts):
            r_, z_ = pts[np.argmin(pts[:, 1])]
            ax.plot([r_ - 0.4, r_ + 0.4], [z_ - 0.08, z_ - 0.08], color=TUNGSTEN, lw=7, solid_capstyle="butt")
    kw = dict(fontsize=13, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.annotate("X-point", xy=xp, xytext=(xp[0] + 2.4, xp[1] - 0.3), color=INK, **kw)
    ax.annotate("separatrix", xy=(R0 + 1.95, 1.2), xytext=(9.5, 2.4), color=INK, **kw)
    ax.annotate("vessel", xy=(R0 + 2.8, -0.6), xytext=(9.6, -0.5), color=MUTED, **kw)
    ax.annotate("scrape-off\nlayer", xy=(R0 + 2.12, -1.8), xytext=(9.6, -3.6), color=BLUE, **kw)
    ax.annotate("divertor\ntargets", xy=(xp[0] + 0.3, z_t - 0.1), xytext=(5.6, -8.6), color=TUNGSTEN, **kw)
    ax.annotate("first wall", xy=(6.95, 3.7), xytext=(9.4, 7.5), color=BLANKET, **kw)
    ax.text(1.7, -7.7, "CS", fontsize=13, color=MUTED, ha="center")
    ax.text(11.9, 0.6, "TF", fontsize=13, color=MUTED, ha="center")
    ax.text(12.0, 4.4, "PF", fontsize=13, color=GREEN, ha="center")
    ax.set_xlim(0.8, 13.2)
    ax.set_ylim(-8.7, 8.5)
    save(fig, "tokamak_section")
    return xp


if __name__ == "__main__":
    style()
    for f in sys.argv[1:] or ["tokamak_explode", "tokamak_section"]:
        globals()[f]()
