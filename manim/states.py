%%manim DynamicModelPage1_States

config.pixel_height = 480
config.pixel_width = 852
config.quality = 'low_quality'

from math import sin, cos, tan, pi

aeroshell_center = 2.5*UP+2*RIGHT
fpa = -15 * pi/180

class DynamicModelPage1_States(Scene):
    """Shows and explains states in the 2DOF dynamic model"""

    def add_section_title(self):
        titlebar = Text('2DOF Dynamic Model', should_center=False) \
                    .scale(0.75) \
                    .to_edge(LEFT, buff=0.5) \
                    .to_edge(DOWN, buff=0.1)

        titlebar_box = Rectangle(color=BLUE, 
                                 width=config.frame_width,
                                 height=0.75,
                                 fill_opacity=1) \
                        .to_edge(DOWN, buff=0)        
        titlebar.move_to(titlebar_box, ORIGIN).to_edge(LEFT, buff=0.5).to_edge(DOWN, 0.1)
        section_titlebar = Group(titlebar, titlebar_box)
        self.add(section_titlebar)
        # self.play(FadeIn(titlebar_box), runtime=0.5)
        return section_titlebar
        
    def add_slide_content(self, title: str, content):
        slide_title = Text(title, color=YELLOW).scale(0.75)
        slide_content = VGroup(slide_title, content).arrange(DOWN, buff=0.5)
        self.add(slide_content.to_corner(UL, buff=0.5))

    def add_aeroshell(self):
        if getattr(self, 'aeroshell', None) is not None:
            self.remove(self.aeroshell)
        aeroshell_img = ImageMobject('msl-aeroshell.png', invert=True)\
                                .shift(0.05*UP+0.2*RIGHT)\
                                .scale(0.33)
        aeroshell_cg = Dot(ORIGIN, color=RED, radius=0.04)
        aeroshell = Group(aeroshell_img, aeroshell_cg)\
                            .shift(aeroshell_center)
        self.add(aeroshell)
        return aeroshell

    def add_planet_surface(self):
        if getattr(self, 'planet_surface', None) is not None:
            self.remove(self.planet_surface)
        planet_edge = Arc(10, 135*pi/180, -90*pi/180, 
                             arc_center=(2, -15, 0), # (2, -12, 0)
                             color=RED_C)
        planet_label = Text('Surface of planet').scale(0.5) \
                                .shift(2*RIGHT + 5.5*DOWN) # 2.5 to show
        planet_surface = Group(planet_edge, planet_label)
        self.add(planet_surface)
        return planet_surface

    def add_altitude_explanation(self):
        alt_line = DashedLine(aeroshell_center, 
                              aeroshell_center + 4.5*DOWN, 
                              dashed_ratio=0.5, 
                              color=GREY)
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
                            Text('Velocity').scale(0.5),
                            Tex(r'$\vec{v}$').scale(0.7) \
                            .set_color(GREY_A)
                        ) \
                        .arrange(DOWN, buff=0.1)\
                        .next_to(velocity_vec, DOWN, buff=0.1) \
                        .shift(0.35*UP)
        velocity_vector = Group(velocity_vec, velocity_label)
        return velocity_vector

    def add_velocity_explanation(self):
        velocity_vec = self.create_velocity_vector()

        velocity_label = velocity_vec[1]
        velocity_mag = MathTex(r'v = |\vec{v}|') \
                            .set_color(YELLOW) \
                            .next_to(velocity_label, DOWN)
        velocity_desc = velocity_mag
        self.add(velocity_desc)
        return Group(velocity_vec, velocity_desc)
    
    def add_fpa_explanation(self):
        local_horizon = self.create_local_horizon()
        velocity_vec = self.create_velocity_vector()

        fpa_arc = Arc(2.0, 0.0, fpa, arc_center=aeroshell_center, color=YELLOW)
        fpa_label = MathTex(r'\gamma', color=YELLOW) \
                        .next_to(fpa_arc, RIGHT, buff=0.1)
        fpa_desc = Group(local_horizon, velocity_vec, fpa_arc, fpa_label)

        self.add(fpa_desc)
        return fpa_desc

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

    def create_state_list(self, states):
        state_list = Matrix([[x] for x in states])
        slide_text = MathTex(r'\textbf{x} =')

        state_def = VGroup(slide_text, state_list) \
                    .arrange(RIGHT, buff=0.5)
        return state_def, state_list

    def add_highlight_to_state(self, state_list, idx):
        """User's responsibility to get rid of box"""        
        box = SurroundingRectangle(state_list.get_rows()[idx])
        state_list.add(box)
        return box

    def construct(self):
        states = ['h', 's', 'v', r'\gamma']
        state_def, state_list = self.create_state_list(states)
        self.add(state_list)
        self.add_slide_content('States', state_def)
        self.add_section_title()

        self.wait(1)

        # Show aeroshell and planet
        aeroshell = self.add_aeroshell()
        planet = self.add_planet_surface()
        self.play(FadeIn(aeroshell))
        self.play(FadeIn(aeroshell), ApplyMethod(planet.shift, 3*UP))
        
        # planet.shift(3*UP)
        self.wait(2)
        
        # Altitude
        box = self.add_highlight_to_state(state_list, 0)
        alt_desc = self.add_altitude_explanation()
        self.play(Create(box), FadeIn(alt_desc))
        self.wait(3)
        self.play(Uncreate(box), FadeOut(alt_desc))
        
        # Velocity
        box = self.add_highlight_to_state(state_list, 2)
        vel_desc = self.add_velocity_explanation()
        self.play(Create(box), FadeIn(vel_desc))
        self.wait(3)
        self.play(FadeOut(box), FadeOut(vel_desc))

        # FPA
        box = self.add_highlight_to_state(state_list, 3)
        fpa_desc = self.add_fpa_explanation()
        self.play(Create(box), FadeIn(fpa_desc))
        self.wait(3)
        self.play(FadeOut(box), FadeOut(fpa_desc))

        # Clean up
        self.wait(1)
        self.play(FadeOut(planet), FadeOut(aeroshell))
        self.wait(2)
        