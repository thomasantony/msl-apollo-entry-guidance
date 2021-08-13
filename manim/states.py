%%manim DynamicModelPage1_States

from manim.mobject.geometry import ArrowTriangleFilledTip

# config.pixel_height = 480
# config.pixel_width = 852
# config.quality = 'low_quality'

from math import sin, cos, tan, pi

planet_center = 2*RIGHT + 12*DOWN # absolute coordinates
planet_radius = 10
aeroshell_center = 2.5*UP+2*RIGHT # absolute coordinates
downrange_angle = 20*pi/180
fpa = -15 * pi/180

def create_aeroshell_image():
    return ImageMobject('msl-aeroshell.png', invert=True)\
                            .shift(0.05*UP-0.2*RIGHT)\
                            .scale(0.33) \
                            .rotate(TAU/2)

def create_altitude_line():
    return DashedLine(aeroshell_center, 
                            aeroshell_center + 4.5*DOWN, 
                            dashed_ratio=0.5, 
                            color=GREY)

def create_lander_with_animation(lander_final_pos):
    lander_rotate_angle = -60*pi/180
    lander_final_scale = 0.25

    lander_path = ArcBetweenPoints(aeroshell_center,
                                    lander_final_pos,
                                    angle=-pi/3,
                                    color=GREY_C,
                                    stroke_opacity=0.5)

    lander = create_aeroshell_image()

    fake_lander = lander.copy().scale(0.)
    lander_path_tracker = MoveAlongPath(fake_lander, lander_path)
    scale_tracker = ValueTracker(1.0)
    angle_tracker = ValueTracker(0.0)
    lander_img = lander[0].get_pixel_array()

    def lander_updater(lnd):
        scale = scale_tracker.get_value()
        angle = angle_tracker.get_value()
        pos = fake_lander.get_center()
        return lnd.become(create_aeroshell_image() \
                            .scale(scale) \
                            .rotate(angle)\
                            .move_to(pos))

    lander.add_updater(lander_updater)
    
    lander_flight = AnimationGroup(
        lander_path_tracker,
        scale_tracker.animate().set_value(lander_final_scale),
        angle_tracker.animate().set_value(lander_rotate_angle)
    )
    return lander, lander_flight

class DynamicModelPage1_States(Scene):
    """Shows and explains states in the 2DOF dynamic model"""

    def add_section_title(self):
        titlebar = Text('2DOF Dynamic Model') \
                    .scale(0.75) \
                    .to_edge(LEFT, buff=0.5) \
                    .to_edge(DOWN, buff=0.1)

        titlebar_box = Rectangle(color=BLUE, 
                                 width=config.frame_width,
                                 height=0.75,
                                 fill_opacity=1) \
                        .to_edge(DOWN, buff=0)        
        titlebar.move_to(titlebar_box, ORIGIN).to_edge(LEFT, buff=0.5).to_edge(DOWN, 0.1)
        section_titlebar = Group(titlebar_box, titlebar)
        return section_titlebar
        
    def create_slide_content(self, title: str, content):
        slide_title = Text(title, color=YELLOW).scale(0.75)
        slide_content = VGroup(slide_title, content).arrange(DOWN, buff=0.5)
        return slide_content.to_corner(UL, buff=0.5)

    def create_aeroshell(self):
        aeroshell_img = create_aeroshell_image()
        aeroshell_cg = Dot(ORIGIN, color=RED, radius=0.04)
        aeroshell = Group(aeroshell_img, aeroshell_cg)\
                            .shift(aeroshell_center)
        return aeroshell

    def add_planet_surface(self):
        if getattr(self, 'planet_surface', None) is not None:
            self.remove(self.planet_surface)
        planet_edge = Arc(planet_radius, 135*pi/180, -90*pi/180, 
                             arc_center=planet_center + 3*DOWN,
                             color=RED_C)
        planet_label = Text('Surface of planet').scale(0.5) \
                                .shift(2*RIGHT + 5.5*DOWN) # 2.5 to show
        planet_surface = Group(planet_edge, planet_label)
        self.add(planet_surface)
        return planet_surface

    
    def add_altitude_desc(self):
        alt_line = create_altitude_line()
        alt_brace = Brace(alt_line, LEFT, color=GREY)
        alt_label = alt_brace.get_tex(r"\text{Altitude }", r"h")    \
                            .set_stroke_opacity(0.5)
        alt_label.set_color_by_tex('h', YELLOW)
        altitude_desc = Group(alt_line, alt_brace, alt_label)
        self.add(altitude_desc)
        return altitude_desc

    def create_velocity_vector(self):
        velocity_vec = Vector(direction=[3*cos(fpa), 3*sin(fpa), 0], color=GREY) \
                    .shift(aeroshell_center)
        velocity_label = Group(
                            Tex(r'$\vec{v}$').scale(0.7) \
                            .set_color(GREY_A)
                        ) \
                        .arrange(DOWN, buff=0.1)\
                        .next_to(velocity_vec, DOWN, buff=0.1) \
                        .shift(0.35*UP)
        velocity_vector = Group(velocity_vec, velocity_label)
        return velocity_vector

    def add_velocity_desc(self):
        velocity_vec = self.create_velocity_vector()

        velocity_label = velocity_vec[1]
        velocity_mag = MathTex(r'v = |\vec{v}|') \
                            .set_color(YELLOW) \
                            .next_to(velocity_label, DOWN)
        velocity_desc = velocity_mag
        self.add(velocity_desc)
        return Group(velocity_vec, velocity_desc)
    
    def add_fpa_desc(self):
        local_horizon = self.create_local_horizon()
        velocity_vec = self.create_velocity_vector()

        fpa_arc = Arc(2.0, 0.0, fpa, arc_center=aeroshell_center, color=YELLOW)
        fpa_label = MathTex(r'\gamma', color=YELLOW) \
                        .scale(0.8) \
                        .next_to(fpa_arc, RIGHT, buff=0.1)
        fpa_desc = Group(local_horizon, velocity_vec, fpa_arc, fpa_label)

        self.add(fpa_desc)
        return fpa_desc

    def add_downrange_desc(self):
        # Downrange
        alt_line = create_altitude_line()

        downrange_arc = Arc(radius = planet_radius + 0.5, 
                            arc_center = planet_center,
                            start_angle = pi/2, angle = -downrange_angle,
                            color = YELLOW_D) \
                        .add_tip(at_start=True, tip_shape=ArrowTriangleFilledTip) \
                        .add_tip(tip_shape=ArrowTriangleFilledTip)

        downrange_dir_vec = np.array([cos(pi/2-downrange_angle), 
                                        sin(pi/2-downrange_angle), 0])
        downrange_line = DashedLine(
            planet_center + downrange_dir_vec * planet_radius,
            planet_center + downrange_dir_vec *(planet_radius + 3),
            dashed_ratio = 0.5,
            color=GREY
        )

        downrange_label_dir = np.array([cos(pi/2-downrange_angle/2), 
                                        sin(pi/2-downrange_angle/2), 0])
        downrange_label = MathTex('s', color=YELLOW) \
                    .move_to(planet_center) \
                    .shift(downrange_label_dir * (planet_radius + 0.75))
        
        # Lander
        lander_final_pos = planet_center \
                     + downrange_dir_vec * (planet_radius + 1) \
                     + 0.2*LEFT + 0.2*DOWN
        lander, lander_anim = create_lander_with_animation(lander_final_pos)
        
        downrange_desc = Group(alt_line, 
                               downrange_arc, 
                               downrange_line, 
                               downrange_label,
                         )
        return downrange_desc, lander, lander_anim, AnimationGroup(
            Create(alt_line),
            GrowFromCenter(downrange_arc),
            FadeIn(downrange_line),
            FadeIn(downrange_label)
        )


    def create_local_horizon(self):
        horizon_line = DashedLine(aeroshell_center,
                                  aeroshell_center+4*RIGHT,
                                  dash_length=0.4,
                                  dashed_ratio=0.6, color=GREY_D)
        horizon_label = Text('Local Horizon') \
                            .next_to(horizon_line, UP, buff=0.05) \
                            .scale(0.3) \
                            .shift(1.0*RIGHT)
        local_horizon = Group(horizon_line, horizon_label)
        return local_horizon

    def add_highlight_to_state(self, state_list, idx):
        """User's responsibility to get rid of box"""        
        box = SurroundingRectangle(state_list.get_rows()[idx])
        state_list.add(box)
        return box

    def construct(self):
        states = ['h', 's', 'v', r'\gamma']
        state_list = Matrix([[x] for x in states])
        slide_text = MathTex(r'\textbf{x} =')

        state_def = VGroup(slide_text, state_list) \
                    .arrange(RIGHT, buff=0.5)
        
        # Show aeroshell and planet
        aeroshell = self.create_aeroshell()
        planet = self.add_planet_surface()

        # Add first to be at bottom layer before title
        self.add(planet)

        section_title = self.add_section_title()
        
        # # Used for testing
        # self.add(aeroshell)
        # self.add(planet.shift(3*UP), aeroshell)
        
        # Section title
        self.play(FadeIn(section_title, shift=RIGHT), runtime=0.5)
        self.wait(1)

        slide_content = self.create_slide_content('States', state_def)
        self.play(Write(slide_content))

        self.play(FadeIn(aeroshell), planet.animate().shift(3*UP))
        
        self.wait(2)
        
        # Altitude
        box = self.add_highlight_to_state(state_list, 0)
        alt_desc = self.add_altitude_desc()
        self.play(Create(box), FadeIn(alt_desc))
        self.wait(3)
        self.play(FadeOut(box), FadeOut(alt_desc))
        state_list.remove(box)
        self.remove(box)

        # Downrange
        box = self.add_highlight_to_state(state_list, 1)
        s_desc, lander, lander_anim, s_desc_anim = self.add_downrange_desc()
        self.add(lander)
        self.play(Create(box), lander_anim, runtime=1.0)
        self.play(s_desc_anim)
        self.wait(3)
        self.play(FadeOut(box), FadeOut(lander), FadeOut(s_desc))
        state_list.remove(box)
        self.remove(box)
        
        # Velocity
        box = self.add_highlight_to_state(state_list, 2)
        vel_desc = self.add_velocity_desc()
        self.play(Create(box), FadeIn(vel_desc))
        self.wait(3)
        self.play(FadeOut(box), FadeOut(vel_desc))
        state_list.remove(box)
        self.remove(box)

        # FPA
        box = self.add_highlight_to_state(state_list, 3)
        fpa_desc = self.add_fpa_desc()
        self.play(Create(box), FadeIn(fpa_desc))
        self.wait(3)
        self.play(FadeOut(box), FadeOut(fpa_desc))
        state_list.remove(box)
        self.remove(box)

        # Clean up
        self.wait(1)
        self.play(FadeOut(planet), FadeOut(aeroshell), FadeOut(slide_content), FadeOut(section_title, shift=LEFT))
        self.wait(2)
