from manim import *

class CreateScene(Scene):
    def construct(self):
        # Title
        title = Text("Quadratic Equations Explained", font_size=48)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title))

        # General form
        general_form = MathTex(r"ax^2 + bx + c = 0", font_size=40)
        self.play(Write(general_form), run_time=2)
        self.wait(1)

        # Explanation of a, b, c
        a_explanation = Text("Where a, b, and c are constants", font_size=24)
        a_explanation.next_to(general_form, DOWN)
        self.play(Write(a_explanation), run_time=1.5)
        self.wait(1)

        # Example equation
        example_equation = MathTex(r"2x^2 + 5x - 3 = 0", font_size=40, color=GREEN)
        example_equation.next_to(a_explanation, DOWN, buff=0.5)
        self.play(Write(example_equation), run_time=2)
        self.wait(1)

        # Identifying a, b, c in the example
        a_value = MathTex("a = 2", font_size=30, color=BLUE).next_to(example_equation, DOWN, buff=0.5).shift(LEFT * 2)
        b_value = MathTex("b = 5", font_size=30, color=BLUE).next_to(a_value, RIGHT * 4)
        c_value = MathTex("c = -3", font_size=30, color=BLUE).next_to(b_value, RIGHT * 4)

        self.play(Write(a_value), Write(b_value), Write(c_value), run_time=1.5)
        self.wait(1)

        # Methods to solve (brief mention)
        methods_title = Text("Methods to Solve:", font_size=36).next_to(a_value, DOWN, buff=1).shift(LEFT * 3)
        self.play(Write(methods_title), run_time=1)
        
        factoring = Text("1. Factoring", font_size=24).next_to(methods_title, DOWN, aligned_edge=LEFT)
        quadratic_formula = Text("2. Quadratic Formula", font_size=24).next_to(factoring, DOWN, aligned_edge=LEFT)
        completing_square = Text("3. Completing the Square", font_size=24).next_to(quadratic_formula, DOWN, aligned_edge=LEFT)
        
        self.play(Write(factoring), run_time=0.75)
        self.play(Write(quadratic_formula), run_time=0.75)
        self.play(Write(completing_square), run_time=0.75)

        self.wait(2)

        self.play(FadeOut(*self.mobjects))