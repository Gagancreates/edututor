from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Text("Quadratic Equations Explained")
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)

        # General form of a quadratic equation
        general_form_text = Text("General Form:")
        general_form_eq = MathTex(r"ax^2 + bx + c = 0")
        general_form_group = VGroup(general_form_text, general_form_eq).arrange(DOWN)
        self.play(Write(general_form_text), run_time=1)
        self.play(Write(general_form_eq), run_time=1.5)
        self.wait(2)

        # Explanation of coefficients
        a_text = MathTex("a", color=RED).move_to(general_form_eq[0][0].get_center()).shift(DOWN * 0.7)
        b_text = MathTex("b", color=GREEN).move_to(general_form_eq[0][2].get_center()).shift(DOWN * 0.7)
        c_text = MathTex("c", color=BLUE).move_to(general_form_eq[0][4].get_center()).shift(DOWN * 0.7)
        a_explain = Text("Coefficient of x²", color=RED).scale(0.6).next_to(a_text, DOWN)
        b_explain = Text("Coefficient of x", color=GREEN).scale(0.6).next_to(b_text, DOWN)
        c_explain = Text("Constant term", color=BLUE).scale(0.6).next_to(c_text, DOWN)
        self.play(Write(a_text), Write(b_text), Write(c_text), run_time=1)
        self.play(Write(a_explain), Write(b_explain), Write(c_explain), run_time=1)
        self.wait(2)
        self.play(FadeOut(a_text, b_text, c_text, a_explain, b_explain, c_explain), run_time=1)

        # Example 1: x^2 + 5x + 6 = 0
        example_eq_text = Text("Example:")
        example_eq = MathTex(r"x^2 + 5x + 6 = 0")
        example_group = VGroup(example_eq_text, example_eq).arrange(DOWN).move_to(DOWN * 1.5)
        self.play(Write(example_eq_text), run_time=1)
        self.play(Write(example_eq), run_time=1.5)
        self.wait(2)

        # Factoring the equation
        factoring_text = Text("Factoring:", color=YELLOW).next_to(example_group, DOWN * 2)
        factored_eq = MathTex(r"(x + 2)(x + 3) = 0", color=YELLOW).next_to(factoring_text, DOWN)
        self.play(Write(factoring_text), run_time=1)
        self.play(Write(factored_eq), run_time=1.5)
        self.wait(2)

        # Finding the roots
        roots_text = Text("Roots:", color=ORANGE).next_to(factored_eq, DOWN * 2)
        root1 = MathTex(r"x = -2", color=ORANGE).next_to(roots_text, DOWN)
        root2 = MathTex(r"x = -3", color=ORANGE).next_to(root1, RIGHT)
        self.play(Write(roots_text), run_time=1)
        self.play(Write(root1), Write(root2), run_time=1.5)
        self.wait(2)

        # Quadratic formula
        self.play(FadeOut(example_group, factoring_text, factored_eq, roots_text, root1, root2), run_time=1)
        quadratic_formula_text = Text("Quadratic Formula:")
        quadratic_formula = MathTex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
        formula_group = VGroup(quadratic_formula_text, quadratic_formula).arrange(DOWN)
        self.play(ReplacementTransform(general_form_group, formula_group), run_time=1.5)
        self.wait(3)

        # Importance of quadratic equations
        importance_text = Text("Quadratic equations are used in many fields:", color=GREEN).shift(UP * 2)
        fields_list = BulletedList("Physics", "Engineering", "Economics", "Computer Science", color=GREEN)
        fields_list.next_to(importance_text, DOWN)
        self.play(Write(importance_text), run_time=1)
        self.play(Write(fields_list), run_time=2)
        self.wait(3)

        # Conclusion
        conclusion_text = Text("Understanding quadratic equations is crucial!", color=BLUE).shift(DOWN * 2)
        self.play(Write(conclusion_text), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(*self.mobjects), run_time=1)