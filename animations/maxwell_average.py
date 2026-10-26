"""What the Maxwell average does to sigma(E) v, and where the reduced mass comes from.

MaxwellAverage. Left, over the centre-of-mass energy E (log axis): sigma v of
D-T with the 5He resonance (Bosch-Hale S factor), the Maxwellian weight
K = E f_M(E; T) (dashed, the kernel per d(ln E)) and their product (shaded).
Each curve is scaled to unit maximum by a T-independent constant, so the
shaded area is proportional to <sigma v>(T). k_B T sweeps 1 -> 100 keV,
log T linear in time. Right: <sigma v>(T) from that area, traced point by
point over the Bosch-Hale (1992) parametrisation (faint dashed). On a linear
energy axis the kernel widens with T: the average is a moment of sigma v with
a T-dependent weight, not a translation-invariant convolution in E. Since the
kernel depends on E/T only, in ln E it is a fixed shape shifted by ln T (a
cross-correlation), which is what the log axis shows; the scene writes it as
<sigma v>(T) = int sigma v(u) K(u - s) du with u = ln E, s = ln k_B T.

RelativeVelocity. A genuine convolution, in one dimension at k_B T = 10 keV:
f_rel(g) = int f_D(v) f_T(v - g) dv. f_T slides across f_D, the overlap
product is shaded, its area is f_rel(g), traced below; the result is the
Maxwellian of the reduced mass m_r = m_D m_T/(m_D + m_T) (dashed), because the
variances T/m_D and T/m_T add.
"""

from manim import *
import numpy as np

from style import (
    BLUE, CURVE_WIDTH, FAINT, GREEN, GRID, INK, LABEL_SIZE, LINEAR, MATH_SIZE, MATH_SMALL,
    MUTED, THIN_WIDTH, VERMILION, StyledScene, axes, label, math,
)
import maxwell_average_model as model

T_START, T_END = 1.0, 100.0     # keV
SWEEP = 14.0                    # s
LOG_E = (-0.5, 3.0)             # log10 of E in keV
N_PTS = 600


def ticks(ax, xs, x_texts, ys, y_texts, y0, x0):
    group = VGroup()
    for x, tex in zip(xs, x_texts):
        group.add(math(tex, color=MUTED, size=MATH_SMALL).next_to(ax.c2p(x, y0), DOWN, buff=0.15))
    for y, tex in zip(ys, y_texts):
        group.add(math(tex, color=MUTED, size=MATH_SMALL).next_to(ax.c2p(x0, y), LEFT, buff=0.15))
    return group


def curve(ax, xs, ys, color, width=CURVE_WIDTH):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [ax.c2p(x, y) for x, y in zip(xs, ys)])


class MaxwellAverage(StyledScene):
    """sigma v, the Maxwell kernel, their product and the traced <sigma v>(T)."""

    def build(self):
        left = axes([LOG_E[0], LOG_E[1], 1], [0, 1.15, 0.5], x_length=6.9, y_length=3.8,
                    axis_config={"include_ticks": False})
        left.move_to(np.array([-2.75, -1.05, 0]))
        right = axes([0, 2, 1], [-27, -21, 2], x_length=3.6, y_length=3.8)
        right.move_to(np.array([4.35, -1.05, 0]))

        left_ticks = ticks(left, [0, 1, 2, 3], ["1", "10", "100", "1000"], [], [], 0, LOG_E[0])
        for x in (0, 1, 2, 3):
            left_ticks.add(Line(left.c2p(x, 0), left.c2p(x, 0.03), stroke_color=INK, stroke_width=1.6))
        right_ticks = ticks(right, [0, 1, 2], ["1", "10", "100"], [-27, -25, -23, -21],
                            ["10^{-27}", "10^{-25}", "10^{-23}", "10^{-21}"], -27, 0)
        lx = math(r"E\ [\mathrm{keV}]", color=MUTED, size=MATH_SMALL)
        lx.next_to(left_ticks, DOWN, buff=0.1).align_to(left.x_axis.get_right(), RIGHT)
        rx = math(r"k_BT\ [\mathrm{keV}]", color=MUTED, size=MATH_SMALL)
        rx.next_to(right_ticks[:3], DOWN, buff=0.1).align_to(right.x_axis.get_right(), RIGHT)
        ry = math(r"\langle\sigma v\rangle\ [\mathrm{m^3/s}]", color=MUTED, size=MATH_SMALL)
        ry.next_to(right.y_axis.get_top(), UP, buff=0.2).align_to(right_ticks[3:], LEFT)

        ln10 = np.log(10)
        lg = np.linspace(LOG_E[0], LOG_E[1], N_PTS)
        e = 10**lg
        sv = model.sigma_v(e)
        sv_n = sv / sv.max()
        sv_curve = curve(left, lg, sv_n, INK)
        peak = lg[np.argmax(sv_n)]
        res = label("⁵He resonance", color=INK, size=LABEL_SIZE - 4)
        res.next_to(left.c2p(peak, 1.0), UP, buff=0.12)

        log_t = ValueTracker(np.log(T_START))

        def temp():
            return float(np.exp(log_t.get_value()))

        def kernel_n():
            return model.kernel(e, temp()) / model.KERNEL_MAX

        kernel = always_redraw(lambda: DashedVMobject(curve(left, lg, kernel_n(), BLUE), num_dashes=60,
                                                      dashed_ratio=0.6))

        def product_shape():
            y = sv_n * kernel_n()
            pts = [left.c2p(lg[0], 0)] + [left.c2p(x, v) for x, v in zip(lg, y)] + [left.c2p(lg[-1], 0)]
            return Polygon(*pts, stroke_color=VERMILION, stroke_width=THIN_WIDTH,
                           fill_color=VERMILION, fill_opacity=0.55)

        product = always_redraw(product_shape)

        # Right panel: Bosch-Hale reference and the traced average from the shaded area.
        tt = np.linspace(0, 2, 200)
        bh = DashedVMobject(curve(right, tt, np.log10(model.bosch_hale(10**tt)), FAINT, THIN_WIDTH),
                            num_dashes=50, dashed_ratio=0.5)
        bh_label = VGroup(DashedVMobject(Line(ORIGIN, 0.5 * RIGHT, stroke_color=FAINT, stroke_width=THIN_WIDTH),
                                         num_dashes=3, dashed_ratio=0.5),
                          label("Bosch–Hale", color=FAINT, size=LABEL_SIZE - 4)).arrange(RIGHT, buff=0.12)
        bh_label.next_to(right.c2p(2, -26.8), UP + LEFT, buff=0.1)

        def point():
            t = temp()
            return right.c2p(np.log10(t), np.log10(model.average(t, n=2500)))

        dot = always_redraw(lambda: Dot(point(), radius=0.08, color=VERMILION))
        trace = TracedPath(point, stroke_color=VERMILION, stroke_width=CURVE_WIDTH)

        t_val = DecimalNumber(T_START, num_decimal_places=1, color=INK, font_size=MATH_SIZE)
        row = VGroup(math(r"k_BT =", color=INK), t_val, math(r"\mathrm{keV}", color=INK)).arrange(RIGHT, buff=0.15)
        row.to_corner(UP + RIGHT, buff=0.55)
        x_left, y_row = row.get_left()[0], row.get_center()[1]
        t_val.add_updater(lambda m: m.set_value(temp()))
        row.add_updater(lambda m: m.arrange(RIGHT, buff=0.15).move_to([0, y_row, 0]).align_to(
            [x_left, 0, 0], LEFT))

        def sample(color, dashed):
            line = Line(ORIGIN, 0.6 * RIGHT, stroke_color=color, stroke_width=CURVE_WIDTH)
            return DashedVMobject(line, num_dashes=3, dashed_ratio=0.6) if dashed else line

        swatch = Square(0.3, stroke_color=VERMILION, stroke_width=THIN_WIDTH, fill_color=VERMILION,
                        fill_opacity=0.55)
        legend = VGroup(
            VGroup(sample(INK, False), math(r"\sigma v", color=INK)).arrange(RIGHT, buff=0.15),
            VGroup(sample(BLUE, True), math(r"K = E\,f_M(E;T)", color=BLUE)).arrange(RIGHT, buff=0.15),
            VGroup(swatch, label("product, area ∝ ⟨σv⟩", color=VERMILION)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.55)
        legend.next_to(left, UP, buff=0.7).align_to(left.y_axis, LEFT)
        title = label("Maxwell average of σv, D–T", color=INK, size=LABEL_SIZE + 2)
        title.to_corner(UP + LEFT, buff=0.55)
        # The average as a correlation on the ln E axis: one kernel shape, shifted by ln k_B T.
        formula = VGroup(
            math(r"\langle\sigma v\rangle(T) = \textstyle\int \sigma v(u)\,K(u-s)\,du", color=INK),
            math(r"u = \ln E,\quad s = \ln k_BT", color=MUTED, size=MATH_SMALL),
        ).arrange(RIGHT, buff=0.6)
        formula.next_to(title, DOWN, buff=0.3).align_to(title, LEFT)

        statics = VGroup(left, right, left_ticks, right_ticks, lx, rx, ry, bh, bh_label,
                         sv_curve, res, legend, title, formula)
        self.play(FadeIn(statics), run_time=0.6)
        self.add(product, kernel, trace, dot, row)
        self.bring_to_front(sv_curve)
        self.wait(1.0)
        self.play(log_t.animate.set_value(np.log(T_END)), run_time=SWEEP, rate_func=LINEAR)
        self.wait(2.5)


class RelativeVelocity(StyledScene):
    """1D convolution f_rel(g) = int f_D(v) f_T(v - g) dv at k_B T = 10 keV."""

    def build(self):
        t = 10.0
        s_d, s_t = model.thermal_width(t, model.MC2_D), model.thermal_width(t, model.MC2_T)
        m_r = model.MC2_D * model.MC2_T / (model.MC2_D + model.MC2_T)
        s_r = model.thermal_width(t, m_r)
        g_lim = 3.6

        top = axes([-4, 4, 1], [0, 0.8, 0.2], x_length=8.6, y_length=2.1)
        top.move_to(np.array([-1.75, 1.35, 0]))
        bot = axes([-4, 4, 1], [0, 0.5, 0.25], x_length=8.6, y_length=2.1)
        bot.move_to(np.array([-1.75, -1.55, 0]))
        tk = VGroup(*[math(f"{v}", color=MUTED, size=MATH_SMALL).next_to(bot.c2p(v, 0), DOWN, buff=0.15)
                      for v in range(-4, 5, 2)])
        title = label("Relative velocity of D and T is a convolution", color=INK, size=LABEL_SIZE + 2)
        title.to_corner(UP + LEFT, buff=0.55)
        v = np.linspace(-4, 4, 801)
        f_d = model.gauss(v, s_d)
        g = ValueTracker(-g_lim)
        d_curve = curve(top, v, f_d, BLUE)

        def shifted():
            return DashedVMobject(curve(top, v, model.gauss(v - g.get_value(), s_t), GREEN),
                                  num_dashes=70, dashed_ratio=0.6)

        def overlap():
            y = f_d * model.gauss(v - g.get_value(), s_t)
            pts = [top.c2p(v[0], 0)] + [top.c2p(x, w) for x, w in zip(v, y)] + [top.c2p(v[-1], 0)]
            return Polygon(*pts, stroke_color=VERMILION, stroke_width=THIN_WIDTH, fill_color=VERMILION,
                           fill_opacity=0.55)

        f_t = always_redraw(shifted)
        shade = always_redraw(overlap)
        vv = np.linspace(-12, 12, 2401)

        def point():
            gg = g.get_value()
            return bot.c2p(gg, model.relative_density(gg, vv, s_d, s_t)[0])

        ref = DashedVMobject(curve(bot, v, model.gauss(v, s_r), FAINT, THIN_WIDTH), num_dashes=60,
                             dashed_ratio=0.5)
        dot = always_redraw(lambda: Dot(point(), radius=0.075, color=VERMILION))
        trace = TracedPath(point, stroke_color=VERMILION, stroke_width=CURVE_WIDTH)
        g_mark = always_redraw(lambda: DashedLine(top.c2p(g.get_value(), 0), bot.c2p(g.get_value(), 0),
                                                  dash_length=0.06, stroke_color=GRID, stroke_width=1.6))

        def sample(color, dashed):
            line = Line(ORIGIN, 0.55 * RIGHT, stroke_color=color, stroke_width=CURVE_WIDTH)
            return DashedVMobject(line, num_dashes=3, dashed_ratio=0.6) if dashed else line

        swatch = Square(0.3, stroke_color=VERMILION, stroke_width=THIN_WIDTH, fill_color=VERMILION,
                        fill_opacity=0.55)
        upper = VGroup(
            VGroup(sample(BLUE, False), math(r"f_D(v)", color=BLUE)).arrange(RIGHT, buff=0.15),
            VGroup(sample(GREEN, True), math(r"f_T(v-g)", color=GREEN)).arrange(RIGHT, buff=0.15),
            VGroup(swatch, math(r"f_D(v)\,f_T(v-g)", color=VERMILION)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        upper.next_to(top.c2p(4, 0.8), RIGHT, buff=0.3).align_to(top.c2p(4, 0.8), UP)
        lower = VGroup(
            math(r"f_{\rm rel}(g) =", color=VERMILION, size=MATH_SMALL),
            math(r"\int f_D(v)\,f_T(v-g)\,dv", color=VERMILION, size=MATH_SMALL),
            VGroup(sample(FAINT, True), label("Maxwellian with", color=FAINT, size=LABEL_SIZE - 4)).arrange(RIGHT, buff=0.15),
            math(r"m_r = \frac{m_Dm_T}{m_D+m_T}", color=FAINT, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        lower.next_to(bot.c2p(4, 0.5), RIGHT, buff=0.3).align_to(bot.c2p(4, 0.5), UP)
        labels = VGroup(upper, lower)
        tx = math(r"v,\ g\ [10^6\,\mathrm{m/s}]", color=MUTED, size=MATH_SMALL)
        tx.next_to(tk, DOWN, buff=0.08).align_to(bot.x_axis.get_right(), RIGHT)
        temp_note = math(r"k_BT = 10\ \mathrm{keV,\ 1D}", color=MUTED, size=MATH_SMALL)
        temp_note.to_corner(UP + RIGHT, buff=0.55)
        labels.add(temp_note)
        density = math(r"[10^{-6}\,\mathrm{s/m}]", color=MUTED, size=MATH_SMALL)
        density.next_to(top.y_axis.get_top(), RIGHT, buff=0.15)
        statics = VGroup(top, bot, tk, tx, title, d_curve, ref, labels, density)
        self.play(FadeIn(statics), run_time=0.6)
        self.add(g_mark, shade, f_t, trace, dot)
        self.bring_to_front(d_curve)
        self.wait(0.8)
        self.play(g.animate.set_value(g_lim), run_time=9.0, rate_func=LINEAR)
        self.wait(2.0)
