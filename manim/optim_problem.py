%%manim ControlPolicy1_Optimization

from manim.mobject.geometry import ArrowTriangleFilledTip
from math import sin, cos, tan, pi


def make_ref_traj(x0, xf):
    ref_traj_t0 = Dot(x0)
    ref_traj_tf = Dot(xf)
    ref_traj = ArcBetweenPoints(x0, xf, angle=-TAU/6)
    ref_traj_t0_label = MathTex('\mathbf{x_0^*}, t_0^*') \
                                .scale(0.6) \
                                .next_to(ref_traj_t0, DL, 0) \
                                .shift((RIGHT+DOWN)*SMALL_BUFF)
    ref_traj_tf_label = MathTex('\mathbf{x_f^*}, t_f^*') \
                                .scale(0.6) \
                                .move_to(xf + MED_SMALL_BUFF*UL + MED_SMALL_BUFF*LEFT)
    ref_traj_Rf_label = MathTex('R_f^*') \
                                .scale(0.6) \
                                .next_to(ref_traj_tf, DOWN)
    ref_traj_label = Tex(r'Reference\\Trajectory') \
                        .scale(0.6) \
                        .next_to(ref_traj, LEFT) \
                        .shift(1.25*RIGHT)
    return Group(ref_traj_t0, 
                    ref_traj_t0_label,
                    ref_traj_tf,
                    ref_traj_tf_label, 
                    ref_traj_Rf_label, 
                    ref_traj,
                    ref_traj_label,
                    )

def make_pert_traj(x0, xf, xf_pred):
    traj_t0 = Dot(x0)
    traj_tf = Dot(xf)
    traj = ArcBetweenPoints(x0, xf, angle=-TAU/8)
    traj_t0_label = MathTex('\mathbf{x_0}, t_0') \
                                .scale(0.6) \
                                .next_to(traj_t0, UP, buff=SMALL_BUFF)
    traj_tf_label = MathTex('\mathbf{x_f}, t_f') \
                                .scale(0.6) \
                                .move_to(xf + MED_SMALL_BUFF*UR + SMALL_BUFF*RIGHT)
    traj_label = Tex(r'Perturbed\\Trajectory') \
                        .scale(0.6) \
                        .next_to(traj, RIGHT) \
                        .shift(0.75*LEFT + 0.5*UP) \
                        .shift(0.1 * DL)

    return Group(traj_t0, 
                    traj_t0_label,
                    traj_tf,
                    traj_tf_label, 
                    traj_label, 
                    traj
                    )

def make_pert_traj_tail(xf, xf_pred):
    hf_line = DashedLine(xf, xf+abs(xf[1])*DOWN)
    hf_brace = Brace(hf_line, LEFT, stroke_width=0.1)
    
    sf_label = MathTex('s_f') \
                    .scale(0.6) \
                    .next_to(hf_line, DOWN) \
                    .shift(UL*SMALL_BUFF)
    Rf_label = MathTex(r'R_f',r' = s_f + \dot{s_f} dt_f') \
                    .scale(0.6) \
                    .move_to(xf_pred + DOWN*MED_LARGE_BUFF + RIGHT)

    tail = DashedVMobject(ArcBetweenPoints(xf, xf_pred, angle=-TAU/9))
    return Group(hf_line,
                hf_brace,
                hf_brace.get_tex('h_f', buff=0.01).scale(0.5),
                sf_label,
                Rf_label,
                tail
    )

def make_axes(origin, s_len, h_len):
    h_axis = Arrow(origin+MED_SMALL_BUFF*DOWN, origin+h_len*UP)
    h_label = MathTex(r'h').next_to(h_axis, UP, SMALL_BUFF)
    s_axis = Arrow(origin+MED_SMALL_BUFF*LEFT, origin+s_len*RIGHT)
    s_label = MathTex(r's').next_to(s_axis, RIGHT, SMALL_BUFF)
    return Group(h_axis, s_axis), Group(h_label, s_label)


class ControlPolicy1_Optimization(Scene):
    def construct(self):
        text_scale = 0.6
        section_title = create_section_title('Minimizing Range Error')
        # slide_title = create_slide_title('Problem Statement')
        
        axes, axes_labels = make_axes(ORIGIN+2*DOWN, 6, 5)

        # Make ref traj
        ref_traj_pts = [0.8*RIGHT+1*UP, 2.5*RIGHT+2*DOWN]
        ref_traj = make_ref_traj(*ref_traj_pts)

        # Make perturbed traj
        pert_traj_pts = [1.25*RIGHT+1.5*UP, 4*RIGHT+1*DOWN, 4.25*RIGHT+2*DOWN]
        
        pert_traj = make_pert_traj(*pert_traj_pts[:2], ORIGIN)
        traj_tail = make_pert_traj_tail(*pert_traj_pts[1:])

        diagram = Group(axes, axes_labels, ref_traj, pert_traj, traj_tail)

        # Add Cost function 
        ocp = MathTex(r'\text{Min } J &= ', r'R_f') \
                        .scale(text_scale) \
                        .to_edge(UP, buff=0.5) \
                        .to_edge(LEFT, buff=1.5)

        # ocp.set_color_by_tex('R_f', YELLOW, substring=False)

        # Show EOMs
        eoms = MathTex(r'\text{s.t: }', '\dot{\mathbf{x}} &= \mathbf{f}(\mathbf{x}, u, t)') \
                .scale(text_scale)
        eoms.next_to(ocp, DOWN, buff=0.25, aligned_edge=LEFT)

        x_bc = MathTex(r'\mathbf{x}(t_0) &= \big[120\text{ km},\;0,\;5.5\text{ km/s},\;-14.5^{\circ}\big] \\',
                       r'h(t_f) &= 0\text{ km}')\
                .scale(text_scale)
        x_bc.next_to(eoms[1], DOWN, buff=0.25, aligned_edge=LEFT) \
            .align_to(ocp, LEFT)

        # Substitude R_f
        ocp_2 = MathTex(r'\text{Min } J &= ',r's_f',r' + \dot{s_f} dt_f') \
                                .scale(text_scale) \
                                .move_to(ocp)


        # Expand d_tf and sfdot
        ocp_3 = MathTex(r'\text{Min } J &= ',r's_f - \cot(\gamma_f) h_f') \
                                .scale(text_scale) \
                                .move_to(ocp)

        phi_brace = Brace(ocp_3[1]).shift(UP*0.15)
        phi_brace_label = phi_brace.get_tex(r'\Phi,\text{ Terminal Point Cost}')\
                                    .scale(0.5) \
                                    .shift(0.25*UP)
        phi_label = Group(phi_brace, phi_brace_label)

        arrow = MathTex(r'\Downarrow') \
                    .scale(1.25) \
                    .next_to(x_bc, DOWN, aligned_edge=ORIGIN, buff=0.7) \
                    .shift(1.0*LEFT)

        # Introduce costates
        costates = MathTex(r'\text{Costates: }',
                           r'\mathbf{\lambda}^\intercal = \left[ \lambda_h \: \lambda_s \: \lambda_v \: \lambda_\gamma]'
                        )\
                        .scale(text_scale) \
                        .next_to(x_bc, DOWN, 1.5) \
                        .align_to(ocp_3, LEFT)

        # bvp_1 = MathTex(r"\text{Min } J' &= s_f - \cot{\gamma_f} h_f + \mathbf{\lambda}^\intercal \mathbf{f}") \
        #                         .scale(0.8) \
        #                         .move_to(ocp)
        

        # Costate Equations
        costate_eoms = MathTex(r'\mathbf{\dot{\lambda}} = -\mathbf{\lambda}^\intercal\frac{\partial \mathbf{f}}{\partial \mathbf{x}}') \
                        .next_to(costates[0], DOWN, buff=0.1, aligned_edge=LEFT) \
                        .scale(text_scale) \
                        .shift(LEFT*SMALL_BUFF*2)

        # Costate BCs
        costate_bc = MathTex(r'\mathbf{\lambda}^\intercal(t_f) = {\partial \Phi \over \partial \mathbf{x}(t_f)} = \left[-\cot{\gamma_f}\;\;1\;\;0\;\;0\;\right]')
        costate_bc.next_to(costate_eoms, RIGHT)\
                  .scale(text_scale) \
                  .shift(1*LEFT)

        # Introduce LambdaU and its BC        
        lambda_u_eom = MathTex(r'\dot{\lambda_u} = -\frac{\partial \mathbf{f}}{\partial u}') \
                        .next_to(costate_eoms, DOWN, buff=0.1, aligned_edge=LEFT) \
                        .scale(text_scale) \
                        .align_to(costate_eoms, LEFT)
        

        lambda_u_bc = MathTex(r'\lambda_u(t_f) = 0') \
                        .next_to(costate_eoms, RIGHT)\
                        .align_to(lambda_u_eom, UP) \
                        .scale(text_scale) \
                        .shift(RIGHT*0.1) \
                        # .next_to(lambda_u_eom, RIGHT)\
        
        x_bc_2 = MathTex(r'\mathbf{x}(t_0) &= \mathbf{X}_0 \\ h(t_f) &= 0') \
                    .scale(text_scale)\
                    .next_to(lambda_u_eom, DOWN, aligned_edge=LEFT)
        

        # self.add(section_title)
        # self.add(axes)
        # self.add(ref_traj)
        # self.add(pert_traj)
        # self.add(traj_tail)
        # self.remove(*diagram)
        # self.add(ocp_3)
        # eoms.next_to(phi_label, DOWN, buff=0.25).align_to(ocp_3, LEFT)
        # x_bc.next_to(eoms[1], DOWN, buff=0.25, aligned_edge=LEFT)

        # self.add(phi_label)
        # self.add(eoms)
        # self.add(x_bc)
        # self.add(arrow)
        # self.add(costates)
        # self.add(costate_eoms)
        # self.add(costate_bc)
        # self.add(lambda_u_eom)
        # self.add(lambda_u_bc)
        # self.add(x_bc_2)

    
        self.play(FadeIn(section_title, shift=RIGHT), runtime=0.5)

        # Show diagram
        self.play(FadeIn(axes), FadeIn(axes_labels), FadeIn(ref_traj))
        self.wait(2)
        self.play(FadeIn(pert_traj))
        self.wait(2)
        self.play(FadeIn(traj_tail))

        self.play(FadeIn(ocp, eoms, x_bc),
                  traj_tail[4].animate().set_color_by_tex('R_f', YELLOW, substring=False),
                  ocp.animate().set_color_by_tex('R_f', YELLOW, substring=False)
                  )

        self.wait(2)

        self.play(ocp.animate().become(ocp_2),
                  traj_tail[4].animate().set_color(WHITE))
        self.wait(1)

        # Add "phi" label 
        self.play(ocp.animate().become(ocp_3), 
                  FadeIn(phi_label), 
                  eoms.animate().next_to(phi_label, DOWN, buff=0.25).align_to(ocp_3, LEFT),
                  x_bc.animate().next_to(phi_label, DOWN, buff=0.60).align_to(ocp_3, LEFT)
        )
        self.wait(2)

        # Needs to be done here because of respositioning of x_bc
        ocp_all = Group(ocp, eoms, x_bc)
        ocp_label_brace = Brace(ocp_all, RIGHT)
        ocp_label = Group(ocp_label_brace, ocp_label_brace.get_text(r'Optimization Problem').scale(0.8))

        bvp = Group(costates, costate_eoms, costate_bc, lambda_u_bc, lambda_u_eom, x_bc_2)
        bvp_label_brace = Brace(bvp, RIGHT)
        bvp_label = Group(bvp_label_brace, bvp_label_brace.get_text(r'Boundary Value Problem').scale(0.8))
        ocp_label.align_to(bvp_label, LEFT)
        arrow.next_to(bvp_label, UP, buff=0.5)
        # self.add(bvp_label_brace, bvp_label, ocp_label_brace, ocp_label, arrow)

        self.play(FadeOut(diagram), FadeIn(ocp_label))
        self.wait(2)
        self.play(FadeIn(arrow), FadeIn(bvp_label))
        self.wait(1)
        self.play(FadeIn(costates))
        self.wait(2)
        self.play(FadeIn(costate_eoms), FadeIn(costate_bc))
        self.wait(2)

        self.play(FadeIn(lambda_u_eom), FadeIn(lambda_u_bc))
        self.wait(2)
        self.play(FadeIn(x_bc_2))

        self.wait(3)
