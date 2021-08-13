%%manim Intro_BankAngle

from manim.mobject.geometry import ArrowTriangleFilledTip
from math import sin, cos, tan, pi
# config.pixel_height = 480
# config.pixel_width = 852
# config.quality = 'low_quality'

def load_c172_image():
    return ImageMobject('C172.png', invert=False) \
                            .scale(0.5)

def create_bank_angle_tracker(initial_angle, lift_vec, rotation_center):
    theta_tracker = ValueTracker(0.0001)
    line1 = DashedLine(ORIGIN, 2*UP)
    line_moving = lift_vec # Line(ORIGIN, UP, stroke_opacity=0.)

    line_ref = line_moving.copy()
    line_moving.rotate(
        theta_tracker.get_value() * DEGREES, about_point=rotation_center
    )
    a = Angle(line1, line_moving, radius=0.5, other_angle=False)
    tex = MathTex(r"\theta").move_to(
        Angle(
            line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
        ).point_from_proportion(0.5)
    )

    l_text = Tex(r"L").move_to(lift_vec.get_end()+ 0.3*UP)
    l_text.add_updater(lambda x: x.move_to(lift_vec.get_end()+0.3*UP))
    bank_angle = Group(line1, line_moving, a, tex, l_text)

    def lift_vec_updater(vec):
        angle = theta_tracker.get_value() * DEGREES
        if abs(angle) < 0.0001 * DEGREES: 
            angle = 0.0001 * np.sign(angle)
        return vec.become(line_ref.copy()).rotate(
            angle, about_point=rotation_center
        )

    line_moving.add_updater(lift_vec_updater)

    def angle_updater(a):
        angle = theta_tracker.get_value() * DEGREES
        try:
            return a.become(Angle(line1, line_moving, radius=0.5, other_angle=angle < 0))
        except:
            return a

    a.add_updater(angle_updater)
    def tex_updater(t):
        angle = theta_tracker.get_value() * DEGREES
        if abs(angle) < 5 * DEGREES:
            return t.set_stroke_opacity(0.)
        else:
            return t.move_to(
                Angle(
                    line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=angle < 0
                ).point_from_proportion(0.5)
            ).set_stroke_opacity(1.0)

    tex.add_updater(tex_updater)

    return theta_tracker, bank_angle
        
class Intro_BankAngle(Scene):
    def construct(self):
        section_title = create_section_title("Lift Modulation")
        self.play(FadeIn(section_title, shift=RIGHT), runtime=0.5)

        g_vec = Vector(2*DOWN, color=RED)
        
        c172 = load_c172_image()
        lift_vec = Vector(2*UP, color=GREEN)
        self.add(c172, lift_vec)
        
        bank_angle_tracker, bank_angle = create_bank_angle_tracker(0, lift_vec, rotation_center=ORIGIN)

        def plane_rotater(p):
            angle = bank_angle_tracker.get_value() * DEGREES
            return p.become(load_c172_image().rotate(
                angle, about_point=ORIGIN
            ))

        c172.add_updater(plane_rotater)
        self.add(g_vec)
        self.add(Tex(r'W').move_to(g_vec.get_end()+0.5*RIGHT))

        self.add(bank_angle)
        self.play(bank_angle_tracker.animate.set_value(45))
        self.wait(2)
        self.play(bank_angle_tracker.animate.set_value(-45))
        self.wait(2)
        self.play(bank_angle_tracker.animate.set_value(-0.0001), FadeOut(bank_angle[3]))
        self.wait(1)

