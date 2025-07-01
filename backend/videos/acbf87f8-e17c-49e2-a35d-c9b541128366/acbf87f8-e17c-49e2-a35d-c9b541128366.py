from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Text("Quadratic Equations Explained", font_size=48)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)

        # Define a Quadratic Equation
        quadratic_form = MathTex("ax^2 + bx + c = 0", font_size=48)
        self.play(Write(quadratic_form), run_time=2)
        self.wait(1)

        # Explain coefficients a, b, and c
        a_explanation = MathTex("a \\neq 0", font_size=36).shift(UP * 2.5 + LEFT * 3)
        b_explanation = Text("b: Coefficient of x", font_size=36).shift(UP * 2.5)
        c_explanation = Text("c: Constant term", font_size=36).shift(UP * 2.5 + RIGHT * 3)

        a_arrow = Arrow(quadratic_form.get_parts_by_tex("a")[0].get_center() + DOWN * 0.2, a_explanation.get_center() + UP * 0.2, buff=0.3)
        b_arrow = Arrow(quadratic_form.get_parts_by_tex("b")[0].get_center() + DOWN * 0.2, b_explanation.get_center() + UP * 0.2, buff=0.3)
        c_arrow = Arrow(quadratic_form.get_parts_by_tex("c")[0].get_center() + DOWN * 0.2, c_explanation.get_center() + UP * 0.2, buff=0.3)

        self.play(Create(a_explanation), Create(a_arrow), run_time=1)
        self.play(Create(b_explanation), Create(b_arrow), run_time=1)
        self.play(Create(c_explanation), Create(c_arrow), run_time=1)
        self.wait(2)
        self.play(FadeOut(a_explanation, b_explanation, c_explanation, a_arrow, b_arrow, c_arrow), run_time=1)

        # Solving Quadratic Equations - Factoring
        factoring_title = Text("Solving by Factoring", font_size=42).shift(UP * 3)
        self.play(ReplacementTransform(quadratic_form, factoring_title), run_time=1)
        self.wait(1)

        example_equation = MathTex("x^2 + 5x + 6 = 0", font_size=40).shift(UP * 1.5)
        self.play(Write(example_equation), run_time=1.5)
        self.wait(1)

        factored_equation = MathTex("(x + 2)(x + 3) = 0", font_size=40).shift(DOWN * 0.0)
        self.play(Transform(example_equation, factored_equation), run_time=1.5)
        self.wait(1)

        solutions = MathTex("x = -2, -3", font_size=40).shift(DOWN * 1.5)
        self.play(Write(solutions), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(factoring_title, factored_equation, solutions), run_time=1)

        # Solving Quadratic Equations - Quadratic Formula
        formula_title = Text("Solving by Quadratic Formula", font_size=42).shift(UP * 3)
        self.play(Write(formula_title), run_time=1)
        self.wait(1)

        quadratic_formula = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", font_size=40).shift(UP * 1)
        self.play(Write(quadratic_formula), run_time=2)
        self.wait(2)

        example_equation2 = MathTex("2x^2 + 5x - 3 = 0", font_size=40).shift(DOWN * 0.5)
        self.play(Write(example_equation2), run_time=1.5)
        self.wait(1)

        substitution = MathTex("x = \\frac{-5 \\pm \\sqrt{5^2 - 4(2)(-3)}}{2(2)}", font_size=36).shift(DOWN * 1.7)
        self.play(Write(substitution), run_time=2)
        self.wait(2)

        solution_formula = MathTex("x = \\frac{-5 \\pm \\sqrt{49}}{4}", font_size=36).shift(DOWN * 2.7)
        self.play(Transform(substitution, solution_formula), run_time=1.5)
        self.wait(1)

        solution_formula2 = MathTex("x = \\frac{-5 \\pm 7}{4}", font_size=36).shift(DOWN * 1.7)
        self.play(Transform(solution_formula, solution_formula2), run_time=1.5)
        self.wait(1)

        solutions2 = MathTex("x = \\frac{1}{2}, -3", font_size=40).shift(DOWN * 0.5)
        self.play(Transform(example_equation2, solutions2), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(formula_title, quadratic_formula, example_equation2, solution_formula2), run_time=1)
        self.play(FadeOut(solutions2), run_time=0.5) # Clean up from previous Transform

        # Conclusion
        conclusion = Text("Quadratic equations are useful in many fields!", font_size=48)
        self.play(Write(conclusion), run_time=2)
        self.wait(2)

        self.play(FadeOut(*self.mobjects), run_time=1)