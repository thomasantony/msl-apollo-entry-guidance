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
    hf_brace = Brace(hf_line, LEFT)
    
    sf_label = MathTex('s_f') \
                    .scale(0.6) \
                    .next_to(hf_line, DOWN) \
                    .shift(UL*SMALL_BUFF)
    Rf_label = MathTex('R_f = s_f + \dot{s_f} dt_f') \
                    .scale(0.6) \
                    .move_to(xf_pred + DOWN*MED_LARGE_BUFF + RIGHT)

    tail = DashedVMobject(ArcBetweenPoints(xf, xf_pred, angle=-TAU/9))
    return Group(hf_line,
                hf_brace,
                hf_brace.get_tex('h_f', buff=0.01).scale(0.6),
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
        section_title = create_section_title('Minimizing Range Error')
        slide_title = create_slide_title('Problem Statement')
        self.play(FadeIn(section_title, shift=RIGHT), runtime=0.5)
        self.play(FadeIn(slide_title, shift=RIGHT))

        self.add(section_title)
        self.add(slide_title)

        axes, axes_labels = make_axes(ORIGIN+2*DOWN, 6, 5)
        self.add(axes)

        # Make ref traj
        ref_traj_pts = [0.8*RIGHT+1*UP, 2.5*RIGHT+2*DOWN]
        ref_traj = make_ref_traj(*ref_traj_pts)
        self.play(FadeIn(axes), FadeIn(axes_labels), FadeIn(ref_traj))
        self.wait(2)

        # Make perturbed traj
        pert_traj_pts = [1.25*RIGHT+1.5*UP, 4*RIGHT+1*DOWN, 4.25*RIGHT+2*DOWN]
        
        pert_traj = make_pert_traj(*pert_traj_pts[:2], ORIGIN)
        traj_tail = make_pert_traj_tail(*pert_traj_pts[1:])
        
        # self.add(ref_traj)
        # self.add(pert_traj)
        # self.add(traj_tail)
        self.play(FadeIn(pert_traj))
        self.wait(1)
        self.play(FadeIn(traj_tail))

        # Add Cost function 
        problem_statement = MathTex(r'\text{Min } J &= R_f') \
                        .scale(0.8) \
                        .next_to(slide_title, DOWN, buff=0.5)
        
        # Show EOMs
        eoms = MathTex(r'\text{Subject to: } \mathbf{f}(\mathbf{x}, u, t)')
        eoms.next_to(problem_statement, DOWN, buff=0.25)

        # self.add(problem_statement, eoms)
        self.play(FadeIn(problem_statement, eoms))
        
        self.wait(1)

        # Substitude R_f
        problem_statement_2 = MathTex(r'\text{Min } J &= s_f + \dot{s_f} dt_f') \
                                .scale(0.8) \
                                .move_to(problem_statement)
        self.play(problem_statement.animate().become(problem_statement_2))

        self.wait(1)

        # Expand d_tf and sfdot
        problem_statement_3 = MathTex(r'\text{Min } J &= s_f - \cot(\gamma_f) h_f') \
                                .scale(0.8) \
                                .move_to(problem_statement)
        self.play(problem_statement.animate().become(problem_statement_3))
        self.wait(2)

        # Introduce costates
        costates = VGroup(Text('Costates:').to_edge(LEFT, 0.5).scale(0.4),
                        MathTex(r'\mathbf{\lambda}^\intercal = \left[ \lambda_h \: \lambda_s \: \lambda_v \: \lambda_\gamma]')\
                        .scale(0.8)
                        )\
                        .arrange(RIGHT) \
                        .next_to(problem_statement, DOWN, 0.25)

        problem_statement_4 = MathTex(r"\text{Min } J' &= s_f - \cot{\gamma_f} h_f + \mathbf{\lambda}^\intercal \mathbf{f}") \
                                .scale(0.8) \
                                .move_to(problem_statement)
        # self.remove(problem_statement, eoms)
        # self.add(problem_statement_4, costates)
        self.play(problem_statement.animate().become(problem_statement_4),
                  FadeOut(eoms),
                  FadeIn(costates))
        self.wait(2)

        # Costate Equations
        costate_eoms = MathTex(r'\mathbf{\dot{\lambda}} = \mathbf{\lambda}^\intercal\frac{\partial \mathbf{f}}{\partial \mathbf{x}}') \
                        .next_to(costates[0], DOWN, aligned_edge=LEFT) \
                        .scale(0.6) \
                        .shift(LEFT*SMALL_BUFF*2)
        # self.add(costate_eoms)
        self.play(FadeIn(costate_eoms))
        self.wait(2)

        # Costate BCs
        costate_bc = MathTex(r'\mathbf{\lambda}^\intercal(t_f) = \left[-\cot{\gamma_f}\;\;1\;\;0\;\;0\;\right]')
        costate_bc.next_to(costate_eoms, RIGHT)\
                  .scale(0.6) \
                  .shift(1*LEFT)
        # self.add(costate_bc)
        self.play(FadeIn(costate_bc))

        self.wait(2)

        # Introduce LambdaU and its BC        
        lambda_u_eom = MathTex(r'\dot{\lambda_u} = \frac{\partial \mathbf{f}}{\partial u}') \
                        .next_to(costate_eoms, DOWN, aligned_edge=LEFT) \
                        .scale(0.6) \
                        .shift(LEFT*SMALL_BUFF*5)
        # self.add(lambda_u_eom)
        self.play(FadeIn(lambda_u_eom))
        
        self.wait(2)

        lambda_u_bc = MathTex(r'\lambda_u(t_f) = 0') \
                        .next_to(lambda_u_eom, RIGHT)\
                        .scale(0.6)
        # self.add(lambda_u_bc)
        self.play(FadeIn(lambda_u_bc))

        self.wait(3)
