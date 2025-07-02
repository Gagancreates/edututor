from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- 1. Introduction (25%) ---
        title = Text("Pythagoras Theorem").scale(1.2).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(1.5)

        intro_text = Text("Unlocking relationships in Right-Angled Triangles.").next_to(title, DOWN, buff=0.8)
        self.play(Write(intro_text), run_time=2)
        self.wait(1.5)

        formula_prompt = Text("The fundamental formula:").next_to(intro_text, DOWN, buff=0.8)
        self.play(Write(formula_prompt), run_time=1.5)
        self.wait(1)

        formula_math = MathTex("a^2 + b^2 = c^2").scale(1.5).next_to(formula_prompt, DOWN, buff=0.8)
        self.play(Write(formula_math), run_time=2)
        self.wait(2.5)

        self.play(FadeOut(title, intro_text, formula_prompt, formula_math), run_time=1.5)
        self.wait(1)

        # --- 2. Core Understanding (40%) ---
        triangle_title = Text("Understanding the Components").to_edge(UP)
        self.play(Write(triangle_title), run_time=1.5)
        self.wait(1)

        # Define vertices for a right-angled triangle (right angle at C)
        v_C = LEFT * 3 + DOWN * 2
        v_A = LEFT * 3 + UP * 2
        v_B = RIGHT * 3 + DOWN * 2

        triangle = Polygon(v_A, v_B, v_C, color=BLUE)
        right_angle_square = Square(side_length=0.4, color=YELLOW, fill_opacity=1).move_to(v_C + RIGHT * 0.2 + UP * 0.2)

        # Labels for vertices
        label_vA = Text("A").next_to(v_A, UP + LEFT, buff=0.2)
        label_vB = Text("B").next_to(v_B, DOWN + RIGHT, buff=0.2)
        label_vC = Text("C").next_to(v_C, DOWN + LEFT, buff=0.2)

        # Labels for sides (lowercase corresponding to opposite vertex)
        side_a_label = MathTex("a").next_to(Line(v_B, v_C), RIGHT, buff=0.2).set_color(GREEN)
        side_b_label = MathTex("b").next_to(Line(v_A, v_C), LEFT, buff=0.2).set_color(RED)
        side_c_label = MathTex("c").next_to(Line(v_A, v_B), UP + RIGHT, buff=0.2).set_color(PURPLE)

        self.play(Create(triangle), Create(right_angle_square), run_time=1.5)
        self.wait(1)
        self.play(FadeIn(label_vA, label_vB, label_vC), run_time=1)
        self.wait(1)
        self.play(FadeIn(side_a_label, side_b_label, side_c_label), run_time=1.5)
        self.wait(1.5)

        hyp_text = Text("The longest side 'c' is called the Hypotenuse.").next_to(triangle, DOWN, buff=1.0)
        hyp_text.set_color_by_tex("Hypotenuse", PURPLE)
        hyp_arrow = Arrow(start=hyp_text.get_top(), end=side_c_label.get_bottom(), buff=0.1, color=PURPLE)

        self.play(Write(hyp_text), Create(hyp_arrow), run_time=2)
        self.wait(2)

        self.play(FadeOut(label_vA, label_vB, label_vC, hyp_text, hyp_arrow, triangle_title), run_time=1.5)
        self.wait(1)

        # Re-position triangle for square visualization
        triangle_group = VGroup(triangle, right_angle_square, side_a_label, side_b_label, side_c_label).move_to(ORIGIN).scale(0.8)
        self.play(triangle_group.animate.move_to(LEFT * 3), run_time=1.5)
        self.wait(1)

        # Create squares on each side
        # Use the actual lengths from the triangle points scaled by 0.8
        a_length = Line(v_B, v_C).get_length() * 0.8
        b_length = Line(v_A, v_C).get_length() * 0.8
        c_length = Line(v_A, v_B).get_length() * 0.8

        sq_a = Square(side_length=a_length, color=GREEN, fill_opacity=0.5).next_to(triangle_group, RIGHT, buff=1.5).shift(UP*1)
        sq_b = Square(side_length=b_length, color=RED, fill_opacity=0.5).next_to(sq_a, DOWN, buff=0.5)
        sq_c = Square(side_length=c_length, color=PURPLE, fill_opacity=0.5).next_to(triangle_group, RIGHT, buff=1.5).shift(DOWN*1.5)

        # Labels for square areas
        label_sq_a = MathTex("a^2").move_to(sq_a.get_center())
        label_sq_b = MathTex("b^2").move_to(sq_b.get_center())
        label_sq_c = MathTex("c^2").move_to(sq_c.get_center())

        self.play(Create(sq_a), Create(sq_b), Create(sq_c), run_time=2)
        self.wait(1.5)
        self.play(FadeIn(label_sq_a, label_sq_b, label_sq_c), run_time=1)
        self.wait(1.5)

        core_concept_text = Text("The areas relate by:").to_edge(UP)
        self.play(Write(core_concept_text), run_time=1.5)
        self.wait(1)

        combined_formula = MathTex("Area_{a^2} + Area_{b^2} = Area_{c^2}").scale(1.2).next_to(core_concept_text, DOWN, buff=0.8)
        self.play(Write(combined_formula), run_time=2)
        self.wait(1.5)

        # Show the actual areas relating
        plus_sign = Tex("+").next_to(label_sq_a, DOWN, buff=0.2)
        equals_sign = Tex("=").next_to(plus_sign, DOWN, buff=0.2)
        
        self.play(FadeIn(plus_sign), run_time=0.5)
        self.wait(1)
        self.play(FadeIn(equals_sign), run_time=0.5)
        self.wait(1)

        visual_sum_text = Text("The sum of the areas of the squares on the two shorter sides",
                                font_size=30).to_edge(DOWN).shift(UP * 0.5)
        visual_sum_text_cont = Text("equals the area of the square on the hypotenuse.",
                                   font_size=30).next_to(visual_sum_text, DOWN)

        self.play(Write(visual_sum_text), run_time=2)
        self.play(Write(visual_sum_text_cont), run_time=2)
        self.wait(2.5)

        # Fade out all core understanding objects
        self.play(FadeOut(triangle_group, sq_a, sq_b, sq_c, label_sq_a, label_sq_b, label_sq_c,
                           plus_sign, equals_sign, core_concept_text, combined_formula,
                           visual_sum_text, visual_sum_text_cont), run_time=1.5)
        self.wait(1)

        # --- 3. Examples (25%) ---
        example_title = Text("Example Calculation").to_edge(UP)
        self.play(Write(example_title), run_time=1.5)
        self.wait(1)

        # Redraw a simple triangle for the example
        ex_v_C = LEFT * 2 + DOWN * 2
        ex_v_A = LEFT * 2 + UP * 1
        ex_v_B = RIGHT * 2 + DOWN * 2

        example_triangle = Polygon(ex_v_A, ex_v_B, ex_v_C, color=BLUE)
        ex_right_angle_square = Square(side_length=0.4, color=YELLOW, fill_opacity=1).move_to(ex_v_C + RIGHT * 0.2 + UP * 0.2)

        ex_side_a_val = MathTex("a = 3").next_to(Line(ex_v_A, ex_v_C), LEFT, buff=0.2).set_color(RED)
        ex_side_b_val = MathTex("b = 4").next_to(Line(ex_v_B, ex_v_C), DOWN, buff=0.2).set_color(GREEN)
        ex_side_c_val = MathTex("c = ?").next_to(Line(ex_v_A, ex_v_B), UP + RIGHT, buff=0.2).set_color(PURPLE)

        self.play(Create(example_triangle), Create(ex_right_angle_square), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(ex_side_a_val, ex_side_b_val, ex_side_c_val), run_time=1.5)
        self.wait(1.5)

        # Show calculation steps
        formula_step1 = MathTex("a^2 + b^2 = c^2").to_edge(RIGHT).shift(UP*1)
        self.play(Write(formula_step1), run_time=1)
        self.wait(1)

        formula_step2 = MathTex("3^2 + 4^2 = c^2").next_to(formula_step1, DOWN, buff=0.5)
        self.play(ReplacementTransform(formula_step1, formula_step2), run_time=1.5)
        self.wait(1)

        formula_step3 = MathTex("9 + 16 = c^2").next_to(formula_step2, DOWN, buff=0.5)
        self.play(ReplacementTransform(formula_step2, formula_step3), run_time=1.5)
        self.wait(1)

        formula_step4 = MathTex("25 = c^2").next_to(formula_step3, DOWN, buff=0.5)
        self.play(ReplacementTransform(formula_step3, formula_step4), run_time=1.5)
        self.wait(1)

        formula_step5 = MathTex("c = \\sqrt{25}").next_to(formula_step4, DOWN, buff=0.5)
        self.play(ReplacementTransform(formula_step4, formula_step5), run_time=1.5)
        self.wait(1)

        formula_step6 = MathTex("c = 5").next_to(formula_step5, DOWN, buff=0.5)
        self.play(ReplacementTransform(formula_step5, formula_step6), run_time=1.5)
        self.wait(2)

        # Update the triangle with the result
        final_c_val = MathTex("c = 5").move_to(ex_side_c_val.get_center()).set_color(PURPLE)
        self.play(ReplacementTransform(ex_side_c_val, final_c_val), run_time=1)
        self.wait(2)

        # Fade out example objects
        self.play(FadeOut(example_title, example_triangle, ex_right_angle_square,
                           ex_side_a_val, ex_side_b_val, final_c_val,
                           formula_step6), run_time=1.5)
        self.wait(1)

        # --- 4. Applications (10%) ---
        applications_title = Text("Real-World Applications").to_edge(UP)
        self.play(Write(applications_title), run_time=1.5)
        self.wait(1.5)

        app_text1 = Text("Used in construction, architecture, and engineering for precise measurements.").next_to(applications_title, DOWN, buff=1).scale(0.8)
        self.play(Write(app_text1), run_time=2)
        self.wait(2)

        app_text2 = Text("Essential for navigation, mapping, and even computer graphics.", font_size=36).next_to(app_text1, DOWN, buff=0.8)
        self.play(Write(app_text2), run_time=2)
        self.wait(2.5)

        conclusion_text = Text("A foundational concept in mathematics!", font_size=40).next_to(app_text2, DOWN, buff=1.0).set_color(GOLD)
        self.play(Write(conclusion_text), run_time=2)
        self.wait(3)

        # --- End Scene ---
        self.play(FadeOut(*self.mobjects), run_time=1.5)
        self.wait(1)