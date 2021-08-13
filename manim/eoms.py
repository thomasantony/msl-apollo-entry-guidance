%%manim DynamicModel2_EOMs

from manim.mobject.geometry import ArrowTriangleFilledTip
from math import sin, cos, tan, pi

class DynamicModel2_EOMs(Scene):
    def construct(self):
        section_title = create_section_title('2DOF Dynamic Model')
        self.play(FadeIn(section_title, shift=RIGHT), runtime=0.5)

        states, eqns, D_exp, L_exp = eom()
        eqns = [
            r'v \sin{\gamma}',
            r'v \cos{\gamma}',
            r' -D/m - {g} \sin(\gamma)',
            r'\frac{1}{v} \left(\frac{v^2 \cos(\gamma)}{ {R_M} + h} + \frac{ L \cos( u )}{m} - g \cos(\gamma)\right)'
        ]
        eqn_list = Matrix([[e] for e in eqns], v_buff=1.5, element_alignment_corner=ORIGIN,
        ).scale(0.6) 
        eom_brace = Brace(eqn_list, UP)
        eom_brace_label = eom_brace.get_tex(r'\mathbf{\dot{x}} = \mathbf{f}(\mathbf{x}, u, t)') \
                                    .scale(0.7)
        eom_def = VGroup(eom_brace, eqn_list, eom_brace_label)

        slide_content = create_slide_content('Equations of Motion', eom_def)

        self.play(FadeIn(slide_content, shift=RIGHT))

        planet_expr = MathTex(r"g &= 3.73 \text{ m/s$^2$}\\", 
                            r"R_M &= 3380 \text{ km}\\",
                            r"\rho_0 &= 0.02 \text{kg/m$^3$}\\",
                            r"H &= 11.1 \text{km}", color=RED) \
                        .to_edge(LEFT, 0.5)\
                        .scale(0.75)
        planet_brace = Brace(planet_expr, RIGHT)
        planet_brace_label = planet_brace.get_tex(r"\text{Environment}").scale(0.8)
        planet_params = VGroup(planet_expr, planet_brace, planet_brace_label)

        vehicle_expr = MathTex(r"\beta &= 120 \text{ kg/m$^2$ } \\", 
                            r"L/D &= 0.24\\", color=BLUE) \
                        .to_edge(LEFT, 0.5)\
                        .scale(0.75)
        vehicle_brace = Brace(vehicle_expr, RIGHT)
        vehicle_brace_label = vehicle_brace.get_tex(r"\text{Vehicle}")\
                                           .scale(0.8)
        vehicle_params = VGroup(vehicle_expr, vehicle_brace, vehicle_brace_label)
        subexpr = MathTex(r"D/m &= \rho V^2 / (2\beta) \\",
                          r"L/m &= (L/D) \rho V^2 / (2\beta) \\",
                          r"\rho &= \rho_0 \exp(-h/H) \\"
                          ) \
                    .to_edge(LEFT, 0.75)\
                    .scale(0.8)
        vehicle_expr.align_to(planet_expr, LEFT)
        
        planet_params.set_opacity(0.)
        vehicle_params.set_opacity(0.)
        desc_box = VGroup(subexpr, 
                          planet_params,
                          vehicle_params)\
                    .arrange(DOWN, 0.8)\
                    .next_to(slide_content, RIGHT, buff=1.5) \
                    .to_edge(UP, 0.5)
        

        self.wait(2.0)
        self.play(FadeIn(desc_box))
        self.wait(2.0)
        self.play(planet_params.animate().set_opacity(1.0), runtime=2.0)
        self.wait(4.0)
        self.play(vehicle_params.animate().set_opacity(1.0))
        self.wait(4.0)
