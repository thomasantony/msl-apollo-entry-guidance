%%manim ControlPolicy2

from manim.mobject.geometry import ArrowTriangleFilledTip
from math import sin, cos, tan, pi

def transform_equations(scene, eqn1, eqn2, indices, runtime=1.0):
    """match indices in multipart equations to transform between them"""

    assert len(eqn1) == len(eqn2), "Equations shold have same number of terms"+str(len(eqn1))+"!="+str(len(eqn2))
    new_copies = []
    animations = []
    a1 = []   # Delete old terms
    a2 = []   # Rearrange old terms
    a3 = []   # Bring in new terms
    for i in range(len(eqn1)):
        # new_copy = eqn2[i].copy().move_to(eqn1[i])
        if i in indices:
            a1.append(FadeOut(eqn1[i], shift=UP))
            a3.append(FadeIn(eqn2[i]))
        else:
            a2.append(ReplacementTransform(eqn1[i], eqn2[i]))

    return AnimationGroup(*a1), AnimationGroup(*a2), AnimationGroup(*a3)

class ControlPolicy2(Scene):
    def construct(self):
        section_title = create_section_title('Minimizing Range Error')
        slide_title = create_slide_title('Apollo Guidance Control Law')
        # self.play(FadeIn(section_title, shift=RIGHT), runtime=0.5)
        # self.play(FadeIn(slide_title, shift=RIGHT))

        self.add(section_title)
        self.add(slide_title)

        F1_expr = r'{H\lambda_h^*(v) \over \big( {D^* \over m}(v) \big)}'
        F2_expr = r'{\lambda_\gamma^*(v) \over v^* \cos{\gamma^*(v)}}'
        F3_expr = r'\lambda_u^*(v)'
        lamS_expr = r'\lambda_s^*(v)'
        delS_expr = r'\delta s(v)'
        delhdot_expr = r'\delta \dot{h}(v)'
        delDM_expr = r'\delta \big( {D \over m}(v) \big)'

        empty_spaces = [r'{}' for _ in range(13)]
        control_policy_0 = MathTex(r'u(v) = u^*(v) + ', r'\delta u', *empty_spaces)\
                                .scale(0.8) \
                                .to_edge(UP, 2.0) \
                                .set_color_by_tex(r'\delta u', BLUE, substring=False)

        self.add(control_policy_0)
        self.wait(1)

        control_policy_1 = MathTex(r'u(v) = u^*(v) + ',
                                   r'{}', r'{\bigg(',
                                   r'- ', lamS_expr, delS_expr,
                                   r'- ', F2_expr, delhdot_expr,
                                   r'- ', F1_expr, delDM_expr,
                                   r'\bigg) \over ',F3_expr,'}') \
                            .scale(0.8) \
                            .to_edge(UP, 2.0) \
                            .set_color_by_tex(delS_expr, YELLOW) \
                            .set_color_by_tex(delhdot_expr, YELLOW) \
                            .set_color_by_tex(delDM_expr, YELLOW) \
                            .set_color_by_tex(lamS_expr, RED) \
                            .set_color_by_tex(F1_expr, RED) \
                            .set_color_by_tex(F2_expr, RED) \
                            .set_color_by_tex(F3_expr, RED)

        a = transform_equations(self, control_policy_0, control_policy_1, list(range(1,13)))
        self.play(a[0], a[1], a[2])

        self.wait(1)
        control_policy_1a = MathTex(r'u(v) = u^*(v) + ',
                                   r'{}', r'{\bigg(',
                                   r'- ', '1', delS_expr,
                                   r'- ', F2_expr, delhdot_expr,
                                   r'- ', F1_expr, delDM_expr,
                                   r'\bigg) \over ',F3_expr,'}') \
                            .scale(0.8) \
                            .to_edge(UP, 2.0) \
                            .set_color_by_tex(delS_expr, YELLOW) \
                            .set_color_by_tex(delhdot_expr, YELLOW) \
                            .set_color_by_tex(delDM_expr, YELLOW) \
                            .set_color_by_tex('1', RED) \
                            .set_color_by_tex(F1_expr, RED) \
                            .set_color_by_tex(F2_expr, RED) \
                            .set_color_by_tex(F3_expr, RED)

        # Remove lambda_s term
        a = transform_equations(self, control_policy_1, control_policy_1a, [4])
        self.play(a[0], a[1])
        self.play(a[2])
        
        control_policy_2 = MathTex(r'u(v) = u^*(v) + ',
                                   r'{}', r'{\bigg(',
                                   r'- ', r'{}', delS_expr,
                                   r'- ', 'F_2 (v)\:',delhdot_expr,
                                   r'- ', 'F_1 (v)\:',delDM_expr,
                                   r'\bigg) \over ', 'F_3(v)', '}') \
                            .scale(0.8) \
                            .move_to(control_policy_1) \
                            .set_color_by_tex(delS_expr, YELLOW) \
                            .set_color_by_tex(delhdot_expr, YELLOW) \
                            .set_color_by_tex(delDM_expr, YELLOW) \
        
        # Bring in gain terms
        a = transform_equations(self, control_policy_1a, control_policy_2, [4, 7, 10, 13])
        self.play(a[0], a[1])
        self.play(a[2])
        self.wait(1)

        delS = r'(s - s^*(v))'
        delhdot = r'\big( \dot{h} - \dot{h}^*(v)\big)'
        delDM = r'\big( {D \over m} - {D^* \over m}(v) \big)'

        control_policy_3 = MathTex(r'u(v) = u^*(v) + ',
                                   r'K', r'{\bigg(',
                                   r'- ', r'{}', delS,
                                   r'- ', r'F_2(v)\:', delhdot,
                                   r'- ', r'F_1(v)\:', delDM,
                                   r'\bigg) \over', 'F_3(v)', '}') \
                            .scale(0.8) \
                            .move_to(control_policy_2)\
                            .set_color_by_tex('K', BLACK)
        # self.add(control_policy_3)
        a = transform_equations(self, control_policy_2, control_policy_3, [5, 8, 11])
        self.play(a[0], a[1])
        self.play(a[2])

        control_law = MathTex(r'\text{Bank Angle, }u &= u^* + \delta u \\',
                                    r'0 &\leq |u| \leq \pi') \
                        .scale(0.8) \
                        .next_to(control_policy_3, DOWN, buff=0.4)
        self.play(FadeIn(control_law))
        
        self.wait(1)
        overcontrol_gain = Tex(r'$K$',' : ``Overcontrol gain"') \
                            .set_color_by_tex('K', RED)\
                            .scale(0.8) \
                            .next_to(control_law, DOWN, buff=LARGE_BUFF)
        
        self.play(FadeIn(overcontrol_gain), control_policy_3.animate().set_color_by_tex('K', RED))
        self.wait(2)
