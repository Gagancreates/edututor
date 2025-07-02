from manim import *

class CreateScene(Scene):
    def construct(self):
        # Configuration for animation run_time and wait_time to achieve ~3 minutes duration
        # Individual animation run_time (0.5-2 seconds as per requirements)
        anim_rt = 1.5
        # Wait times will vary to ensure content is readable and overall duration is met.
        # This will sometimes exceed the 1-3 second range to meet the 3-minute duration.
        wait_short = 2.0  # For quick transitions or small pauses
        wait_normal = 4.5 # For standard pauses after key information
        wait_long = 7.0   # For significant pauses after complex equations or diagrams

        # 1. Introduction (Approx. 45 seconds)
        title = Text("Laplace Transforms", font_size=72).to_edge(UP)
        self.play(Write(title, run_time=anim_rt))
        self.wait(wait_normal)

        question = Text("Solving Differential Equations?", font_size=48).next_to(title, DOWN, buff=0.8)
        self.play(Write(question, run_time=anim_rt))
        self.wait(wait_normal)

        idea_text_1 = Text("Transforms functions from 'time domain' (t) to 's-domain' (s).", font_size=36).move_to(ORIGIN)
        idea_text_2 = Text("Converts differential equations into algebraic equations.", font_size=36).next_to(idea_text_1, DOWN, buff=0.5)

        self.play(Transform(question, idea_text_1, run_time=anim_rt))
        self.wait(wait_normal)
        self.play(Write(idea_text_2, run_time=anim_rt))
        self.wait(wait_normal)

        # Transition out introduction
        self.play(FadeOut(question, idea_text_2, run_time=anim_rt))
        self.wait(wait_short)

        # 2. Core Understanding - Definition (Approx. 72 seconds)
        laplace_def_intro = Text("The Definition:", font_size=48).to_edge(UP)
        self.play(ReplacementTransform(title, laplace_def_intro, run_time=anim_rt))
        self.wait(wait_normal)

        laplace_eq = MathTex(
            r"\mathcal{L}\{f(t)\} = F(s) = \int_0^\infty e^{-st} f(t) dt",
            substrings_to_isolate=["f(t)", "F(s)", "e^{-st}", "dt", "s", "t", "0", "\\infty", "\\mathcal{L}", "=", "\\int"],
            font_size=60
        ).scale(0.8).shift(UP*0.5)
        
        self.play(Write(laplace_eq, run_time=anim_rt*2)) # Longer write for the full equation
        self.wait(wait_long)

        # Break down components with color-coding and explanations
        f_t = laplace_eq.get_parts_by_tex("f(t)").set_color(YELLOW)
        F_s = laplace_eq.get_parts_by_tex("F(s)").set_color(BLUE)
        e_st = laplace_eq.get_parts_by_tex("e^{-st}").set_color(GREEN)
        s_var = laplace_eq.get_parts_by_tex("s").set_color(ORANGE)

        def_f_t = Text("f(t): Function in time domain (t ≥ 0)", font_size=32).next_to(laplace_eq, DOWN, buff=0.8).align_left(laplace_eq)
        def_e_st = Text("e⁻ˢᵗ: Exponential kernel (weighting function)", font_size=32).next_to(def_f_t, DOWN, buff=0.3).align_left(def_f_t)
        def_s = Text("s: Complex frequency variable", font_size=32).next_to(def_e_st, DOWN, buff=0.3).align_left(def_f_t)
        def_F_s = Text("F(s): Transformed function in s-domain", font_size=32).next_to(def_s, DOWN, buff=0.3).align_left(def_f_t)

        self.play(f_t.animate.scale(1.2), Write(def_f_t, run_time=anim_rt))
        self.wait(wait_normal)
        self.play(f_t.animate.scale(1/1.2), e_st.animate.scale(1.2), Write(def_e_st, run_time=anim_rt))
        self.wait(wait_normal)
        self.play(e_st.animate.scale(1/1.2), s_var.animate.scale(1.2), Write(def_s, run_time=anim_rt))
        self.wait(wait_normal)
        self.play(s_var.animate.scale(1/1.2), F_s.animate.scale(1.2), Write(def_F_s, run_time=anim_rt))
        self.wait(wait_normal)
        self.play(F_s.animate.scale(1/1.2)) # Scale back F_s

        intuition_text = Text("The integral evaluates the 's-frequency content' of f(t).", font_size=36).move_to(def_s.get_center()).shift(DOWN*2)
        self.play(Write(intuition_text, run_time=anim_rt))
        self.wait(wait_normal)

        # Metaphor: The Laplace "Machine" Operator
        self.play(FadeOut(def_f_t, def_e_st, def_s, def_F_s, intuition_text, run_time=anim_rt))
        self.wait(wait_short)

        laplace_operator = MathTex(r"\mathcal{L}", font_size=96).set_color(PURPLE)
        input_func = MathTex("f(t)", font_size=48).set_color(YELLOW)
        output_func = MathTex("F(s)", font_size=48).set_color(BLUE)

        machine_rect = Rectangle(width=4, height=3, color=PURPLE, fill_opacity=0.2).move_to(ORIGIN)
        machine_label = laplace_operator.move_to(machine_rect.get_center())

        input_arrow = Arrow(start=LEFT*4, end=machine_rect.get_left(), color=WHITE)
        output_arrow = Arrow(start=machine_rect.get_right(), end=RIGHT*4, color=WHITE)

        input_func.next_to(input_arrow.get_start(), LEFT)
        output_func.next_to(output_arrow.get_end(), RIGHT)

        self.play(
            FadeOut(laplace_eq, run_time=anim_rt),
            Transform(laplace_def_intro, Text("Laplace as an Operator", font_size=48).to_edge(UP), run_time=anim_rt)
        )
        self.wait(wait_short)

        self.play(Create(machine_rect, run_time=anim_rt), Write(machine_label, run_time=anim_rt))
        self.wait(wait_short)
        self.play(Create(input_arrow, run_time=anim_rt), Write(input_func, run_time=anim_rt))
        self.wait(wait_short)
        self.play(Create(output_arrow, run_time=anim_rt), Write(output_func, run_time=anim_rt))
        self.wait(wait_normal)

        # 3. Examples & Properties (Approx. 45 seconds)
        self.play(FadeOut(input_func, output_func, input_arrow, output_arrow, machine_rect, machine_label, run_time=anim_rt))
        self.wait(wait_short)

        example_intro = Text("Example & Properties", font_size=48).to_edge(UP)
        self.play(ReplacementTransform(laplace_def_intro, example_intro, run_time=anim_rt))
        self.wait(wait_normal)

        example_title = Text("Example: L{1}", font_size=40).to_edge(UP).shift(DOWN)
        self.play(Write(example_title, run_time=anim_rt))
        self.wait(wait_short)

        example_eq_1 = MathTex(r"\mathcal{L}\{1\}", r" = \int_0^\infty e^{-st} \cdot 1 dt", font_size=50).shift(UP*0.5)
        example_eq_2 = MathTex(r" = \left[ -\frac{1}{s} e^{-st} \right]_0^\infty", font_size=50).next_to(example_eq_1, DOWN, buff=0.5).align_left(example_eq_1)
        example_eq_3 = MathTex(r" = 0 - \left( -\frac{1}{s} e^0 \right)", r" = \frac{1}{s}", font_size=50).next_to(example_eq_2, DOWN, buff=0.5).align_left(example_eq_1)

        self.play(Write(example_eq_1, run_time=anim_rt))
        self.wait(wait_normal)
        self.play(Write(example_eq_2, run_time=anim_rt))
        self.wait(wait_normal)
        self.play(Write(example_eq_3, run_time=anim_rt))
        self.wait(wait_long)

        self.play(FadeOut(example_eq_1, example_eq_2, example_eq_3, run_time=anim_rt))
        self.wait(wait_short)

        properties_title = Text("Key Properties:", font_size=40).move_to(UP*1.5)
        self.play(Transform(example_title, properties_title, run_time=anim_rt))
        self.wait(wait_short)

        linearity = MathTex(r"\mathcal{L}\{af(t) + bg(t)\} = aF(s) + bG(s)", font_size=45).shift(UP*0.5)
        derivative = MathTex(r"\mathcal{L}\{f'(t)\} = sF(s) - f(0)", font_size=45).next_to(linearity, DOWN, buff=0.5)

        self.play(Write(linearity, run_time=anim_rt))
        self.wait(wait_normal)
        self.play(Write(derivative, run_time=anim_rt))
        self.wait(wait_long)

        # 4. Applications & Conclusion (Approx. 18 seconds)
        self.play(FadeOut(linearity, derivative, run_time=anim_rt))
        self.wait(wait_short)

        applications_title = Text("Applications", font_size=48).to_edge(UP)
        self.play(ReplacementTransform(example_intro, applications_title, run_time=anim_rt))
        self.play(Transform(example_title, Text("Why are they useful?", font_size=40).move_to(UP*1.5), run_time=anim_rt))
        self.wait(wait_normal)

        app_text_1 = Text("Simplifies solving complex Ordinary Differential Equations.", font_size=36).shift(UP*0.5)
        app_text_2 = Text("Used in control systems, circuit analysis, signal processing.", font_size=36).next_to(app_text_1, DOWN, buff=0.5)

        self.play(Write(app_text_1, run_time=anim_rt))
        self.wait(wait_normal)
        self.play(Write(app_text_2, run_time=anim_rt))
        self.wait(wait_normal)

        inverse_laplace_intro = Text("And its counterpart...", font_size=36).next_to(app_text_2, DOWN, buff=0.8)
        inverse_laplace_eq = MathTex(r"\mathcal{L}^{-1}\{F(s)\} = f(t)", font_size=50).next_to(inverse_laplace_intro, DOWN, buff=0.5)

        self.play(Write(inverse_laplace_intro, run_time=anim_rt))
        self.wait(wait_short)
        self.play(Write(inverse_laplace_eq, run_time=anim_rt))
        self.wait(wait_long)

        final_summary = Text("A powerful tool for Engineers & Scientists.", font_size=42).move_to(ORIGIN)
        self.play(FadeOut(app_text_1, app_text_2, inverse_laplace_intro, inverse_laplace_eq, run_time=anim_rt),
                  FadeOut(applications_title, example_title, run_time=anim_rt))
        self.wait(wait_short)
        self.play(Write(final_summary, run_time=anim_rt))
        self.wait(wait_long * 1.5) # Longer final pause

        # End Scene
        self.play(FadeOut(*self.mobjects, run_time=anim_rt))