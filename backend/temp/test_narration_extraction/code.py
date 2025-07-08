from manim import *

class CreateScene(Scene):
    def construct(self):
        self.run_animation_time = 0.8  # Consistent animation duration
        self.wait_time = 1.5          # Consistent pause duration

        # NARRATION: Welcome to our exploration of algebra! Today, we're going to demystify
        # NARRATION: one of the most powerful tools for solving quadratic equations:
        # NARRATION: the quadratic formula. Let's begin by understanding what a quadratic equation looks like.
        title = Text("Understanding Quadratic Equations", color=WHITE).to_edge(UP)
        animations = []
        animations.append(Write(title, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        # NARRATION: A quadratic equation is a polynomial equation of the second degree,
        # NARRATION: meaning it contains at least one term where the variable is squared.
        # NARRATION: Its standard form is `ax^2 + bx + c = 0`, where 'a', 'b', and 'c' are coefficients,
        # NARRATION: and 'a' cannot be zero.
        standard_form_text = Text("Standard Form:", color=BLUE).next_to(title, DOWN, buff=0.8).to_edge(LEFT)
        standard_form_eq = MathTex(r"ax^2 + bx + c = 0", color=YELLOW).next_to(standard_form_text, RIGHT)

        animations = []
        animations.append(FadeIn(standard_form_text, run_time=self.run_animation_time))
        animations.append(Write(standard_form_eq, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        # NARRATION: To illustrate, let's consider a specific example.
        # NARRATION: We'll solve the equation: `2x^2 + 5x - 3 = 0`.
        # NARRATION: Here, we need to identify the values of 'a', 'b', and 'c'.
        problem_text = Text("Example Problem:", color=BLUE).next_to(standard_form_eq, DOWN, buff=0.8).to_edge(LEFT)
        problem_eq = MathTex(r"2x^2 + 5x - 3 = 0", color=GREEN).next_to(problem_text, RIGHT)

        animations = []
        animations.append(FadeIn(problem_text, run_time=self.run_animation_time))
        animations.append(Write(problem_eq, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        # NARRATION: By comparing our example to the standard form,
        # NARRATION: we can clearly see that 'a' is 2, 'b' is 5, and 'c' is -3.
        a_value = MathTex(r"a = 2", color=ORANGE).next_to(problem_eq, DOWN, buff=0.5).to_edge(LEFT, buff=1.5)
        b_value = MathTex(r"b = 5", color=ORANGE).next_to(a_value, RIGHT, buff=1.5)
        c_value = MathTex(r"c = -3", color=ORANGE).next_to(b_value, RIGHT, buff=1.5)

        animations = []
        animations.append(Write(a_value, run_time=self.run_animation_time))
        animations.append(Write(b_value, run_time=self.run_animation_time))
        animations.append(Write(c_value, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2) # Longer wait to absorb coefficients

        # NARRATION: Now that we've identified our coefficients, let's introduce the strategy:
        # NARRATION: the Quadratic Formula itself. This formula provides a direct way
        # NARRATION: to find the values of 'x' that satisfy a quadratic equation.
        elements_to_fade_out = VGroup(title, standard_form_text, standard_form_eq, problem_text, problem_eq, a_value, b_value, c_value)
        animations = []
        animations.append(FadeOut(elements_to_fade_out, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time / 2)

        strategy_title = Text("The Quadratic Formula", color=WHITE).to_edge(UP)
        animations = []
        animations.append(Write(strategy_title, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        # NARRATION: This is the quadratic formula. It looks complex at first,
        # NARRATION: but by breaking it down, we'll see how straightforward it is to use.
        quadratic_formula_eq = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            color=YELLOW
        ).scale(1.5).move_to(ORIGIN)

        animations = []
        animations.append(Write(quadratic_formula_eq, run_time=self.run_animation_time * 2)) # Longer write for complex formula
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2)

        # NARRATION: Our goal is to substitute the values of 'a', 'b', and 'c' from our example
        # NARRATION: into this formula, and then simplify the expression to find the solutions for 'x'.
        # NARRATION: These solutions are also known as the roots of the equation.
        explanation_formula = Text(
            "Use a=2, b=5, c=-3 to find x.",
            color=WHITE, font_size=30
        ).next_to(quadratic_formula_eq, DOWN, buff=0.8)

        animations = []
        animations.append(Write(explanation_formula, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2)

        elements_to_fade_out = VGroup(strategy_title, quadratic_formula_eq, explanation_formula)
        animations = []
        animations.append(FadeOut(elements_to_fade_out, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time / 2)

        # --- Step-by-Step Solution ---
        # Original problem context for reference
        original_problem_display = MathTex(r"2x^2 + 5x - 3 = 0", color=GREEN).to_corner(UL).scale(0.8)
        coefficients_display = MathTex(r"a=2, b=5, c=-3", color=ORANGE).next_to(original_problem_display, DOWN).scale(0.8)
        initial_formula_display = MathTex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}", color=YELLOW).to_corner(UR).scale(0.8)

        animations = []
        animations.append(FadeIn(original_problem_display, run_time=self.run_animation_time))
        animations.append(FadeIn(coefficients_display, run_time=self.run_animation_time))
        animations.append(FadeIn(initial_formula_display, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        # NARRATION: Let's begin our step-by-step solution.
        # NARRATION: Step 1 involves substituting the identified values of 'a', 'b', and 'c'
        # NARRATION: into the quadratic formula. This is the foundation for all subsequent calculations.
        step1_title = Text("Step 1: Substitute Values", color=BLUE).to_edge(UP)
        animations = []
        animations.append(Write(step1_title, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        substituted_eq = MathTex(
            r"x = \frac{-(5) \pm \sqrt{(5)^2 - 4(2)(-3)}}{2(2)}",
            color=WHITE
        ).scale(1.2).move_to(ORIGIN)

        animations = []
        animations.append(Write(substituted_eq, run_time=self.run_animation_time * 2))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2)

        animations = []
        animations.append(FadeOut(step1_title, substituted_eq, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time / 2)

        # NARRATION: Step 2 focuses on calculating the discriminant, which is the part under the square root:
        # NARRATION: `b^2 - 4ac`. This value tells us about the nature of the roots.
        step2_title = Text("Step 2: Calculate Discriminant (D)", color=BLUE).to_edge(UP)
        animations = []
        animations.append(Write(step2_title, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        discriminant_formula = MathTex(r"D = b^2 - 4ac", color=YELLOW).move_to(ORIGIN).shift(UP)
        discriminant_sub = MathTex(r"D = (5)^2 - 4(2)(-3)", color=WHITE).next_to(discriminant_formula, DOWN)
        discriminant_calc1 = MathTex(r"D = 25 - (-24)", color=WHITE).next_to(discriminant_sub, DOWN)
        discriminant_calc2 = MathTex(r"D = 25 + 24", color=WHITE).next_to(discriminant_calc1, DOWN)
        discriminant_result = MathTex(r"D = 49", color=GREEN).next_to(discriminant_calc2, DOWN)

        animations = []
        animations.append(Write(discriminant_formula, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Write(discriminant_sub, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(discriminant_sub, discriminant_calc1, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(discriminant_calc1, discriminant_calc2, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(ReplacementTransform(discriminant_calc2, discriminant_result, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2)

        animations = []
        animations.append(FadeOut(step2_title, discriminant_formula, discriminant_sub, discriminant_result, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time / 2)


        # NARRATION: Step 3 is to take the square root of the discriminant.
        # NARRATION: Since our discriminant is 49, its square root is simply 7.
        step3_title = Text("Step 3: Square Root of Discriminant", color=BLUE).to_edge(UP)
        animations = []
        animations.append(Write(step3_title, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        sqrt_d_eq = MathTex(r"\sqrt{D} = \sqrt{49}", color=WHITE).scale(1.2).move_to(ORIGIN)
        sqrt_d_result = MathTex(r"\sqrt{D} = 7", color=GREEN).scale(1.2).move_to(ORIGIN)

        animations = []
        animations.append(Write(sqrt_d_eq, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(sqrt_d_eq, sqrt_d_result, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2)

        animations = []
        animations.append(FadeOut(step3_title, sqrt_d_eq, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time / 2)

        # NARRATION: Step 4 is to calculate the denominator of the quadratic formula, which is `2a`.
        # NARRATION: For our problem, with 'a' being 2, this simply becomes 2 times 2.
        step4_title = Text("Step 4: Calculate Denominator (2a)", color=BLUE).to_edge(UP)
        animations = []
        animations.append(Write(step4_title, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        denominator_eq = MathTex(r"2a = 2(2)", color=WHITE).scale(1.2).move_to(ORIGIN)
        denominator_result = MathTex(r"2a = 4", color=GREEN).scale(1.2).move_to(ORIGIN)

        animations = []
        animations.append(Write(denominator_eq, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(denominator_eq, denominator_result, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2)

        animations = []
        animations.append(FadeOut(step4_title, denominator_eq, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time / 2)

        # NARRATION: Now, for Step 5, we reassemble the simplified parts back into the quadratic formula.
        # NARRATION: We have -b which is -5, plus or minus the square root of D which is 7,
        # NARRATION: all divided by 2a which is 4.
        step5_title = Text("Step 5: Reassemble Formula", color=BLUE).to_edge(UP)
        animations = []
        animations.append(Write(step5_title, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        reassembled_eq = MathTex(
            r"x = \frac{-5 \pm 7}{4}",
            color=WHITE
        ).scale(1.5).move_to(ORIGIN)

        animations = []
        animations.append(Write(reassembled_eq, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2)

        animations = []
        animations.append(FadeOut(step5_title, reassembled_eq, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time / 2)


        # NARRATION: In Step 6, we finally separate the formula into two distinct solutions:
        # NARRATION: one using the positive sign, and one using the negative sign.
        # NARRATION: This is because quadratic equations can have up to two real solutions.
        step6_title = Text("Step 6: Calculate Two Solutions", color=BLUE).to_edge(UP)
        animations = []
        animations.append(Write(step6_title, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        # Solution 1
        x1_eq_start = MathTex(r"x_1 = \frac{-5 + 7}{4}", color=WHITE).scale(1.2).shift(LEFT * 3)
        x1_eq_step1 = MathTex(r"x_1 = \frac{2}{4}", color=WHITE).scale(1.2).shift(LEFT * 3)
        x1_eq_result = MathTex(r"x_1 = \frac{1}{2}", color=GREEN).scale(1.2).shift(LEFT * 3)

        # Solution 2
        x2_eq_start = MathTex(r"x_2 = \frac{-5 - 7}{4}", color=WHITE).scale(1.2).shift(RIGHT * 3)
        x2_eq_step1 = MathTex(r"x_2 = \frac{-12}{4}", color=WHITE).scale(1.2).shift(RIGHT * 3)
        x2_eq_result = MathTex(r"x_2 = -3", color=GREEN).scale(1.2).shift(RIGHT * 3)

        # Display both initial forms
        animations = []
        animations.append(Write(x1_eq_start, run_time=self.run_animation_time))
        animations.append(Write(x2_eq_start, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        # Calculate x1
        animations = []
        animations.append(Transform(x1_eq_start, x1_eq_step1, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(x1_eq_step1, x1_eq_result, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 0.5)

        # Calculate x2
        animations = []
        animations.append(Transform(x2_eq_start, x2_eq_step1, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(x2_eq_step1, x2_eq_result, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2)

        # Final solutions summary
        final_solutions_text = Text("The solutions are:", color=WHITE).to_edge(DOWN).shift(UP * 0.5)
        solutions_summary = VGroup(x1_eq_result.copy(), x2_eq_result.copy()).arrange(RIGHT, buff=1.0).next_to(final_solutions_text, DOWN)
        solutions_summary.set_color(GREEN)

        animations = []
        animations.append(FadeOut(step6_title, x1_eq_start, x1_eq_step1, x2_eq_start, x2_eq_step1, run_time=self.run_animation_time))
        animations.append(Write(final_solutions_text, run_time=self.run_animation_time))
        animations.append(Transform(VGroup(x1_eq_result, x2_eq_result), solutions_summary, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2)

        elements_to_fade_out = VGroup(original_problem_display, coefficients_display, initial_formula_display, final_solutions_text, solutions_summary)
        animations = []
        animations.append(FadeOut(elements_to_fade_out, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time / 2)


        # --- Verification ---
        # NARRATION: Finally, let's verify one of our solutions to ensure it's correct.
        # NARRATION: We'll take `x = 1/2` and substitute it back into our original equation:
        # NARRATION: `2x^2 + 5x - 3 = 0`. If our calculation is correct, the equation should balance to zero.
        verification_title = Text("Verification", color=WHITE).to_edge(UP)
        animations = []
        animations.append(Write(verification_title, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        original_eq_verify = MathTex(r"2x^2 + 5x - 3 = 0", color=GREEN).move_to(UP)
        substitute_x_val = MathTex(r"\text{Substitute } x = \frac{1}{2}", color=BLUE).next_to(original_eq_verify, DOWN)

        animations = []
        animations.append(Write(original_eq_verify, run_time=self.run_animation_time))
        animations.append(Write(substitute_x_val, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        verify_step1 = MathTex(r"2\left(\frac{1}{2}\right)^2 + 5\left(\frac{1}{2}\right) - 3 = 0", color=WHITE).next_to(substitute_x_val, DOWN)
        verify_step2 = MathTex(r"2\left(\frac{1}{4}\right) + \frac{5}{2} - 3 = 0", color=WHITE).next_to(verify_step1, DOWN)
        verify_step3 = MathTex(r"\frac{1}{2} + \frac{5}{2} - 3 = 0", color=WHITE).next_to(verify_step2, DOWN)
        verify_step4 = MathTex(r"\frac{6}{2} - 3 = 0", color=WHITE).next_to(verify_step3, DOWN)
        verify_step5 = MathTex(r"3 - 3 = 0", color=WHITE).next_to(verify_step4, DOWN)
        verify_final = MathTex(r"0 = 0", color=GREEN).next_to(verify_step5, DOWN)

        animations = []
        animations.append(Write(verify_step1, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(verify_step1, verify_step2, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(verify_step2, verify_step3, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(verify_step3, verify_step4, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(verify_step4, verify_step5, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time)

        animations = []
        animations.append(Transform(verify_step5, verify_final, run_time=self.run_animation_time))
        if animations:
            self.play(*animations)
        self.wait(self.wait_time * 2)

        # NARRATION: Since we arrived at `0 = 0`, our solution `x = 1/2` is indeed correct!
        # NARRATION: This process confirms the validity of the quadratic formula and our steps.
        # NARRATION: Thank you for joining this explanation of the quadratic formula!
        self.play(FadeOut(*self.mobjects, run_time=self.run_animation_time))