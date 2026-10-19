"""Head-on D-T collision seen from above, classical and quantum side by side.

Both panels show the collision plane in real space, centre-of-mass frame,
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
    MUTED, ORANGE, SMALL_SIZE, THIN_WIDTH, VERMILION, StyledScene, label, math,
)
import radial_coulomb as model

X_LO, X_HI = -8.0, 5.4   # collision-axis window of each panel, in r_c (CM at 0)
PANEL_W = 6.6           # panel width, Manim units
PANEL_H = 5.0
SCALE = PANEL_W / (X_HI - X_LO)
CENTRES = (np.array([-3.5, 0.05, 0]), np.array([3.5, 0.05, 0]))
T_START, T_END = 12.0, 58.2     # model time (hbar/E), symmetric about the classical turn 35.1
PLAY_TIME = 12.5
HOLD = 0.6
SIGMA_Y = {"D": 0.42, "T": 0.52}    # illustrative transverse widths, in r_c
DOT_R = {"D": 0.15, "T": 0.20}      # Manim units
COLOR = {"D": BLUE, "T": VERMILION}
INSIDE = ORANGE                     # parts of the clouds with r < r_c
INSIDE_GAIN = 6.0
PX_PER_UNIT = 135                   # 1080p
TONE = 0.55                         # tone-map scale, in units of the incoming peak


def hex_rgb(color):
    return np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)], float) / 255


class CoulombCollision(StyledScene):
    """Classical point particles (left) and quantum clouds (right)."""

    def build(self):
        packet = model.RadialPacket()
        mass_d, mass_t = model.M_D, model.M_T
        x_turn_d, x_turn_t = model.cm_positions(1.0)
        unit_as = model.time_unit_s() * 1e18
        tracker = ValueTracker(T_START)

        def to_scene(panel, x, y=0.0):
            x = x - 0.5 * (X_LO + X_HI)
            return CENTRES[panel] + np.array([x * SCALE, y * SCALE, 0])

        # --- static frame of both panels ---------------------------------
        statics, bands = VGroup(), VGroup()
        headings = []
        for panel, title in enumerate(("Classical", "Quantum")):
            box = Rectangle(width=PANEL_W, height=PANEL_H, stroke_color=GRID,
                            stroke_width=THIN_WIDTH).move_to(CENTRES[panel])
            band = Rectangle(width=SCALE * (x_turn_t - x_turn_d), height=PANEL_H,
                             stroke_width=0, fill_color=GRID, fill_opacity=0.28)
            band.move_to(to_scene(panel, 0.5 * (x_turn_d + x_turn_t)))
            axis = DashedLine(to_scene(panel, X_LO), to_scene(panel, X_HI),
                              dash_length=0.08, stroke_color=FAINT, stroke_width=1.6)
            cm = VGroup(Line(to_scene(panel, 0, -0.25), to_scene(panel, 0, 0.25)),
                        Line(to_scene(panel, -0.25, 0), to_scene(panel, 0.25, 0)))
            cm.set_stroke(INK, 2.0)
            cm_label = label("CM", color=MUTED, size=SMALL_SIZE)
            cm_label.next_to(to_scene(panel, 0, -1.35), DOWN, buff=0)
            # Scale bar r_c between the classical turning positions of D and T.
            y_bar = -0.5 * PANEL_H / SCALE + 0.9
            left, right = to_scene(panel, x_turn_d, y_bar), to_scene(panel, x_turn_t, y_bar)
            bar = VGroup(Line(left, right), Line(left + 0.12 * UP, left + 0.12 * DOWN),
                         Line(right + 0.12 * UP, right + 0.12 * DOWN)).set_stroke(INK, 3.0)
            bar_label = math(r"r_c", color=INK, size=MATH_SIZE).next_to(bar, RIGHT, buff=0.15)
            heading = label(title, color=INK, size=LABEL_SIZE + 6)
            heading.next_to(box, UP, buff=0.18).align_to(box, LEFT).shift(0.1 * RIGHT)
            if headings:
                heading.align_to(headings[0], UP)      # same cap line
            headings.append(heading)
            bands.add(band)
            statics.add(box, axis, cm, cm_label, bar, bar_label, heading)
            inside = math(r"r<r_c", color=INSIDE if panel else MUTED, size=MATH_SMALL)
            inside.next_to(to_scene(panel, 0, 0.5 * PANEL_H / SCALE), DOWN, buff=0.15)
            statics.add(inside)

        clocks = VGroup()
        for panel in (0, 1):
            clock = VGroup(math(r"t =", color=INK, size=MATH_SIZE),
                           DecimalNumber(0.0, num_decimal_places=2, color=INK, font_size=MATH_SIZE),
                           math(r"\mathrm{as}", color=INK, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
            clock.next_to(CENTRES[panel] + np.array([0.5 * PANEL_W, 0.5 * PANEL_H, 0]),
                          UP + LEFT, buff=0.18)
            clock.shift(0.36 * LEFT)
            clocks.add(clock)

        def update_clock(mob):
            mob[1].set_value((tracker.get_value() - T_START) * unit_as)

        for clock in clocks:
            update_clock(clock)
            clock.add_updater(update_clock)

        footer = label("D–T head-on, centre-of-mass frame, same energy E = 7.5 keV (η = 2)",
                       color=MUTED, size=SMALL_SIZE)
        footer.move_to([0, -3.3, 0])

        # --- classical panel: two point particles -------------------------
        dots = {s: Dot(radius=DOT_R[s], color=COLOR[s]) for s in ("D", "T")}
        names = {s: label(s, color=COLOR[s], size=LABEL_SIZE) for s in ("D", "T")}

        def classical_x():
            r = float(model.classical_orbit([tracker.get_value()])[0][0])
            return dict(zip(("D", "T"), model.cm_positions(r)))

        def place(species, panel, get_x):
            def update(mob):
                x = get_x()[species]
                mob.move_to(to_scene(panel, x))
                mob.set_opacity(1.0 if X_LO + 0.3 < x < X_HI - 0.3 else 0.0)
            return update

        def place_name(species, panel, get_x):
            def update(mob):
                x = get_x()[species]
                mob.next_to(to_scene(panel, x, 1.2), UP, buff=0)
                mob.set_opacity(1.0 if X_LO + 0.3 < x < X_HI - 0.3 else 0.0)
            return update

        classical = Group()
        for s in ("D", "T"):
            for mob, maker in ((dots[s], place), (names[s], place_name)):
                maker(s, 0, classical_x)(mob)
                mob.add_updater(maker(s, 0, classical_x))
                classical.add(mob)

        # --- quantum panel: probability clouds -----------------------------
        n_x = int(round(PANEL_W * PX_PER_UNIT))
        n_y = int(round(PANEL_H * PX_PER_UNIT))
        xs = X_LO + (np.arange(n_x) + 0.5) / n_x * (X_HI - X_LO)
        ys = ((np.arange(n_y) + 0.5) / n_y - 0.5) * PANEL_H / SCALE
        profile = {s: np.exp(-ys**2 / (2 * SIGMA_Y[s] ** 2))[:, None] for s in ("D", "T")}
        peak0 = np.max(np.abs(packet.at(T_START)) ** 2)

        def cloud_pixels():
            density = np.abs(packet.at(tracker.get_value())) ** 2 / peak0
            rho_d, rho_t, r_d, r_t = model.marginal_densities(xs, packet.r, density)
            # Show each cloud on the radial scale (rho in units of the incoming peak).
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
        cloud.stretch_to_fit_width(PANEL_W).stretch_to_fit_height(PANEL_H)
        cloud.move_to(CENTRES[1])

        def update_cloud(mob):
            mob.pixel_array = cloud_pixels()

        cloud.add_updater(update_cloud)

        def quantum_x():
            u = packet.at(tracker.get_value())
            mean_r = float(np.sum(packet.r * np.abs(u) ** 2) * packet.dr)
            return dict(zip(("D", "T"), model.cm_positions(mean_r)))

        q_names = Group()
        for s in ("D", "T"):
            mob = label(s, color=COLOR[s], size=LABEL_SIZE)
            place_name(s, 1, quantum_x)(mob)
            mob.add_updater(place_name(s, 1, quantum_x))
            q_names.add(mob)

        # The cloud image sits above the band shading, below frame and labels.
        self.add(bands, cloud, statics, classical, q_names, clocks, footer)
        self.wait(HOLD)
        self.play(tracker.animate.set_value(T_END), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(HOLD)
