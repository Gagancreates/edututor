from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- Introduction: What are Quadratic Equations? ---
        # Display the main title of the animation.
        title = Text("Understanding Quadratic Equations", color=BLUE_B).scale(1.2)
        self.play(Write(title), run_time=2)
        self.wait(3.5) # Pause to let the viewer read the title

        # Introduce the basic definition of a quadratic equation.
        definition_text = Text(
            "Equations where the highest power of the variable is 2.",
            font_size=36
        ).next_to(title, DOWN, buff=0.8)
        self.play(FadeIn(definition_text, shift=UP), run_time=2)
        self.wait(4) # Give time for definition comprehension

        # Fade out the introductory text to make way for the general form.
        self.play(FadeOut(title, shift=UP), FadeOut(definition_text, shift=UP), run_time=1.5)
        self.wait(2)

        # Introduce the general form of a quadratic equation.
        general_form_label = Text("General Form:", color=YELLOW_A).to_edge(UP + LEFT)
        self.play(Write(general_form_label), run_time=1.5)
        self.wait(2.5)

        # Display the mathematical general form.
        quadratic_equation = MathTex("ax^2 + bx + c = 0", color=WHITE).scale(1.5)
        self.play(Write(quadratic_equation), run_time=3)
        self.wait(4) # Pause on the main equation

        # Explain the role of coefficients a, b, and c.
        a_text = Text("a: coefficient of x²", font_size=30, color=RED).next_to(quadratic_equation, DOWN, buff=0.5).shift(LEFT*3)
        b_text = Text("b: coefficient of x", font_size=30, color=GREEN).next_to(a_text, RIGHT, buff=1)
        c_text = Text("c: constant term", font_size=30, color=PURPLE).next_to(b_text, RIGHT, buff=1)

        self.play(Write(a_text), run_time=1.5)
        self.play(Write(b_text), run_time=1.5)
        self.play(Write(c_text), run_time=1.5)
        self.wait(4.5) # Allow time to digest the coefficients

        # Emphasize that 'a' cannot be zero.
        a_not_zero = MathTex("a \\neq 0", color=RED).scale(1.2).next_to(quadratic_equation, RIGHT, buff=1.5).shift(UP*0.5)
        a_not_zero_explanation = Text("Otherwise, it's not quadratic!", font_size=30).next_to(a_not_zero, DOWN, buff=0.5)

        self.play(Create(a_not_zero), run_time=1.5)
        self.play(Write(a_not_zero_explanation), run_time=2)
        self.wait(5.5) # Explain the importance of 'a'

        # Clear the screen from the coefficient explanations.
        self.play(
            FadeOut(general_form_label),
            FadeOut(a_text), FadeOut(b_text), FadeOut(c_text),
            FadeOut(a_not_zero), FadeOut(a_not_zero_explanation),
            run_time=2
        )
        self.wait(3)

        # --- Visualizing the Graph: Parabola ---
        # Move the quadratic equation to the top for context and introduce graph concept.
        self.play(quadratic_equation.animate.scale(0.8).to_edge(UP), run_time=1.5)
        self.wait(2.5)

        graph_title = Text("Graphs as Parabolas", color=YELLOW_A).to_edge(UL)
        self.play(Write(graph_title), run_time=1.5)
        self.wait(2.5)

        # Create coordinate axes for graphing.
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 8, 2],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        self.play(Create(axes), Write(axes_labels), run_time=2)
        self.wait(3)

        # Plot a simple parabola (y = x^2) and its equation.
        parabola = axes.get_graph(lambda x: x**2, color=ORANGE)
        parabola_eq = MathTex("y = x^2", color=ORANGE).next_to(parabola, RIGHT, buff=0.5)

        self.play(Create(parabola), run_time=2.5)
        self.play(Write(parabola_eq), run_time=1.5)
        self.wait(5) # Observe the basic parabola shape

        # Explain that solutions are the x-intercepts (roots).
        roots_text = Text("Solutions are x-intercepts (roots)", font_size=36).to_edge(DOWN)
        self.play(FadeIn(roots_text, shift=DOWN), run_time=2)
        self.wait(3)

        # Mark the root for y = x^2.
        dot1 = Dot(axes.coords_to_point(0, 0), color=RED)
        label1 = Tex("0", color=RED).next_to(dot1, DOWN)
        self.play(Create(dot1), Write(label1), run_time=1.5)
        self.wait(4.5)

        # Show another parabola example (y = -x^2 + 4) to illustrate varying roots.
        parabola_open_down = axes.get_graph(lambda x: -x**2 + 4, color=BLUE)
        parabola_open_down_eq = MathTex("y = -x^2 + 4", color=BLUE).next_to(parabola_open_down, LEFT, buff=0.5)
        self.play(ReplacementTransform(parabola, parabola_open_down), ReplacementTransform(parabola_eq, parabola_open_down_eq), run_time=2)
        self.wait(4.5)

        # Mark the roots for the new parabola.
        dot_left = Dot(axes.coords_to_point(-2, 0), color=RED)
        label_left = Tex("-2", color=RED).next_to(dot_left, DOWN)
        dot_right = axes.coords_to_point(2, 0)
        label_right = Tex("2", color=RED).next_to(dot_right, DOWN)
        self.play(Transform(dot1, dot_left), Transform(label1, label_left), Create(Dot(dot_right)), Write(label_right), run_time=2)
        self.wait(6.5)

        # Clear all graph-related elements.
        self.play(
            FadeOut(graph_title),
            FadeOut(axes),
            FadeOut(axes_labels),
            FadeOut(parabola_open_down),
            FadeOut(parabola_open_down_eq),
            FadeOut(roots_text),
            FadeOut(dot1), # This is dot_left now
            FadeOut(label1), # This is label_left now
            FadeOut(Dot(dot_right)), # This is the Dot object for dot_right coords
            FadeOut(label_right),
            run_time=2.5
        )
        self.wait(4.5)

        # --- Solving Quadratic Equations: Quadratic Formula ---
        # Transform the quadratic equation text into a new title for solving methods.
        solving_title = Text("Solving Quadratic Equations", color=BLUE_B).to_edge(UP)
        self.play(Transform(quadratic_equation, solving_title), run_time=1.5)
        self.wait(3)

        # Introduce the quadratic formula.
        formula_label = Text("The Quadratic Formula:", color=YELLOW_A).shift(UP * 2)
        self.play(Write(formula_label), run_time=1.5)
        self.wait(3)

        # Display the quadratic formula.
        quadratic_formula = MathTex(
            "x = {-b \\pm \\sqrt{b^2 - 4ac}} \\over {2a}",
            color=GREEN_SCREEN
        ).scale(1.5)
        self.play(Write(quadratic_formula), run_time=3)
        self.wait(5) # Give ample time to see the formula

        # Explain the discriminant part of the formula.
        discriminant_label = Text("The Discriminant:", color=PINK).shift(DOWN * 2)
        self.play(Write(discriminant_label), run_time=1.5)
        self.wait(3.5)

        discriminant_formula = MathTex("\\Delta = b^2 - 4ac", color=PINK).next_to(discriminant_label, DOWN, buff=0.5).scale(1.2)
        self.play(Write(discriminant_formula), run_time=2)
        self.wait(4.5)

        # Explain the cases for the discriminant determining the number of solutions.
        case1_text = Text("1. If Δ > 0:", font_size=36, color=ORANGE).shift(LEFT*3 + DOWN*0.5)
        case1_result = Text("Two distinct real solutions", font_size=30).next_to(case1_text, DOWN, buff=0.3)
        self.play(Write(case1_text), FadeIn(case1_result, shift=RIGHT), run_time=2)
        self.wait(4.5)

        case2_text = Text("2. If Δ = 0:", font_size=36, color=ORANGE).shift(LEFT*3 + DOWN*1.7)
        case2_result = Text("One real solution (repeated)", font_size=30).next_to(case2_text, DOWN, buff=0.3)
        self.play(Write(case2_text), FadeIn(case2_result, shift=RIGHT), run_time=2)
        self.wait(4.5)

        case3_text = Text("3. If Δ < 0:", font_size=36, color=ORANGE).shift(LEFT*3 + DOWN*2.9)
        case3_result = Text("No real solutions (complex solutions)", font_size=30).next_to(case3_text, DOWN, buff=0.3)
        self.play(Write(case3_text), FadeIn(case3_result, shift=RIGHT), run_time=2)
        self.wait(5)

        # Clear the solving section.
        self.play(
            FadeOut(quadratic_equation), # This was the transformed solving_title
            FadeOut(formula_label),
            FadeOut(quadratic_formula),
            FadeOut(discriminant_label),
            FadeOut(discriminant_formula),
            FadeOut(case1_text), FadeOut(case1_result),
            FadeOut(case2_text), FadeOut(case2_result),
            FadeOut(case3_text), FadeOut(case3_result),
            run_time=2.5
        )
        self.wait(4.5)

        # --- Conclusion ---
        # Display the conclusion title.
        summary_title = Text("Key Takeaways", color=BLUE_B).to_edge(UP)
        self.play(Write(summary_title), run_time=1.5)
        self.wait(2.5)

        # Summarize the main points learned.
        point1 = Text("1. General form: ax² + bx + c = 0 (a ≠ 0)", font_size=36).shift(UP * 1.5 + LEFT * 0.5)
        point2 = Text("2. Graphs are parabolas (U-shaped)", font_size=36).next_to(point1, DOWN, buff=0.7).align_to(point1, LEFT)
        point3 = Text("3. Solved using the Quadratic Formula", font_size=36).next_to(point2, DOWN, buff=0.7).align_to(point1, LEFT)
        point4 = Text("4. Discriminant (Δ) determines number of solutions", font_size=36).next_to(point3, DOWN, buff=0.7).align_to(point1, LEFT)

        self.play(FadeIn(point1, shift=LEFT), run_time=1.5)
        self.play(FadeIn(point2, shift=LEFT), run_time=1.5)
        self.play(FadeIn(point3, shift=LEFT), run_time=1.5)
        self.play(FadeIn(point4, shift=LEFT), run_time=1.5)
        self.wait(10) # Ample time for summary review

        # Display a thank you message.
        thank_you = Text("Thank you for watching!", color=GREEN_A).scale(1.2)
        self.play(
            FadeOut(summary_title),
            FadeOut(point1),
            FadeOut(point2),
            FadeOut(point3),
            FadeOut(point4),
            FadeIn(thank_you),
            run_time=2
        )
        self.wait(4)

        # Final cleanup of the scene.
        self.play(FadeOut(*self.mobjects), run_time=1.5)