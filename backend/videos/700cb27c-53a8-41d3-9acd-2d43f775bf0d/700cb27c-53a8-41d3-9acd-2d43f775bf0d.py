from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Tex("Quadratic Equations").scale(1.5)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Definition
        definition_text = Tex(
            "A quadratic equation is an equation of the form:",
            " $ax^2 + bx + c = 0$",
            " where $a \\neq 0$."
        ).scale(0.8)
        self.play(Write(definition_text))
        self.wait(2)

        a, b, c = MathTex("a"), MathTex("b"), MathTex("c")
        a_explanation = Tex("a: Quadratic coefficient").scale(0.6).next_to(a, DOWN)
        b_explanation = Tex("b: Linear coefficient").scale(0.6).next_to(b, DOWN)
        c_explanation = Tex("c: Constant term").scale(0.6).next_to(c, DOWN)

        self.play(TransformMatchingTex(definition_text[1], VGroup(a,MathTex("x^2"),MathTex("+"),b,MathTex("x"),MathTex("+"),c,MathTex("="),MathTex("0"))))
        self.wait(1)
        a.move_to([-4, -2, 0])
        b.move_to([0, -2, 0])
        c.move_to([4, -2, 0])
        self.play(Write(a_explanation), Write(b_explanation), Write(c_explanation))

        self.wait(2)
        self.play(FadeOut(definition_text, a_explanation, b_explanation, c_explanation, a, MathTex("x^2"), MathTex("+"), b, MathTex("x"), MathTex("+"), c, MathTex("="), MathTex("0")))

        # Example Equation
        example_equation = MathTex("x^2 - 5x + 6 = 0").scale(1.2)
        self.play(Write(example_equation))
        self.wait(1)

        # Solving by Factoring
        factoring_text = Tex("Solving by Factoring").scale(1)
        factoring_text.to_edge(UP)
        self.play(Write(factoring_text))

        factored_equation = MathTex("(x - 2)(x - 3) = 0").scale(1.2).next_to(example_equation, DOWN, buff=0.5)
        self.play(Write(factored_equation))
        self.wait(1)

        x_equals_2 = MathTex("x - 2 = 0 \\Rightarrow x = 2").scale(1).next_to(factored_equation, DOWN, buff=0.5)
        x_equals_3 = MathTex("x - 3 = 0 \\Rightarrow x = 3").scale(1).next_to(x_equals_2, DOWN, buff=0.5)
        self.play(Write(x_equals_2), Write(x_equals_3))
        self.wait(2)

        self.play(FadeOut(example_equation, factoring_text, factored_equation, x_equals_2, x_equals_3))

        # Quadratic Formula
        quadratic_formula_text = Tex("The Quadratic Formula").scale(1)
        quadratic_formula_text.to_edge(UP)
        self.play(Write(quadratic_formula_text))

        formula = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}").scale(1.2)
        self.play(Write(formula))
        self.wait(2)

        # Applying the Formula to the same equation: x^2 - 5x + 6 = 0
        example_equation_2 = MathTex("x^2 - 5x + 6 = 0").scale(1)
        self.play(Write(example_equation_2))
        self.wait(1)

        a_val = MathTex("a = 1").scale(0.8).next_to(example_equation_2, DOWN, buff=0.5)
        b_val = MathTex("b = -5").scale(0.8).next_to(a_val, DOWN, buff=0.5)
        c_val = MathTex("c = 6").scale(0.8).next_to(b_val, DOWN, buff=0.5)
        self.play(Write(a_val), Write(b_val), Write(c_val))
        self.wait(1)

        substituted_formula = MathTex("x = \\frac{-(-5) \\pm \\sqrt{(-5)^2 - 4(1)(6)}}{2(1)}").scale(0.8).next_to(c_val, DOWN, buff=0.5)
        self.play(Write(substituted_formula))
        self.wait(2)

        simplified_formula = MathTex("x = \\frac{5 \\pm \\sqrt{25 - 24}}{2} = \\frac{5 \\pm 1}{2}").scale(0.8).next_to(substituted_formula, DOWN, buff=0.5)
        self.play(Write(simplified_formula))
        self.wait(2)

        x_equals_4 = MathTex("x = \\frac{5 + 1}{2} = 3").scale(0.8).next_to(simplified_formula, DOWN, buff=0.5)
        x_equals_5 = MathTex("x = \\frac{5 - 1}{2} = 2").scale(0.8).next_to(x_equals_4, DOWN, buff=0.5)
        self.play(Write(x_equals_4), Write(x_equals_5))

        self.wait(2)
        self.play(FadeOut(quadratic_formula_text, formula, example_equation_2, a_val, b_val, c_val, substituted_formula, simplified_formula, x_equals_4, x_equals_5))

        # Graphing Quadratic Equations
        graph_text = Tex("Graphing Quadratic Equations").scale(1)
        graph_text.to_edge(UP)
        self.play(Write(graph_text))

        axes = Axes(x_range=[-5, 5, 1], y_range=[-5, 10, 1], axis_config={"include_tip": False})
        labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(labels))

        parabola = axes.plot(lambda x: x**2 - 5*x + 6, color=GREEN)
        self.play(Create(parabola))
        self.wait(1)

        vertex = axes.coords_to_point(2.5, -0.25)
        vertex_dot = Dot(vertex, color=RED)
        vertex_label = Tex("Vertex").scale(0.6).next_to(vertex_dot, UP, buff=0.1)
        self.play(Create(vertex_dot), Write(vertex_label))

        roots = [2, 3]
        root_dots = [Dot(axes.coords_to_point(root, 0), color=YELLOW) for root in roots]
        root_labels = [Tex("Root").scale(0.6).next_to(root_dot, DOWN, buff=0.1) for root_dot in root_dots]
        self.play(*[Create(dot) for dot in root_dots], *[Write(label) for label in root_labels])

        self.wait(3)

        self.play(FadeOut(graph_text, axes, labels, parabola, vertex_dot, vertex_label, *root_dots, *root_labels))

        # Conclusion
        conclusion_text = Tex("Quadratic equations are everywhere!").scale(1)
        self.play(Write(conclusion_text))
        self.wait(2)
        self.play(FadeOut(conclusion_text))

        thanks = Tex("Thanks for watching!").scale(1.2)
        self.play(Write(thanks))
        self.wait(2)
        self.play(FadeOut(thanks))