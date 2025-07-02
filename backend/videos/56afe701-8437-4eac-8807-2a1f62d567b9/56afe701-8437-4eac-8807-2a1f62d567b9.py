from manim import *

class CreateScene(Scene):
    def construct(self):
        # 1. Introduction - Title and Basic Definition
        title = Text("Understanding Quadratic Equations", color=BLUE).scale(1.2)
        self.play(Write(title), run_time=1.5)
        self.wait(1)

        definition = Text("Equations with the highest power of 2 for a variable.", font_size=36)
        definition.next_to(title, DOWN, buff=0.8)
        self.play(Write(definition), run_time=2)
        self.wait(1.5)

        self.play(FadeOut(title, shift=UP), FadeOut(definition, shift=UP), run_time=1)
        self.wait(0.5)

        # 2. Standard Form of a Quadratic Equation
        standard_form_text = Text("The Standard Form:", color=GREEN).to_edge(UP)
        standard_form_equation = MathTex("ax^2 + bx + c = 0", color=YELLOW).scale(1.5)
        
        self.play(Write(standard_form_text), run_time=1)
        self.play(Write(standard_form_equation), run_time=2)
        self.wait(1.5)

        # 3. Breaking Down the Standard Form
        # Coefficients a, b, c
        a_coeff = MathTex("a", color=RED).next_to(standard_form_equation[0][0], UP, buff=0.5)
        a_label = Text("Coefficient of", font_size=28).next_to(a_coeff, DOWN, buff=0.2)
        a_x_squared = MathTex("x^2", color=YELLOW).next_to(a_label, DOWN, buff=0.1)
        a_info = VGroup(a_coeff, a_label, a_x_squared).move_to(LEFT * 4 + DOWN * 0.5)
        a_arrow = Arrow(start=a_coeff.get_top(), end=standard_form_equation[0][0].get_bottom(), color=RED)

        b_coeff = MathTex("b", color=BLUE).next_to(standard_form_equation[0][4], UP, buff=0.5)
        b_label = Text("Coefficient of", font_size=28).next_to(b_coeff, DOWN, buff=0.2)
        b_x = MathTex("x", color=YELLOW).next_to(b_label, DOWN, buff=0.1)
        b_info = VGroup(b_coeff, b_label, b_x).move_to(LEFT * 0 + DOWN * 0.5)
        b_arrow = Arrow(start=b_coeff.get_top(), end=standard_form_equation[0][4].get_bottom(), color=BLUE)

        c_coeff = MathTex("c", color=GREEN).next_to(standard_form_equation[0][8], UP, buff=0.5)
        c_label = Text("Constant Term", font_size=28).next_to(c_coeff, DOWN, buff=0.2)
        c_info = VGroup(c_coeff, c_label).move_to(RIGHT * 4 + DOWN * 0.5)
        c_arrow = Arrow(start=c_coeff.get_top(), end=standard_form_equation[0][8].get_bottom(), color=GREEN)

        self.play(GrowArrow(a_arrow), Write(a_info), run_time=1.2)
        self.wait(0.75)
        self.play(GrowArrow(b_arrow), Write(b_info), run_time=1.2)
        self.wait(0.75)
        self.play(GrowArrow(c_arrow), Write(c_info), run_time=1.2)
        self.wait(1.5)

        not_equal_zero = MathTex("\\text{where } a \\neq 0", color=ORANGE).next_to(standard_form_equation, DOWN, buff=0.5)
        self.play(Write(not_equal_zero), run_time=1)
        self.wait(1)

        self.play(
            FadeOut(standard_form_text),
            FadeOut(a_arrow), FadeOut(a_info),
            FadeOut(b_arrow), FadeOut(b_info),
            FadeOut(c_arrow), FadeOut(c_info),
            FadeOut(not_equal_zero),
            run_time=1
        )
        self.wait(0.5)

        # 4. Examples of Quadratic Equations
        examples_title = Text("Examples", color=PURPLE).to_edge(UP)
        self.play(Transform(standard_form_equation, standard_form_equation.copy().scale(0.8).to_edge(UP)), run_time=1)
        self.add(examples_title) # Add it first, then Write
        self.play(Write(examples_title), run_time=0.8) # Write example title, already positioned
        self.wait(0.5)

        example1_eq = MathTex("1) x^2 - 4x + 4 = 0", color=YELLOW).next_to(standard_form_equation, DOWN, buff=0.7)
        example1_coeffs = MathTex("a=1, b=-4, c=4", color=WHITE).next_to(example1_eq, RIGHT, buff=0.5)

        self.play(Write(example1_eq), run_time=1.2)
        self.play(Write(example1_coeffs), run_time=1)
        self.wait(1.5)

        example2_eq = MathTex("2) 2x^2 + 5 = 0", color=YELLOW).next_to(example1_eq, DOWN, buff=0.7)
        example2_coeffs = MathTex("a=2, b=0, c=5", color=WHITE).next_to(example2_eq, RIGHT, buff=0.5)

        self.play(Write(example2_eq), run_time=1.2)
        self.play(Write(example2_coeffs), run_time=1)
        self.wait(1.5)

        example3_eq = MathTex("3) -x^2 + 3x = 0", color=YELLOW).next_to(example2_eq, DOWN, buff=0.7)
        example3_coeffs = MathTex("a=-1, b=3, c=0", color=WHITE).next_to(example3_eq, RIGHT, buff=0.5)

        self.play(Write(example3_eq), run_time=1.2)
        self.play(Write(example3_coeffs), run_time=1)
        self.wait(1.5)

        self.play(
            FadeOut(examples_title),
            FadeOut(example1_eq), FadeOut(example1_coeffs),
            FadeOut(example2_eq), FadeOut(example2_coeffs),
            FadeOut(example3_eq), FadeOut(example3_coeffs),
            FadeOut(standard_form_equation), # Fade out the standard form too
            run_time=1.5
        )
        self.wait(0.5)

        # 5. Why are they important? - Applications and Solutions
        importance_title = Text("Why are they important?", color=GOLD).to_edge(UP)
        importance_text1 = Text("Used to model trajectories, areas, and many real-world problems.", font_size=36).next_to(importance_title, DOWN, buff=0.8)
        self.play(Write(importance_title), run_time=1)
        self.play(Write(importance_text1), run_time=2)
        self.wait(1.5)

        solutions_text = Text("Finding the 'solutions' or 'roots' means finding the value(s) of x", font_size=36)
        solutions_text2 = Text("that make the equation true.", font_size=36).next_to(solutions_text, DOWN, buff=0.5)
        solutions_group = VGroup(solutions_text, solutions_text2).next_to(importance_text1, DOWN, buff=0.8)

        self.play(Write(solutions_group), run_time=2)
        self.wait(1.5)

        self.play(FadeOut(importance_title), FadeOut(importance_text1), FadeOut(solutions_group), run_time=1)
        self.wait(0.5)

        # 6. Graphical Representation (Parabola)
        graph_title = Text("Graphical Representation", color=PINK).to_edge(UP)
        self.play(Write(graph_title), run_time=1)
        self.wait(0.5)

        # Create Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY, "stroke_width": 2},
            tips=False
        ).scale(0.8).shift(DOWN*0.5)

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        self.play(Create(axes), Create(x_label), Create(y_label), run_time=1.5)

        # Create a sample parabola (e.g., y = x^2 - 1)
        parabola_eq_text = MathTex("y = x^2 - 1", color=YELLOW).scale(0.9).next_to(axes, UP, buff=0.5)
        
        # Define the function for the parabola
        def func(x):
            return x**2 - 1

        parabola = axes.get_graph(func, x_range=[-2.5, 2.5], color=ORANGE)
        
        self.play(Write(parabola_eq_text), run_time=0.8)
        self.play(Create(parabola), run_time=1.5)
        self.wait(1.5)

        # Show roots on the graph
        root1_dot = Dot(axes.c2p(-1, 0), color=RED)
        root2_dot = Dot(axes.c2p(1, 0), color=RED)
        roots_text = Text("Solutions are where the graph crosses the x-axis", font_size=32).next_to(axes, DOWN, buff=0.8)
        roots_text.set_color_by_tex("x-axis", RED)

        self.play(FadeIn(root1_dot, scale=0.5), FadeIn(root2_dot, scale=0.5), run_time=0.75)
        self.play(Write(roots_text), run_time=1.5)
        self.wait(2)

        # 7. Conclusion
        self.play(
            FadeOut(graph_title),
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            FadeOut(parabola_eq_text), FadeOut(parabola),
            FadeOut(root1_dot), FadeOut(root2_dot),
            FadeOut(roots_text),
            run_time=1.5
        )
        self.wait(0.5)

        conclusion_text1 = Text("Quadratic equations are fundamental in mathematics.", color=BLUE).scale(0.9)
        conclusion_text2 = Text("Keep exploring their properties and applications!", color=GREEN).scale(0.9).next_to(conclusion_text1, DOWN, buff=0.7)
        
        self.play(Write(conclusion_text1), run_time=1.5)
        self.play(Write(conclusion_text2), run_time=1.5)
        self.wait(1.5)

        # Final fade out
        self.play(FadeOut(*self.mobjects), run_time=1.5)