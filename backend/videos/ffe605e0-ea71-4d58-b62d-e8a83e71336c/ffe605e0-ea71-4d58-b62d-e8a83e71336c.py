from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction: What are Quadratic Equations?
        # Set up the title of the animation
        title = Text("What are Quadratic Equations?", color=BLUE_B).scale(1.2)
        self.play(Write(title), run_time=2)
        self.wait(2)

        # Introduce the basic definition
        definition = Text("An equation of degree 2.", color=WHITE).next_to(title, DOWN, buff=0.8)
        self.play(Write(definition), run_time=2)
        self.wait(3)

        # Transition the title to the top and fade out definition
        self.play(FadeOut(definition), run_time=1)
        self.play(title.animate.to_edge(UP).scale(0.8), run_time=1)
        self.wait(1)

        # General Form of a Quadratic Equation
        general_form_text = Text("General Form:", color=YELLOW).next_to(title, DOWN, buff=0.7)
        general_form = MathTex("ax^2 + bx + c = 0", color=GREEN_C).next_to(general_form_text, DOWN, buff=0.5).scale(1.5)
        self.play(Write(general_form_text), run_time=1.5)
        self.play(Create(general_form), run_time=2.5)
        self.wait(5) # Give ample time to observe the general form

        # Understanding the Terms: a, b, c
        # Highlight and explain coefficient 'a'
        a_coeff = general_form.get_parts_by_tex("a")
        self.play(Indicate(a_coeff, color=RED), run_time=1.5)
        a_text = Text("'a' is the coefficient of x²", color=RED).next_to(general_form, DOWN, buff=0.5).shift(LEFT*2)
        self.play(Write(a_text), run_time=2)
        self.wait(3.5)

        # Highlight and explain coefficient 'b'
        b_coeff = general_form.get_parts_by_tex("b")
        self.play(FadeOut(a_text), run_time=0.5)
        self.play(Indicate(b_coeff, color=BLUE), run_time=1.5)
        b_text = Text("'b' is the coefficient of x", color=BLUE).next_to(general_form, DOWN, buff=0.5).shift(LEFT*2)
        self.play(Write(b_text), run_time=2)
        self.wait(3.5)

        # Highlight and explain constant term 'c'
        c_coeff = general_form.get_parts_by_tex("c")
        self.play(FadeOut(b_text), run_time=0.5)
        self.play(Indicate(c_coeff, color=ORANGE), run_time=1.5)
        c_text = Text("'c' is the constant term", color=ORANGE).next_to(general_form, DOWN, buff=0.5).shift(LEFT*2)
        self.play(Write(c_text), run_time=2)
        self.wait(3.5)

        self.play(FadeOut(c_text), run_time=0.5)

        # Important condition: 'a' cannot be zero
        a_neq_0 = MathTex("a \\neq 0", color=PURPLE).next_to(general_form, DOWN, buff=0.5)
        self.play(FadeIn(a_neq_0), run_time=1.5)
        explanation_neq_0 = Text("If a = 0, it's not quadratic!", color=LIGHT_GRAY).next_to(a_neq_0, DOWN, buff=0.5).scale(0.8)
        self.play(Write(explanation_neq_0), run_time=2)
        self.wait(5) # Long wait for a critical concept

        # Transition to visualization
        self.play(FadeOut(general_form_text, general_form, a_neq_0, explanation_neq_0), run_time=1.5)
        self.wait(1)

        # Visualizing Quadratic Equations: The Parabola
        visualization_title = Text("Visualizing Quadratics: The Parabola", color=YELLOW_A).scale(1)
        self.play(Write(visualization_title), run_time=2)
        self.wait(2)
        self.play(visualization_title.animate.to_edge(UP).scale(0.8), run_time=1.5)
        self.wait(1)

        # Create coordinate axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": GRAY},
            x_axis_config={"numbers_to_include": [-2, -1, 1, 2]},
            y_axis_config={"numbers_to_include": [1, 2, 3, 4]}
        ).add_coordinates()
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        self.play(Create(axes), Create(axes_labels), run_time=2.5)
        self.wait(2.5)

        # Plot a simple parabola y = x^2 - 1 to show roots clearly
        parabola_eq_text = MathTex("y = x^2 - 1", color=PURPLE_C).next_to(axes, UP, buff=0.5).shift(LEFT*2)
        graph = axes.get_graph(lambda x: x**2 - 1, x_range=[-2.2, 2.2], color=TEAL_C)

        self.play(Write(parabola_eq_text), run_time=1.5)
        self.play(Create(graph), run_time=2.5)
        self.wait(4) # Allow time to see the graph

        # Explain roots as x-intercepts
        roots_text = Text("Solutions (roots) are x-intercepts:", color=YELLOW).next_to(parabola_eq_text, DOWN, buff=0.5).scale(0.8)
        self.play(Write(roots_text), run_time=2)
        self.wait(1.5)

        # Mark the roots on the graph
        root1_dot = Dot(axes.c2p(-1, 0), color=RED)
        root2_dot = Dot(axes.c2p(1, 0), color=RED)
        root1_label = MathTex("x = -1", color=RED).next_to(root1_dot, DOWN)
        root2_label = MathTex("x = 1", color=RED).next_to(root2_dot, DOWN)

        self.play(FadeIn(root1_dot, root2_dot), run_time=1.5)
        self.play(Write(root1_label), Write(root2_label), run_time=2)
        self.wait(5) # Observe the roots

        # Transition to finding solutions with the formula
        self.play(FadeOut(axes, axes_labels, graph, parabola_eq_text, roots_text, root1_dot, root2_dot, root1_label, root2_label, visualization_title), run_time=2)
        self.wait(1)

        # Finding the Solutions: The Quadratic Formula
        formula_intro_text = Text("How to find these solutions?", color=BLUE_B).scale(1.1)
        self.play(Write(formula_intro_text), run_time=2)
        self.wait(2.5)

        formula_text = Text("Using the Quadratic Formula!", color=YELLOW_A).next_to(formula_intro_text, DOWN, buff=0.7)
        self.play(Write(formula_text), run_time=2)
        self.wait(3)

        self.play(FadeOut(formula_intro_text, formula_text), run_time=1)

        # Display the Quadratic Formula
        quadratic_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            color=GREEN_A
        ).scale(1.5)
        self.play(Write(quadratic_formula), run_time=4) # Longer run_time for complex formula
        self.wait(6) # Ample time to read and understand the formula

        # Explain the Discriminant
        discriminant_intro = Text("The part under the square root is important:", color=WHITE).to_edge(UP)
        self.play(FadeIn(discriminant_intro), run_time=1.5)
        self.wait(1.5)

        discriminant_formula = MathTex("\\Delta = b^2 - 4ac", color=ORANGE).next_to(discriminant_intro, DOWN, buff=0.7).scale(1.2)
        
        # Highlight the discriminant part in the main formula
        discriminant_in_formula = quadratic_formula.submobjects[6] 
        discriminant_box = SurroundingRectangle(discriminant_in_formula, color=ORANGE, buff=0.1)

        self.play(Create(discriminant_box), run_time=1.5)
        self.play(Write(discriminant_formula), run_time=2)
        self.wait(4.5) # Time to connect the discriminant to the formula

        self.play(FadeOut(discriminant_box), run_time=1)

        # Cases for Discriminant
        discriminant_cases_title = Text("This is the Discriminant (Δ)", color=YELLOW_B).next_to(discriminant_formula, UP, buff=0.5)
        self.play(Transform(discriminant_intro, discriminant_cases_title), run_time=1.5)
        self.wait(1.5)

        # Case 1: Two real solutions
        case1_delta = MathTex("\\Delta > 0", color=RED).next_to(discriminant_formula, DOWN, buff=0.7).align_to(discriminant_formula, LEFT)
        case1_text = Text("Two distinct real solutions", color=WHITE).next_to(case1_delta, RIGHT, buff=0.5)
        self.play(Write(case1_delta), Write(case1_text), run_time=2)
        self.wait(4.5)

        # Case 2: One real solution
        case2_delta = MathTex("\\Delta = 0", color=BLUE).next_to(case1_delta, DOWN, buff=0.5).align_to(case1_delta, LEFT)
        case2_text = Text("One real solution (repeated)", color=WHITE).next_to(case2_delta, RIGHT, buff=0.5)
        self.play(Write(case2_delta), Write(case2_text), run_time=2)
        self.wait(4.5)

        # Case 3: No real solutions
        case3_delta = MathTex("\\Delta < 0", color=PURPLE).next_to(case2_delta, DOWN, buff=0.5).align_to(case2_delta, LEFT)
        case3_text = Text("No real solutions", color=WHITE).next_to(case3_delta, RIGHT, buff=0.5)
        self.play(Write(case3_delta), Write(case3_text), run_time=2)
        self.wait(4.5)

        # Conclusion
        self.play(FadeOut(quadratic_formula, discriminant_intro, discriminant_formula, case1_delta, case1_text, case2_delta, case2_text, case3_delta, case3_text), run_time=2)
        self.wait(1)

        # Recap the general form and importance
        final_recap_text = Text("Quadratic Equations:", color=YELLOW).scale(1.1).to_edge(UP)
        final_form = MathTex("ax^2 + bx + c = 0", color=GREEN_C).next_to(final_recap_text, DOWN, buff=0.8).scale(1.5)
        self.play(Write(final_recap_text), run_time=1.5)
        self.play(Create(final_form), run_time=2)
        self.wait(4.5)

        importance_text = Text("Fundamental in Math & Science!", color=WHITE).next_to(final_form, DOWN, buff=0.7)
        self.play(Write(importance_text), run_time=2)
        self.wait(5)

        # End Scene by fading out all mobjects
        self.play(FadeOut(*self.mobjects), run_time=2)