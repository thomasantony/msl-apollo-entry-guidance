%%manim DynamicModel2_EOMs

from manim.mobject.geometry import ArrowTriangleFilledTip
from math import sin, cos, tan, pi

class DynamicModel2_EOMs(Scene):
    def construct(self):
        section_title = create_section_title('2DOF Dynamic Model')
        self.play(FadeIn(section_title, shift=RIGHT), runtime=0.5)
        # self.add(section_title)
        slide_title = create_slide_title('Equations of Motion')
        self.play(FadeIn(slide_title, shift=RIGHT))
        # self.add(slide_title)
        
        states, eqns, D_exp, L_exp = eom()

        eom_dxdt = [r'dh \over dt',
                 r'ds \over dt',
                 r'dv \over dt',
                 r'd\gamma \over dt',
                 ]
        eqns = [
            r'v \sin{\gamma}',
            r'v \cos{\gamma}',
            r' -{{D/m}} - {{g}} \sin(\gamma)',
            r'{1 \over v} \left({v^2 \cos(\gamma) \over {{R_M}} + h} + {{L/m}} {{\cos(u)}} - {{g}}\cos(\gamma)\right)'
        ]
        
        dxdt_list = Matrix([[e] for e in eom_dxdt], v_buff=1.5, element_alignment_corner=ORIGIN)\
                        .scale(0.6) \

        dxdt_entries = dxdt_list.get_entries()

        dxdt_brace = Brace(dxdt_list, UP)
        dxdt_brace_label = dxdt_brace.get_tex(r'\mathbf{\dot{x}} = \mathbf{f}(\mathbf{x}, u, t)') \
                                    .scale(0.7)
        dxdt_def = Group(dxdt_brace, dxdt_list, dxdt_brace_label) \
                    .next_to(slide_title, DOWN)
        
        eom_list = Matrix([[e] for e in eqns], v_buff=1.5, element_alignment_corner=ORIGIN)\
                        .scale(0.6) \

        # Repeat brace
        eom_brace = Brace(eom_list, UP)
        eom_brace_label = eom_brace.get_tex(r'\mathbf{\dot{x}} = \mathbf{f}(\mathbf{x}, u, t)') \
                                    .scale(0.7)
        eom_def = Group(eom_brace, eom_list, eom_brace_label) \
                    .next_to(slide_title, DOWN)
        for e in eom_list.get_entries():
            e.set_opacity(0.0)

        self.add(dxdt_def)
        self.play(FadeIn(dxdt_def))
        self.wait(2)
        
        self.play(*[e.animate().set_opacity(0.0) 
                    for e in dxdt_list.get_entries()]
                  , run_time=0.5)
        self.play(ReplacementTransform(dxdt_list, eom_list),
                  ReplacementTransform(dxdt_brace, eom_brace))
        self.play(*[e.animate().set_opacity(1.0) 
                    for e in eom_list.get_entries()], run_time=0.5)
        self.wait(1)

        # self.add(eom_def)

        DM_expr = MathTex(r"D/m", r"= ", r"\rho",  r"V^2 / (2", r"\beta", r")") \
                    .next_to(eom_def, RIGHT, 1.5)
        LM_expr = MathTex(r"L/m", r"= ", r"(",r"L/D",r")", r"\rho V^2 / (2\beta)") \
                    .next_to(DM_expr, DOWN, aligned_edge=LEFT) \
                    .align_to(DM_expr, LEFT)
        subexpr = Group(DM_expr,
                        LM_expr,
                    ) \
                    .scale(0.8)

        rho_expr = MathTex(r"\rho", r"=", r"\rho_0", r"\exp(-h/",r"H",r")") \
                    .align_to(LM_expr, LEFT)
        rho0_val = MathTex(r"\rho_0", r"&= 0.02 \text{kg/m$^3$}\\") \
                    .next_to(rho_expr, DOWN) \
                    .align_to(rho_expr, LEFT)
        H_val = MathTex(r"H", r"&= 11.1 \text{km}") \
                    .next_to(rho0_val, DOWN) \
                    .align_to(rho0_val, LEFT)

        g_val = MathTex(r"g", r"&= 3.73 \text{ m/s$^2$}\\") \
                    .next_to(H_val, DOWN) \
                    .align_to(H_val, LEFT)
        RM_val = MathTex(r"R_M", r"&= 3380 \text{ km}\\") \
                    .next_to(g_val, DOWN) \
                    .align_to(g_val, LEFT)
        
        planet_expr = Group(rho_expr, 
                            rho0_val,
                            H_val,
                            g_val, 
                            RM_val,
                            ) \
                        .scale(0.75)
        planet_brace = Brace(planet_expr, RIGHT)
        planet_brace_label = planet_brace.get_tex(r"\text{Environment}").scale(0.8)
        planet_params = Group(planet_expr, planet_brace, planet_brace_label)

        beta_val = MathTex(r"\beta", r"&= 120 \text{ kg/m$^2$ } \\")
        LD_val = MathTex(r"L/D", r"&= 0.24\\") \
                    .next_to(beta_val, DOWN) \
                    .align_to(beta_val, LEFT)

        vehicle_expr = Group(beta_val, 
                            LD_val) \
                        .scale(0.75) \
                        .set_opacity(1.)
        vehicle_brace = Brace(vehicle_expr, RIGHT)
        vehicle_brace_label = vehicle_brace.get_tex(r"\text{Vehicle}")\
                                           .scale(0.8)
        vehicle_params = Group(vehicle_expr, vehicle_brace, vehicle_brace_label)

        
        planet_params.next_to(subexpr, DOWN, aligned_edge=LEFT, buff=0.8) \
                     .align_to(subexpr, LEFT)
        vehicle_params.next_to(planet_params, DOWN, aligned_edge=LEFT, buff=0.8) \
                     .align_to(planet_params, LEFT)

        planet_params.set_opacity(0.)
        vehicle_params.set_opacity(0.)
        desc_box = Group(subexpr, 
                        planet_params,
                        vehicle_params,
                    )\
                    .next_to(eom_def, RIGHT, buff=1.5) \
                    .to_edge(UP, 0.5) \

        eom_entries = eom_list.get_entries()

        # Show just D/m
        DM_expr.set_color_by_tex(r"D/m", YELLOW)
        self.play(
            eom_entries[2].animate().set_color_by_tex(r"D/m", YELLOW),
            FadeIn(subexpr[0])
        )
        self.wait(1)

        # Highlight rho and show rho expression
        rho_color = RED_C
        rho_expr.set_color_by_tex(r'\rho', rho_color, substring=False)
        self.play(
            DM_expr.animate().set_color_by_tex(r"\rho", rho_color, substring=False),
            FadeIn(rho_expr)
        )
        self.wait(1)

        # Highlight rho0 and H
        rho0_color = GREEN_C
        H_color = BLUE_C
        beta_color = GREEN_C
        rho0H_cmap = {
            r"\rho_0": rho0_color,
            r"H": H_color,
            r"\beta": beta_color,
        }
        
        rho0_val.set_color_by_tex_to_color_map(rho0H_cmap, substring=False)
        H_val.set_color_by_tex_to_color_map(rho0H_cmap, substring=False)
        beta_val.set_color_by_tex_to_color_map(rho0H_cmap, substring=False)

        self.play(
            rho_expr.animate().set_color_by_tex_to_color_map(rho0H_cmap, substring=False),
            DM_expr.animate().set_color_by_tex_to_color_map(rho0H_cmap, substring=False),
            FadeIn(H_val),
            FadeIn(rho0_val),
            FadeIn(beta_val),
        )
        self.wait(1)

        # # Highlight L/m
        cmap = {r"L/m": YELLOW, r"L": YELLOW, r'L/D': GREEN_A}
        subexpr[1].set_color_by_tex_to_color_map(cmap, substring=False)
        LD_val.set_color_by_tex_to_color_map(cmap, substring=False)
        self.play(
            # Reset colors on previous expr
            DM_expr.animate().set_color(WHITE),
            rho_expr.animate().set_color(WHITE),
            rho0_val.animate().set_color(WHITE),
            H_val.animate().set_color(WHITE),
            beta_val.animate().set_color(WHITE),

            eom_entries[3].animate().set_color_by_tex_to_color_map(cmap, substring=False),
            FadeIn(subexpr[1]), # L/m expr
            FadeIn(LD_val),
        )

        self.wait(1)

        # Highlight u
        self.play(
            # Reset colors
            subexpr[1].animate().set_color(WHITE),
            LD_val.animate().set_color(WHITE),
            eom_entries[3].animate().set_color_by_tex(r"\cos(u)", YELLOW)
        )

        self.wait(1)

        # Highlight g and R_M
        g_color = MAROON
        RM_color = GREEN_A
        cmap = {r'g': g_color, r'{{g}}': g_color, r'R_M': RM_color, r'{{R_M}}': RM_color}
        g_val.set_color_by_tex_to_color_map(cmap, substring=False),
        RM_val.set_color_by_tex_to_color_map(cmap, substring=False),

        self.play(
            eom_entries[2].animate().set_color_by_tex_to_color_map(cmap, substring=False),
            eom_entries[3].animate().set_color_by_tex_to_color_map(cmap, substring=False),
            FadeIn(g_val),
            FadeIn(RM_val),
        )

        self.wait(1)
