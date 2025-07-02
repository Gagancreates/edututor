from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- 1. Introduction: Definition, Importance (approx. 45 seconds) ---
        title = Text("What is Machine Learning?", font_size=50).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(2)

        definition_text = Text("Machines learning from data without explicit programming.", font_size=38).next_to(title, DOWN, buff=0.8)
        self.play(Write(definition_text), run_time=2)
        self.wait(2.5)

        analogy_text = Text("Like humans learning from experience.", font_size=32).next_to(definition_text, DOWN, buff=0.6)
        self.play(FadeIn(analogy_text), run_time=1)
        self.wait(2)

        keywords_title = Text("Key Concepts:", font_size=40).next_to(analogy_text, DOWN, buff=1.0).to_edge(LEFT)
        self.play(Write(keywords_title), run_time=1)
        self.wait(1)

        keyword1 = Text("Data", font_size=35, color=BLUE)
        keyword2 = Text("Patterns", font_size=35, color=GREEN)
        keyword3 = Text("Prediction", font_size=35, color=RED)
        keyword4 = Text("Learning", font_size=35, color=YELLOW)

        keywords_group = VGroup(keyword1, keyword2, keyword3, keyword4).arrange(RIGHT, buff=0.8).next_to(keywords_title, RIGHT, buff=0.5)

        self.play(FadeIn(keywords_group), run_time=1.5)
        self.wait(2)

        # Clear introduction elements
        self.play(FadeOut(title, definition_text, analogy_text, keywords_title, keywords_group), run_time=1.5)
        self.wait(1)

        # --- 2. Core Understanding: Types of Machine Learning (approx. 72 seconds) ---
        types_title = Text("Types of Machine Learning", font_size=50).to_edge(UP)
        self.play(Write(types_title), run_time=1.5)
        self.wait(2)

        # Supervised Learning
        supervised_title = Text("1. Supervised Learning", font_size=40, color=BLUE).to_edge(LEFT).shift(UP*1.5)
        self.play(FadeIn(supervised_title), run_time=1)
        self.wait(1.5)

        supervised_desc1 = Text("Learning from Labeled Data.", font_size=32).next_to(supervised_title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(supervised_desc1), run_time=1.5)
        self.wait(1.5)

        input_box = Rectangle(width=2, height=1.5, color=WHITE).shift(LEFT*4 + DOWN*0.5)
        input_text = Text("Input (X)", font_size=28).move_to(input_box.center)
        output_box = Rectangle(width=2, height=1.5, color=WHITE).shift(RIGHT*4 + DOWN*0.5)
        output_text = Text("Output (Y)", font_size=28).move_to(output_box.center)
        label_text = Text("(Labels)", font_size=20, color=YELLOW).next_to(output_box, DOWN, buff=0.2)
        
        model_box = Rectangle(width=3, height=1.5, color=GREEN).move_to(ORIGIN + DOWN*0.5)
        model_text = Text("ML Model", font_size=28).move_to(model_box.center)
        arrow1 = Arrow(input_box.get_right(), model_box.get_left(), buff=0.1)
        arrow2 = Arrow(model_box.get_right(), output_box.get_left(), buff=0.1)

        self.play(Create(VGroup(input_box, input_text)), run_time=0.8)
        self.play(Create(VGroup(output_box, output_text)), run_time=0.8)
        self.play(Create(label_text), run_time=0.5)
        self.play(Create(model_box), Write(model_text), Create(arrow1), Create(arrow2), run_time=1.5)
        self.wait(2.5)

        teacher_student = Text("Analogy: Teacher-Student (with answer key)", font_size=28, color=YELLOW).next_to(model_box, DOWN, buff=1.0)
        self.play(FadeIn(teacher_student), run_time=1)
        self.wait(2)
        
        self.play(FadeOut(supervised_desc1, input_box, input_text, output_box, output_text, label_text, model_box, model_text, arrow1, arrow2, teacher_student), run_time=1.5)
        self.wait(0.5)

        # Unsupervised Learning
        unsupervised_title = Text("2. Unsupervised Learning", font_size=40, color=ORANGE).next_to(supervised_title, DOWN, buff=1.5).to_edge(LEFT)
        self.play(FadeIn(unsupervised_title), run_time=1)
        self.wait(1.5)

        unsupervised_desc1 = Text("Finding patterns in unlabeled data.", font_size=32).next_to(unsupervised_title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(unsupervised_desc1), run_time=1.5)
        self.wait(1.5)

        data_points = VGroup(*[Dot(point) for point in [
            np.array([-3, -1, 0]), np.array([-3.5, -0.5, 0]), np.array([-2.8, -1.2, 0]),
            np.array([3, -1, 0]), np.array([3.5, -0.5, 0]), np.array([2.8, -1.2, 0]),
            np.array([0, 1.5, 0]), np.array([-0.5, 1.8, 0]), np.array([0.5, 1.2, 0])
        ]]).scale(0.8).move_to(ORIGIN).shift(DOWN*0.5)

        self.play(Create(data_points), run_time=1.5)
        self.wait(1.5)

        cluster1 = Circle(radius=0.7, color=BLUE, fill_opacity=0.2).move_to(np.array([-3.1, -0.8, 0]))
        cluster2 = Circle(radius=0.7, color=RED, fill_opacity=0.2).move_to(np.array([3.1, -0.8, 0]))
        cluster3 = Circle(radius=0.7, color=GREEN, fill_opacity=0.2).move_to(np.array([0, 1.5, 0]))

        self.play(FadeIn(cluster1, cluster2, cluster3), run_time=1.5)
        self.wait(2)

        unsupervised_analogy = Text("Analogy: Discovering insights without guidance", font_size=28, color=YELLOW).next_to(cluster3, DOWN, buff=1.0)
        self.play(FadeIn(unsupervised_analogy), run_time=1)
        self.wait(2)

        self.play(FadeOut(unsupervised_desc1, data_points, cluster1, cluster2, cluster3, unsupervised_analogy), run_time=1.5)
        self.wait(0.5)

        # Reinforcement Learning
        reinforcement_title = Text("3. Reinforcement Learning", font_size=40, color=PURPLE).next_to(unsupervised_title, DOWN, buff=1.5).to_edge(LEFT)
        self.play(FadeIn(reinforcement_title), run_time=1)
        self.wait(1.5)

        reinforcement_desc1 = Text("Learning through trial and error with rewards.", font_size=32).next_to(reinforcement_title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(reinforcement_desc1), run_time=1.5)
        self.wait(1.5)

        agent_square = Square(side_length=1.5, color=WHITE).shift(LEFT*4 + DOWN*0.5)
        agent_text = Text("Agent", font_size=28).move_to(agent_square.center)
        env_square = Square(side_length=1.5, color=WHITE).shift(RIGHT*4 + DOWN*0.5)
        env_text = Text("Environment", font_size=28).move_to(env_square.center)

        arrow_agent_env = Arrow(agent_square.get_right(), env_square.get_left(), buff=0.1)
        action_text = Text("Action", font_size=20, color=RED).next_to(arrow_agent_env, UP, buff=0.1)

        arrow_env_agent = Arrow(env_square.get_left(), agent_square.get_right(), buff=0.1)
        state_text = Text("State", font_size=20, color=BLUE).next_to(arrow_env_agent, UP, buff=0.1)
        reward_text = Text("Reward", font_size=20, color=GREEN).next_to(arrow_env_agent, DOWN, buff=0.1)

        self.play(Create(VGroup(agent_square, agent_text, env_square, env_text)), run_time=1)
        self.play(Create(arrow_agent_env), Write(action_text), run_time=1)
        self.play(Create(arrow_env_agent), Write(state_text), Write(reward_text), run_time=1.5)
        self.wait(2.5)

        reinforcement_analogy = Text("Analogy: Learning to ride a bike", font_size=28, color=YELLOW).next_to(VGroup(agent_square, env_square), DOWN, buff=1.0)
        self.play(FadeIn(reinforcement_analogy), run_time=1)
        self.wait(2)

        self.play(FadeOut(types_title, supervised_title, unsupervised_title, reinforcement_title,
                          reinforcement_desc1, agent_square, agent_text, env_square, env_text,
                          arrow_agent_env, action_text, arrow_env_agent, state_text, reward_text,
                          reinforcement_analogy), run_time=1.5)
        self.wait(1)

        # --- 3. Examples in Action (approx. 45 seconds) ---
        examples_title = Text("Examples in Action", font_size=50).to_edge(UP)
        self.play(Write(examples_title), run_time=1.5)
        self.wait(2)

        # Supervised Example: Image Classification
        supervised_ex_title = Text("Supervised: Image Classification", font_size=38, color=BLUE).next_to(examples_title, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(supervised_ex_title), run_time=1)
        self.wait(1)

        input_img_box = Rectangle(width=2, height=2, color=WHITE).shift(LEFT*3.5 + UP*0.5)
        input_img_text = Text("Input Image", font_size=24).move_to(input_img_box.center).shift(UP*0.5)
        cat_text = Tex(r"$\text{Cat}$", font_size=28).move_to(input_img_box.center).shift(DOWN*0.3)
        
        ml_model_process = Rectangle(width=2.5, height=1.5, color=GREEN).next_to(input_img_box, RIGHT, buff=0.5)
        ml_model_text_ex = Text("ML Model", font_size=28).move_to(ml_model_process.center)

        output_pred_box = Rectangle(width=2, height=1.5, color=WHITE).next_to(ml_model_process, RIGHT, buff=0.5)
        cat_label = Text("Cat (95%)", font_size=28, color=YELLOW).move_to(output_pred_box.center).shift(UP*0.3)
        dog_label = Text("Dog (5%)", font_size=28, color=YELLOW).move_to(output_pred_box.center).shift(DOWN*0.3)

        arrow_ex1 = Arrow(input_img_box.get_right(), ml_model_process.get_left(), buff=0.1)
        arrow_ex2 = Arrow(ml_model_process.get_right(), output_pred_box.get_left(), buff=0.1)

        self.play(Create(VGroup(input_img_box, input_img_text, cat_text)), run_time=1)
        self.play(Create(VGroup(ml_model_process, ml_model_text_ex)), run_time=1)
        self.play(Create(VGroup(output_pred_box, cat_label, dog_label)), run_time=1)
        self.play(Create(arrow_ex1), Create(arrow_ex2), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(supervised_ex_title, input_img_box, input_img_text, cat_text,
                          ml_model_process, ml_model_text_ex, output_pred_box, cat_label, dog_label,
                          arrow_ex1, arrow_ex2), run_time=1.5)
        self.wait(0.5)

        # Unsupervised Example: Customer Segmentation
        unsupervised_ex_title = Text("Unsupervised: Customer Segmentation", font_size=38, color=ORANGE).next_to(examples_title, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(unsupervised_ex_title), run_time=1)
        self.wait(1)

        customer_data = Text("Customer Data", font_size=30).shift(LEFT*4 + UP*0.5)
        customer_dots = VGroup(*[Dot(point) for point in [
            np.array([-4.5, -0.5, 0]), np.array([-4.2, -0.8, 0]), np.array([-3.8, -0.6, 0]),
            np.array([-3.5, 0.2, 0]), np.array([-3.7, 0.5, 0]), np.array([-4.0, 0.3, 0]),
        ]]).scale(0.8).next_to(customer_data, DOWN, buff=0.5)

        ml_model_process_un = Rectangle(width=2.5, height=1.5, color=GREEN).next_to(customer_data, RIGHT, buff=0.5).shift(DOWN*0.5)
        ml_model_text_un = Text("ML Model", font_size=28).move_to(ml_model_process_un.center)

        segments = VGroup(
            Text("Segment A", font_size=28, color=BLUE).shift(RIGHT*3.5 + UP*1.0),
            Text("Segment B", font_size=28, color=RED).shift(RIGHT*3.5 + UP*0.0),
            Text("Segment C", font_size=28, color=GREEN).shift(RIGHT*3.5 + DOWN*1.0)
        )
        
        arrow_ex3 = Arrow(VGroup(customer_data, customer_dots).get_right(), ml_model_process_un.get_left(), buff=0.1)
        arrow_ex4 = Arrow(ml_model_process_un.get_right(), segments.get_left(), buff=0.1)

        self.play(Create(VGroup(customer_data, customer_dots)), run_time=1)
        self.play(Create(VGroup(ml_model_process_un, ml_model_text_un)), run_time=1)
        self.play(Create(segments), run_time=1)
        self.play(Create(arrow_ex3), Create(arrow_ex4), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(unsupervised_ex_title, customer_data, customer_dots, ml_model_process_un, ml_model_text_un, segments, arrow_ex3, arrow_ex4), run_time=1.5)
        self.wait(0.5)

        # Reinforcement Example: Robot Navigation
        reinforcement_ex_title = Text("Reinforcement: Robot Navigation", font_size=38, color=PURPLE).next_to(examples_title, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(reinforcement_ex_title), run_time=1)
        self.wait(1)
        
        robot = Circle(radius=0.4, color=WHITE, fill_opacity=0.8).shift(LEFT*5 + DOWN*0.5)
        robot_text = Text("Robot", font_size=24).move_to(robot.center)
        
        grid_square = Square(side_length=1.5, color=GREY).shift(LEFT*2.5 + DOWN*0.5)
        grid_text = Text("Environment", font_size=24).move_to(grid_square.center)

        target = Circle(radius=0.3, color=GREEN, fill_opacity=0.8).shift(RIGHT*3.5 + DOWN*0.5)
        target_text = Text("Goal", font_size=24).move_to(target.center)

        arrow_r1 = Arrow(robot.get_right(), grid_square.get_left(), buff=0.1)
        arrow_r2 = Arrow(grid_square.get_right(), target.get_left(), buff=0.1)
        
        # Simulate movement
        path_line = Line(robot.get_center(), target.get_center(), color=YELLOW, stroke_width=4, stroke_opacity=0)
        self.play(Create(VGroup(robot, robot_text)), run_time=0.8)
        self.play(Create(VGroup(grid_square, grid_text)), run_time=0.8)
        self.play(Create(VGroup(target, target_text)), run_time=0.8)
        self.play(Create(arrow_r1), Create(arrow_r2), run_time=1.5)
        self.wait(1)

        self.play(robot.animate.move_to(target.get_center()), Create(path_line, run_time=2))
        self.wait(2)

        self.play(FadeOut(examples_title, reinforcement_ex_title, robot, robot_text, grid_square, grid_text, target, target_text, arrow_r1, arrow_r2, path_line), run_time=1.5)
        self.wait(1)

        # --- 4. Real-World Applications (approx. 18 seconds) ---
        applications_title = Text("Real-World Applications", font_size=50).to_edge(UP)
        self.play(Write(applications_title), run_time=1.5)
        self.wait(1.5)

        app1 = Text("• Self-Driving Cars", font_size=38).shift(UP*1.5).to_edge(LEFT)
        app2 = Text("• Recommendation Systems", font_size=38).next_to(app1, DOWN, buff=0.8).to_edge(LEFT)
        app3 = Text("• Medical Diagnosis", font_size=38).next_to(app2, DOWN, buff=0.8).to_edge(LEFT)

        self.play(FadeIn(app1), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(app2), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(app3), run_time=0.8)
        self.wait(2.5)

        final_thought = Text("Machine Learning is transforming our world.", font_size=40, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Write(final_thought), run_time=1.5)
        self.wait(2)

        # End with FadeOut of all mobjects
        self.play(FadeOut(*self.mobjects), run_time=1.5)