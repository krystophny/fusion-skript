"""Head-on Coulomb encounter: classical reflection at r_c and the quantum
tail in the classically forbidden region r < r_c.

Model (animations/radial_coulomb.py): relative motion of two nuclei with
reduced mass m and V(r) = Z_1 Z_2 e^2/(4 pi eps_0 r), head-on (l = 0), so the
radial function u(r) = r R(r) with u(0) = 0 carries the whole problem. Lengths
in r_c, energies in the mean energy E of the packet (V(r_c) = E), Sommerfeld
parameter eta = 2 (D-T at about 7.5 keV), incoming Gaussian packet with an
energy spread of 12 percent (rms). Exact evolution of the discretized radial
Hamiltonian (norm conserved to roundoff).

Top: V(r), the energy line E and the turning point r_c, as on the deck's
"Classical turning point" sketch. The classical particle at energy E (dot)
comes in along the energy line, is reflected at r_c and goes out. The quantum
probability density |u|^2 is drawn on the energy line as baseline (fixed
scale). Bottom: log10(|u|^2 r_c) on the same r axis; inside the shaded region
r < r_c it decays like the WKB factor exp(-2 int kappa dr) instead of
vanishing.
"""

from manim import *
import numpy as np

from style import (
    AXIS, AXIS_WIDTH, BLUE, CURVE_WIDTH, DOT_RADIUS, GRID, INK, LINEAR, MUTED,
    THIN_WIDTH, VERMILION, StyledScene, axes, label, math, LABEL_SIZE, MATH_SIZE,
    MATH_SMALL,
)
import radial_coulomb as model

X_MAX = 8.0             # r/r_c range
Y_MAX = 3.0             # V/E range of the upper panel
SCALE = 1.4             # |u|^2 r_c -> height in units of E
LOG_LO, LOG_HI = -5.0, 0.0
T_START, T_END = 0.0, 70.2    # physical time (r_c/v units of the model); turn at 35.1
PLAY_TIME = 12.0
HOLD = 0.6


class CoulombReflection(StyledScene):
    """One r axis: V(r), E, classical dot, quantum |u|^2; log strip below."""

    def build(self):
        packet = model.RadialPacket()
        r = packet.r
        shown = r <= X_MAX
        rs = r[shown]

        top = axes([0, X_MAX, 1], [0, Y_MAX, 1], x_length=11.0, y_length=3.9,
                   ticks=False)
        top.move_to([0.35, 1.35, 0])
        low = axes([0, X_MAX, 1], [LOG_LO, LOG_HI, 1], x_length=11.0, y_length=1.6,
                   ticks=False)
        low.move_to([0.35, -2.25, 0])

        def p_top(x, y):
            return top.c2p(x, y)

        def p_low(x, y):
            return low.c2p(x, y)

        # Classically forbidden band r < r_c in both panels.
        bands = VGroup(*[
            Polygon(f(0, a), f(1, a), f(1, b), f(0, b), stroke_width=0,
                    fill_color=GRID, fill_opacity=0.35)
            for f, a, b in ((p_top, 0, Y_MAX), (p_low, LOG_LO, LOG_HI))])
        forbidden = VGroup(math(r"r<r_c", color=MUTED, size=MATH_SMALL),
                           label("classically forbidden", color=MUTED, size=LABEL_SIZE - 4)
                           ).arrange(RIGHT, buff=0.2)
        forbidden.next_to(p_top(1.1, Y_MAX), DOWN + RIGHT, buff=0.12)

        r_v = np.linspace(1 / Y_MAX, X_MAX, 400)
        potential = VMobject().set_points_smoothly([p_top(x, 1 / x) for x in r_v])
        potential.set_stroke(INK, CURVE_WIDTH)
        v_label = math(r"V(r)", color=INK, size=MATH_SIZE).next_to(p_top(0.5, 2.4), RIGHT, buff=0.1)
        energy = DashedVMobject(Line(p_top(0, 1), p_top(X_MAX, 1)), num_dashes=60)
        energy.set_stroke(MUTED, THIN_WIDTH)
        e_label = math(r"E", color=MUTED, size=MATH_SIZE).next_to(p_top(X_MAX, 1), RIGHT, buff=0.15)
        drop = DashedVMobject(Line(p_top(1, 0), p_top(1, 1)), num_dashes=8).set_stroke(MUTED, THIN_WIDTH)
        drop_low = DashedVMobject(Line(p_low(1, LOG_LO), p_low(1, LOG_HI)), num_dashes=12)
        drop_low.set_stroke(MUTED, THIN_WIDTH)

        ticks = VGroup()
        for x, tex in ((0, "0"), (1, "r_c"), (2, "2r_c"), (4, "4r_c"), (6, "6r_c"), (8, "8r_c")):
            pos = p_low(x, LOG_LO)
            ticks.add(Line(pos, pos + DOWN * 0.08, color=AXIS, stroke_width=AXIS_WIDTH))
            ticks.add(math(tex, color=MUTED, size=MATH_SMALL).next_to(pos, DOWN, buff=0.12))
        rc_top = math(r"r_c", color=MUTED, size=MATH_SMALL).next_to(p_top(1, 0), DOWN, buff=0.12)
        r_label = math(r"r", color=MUTED, size=MATH_SIZE).next_to(p_top(X_MAX, 0), RIGHT, buff=0.15)
        for v in (-4, -2, 0):
            pos = p_low(0, v)
            ticks.add(Line(pos, pos + LEFT * 0.08, color=AXIS, stroke_width=AXIS_WIDTH))
            ticks.add(math(str(v), color=MUTED, size=MATH_SMALL).next_to(pos, LEFT, buff=0.1))
        log_label = math(r"\log_{10}(|u|^2 r_c)", color=MUTED, size=MATH_SMALL)
        log_label.next_to(p_low(X_MAX, LOG_HI), UP, buff=0.12).align_to(p_low(X_MAX, 0), RIGHT)

        tracker = ValueTracker(T_START)

        def density():
            u = packet.at(tracker.get_value())[shown]
            return np.abs(u) ** 2

        def wave_shape():
            rho = density()
            pts = [p_top(x, 1 + SCALE * d) for x, d in zip(rs[::2], rho[::2])]
            return pts

        wave = VMobject()

        def update_wave(mob):
            pts = wave_shape()
            outline = [p_top(rs[0], 1)] + pts + [p_top(rs[::2][-1], 1)]
            new = VMobject().set_points_as_corners(outline)
            new.set_stroke(VERMILION, CURVE_WIDTH).set_fill(VERMILION, opacity=0.25)
            mob.become(new)

        update_wave(wave)
        wave.add_updater(update_wave)

        log_curve = VMobject()

        def update_log(mob):
            with np.errstate(divide="ignore"):
                values = np.log10(density()[::2])
            keep = values >= LOG_LO
            pts = [p_low(x, min(v, LOG_HI)) for x, v, k in zip(rs[::2], values, keep) if k]
            if len(pts) < 2:
                pts = [p_low(X_MAX, LOG_LO)] * 2
            mob.become(VMobject().set_points_as_corners(pts).set_stroke(VERMILION, CURVE_WIDTH))

        update_log(log_curve)
        log_curve.add_updater(update_log)

        dot = Dot(radius=DOT_RADIUS * 1.8, color=BLUE)

        def update_dot(mob):
            x = float(model.classical_orbit([tracker.get_value()])[0][0])
            mob.move_to(p_top(x, 1))
            mob.set_opacity(1.0 if x <= X_MAX else 0.0)

        update_dot(dot)
        dot.add_updater(update_dot)

        legend = VGroup(
            VGroup(Dot(radius=DOT_RADIUS * 1.8, color=BLUE),
                   label("classical particle", color=MUTED, size=LABEL_SIZE - 4)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.28, stroke_color=VERMILION, stroke_width=CURVE_WIDTH,
                          fill_color=VERMILION, fill_opacity=0.25),
                   label("quantum", color=MUTED, size=LABEL_SIZE - 4),
                   math(r"|u|^2", color=MUTED, size=MATH_SMALL)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.6)
        legend.move_to(p_top(X_MAX, 0.6)).align_to(p_top(X_MAX, 0), RIGHT)

        self.add(bands, forbidden, potential, energy, drop, drop_low, wave, log_curve,
                 top, low, ticks, rc_top, r_label, v_label, e_label, log_label, legend, dot)
        self.wait(HOLD)
        self.play(tracker.animate.set_value(T_END), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(HOLD)
