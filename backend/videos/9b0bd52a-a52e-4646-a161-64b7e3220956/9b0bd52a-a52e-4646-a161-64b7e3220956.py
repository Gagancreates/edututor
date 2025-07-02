from manim import *

class CreateScene(Scene):
    def construct(self):
        # 1. Introduction (25%)
        title = Text("Newton's Laws of Motion", font_size=60).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(4)

        intro_text1 = Text("Fundamental principles describing how objects move and interact.", font_size=36).next_to(title, DOWN, buff=0.7)
        self.play(FadeIn(intro_text1), run_time=1.5)
        self.wait(4)

        intro_text2 = Text("Building on our everyday observations of motion.", font_size=36).next_to(intro_text1, DOWN, buff=0.7)
        self.play(FadeIn(intro_text2), run_time=1.5)
        self.wait(5)

        # Clear introduction
        self.play(FadeOut(title, intro_text1, intro_text2), run_time=1.0)
        self.wait(1)

        # 2. Core Understanding (40%)

        # First Law
        first_law_title = Text("1. Law of Inertia", font_size=50, color=BLUE).to_edge(UP)
        self.play(Write(first_law_title), run_time=1.0)
        self.wait(2)

        first_law_def = Text(
            "An object at rest stays at rest, and an object in motion stays in motion\n"
            "with the same speed and in the same direction unless acted upon by an\n"
            "unbalanced force.",
            font_size=32,
            line_spacing=1.2
        ).next_to(first_law_title, DOWN, buff=0.5)
        self.play(Write(first_law_def), run_time=2.0)
        self.wait(3)

        # Visual for First Law (Object at rest)
        block_at_rest = Square(side_length=1.5, fill_opacity=0.8, color=RED).move_to(LEFT * 3)
        rest_label = Text("At Rest", font_size=24).next_to(block_at_rest, DOWN)
        self.play(Create(block_at_rest), Write(rest_label), run_time=1.0)
        self.wait(1.5)

        force_arrow_rest = Arrow(LEFT * 1.5, ORIGIN, buff=0).next_to(block_at_rest, RIGHT, buff=0.1).set_color(YELLOW)
        force_label_rest = Text("Unbalanced Force", font_size=20).next_to(force_arrow_rest, UP)
        self.play(Create(force_arrow_rest), Write(force_label_rest), run_time=1.0)
        self.wait(1.5)

        # Animate motion
        self.play(
            FadeOut(force_arrow_rest, force_label_rest, rest_label),
            block_at_rest.animate.shift(RIGHT * 6),
            run_time=2.0
        )
        self.wait(0.5)
        motion_label = Text("In Motion", font_size=24).next_to(block_at_rest, DOWN)
        self.play(Write(motion_label), run_time=0.5)
        self.wait(2.5)

        # Clear first law visuals
        self.play(FadeOut(first_law_title, first_law_def, block_at_rest, motion_label), run_time=1.0)
        self.wait(0.5)

        # Second Law
        second_law_title = Text("2. F = ma (Force and Acceleration)", font_size=50, color=GREEN).to_edge(UP)
        self.play(Write(second_law_title), run_time=1.0)
        self.wait(2)

        second_law_def = Text(
            "The acceleration of an object is directly proportional to the net force\n"
            "acting on it and inversely proportional to its mass.",
            font_size=32,
            line_spacing=1.2
        ).next_to(second_law_title, DOWN, buff=0.5)
        self.play(Write(second_law_def), run_time=2.0)
        self.wait(3)

        formula = MathTex("F", "=", "m", "a", font_size=96).move_to(ORIGIN)
        self.play(Write(formula), run_time=1.5)
        self.wait(2.5)

        # Visual for Second Law
        mass_block = Square(side_length=1.5, fill_opacity=0.8, color=ORANGE).move_to(LEFT * 2.5)
        force_arrow_2 = Arrow(LEFT * 1, ORIGIN, buff=0).next_to(mass_block, RIGHT, buff=0.1).set_color(YELLOW)
        accel_arrow_2 = Arrow(ORIGIN, RIGHT * 2, buff=0).next_to(mass_block, RIGHT * 3, buff=0.1).set_color(PURPLE)
        force_label_2 = MathTex("F", font_size=40).next_to(force_arrow_2, UP)
        mass_label_2 = MathTex("m", font_size=40).next_to(mass_block, DOWN)
        accel_label_2 = MathTex("a", font_size=40).next_to(accel_arrow_2, UP)

        self.play(
            Create(mass_block), Write(mass_label_2),
            Create(force_arrow_2), Write(force_label_2),
            Create(accel_arrow_2), Write(accel_label_2),
            Transform(formula, formula.copy().next_to(mass_block, LEFT * 4)), # Move formula out of the way
            run_time=1.5
        )
        self.wait(3)

        # Clear second law visuals
        self.play(FadeOut(second_law_title, second_law_def, formula, mass_block, force_arrow_2, accel_arrow_2, force_label_2, mass_label_2, accel_label_2), run_time=1.0)
        self.wait(0.5)

        # Third Law
        third_law_title = Text("3. Action-Reaction", font_size=50, color=YELLOW).to_edge(UP)
        self.play(Write(third_law_title), run_time=1.0)
        self.wait(2)

        third_law_def = Text(
            "For every action, there is an equal and opposite reaction.",
            font_size=32
        ).next_to(third_law_title, DOWN, buff=0.5)
        self.play(Write(third_law_def), run_time=1.5)
        self.wait(3)

        # Visual for Third Law
        block_a = Square(side_length=1.5, fill_opacity=0.8, color=RED).move_to(LEFT * 2.5)
        block_b = Square(side_length=1.5, fill_opacity=0.8, color=BLUE).move_to(RIGHT * 2.5)

        label_a = Text("A", font_size=36).move_to(block_a.get_center())
        label_b = Text("B", font_size=36).move_to(block_b.get_center())

        self.play(Create(block_a), Create(block_b), Write(label_a), Write(label_b), run_time=1.0)
        self.wait(1.5)

        force_ab = Arrow(block_a.get_right(), block_b.get_left(), buff=0.1).set_color(GREEN)
        force_ba = Arrow(block_b.get_left(), block_a.get_right(), buff=0.1).set_color(PURPLE)

        force_ab_label = MathTex("F_{AB}", font_size=40).next_to(force_ab, UP)
        force_ba_label = MathTex("F_{BA}", font_size=40).next_to(force_ba, UP)

        self.play(Create(force_ab), Write(force_ab_label), run_time=1.0)
        self.wait(1.5)
        self.play(Create(force_ba), Write(force_ba_label), run_time=1.0)
        self.wait(2)

        # Emphasize equality and opposition
        equality_text = MathTex("F_{AB}", "=", "-F_{BA}", font_size=60).next_to(third_law_def, DOWN, buff=1.0)
        self.play(Write(equality_text), run_time=1.5)
        self.wait(3)

        # Clear third law visuals
        self.play(FadeOut(third_law_title, third_law_def, block_a, block_b, label_a, label_b, force_ab, force_ab_label, force_ba, force_ba_label, equality_text), run_time=1.0)
        self.wait(0.5)

        # 3. Examples (25%)

        examples_title = Text("Examples in Action", font_size=50, color=WHITE).to_edge(UP)
        self.play(Write(examples_title), run_time=1.0)
        self.wait(2)

        # Example 1: First Law (Car braking)
        example1_text = Text("1. First Law: Car Braking", font_size=36).next_to(examples_title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(example1_text), run_time=1.0)
        self.wait(1)

        car = Rectangle(width=3, height=1.5, fill_opacity=0.8, color=GRAY).move_to(LEFT * 2)
        passenger = Circle(radius=0.3, fill_opacity=0.8, color=WHITE).move_to(car.get_center() + UP * 0.3)
        self.play(Create(car), Create(passenger), run_time=1.0)
        self.wait(0.5)
        
        # Simulate car moving
        self.play(car.animate.shift(RIGHT * 4), passenger.animate.shift(RIGHT * 4), run_time=1.5)
        self.wait(0.5)

        # Simulate braking (car stops, passenger continues)
        self.play(car.animate.shift(LEFT * 1), passenger.animate.shift(RIGHT * 1), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(example1_text, car, passenger), run_time=1.0)
        self.wait(0.5)

        # Example 2: Second Law (Pushing carts)
        example2_text = Text("2. Second Law: Pushing Carts", font_size=36).next_to(examples_title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(example2_text), run_time=1.0)
        self.wait(1)

        light_cart = Rectangle(width=2, height=1, fill_opacity=0.8, color=RED).move_to(LEFT * 3)
        heavy_cart = Rectangle(width=3, height=1.5, fill_opacity=0.8, color=BLUE).next_to(light_cart, RIGHT, buff=2)

        light_cart_label = Text("Light (m)", font_size=24).next_to(light_cart, DOWN)
        heavy_cart_label = Text("Heavy (2m)", font_size=24).next_to(heavy_cart, DOWN)

        self.play(Create(light_cart), Write(light_cart_label), Create(heavy_cart), Write(heavy_cart_label), run_time=1.5)
        self.wait(0.5)

        force_push_light = Arrow(light_cart.get_left() - LEFT * 0.5, light_cart.get_left(), buff=0).set_color(YELLOW)
        force_push_heavy = Arrow(heavy_cart.get_left() - LEFT * 0.5, heavy_cart.get_left(), buff=0).set_color(YELLOW)

        force_label_push = Text("Same Force (F)", font_size=24).next_to(force_push_light, UP).shift(LEFT*1.5)

        self.play(Create(force_push_light), Create(force_push_heavy), Write(force_label_push), run_time=1.0)
        self.wait(1.5)

        # Simulate acceleration
        accel_light = Text("a (Large)", font_size=24, color=GREEN).next_to(light_cart, RIGHT)
        accel_heavy = Text("a/2 (Small)", font_size=24, color=GREEN).next_to(heavy_cart, RIGHT)

        self.play(
            light_cart.animate.shift(RIGHT * 2), Write(accel_light),
            heavy_cart.animate.shift(RIGHT * 1), Write(accel_heavy),
            run_time=1.5
        )
        self.wait(2.5)

        self.play(FadeOut(example2_text, light_cart, heavy_cart, light_cart_label, heavy_cart_label, force_push_light, force_push_heavy, force_label_push, accel_light, accel_heavy), run_time=1.0)
        self.wait(0.5)

        # Example 3: Third Law (Rocket Propulsion)
        example3_text = Text("3. Third Law: Rocket Propulsion", font_size=36).next_to(examples_title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(example3_text), run_time=1.0)
        self.wait(1)

        rocket = Polygon(
            [-0.5, -1, 0], [0.5, -1, 0], [0.5, 1, 0], [1, 1.5, 0], [0, 2.5, 0], [-1, 1.5, 0], [-0.5, 1, 0]
        ).scale(0.8).move_to(UP*0.5)
        rocket.set_fill(GREY_BROWN, opacity=0.8)
        rocket.set_stroke(WHITE, width=2)
        self.play(Create(rocket), run_time=1.0)
        self.wait(0.5)

        exhaust_particles = VGroup(
            *[Dot(point=rocket.get_bottom() + DOWN * i * 0.2 + LEFT * random.uniform(-0.1, 0.1), radius=0.05, color=ORANGE) for i in range(1, 6)]
        )
        exhaust_label = Text("Action: Exhaust Gas Down", font_size=24, color=RED).next_to(exhaust_particles, DOWN)
        
        self.play(FadeIn(exhaust_particles), Write(exhaust_label), run_time=1.0)
        self.play(
            exhaust_particles.animate.shift(DOWN * 1.5),
            run_time=1.0
        )
        self.wait(2)

        rocket_motion = Arrow(rocket.get_top(), rocket.get_top() + UP * 1.5, buff=0.1).set_color(BLUE)
        rocket_motion_label = Text("Reaction: Rocket Up", font_size=24, color=BLUE).next_to(rocket_motion, UP)
        
        self.play(
            FadeOut(exhaust_particles), # Exhaust disappears
            Create(rocket_motion), Write(rocket_motion_label),
            rocket.animate.shift(UP * 1), # Rocket moves up
            run_time=1.5
        )
        self.wait(2.5)

        self.play(FadeOut(examples_title, example3_text, rocket, rocket_motion, rocket_motion_label, exhaust_label), run_time=1.0)
        self.wait(0.5)

        # 4. Applications (10%)
        applications_title = Text("Real-World Applications", font_size=50, color=PURPLE).to_edge(UP)
        self.play(Write(applications_title), run_time=1.0)
        self.wait(2)

        app_list = VGroup(
            Text("• Engineering Design", font_size=36),
            Text("• Space Exploration", font_size=36),
            Text("• Sports and Athletics", font_size=36)
        ).arrange(DOWN, center=False, aligned_edge=LEFT).next_to(applications_title, DOWN, buff=0.7).to_edge(LEFT)

        self.play(Write(app_list[0]), run_time=1.0)
        self.wait(1.5)
        self.play(Write(app_list[1]), run_time=1.0)
        self.wait(1.5)
        self.play(Write(app_list[2]), run_time=1.0)
        self.wait(2.5)

        final_thought = Text("These laws form the bedrock of classical physics!", font_size=40, color=GOLD).next_to(app_list, DOWN, buff=1.0)
        self.play(Write(final_thought), run_time=1.5)
        self.wait(3.5)

        # End of scene
        self.play(FadeOut(*self.mobjects), run_time=1.5)