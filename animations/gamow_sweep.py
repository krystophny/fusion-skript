"""Gamow peak of D-T while the temperature rises from 2 to 60 keV.

On one logarithmic axis over the centre-of-mass energy E: the Maxwell factor
exp(-E/k_B T), the tunnelling factor exp(-sqrt(E_G/E)) (fixed, E_G = 1182 keV
for D-T) and their product, whose maximum lies at the Gamow energy
E_0 = (E_G (k_B T)^2/4)^(1/3) with 1/e full width 4 sqrt(E_0 k_B T/3) (shaded).
The peak value is exp(-3 E_0/k_B T). k_B T grows exponentially in time
(log T linear), so equal times are equal temperature ratios. The traced path
shows the peak moving to higher energy and growing by almost five decades.

B_G = sqrt(E_G) = 34.3827 keV^(1/2): Bosch and Hale, Nucl. Fusion 32, 611 (1992);
the same value as data/ch02/cross-sections.json.
"""

from manim import *
import numpy as np

from style import (
    BLUE, CURVE_WIDTH, FAINT, GREEN, GRID, INK, LABEL_SIZE, LINEAR, MATH_SIZE, MATH_SMALL,
    MUTED, THIN_WIDTH, VERMILION, StyledScene, axes, label, math,
)

E_G = 34.3827 ** 2          # keV
T_START, T_END = 2.0, 60.0  # keV
E_MAX = 250.0               # keV
LOG_MIN = -12               # lowest decade shown
SWEEP = 12.0                # s
N_PTS = 500


def gamow(t):
    e0 = (E_G * t**2 / 4) ** (1 / 3)
    return e0, 4 * np.sqrt(e0 * t / 3)


class GamowSweep(StyledScene):
    """Maxwell tail times tunnelling factor, swept in temperature."""

    def build(self):
        ax = axes([0, E_MAX, 50], [LOG_MIN, 0, 4], x_length=7.9, y_length=5.3)
        ax.move_to(np.array([-1.2, -0.3, 0]))
        x_ticks = VGroup(*[math(f"{v}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, LOG_MIN), DOWN, buff=0.15)
                           for v in range(0, int(E_MAX) + 1, 50)])
        y_ticks = VGroup(*[math(f"10^{{{v}}}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                           for v in range(LOG_MIN, 1, 4)])
        x_title = math(r"E\ [\mathrm{keV}]", color=MUTED, size=MATH_SMALL)
        x_title.next_to(x_ticks, DOWN, buff=0.12).align_to(ax.x_axis.get_right(), RIGHT)
        y_title = label("factor", color=MUTED, size=LABEL_SIZE - 4)
        y_title.next_to(ax.y_axis.get_top(), UP, buff=0.2).align_to(y_ticks, LEFT)
        grid = VGroup(*[Line(ax.c2p(0, v), ax.c2p(E_MAX, v), stroke_color=GRID, stroke_width=1.0)
                        for v in range(LOG_MIN + 4, 1, 4)])

        log_t = ValueTracker(np.log(T_START))
        e = np.linspace(E_MAX / N_PTS, E_MAX, N_PTS)

        def poly(log10_y, color, width=CURVE_WIDTH):
            keep = log10_y >= LOG_MIN
            pts = [ax.c2p(x, y) for x, y in zip(e[keep], np.minimum(log10_y[keep], 0.3))]
            return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)

        tunnel_log = -np.sqrt(E_G / e) / np.log(10)
        tunnel = DashedVMobject(poly(tunnel_log, GREEN), num_dashes=110, dashed_ratio=0.35)

        def temp():
            return float(np.exp(log_t.get_value()))

        maxwell = always_redraw(lambda: DashedVMobject(
            poly(-e / temp() / np.log(10), BLUE), num_dashes=70, dashed_ratio=0.6))
        product = always_redraw(lambda: poly(-e / temp() / np.log(10) + tunnel_log, VERMILION))

        def window():
            e0, w = gamow(temp())
            lo, hi = max(e0 - w / 2, 0), min(e0 + w / 2, E_MAX)
            band = Polygon(ax.c2p(lo, LOG_MIN), ax.c2p(hi, LOG_MIN), ax.c2p(hi, 0), ax.c2p(lo, 0),
                           stroke_width=0, fill_color=VERMILION, fill_opacity=0.13)
            line = DashedLine(ax.c2p(e0, LOG_MIN), ax.c2p(e0, 0), dash_length=0.07,
                              stroke_color=FAINT, stroke_width=THIN_WIDTH)
            return VGroup(band, line)

        band = always_redraw(window)

        def peak_point():
            e0, _ = gamow(temp())
            return ax.c2p(e0, -3 * e0 / temp() / np.log(10))

        dot = always_redraw(lambda: Dot(peak_point(), radius=0.085, color=VERMILION))
        path = TracedPath(peak_point, stroke_color=VERMILION, stroke_width=2.0, stroke_opacity=0.7)

        # Readouts, top left inside the axes
        t_val = DecimalNumber(T_START, num_decimal_places=1, color=INK, font_size=MATH_SIZE)
        e_val = DecimalNumber(gamow(T_START)[0], num_decimal_places=1, color=VERMILION, font_size=MATH_SIZE)
        row_t = VGroup(math(r"k_BT =", color=INK), t_val, math(r"\mathrm{keV}", color=INK)).arrange(RIGHT, buff=0.15)
        row_e = VGroup(math(r"E_0 =", color=VERMILION), e_val, math(r"\mathrm{keV}", color=VERMILION)).arrange(RIGHT, buff=0.15)
        readout = VGroup(row_t, row_e).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        readout.next_to(ax.c2p(E_MAX, 0), RIGHT, buff=0.7).align_to(ax.c2p(0, 0), UP)
        left = readout.get_left()[0]
        t_val.add_updater(lambda m: m.set_value(temp()))
        e_val.add_updater(lambda m: m.set_value(gamow(temp())[0]))
        for row in (row_t, row_e):
            y = row.get_center()[1]
            # Re-space each frame: the number changes width as it grows.
            row.add_updater(lambda m, y=y: m.arrange(RIGHT, buff=0.15).move_to([0, y, 0]).align_to(
                [left, 0, 0], LEFT))

        # Legend: line samples with the same dash patterns as the curves
        def sample(color, dash):
            line = Line(ORIGIN, 0.7 * RIGHT, stroke_color=color, stroke_width=CURVE_WIDTH)
            return DashedVMobject(line, num_dashes=dash[0], dashed_ratio=dash[1]) if dash else line

        legend = VGroup(
            VGroup(sample(BLUE, (3, 0.6)), math(r"e^{-E/k_BT}", color=BLUE)),
            VGroup(sample(GREEN, (5, 0.35)), math(r"e^{-\sqrt{E_G/E}}", color=GREEN)),
            VGroup(sample(VERMILION, None), label("product", color=VERMILION)),
        )
        for row in legend:
            row.arrange(RIGHT, buff=0.2)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        legend.next_to(readout, DOWN, buff=0.7).align_to(readout, LEFT)
        names = VGroup(label("Maxwell tail", color=BLUE, size=LABEL_SIZE - 4),
                       label("tunnelling", color=GREEN, size=LABEL_SIZE - 4))
        for name, row in zip(names, legend[:2]):
            name.next_to(row, DOWN, buff=0.08).align_to(row[1], LEFT)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.62).next_to(readout, DOWN, buff=0.7).align_to(readout, LEFT)
        for name, row in zip(names, legend[:2]):
            name.next_to(row, DOWN, buff=0.08).align_to(row[1], LEFT)
        legend.add(names)
        title = label("D–T: Gamow peak as the plasma heats up", color=INK, size=LABEL_SIZE + 4)
        title.to_corner(UP + LEFT, buff=0.55)

        statics = VGroup(grid, ax, x_ticks, y_ticks, x_title, y_title, tunnel, title)
        self.play(FadeIn(statics), run_time=0.6)
        self.add(band, maxwell, product, path, dot, legend, readout)
        self.wait(1.2)
        self.play(log_t.animate.set_value(np.log(T_END)), run_time=SWEEP, rate_func=LINEAR)
        self.wait(2.0)
