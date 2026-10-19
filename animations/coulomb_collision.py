"""Head-on D-T collision seen from above: classical, quantum, then both.

Three parts on the same clock, axes, scale and r_c marker: the classical
collision alone, the quantum collision alone, both side by side. Every panel shows the collision plane in real space, centre-of-mass frame,
head-on (l = 0), at the same energy E (eta = 2, D-T at 7.5 keV) and on the
same clock. The separation r of the two nuclei sets their positions on the
collision axis, x_D = -(m_T/M) r and x_T = +(m_D/M) r (radial_coulomb.py).

Left, classical: two point particles; r(t) from the energy quadrature
(classical_orbit). They slow down, turn at the separation r_c and fly apart.

Right, quantum: the same view with each nucleus a probability cloud. Along the
axis the clouds are the marginal densities of x_D and x_T obtained from the
radial |u(r, t)|^2 of the l = 0 wave packet by the same relations; across the
axis they get a fixed Gaussian width only for visibility. During reflection
incoming and outgoing waves interfere (fringes). The parts of the clouds that
stand for separations r < r_c (the band between the classical turning
positions) are drawn in a separate, brightened color.
"""

from manim import *
import numpy as np

from style import (
    BLUE, FAINT, GRID, INK, LABEL_SIZE, LINEAR, MATH_SIZE, MATH_SMALL,
    MUTED, ORANGE, THIN_WIDTH, VERMILION, StyledScene, label, math,
)
import radial_coulomb as model

X_LO, X_HI = -8.0, 5.4   # collision-axis window of each panel, in r_c (CM at 0)
PANEL_W = 6.6           # panel width, Manim units
PANEL_H = 5.0
SOLO_W = 12.6           # full-width panel, same axis window
CENTRES = (np.array([-3.5, 0.05, 0]), np.array([3.5, 0.05, 0]))
SOLO_CENTRE = np.array([0.0, 0.05, 0])
T_START, T_END = 12.0, 58.2     # model time (hbar/E), symmetric about the classical turn 35.1
PLAY_TIME = 10.5        # per part
HOLD = 0.4
FADE = 0.4
SIGMA_Y = {"D": 0.42, "T": 0.52}    # illustrative transverse widths, in r_c
DOT_R = {"D": 0.035, "T": 0.0525}   # Manim units: ~9 and 14 px, << r_c (66 px)
COLOR = {"D": BLUE, "T": VERMILION}
INSIDE = ORANGE                     # parts of the clouds with r < r_c
INSIDE_GAIN = 6.0
PX_PER_UNIT = 135                   # 1080p
TONE = 0.55                         # tone-map scale, in units of the incoming peak


def hex_rgb(color):
    return np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)], float) / 255


class CoulombCollision(StyledScene):
    """Classical point particles, quantum clouds, then both side by side."""

    def build(self):
        packet = model.RadialPacket()
        mass_d, mass_t = model.M_D, model.M_T
        x_turn_d, x_turn_t = model.cm_positions(1.0)
        unit_as = model.time_unit_s() * 1e18
        tracker = ValueTracker(T_START)
        peak0 = np.max(np.abs(packet.at(T_START)) ** 2)

        def classical_x():
            r = float(model.classical_orbit([tracker.get_value()])[0][0])
            return dict(zip(("D", "T"), model.cm_positions(r)))

        def quantum_x():
            u = packet.at(tracker.get_value())
            mean_r = float(np.sum(packet.r * np.abs(u) ** 2) * packet.dr)
            return dict(zip(("D", "T"), model.cm_positions(mean_r)))

        def make_panel(title, centre, width, quantum):
            """Layers (bottom to top) of one panel; the scale follows its width."""
            scale = width / (X_HI - X_LO)

            def to_scene(x, y=0.0):
                return centre + np.array([(x - 0.5 * (X_LO + X_HI)) * scale, y, 0])

            box = Rectangle(width=width, height=PANEL_H, stroke_color=GRID,
                            stroke_width=THIN_WIDTH).move_to(centre)
            band = Rectangle(width=scale * (x_turn_t - x_turn_d), height=PANEL_H,
                             stroke_width=0, fill_color=GRID, fill_opacity=0.28)
            band.move_to(to_scene(0.5 * (x_turn_d + x_turn_t)))
            axis = DashedLine(to_scene(X_LO), to_scene(X_HI), dash_length=0.08,
                              stroke_color=FAINT, stroke_width=1.6)
            cm = VGroup(Line(to_scene(0, -0.12), to_scene(0, 0.12)),
                        Line(to_scene(0) + 0.12 * LEFT, to_scene(0) + 0.12 * RIGHT))
            cm.set_stroke(INK, 2.0)
            # Scale bar r_c between the classical turning positions of D and T.
            y_bar = -0.5 * PANEL_H + 0.45
            left, right = to_scene(x_turn_d, y_bar), to_scene(x_turn_t, y_bar)
            bar = VGroup(Line(left, right), Line(left + 0.12 * UP, left + 0.12 * DOWN),
                         Line(right + 0.12 * UP, right + 0.12 * DOWN)).set_stroke(INK, 3.0)
            bar_label = math(r"r_c", color=INK, size=MATH_SIZE).next_to(bar, RIGHT, buff=0.15)
            heading = label(title, color=INK, size=LABEL_SIZE + 6)
            heading.next_to(box, UP, buff=0.18).align_to(box, LEFT).shift(0.1 * RIGHT)
            heading.shift((box.get_top()[1] + 0.57 - heading.get_top()[1]) * UP)  # common cap line
            inside = math(r"r<r_c", color=INSIDE if quantum else MUTED, size=MATH_SMALL)
            inside.next_to(to_scene(0, 0.5 * PANEL_H), DOWN, buff=0.15)
            statics = VGroup(box, axis, cm, bar, bar_label, heading, inside)

            clock = VGroup(math(r"t =", color=INK, size=MATH_SIZE),
                           DecimalNumber(0.0, num_decimal_places=2, color=INK, font_size=MATH_SIZE),
                           math(r"\mathrm{as}", color=INK, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
            clock.next_to(centre + np.array([0.5 * width, 0.5 * PANEL_H, 0]),
                          UP + LEFT, buff=0.18)
            clock.shift(0.36 * LEFT)

            def update_clock(mob):
                mob[1].set_value((tracker.get_value() - T_START) * unit_as)

            update_clock(clock)
            clock.add_updater(update_clock)

            def follow(species, get_x, mob, dy):
                def update(m):
                    x = get_x()[species]
                    m.move_to(to_scene(x, dy)) if dy == 0 else m.next_to(to_scene(x, dy), UP, buff=0)
                    m.set_opacity(1.0 if X_LO + 0.3 < x < X_HI - 0.3 else 0.0)
                update(mob)
                mob.add_updater(update)
                return mob

            below = Group(band)
            moving = Group()
            if not quantum:
                for s in ("D", "T"):
                    moving.add(follow(s, classical_x, Dot(radius=DOT_R[s], color=COLOR[s]), 0))
                    moving.add(follow(s, classical_x, label(s, color=COLOR[s], size=LABEL_SIZE), 0.6))
                return below, statics, moving, clock

            n_x = int(round(width * PX_PER_UNIT))
            n_y = int(round(PANEL_H * PX_PER_UNIT))
            xs = X_LO + (np.arange(n_x) + 0.5) / n_x * (X_HI - X_LO)
            ys = ((np.arange(n_y) + 0.5) / n_y - 0.5) * PANEL_H / scale
            profile = {s: np.exp(-ys**2 / (2 * SIGMA_Y[s] ** 2))[:, None] for s in ("D", "T")}

            def cloud_pixels():
                density = np.abs(packet.at(tracker.get_value())) ** 2 / peak0
                rho_d, rho_t, r_d, r_t = model.marginal_densities(xs, packet.r, density)
                # Each cloud on the radial scale (rho in units of the incoming peak).
                rho = {"D": rho_d * mass_t / (mass_d + mass_t), "T": rho_t * mass_d / (mass_d + mass_t)}
                sep = {"D": r_d, "T": r_t}
                rgb = np.zeros((n_y, n_x, 3))
                for s in ("D", "T"):
                    inner = (sep[s] < 1.0) & (sep[s] > 0)
                    gain = np.where(inner, INSIDE_GAIN, 1.0)[None, :]
                    level = 1 - np.exp(-gain * rho[s][None, :] * profile[s] / TONE)
                    color = np.where(inner[:, None], hex_rgb(INSIDE), hex_rgb(COLOR[s]))
                    rgb += level[..., None] * color[None, :, :]
                # Straight alpha so that the r < r_c band shading stays underneath.
                alpha = np.clip(rgb.max(axis=2, keepdims=True), 0, 1)
                color = np.clip(rgb / np.maximum(alpha, 1e-6), 0, 1)
                return np.round(255 * np.concatenate([color, alpha], 2)).astype(np.uint8)

            cloud = ImageMobject(cloud_pixels())
            cloud.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
            cloud.stretch_to_fit_width(width).stretch_to_fit_height(PANEL_H)
            cloud.move_to(centre)
            cloud.add_updater(lambda mob: setattr(mob, "pixel_array", cloud_pixels()))
            below.add(cloud)
            for s in ("D", "T"):
                moving.add(follow(s, quantum_x, label(s, color=COLOR[s], size=LABEL_SIZE), 0.6))
            return below, statics, moving, clock

        def show(*panels):
            """The cloud image sits above the band, below frame and labels."""
            layers = [Group(*[p[i] for p in panels]) for i in range(4)]
            whole = Group(*layers)
            self.add(*layers)
            self.play(FadeIn(whole), run_time=FADE)
            return whole

        def run(whole, last=False):
            self.wait(HOLD)
            tracker.set_value(T_START)
            self.play(tracker.animate.set_value(T_END), run_time=PLAY_TIME, rate_func=LINEAR)
            self.wait(HOLD)
            if last:
                return
            self.play(FadeOut(whole), run_time=FADE)
            for mob in whole.get_family():
                mob.clear_updaters()
            self.remove(*whole.submobjects)

        tracker.set_value(T_START)
        run(show(make_panel("Classical", SOLO_CENTRE, SOLO_W, False)))
        run(show(make_panel("Quantum", SOLO_CENTRE, SOLO_W, True)))
        run(show(make_panel("Classical", CENTRES[0], PANEL_W, False),
                 make_panel("Quantum", CENTRES[1], PANEL_W, True)), last=True)
