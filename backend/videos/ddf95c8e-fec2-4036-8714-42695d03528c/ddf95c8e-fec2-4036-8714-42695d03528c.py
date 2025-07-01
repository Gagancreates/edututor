from manim import *

class CreateScene(Scene):
    def construct(self):
        # Set the background color
        self.camera.background_color = WHITE

        # Title and Introduction
        title = Text("Laplace Transforms Explained", color=BLUE).scale(1.2)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        intro_text = Text("A tool to simplify complex problems in Engineering and Physics", color=BLACK).scale(0.7)
        self.play(Write(intro_text))
        self.wait(3)
        self.play(FadeOut(intro_text))

        # Define the Laplace Transform
        laplace_formula_title = Text("The Laplace Transform:", color=BLUE).scale(0.8)
        laplace_formula = MathTex(r"F(s) = \int_0^\infty f(t) e^{-st} \, dt", color=BLACK).scale(1.0)
        self.play(Write(laplace_formula_title))
        self.play(Write(laplace_formula))
        self.wait(3)

        # Highlight key parts of the formula
        f_t = MathTex("f(t)", color=RED).move_to(laplace_formula[0][1:4].get_center()).scale(1.0)
        s = MathTex("s", color=GREEN).move_to(laplace_formula[0][6].get_center()).scale(1.0)
        e = MathTex("e^{-st}", color=YELLOW).move_to(laplace_formula[0][7:12].get_center()).scale(1.0)

        self.play(Indicate(f_t, color=RED, scale_factor=1.2))
        self.wait(1)
        self.play(Indicate(s, color=GREEN, scale_factor=1.2))
        self.wait(1)
        self.play(Indicate(e, color=YELLOW, scale_factor=1.2))
        self.wait(2)

        self.play(FadeOut(laplace_formula_title, laplace_formula, f_t, s, e))

        # Example: Transforming f(t) = 1
        example_title = Text("Example: f(t) = 1", color=BLUE).scale(0.8)
        self.play(Write(example_title))
        self.wait(1)

        f_t_eq_1 = MathTex("f(t) = 1", color=BLACK).scale(0.9)
        self.play(Write(f_t_eq_1))
        self.wait(1)

        laplace_formula_1 = MathTex(r"F(s) = \int_0^\infty 1 \cdot e^{-st} \, dt", color=BLACK).scale(0.9)
        self.play(Write(laplace_formula_1))
        self.wait(2)

        integration_result = MathTex(r"F(s) = \left[ -\frac{1}{s} e^{-st} \right]_0^\infty", color=BLACK).scale(0.9)
        self.play(Write(integration_result))
        self.wait(2)

        final_result = MathTex(r"F(s) = \frac{1}{s}", color=BLACK).scale(0.9)
        self.play(Write(final_result))
        self.wait(3)

        self.play(FadeOut(example_title, f_t_eq_1, laplace_formula_1, integration_result, final_result))

        # Example: Transforming f(t) = e^(at)
        example_title_exp = Text("Example: f(t) = e^{at}", color=BLUE).scale(0.8)
        self.play(Write(example_title_exp))
        self.wait(1)

        f_t_eq_exp = MathTex("f(t) = e^{at}", color=BLACK).scale(0.9)
        self.play(Write(f_t_eq_exp))
        self.wait(1)

        laplace_formula_exp = MathTex(r"F(s) = \int_0^\infty e^{at} \cdot e^{-st} \, dt", color=BLACK).scale(0.9)
        self.play(Write(laplace_formula_exp))
        self.wait(2)

        combined_exponent = MathTex(r"F(s) = \int_0^\infty e^{(a-s)t} \, dt", color=BLACK).scale(0.9)
        self.play(Write(combined_exponent))
        self.wait(2)

        integration_result_exp = MathTex(r"F(s) = \left[ \frac{1}{a-s} e^{(a-s)t} \right]_0^\infty", color=BLACK).scale(0.9)
        self.play(Write(integration_result_exp))
        self.wait(2)

        final_result_exp = MathTex(r"F(s) = \frac{1}{s-a}", color=BLACK).scale(0.9)
        self.play(Write(final_result_exp))
        self.wait(3)

        self.play(FadeOut(example_title_exp, f_t_eq_exp, laplace_formula_exp, combined_exponent, integration_result_exp, final_result_exp))

        # Applications
        applications_title = Text("Applications:", color=BLUE).scale(1.0)
        self.play(Write(applications_title))
        self.wait(1)

        applications_list = BulletedList(
            "Solving Differential Equations",
            "Circuit Analysis",
            "Control Systems",
            "Signal Processing",
            color=BLACK,
            buff=0.5
        ).scale(0.7)

        self.play(Write(applications_list))
        self.wait(5)

        self.play(FadeOut(applications_title, applications_list))

        # Conclusion
        conclusion_text = Text("Laplace Transforms: Powerful tools for simplification and analysis!", color=GREEN).scale(0.8)
        self.play(Write(conclusion_text))
        self.wait(4)
        self.play(FadeOut(conclusion_text))

        end_text = Text("Thank you for watching!", color=BLUE).scale(1.0)
        self.play(Write(end_text))
        self.wait(3)
        self.play(FadeOut(end_text))