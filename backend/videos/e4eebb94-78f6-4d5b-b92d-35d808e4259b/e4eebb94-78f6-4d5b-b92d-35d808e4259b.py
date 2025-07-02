from manim import *

class CreateScene(Scene):
    def construct(self):
        # Set up a color palette
        COLOR_TITLE = BLUE_C
        COLOR_HEADING = TEAL_C
        COLOR_TEXT = WHITE
        COLOR_HIGHLIGHT = YELLOW_B
        COLOR_EXAMPLE = GREEN_D
        COLOR_DATA = RED_B
        COLOR_MODEL = PURPLE_B
        COLOR_ARROW = GRAY_A

        # Introduction
        title = Text("Understanding Machine Learning", font_size=50, color=COLOR_TITLE)
        self.play(Write(title), run_time=1.5)
        self.wait(1)

        definition_ml = Text(
            "Machine Learning (ML) teaches computers to learn from data",
            font_size=36, color=COLOR_TEXT
        ).next_to(title, DOWN, buff=0.8)
        definition_ml_cont = Text(
            "without explicit programming.",
            font_size=36, color=COLOR_TEXT
        ).next_to(definition_ml, DOWN)

        self.play(Write(definition_ml), run_time=2)
        self.play(Write(definition_ml_cont), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(title, definition_ml, definition_ml_cont), run_time=1)
        self.wait(0.5)

        # How ML Works
        how_ml_works_heading = Text("How Machine Learning Works", font_size=45, color=COLOR_HEADING)
        self.play(Write(how_ml_works_heading), run_time=1.5)
        self.wait(1)

        # Data Input
        data_text = Text("1. Data Input", font_size=32, color=COLOR_TEXT).shift(LEFT * 4 + UP * 2)
        data_box = Rectangle(width=2, height=1.5, color=COLOR_DATA, fill_opacity=0.5).next_to(data_text, DOWN, buff=0.5)
        data_label = Text("Data", color=BLACK).move_to(data_box)

        # Draw some example data points inside the box
        data_points = VGroup(*[
            Circle(radius=0.1, color=COLOR_HIGHLIGHT, fill_opacity=0.8).move_to(data_box.get_center() + UL * 0.3 + x * RIGHT * 0.4 + y * DOWN * 0.3)
            for x in range(3) for y in range(2)
        ])

        self.play(FadeIn(data_text, data_box, data_label, data_points), run_time=1.5)
        self.wait(1)

        # Model Processing
        arrow1 = Arrow(data_box.get_right(), ORIGIN + LEFT * 1.5, color=COLOR_ARROW)
        model_text = Text("2. Model/Algorithm", font_size=32, color=COLOR_TEXT).shift(RIGHT * 0 + UP * 2)
        model_box = Rectangle(width=3, height=2, color=COLOR_MODEL, fill_opacity=0.5).next_to(model_text, DOWN, buff=0.5)
        model_label = Text("ML Model", color=BLACK).move_to(model_box)
        model_brain = ImageMobject("brain_icon.png").scale(0.5).move_to(model_box) # Placeholder, will be replaced by a simple shape if external assets are forbidden.
        # Replacing ImageMobject with a simple shape to adhere to constraints
        model_brain = Polygon(
            [-0.5, 0.5, 0], [0.5, 0.5, 0], [0.7, 0, 0], [0.5, -0.5, 0], [-0.5, -0.5, 0], [-0.7, 0, 0],
            color=COLOR_HIGHLIGHT, fill_opacity=0.7
        ).scale(0.5).move_to(model_box)


        self.play(Create(arrow1), run_time=0.7)
        self.play(FadeIn(model_text, model_box, model_label, model_brain), run_time=1.5)
        self.wait(1)

        # Output/Prediction
        arrow2 = Arrow(model_box.get_right(), ORIGIN + RIGHT * 4, color=COLOR_ARROW)
        output_text = Text("3. Output/Prediction", font_size=32, color=COLOR_TEXT).shift(RIGHT * 4 + UP * 2)
        output_box = Rectangle(width=2, height=1.5, color=COLOR_EXAMPLE, fill_opacity=0.5).next_to(output_text, DOWN, buff=0.5)
        output_label = Text("Prediction", color=BLACK).move_to(output_box)

        self.play(Create(arrow2), run_time=0.7)
        self.play(FadeIn(output_text, output_box, output_label), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(how_ml_works_heading, data_text, data_box, data_label, data_points, arrow1, model_text, model_box, model_label, model_brain, arrow2, output_text, output_box, output_label), run_time=1.5)
        self.wait(0.5)

        # Types of Machine Learning
        types_heading = Text("Types of Machine Learning", font_size=45, color=COLOR_HEADING)
        self.play(Write(types_heading), run_time=1.5)
        self.wait(1)

        # 1. Supervised Learning
        supervised_heading = Text("1. Supervised Learning", font_size=40, color=COLOR_TITLE).to_edge(UP)
        supervised_def = Text(
            "Learning from labeled data (input-output pairs).",
            font_size=32, color=COLOR_TEXT
        ).next_to(supervised_heading, DOWN, buff=0.7)

        self.play(ReplacementTransform(types_heading, supervised_heading), run_time=1.5)
        self.play(Write(supervised_def), run_time=2)
        self.wait(1)

        # Classification Example
        classification_title = Text("a. Classification", font_size=35, color=COLOR_EXAMPLE).shift(UP * 0.5 + LEFT * 3)
        class_desc = Text("Predicting categories (e.g., Cat or Dog).", font_size=28, color=COLOR_TEXT).next_to(classification_title, DOWN)
        # Visual: Labeled data points
        group1 = VGroup(*[Dot(point=[random.uniform(-4, -2), random.uniform(-1.5, 0.5), 0], color=BLUE) for _ in range(10)])
        group2 = VGroup(*[Dot(point=[random.uniform(-1, 1), random.uniform(-1.5, 0.5), 0], color=ORANGE) for _ in range(10)])
        separator_line = Line(start=[-2.5, -2.5, 0], end=[-2.5, 2.5, 0], color=WHITE, stroke_width=3)
        label1 = Text("Class A", color=BLUE, font_size=24).next_to(group1, LEFT, buff=0.5)
        label2 = Text("Class B", color=ORANGE, font_size=24).next_to(group2, RIGHT, buff=0.5)

        self.play(FadeIn(classification_title, class_desc), run_time=1)
        self.play(Create(group1), Create(group2), run_time=1.5)
        self.play(Create(separator_line), FadeIn(label1, label2), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(classification_title, class_desc, group1, group2, separator_line, label1, label2), run_time=1)
        self.wait(0.5)

        # Regression Example
        regression_title = Text("b. Regression", font_size=35, color=COLOR_EXAMPLE).shift(UP * 0.5 + LEFT * 3)
        reg_desc = Text("Predicting continuous values (e.g., House Price).", font_size=28, color=COLOR_TEXT).next_to(regression_title, DOWN)
        # Visual: Data points and a line fitting them
        x_values = np.linspace(-3, 3, 20)
        y_values = x_values * 0.5 + np.random.normal(0, 0.3, 20)
        dots = VGroup(*[Dot(point=[x, y, 0], color=COLOR_HIGHLIGHT) for x, y in zip(x_values, y_values)])
        fit_line = Line(start=[-3.5, -3.5*0.5, 0], end=[3.5, 3.5*0.5, 0], color=GREEN, stroke_width=4)

        self.play(FadeIn(regression_title, reg_desc), run_time=1)
        self.play(Create(dots), run_time=1.5)
        self.play(Create(fit_line), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(supervised_heading, supervised_def, regression_title, reg_desc, dots, fit_line), run_time=1.5)
        self.wait(0.5)

        # 2. Unsupervised Learning
        unsupervised_heading = Text("2. Unsupervised Learning", font_size=40, color=COLOR_TITLE).to_edge(UP)
        unsupervised_def = Text(
            "Learning from unlabeled data; finding hidden patterns.",
            font_size=32, color=COLOR_TEXT
        ).next_to(unsupervised_heading, DOWN, buff=0.7)

        self.play(Write(unsupervised_heading), run_time=1.5)
        self.play(Write(unsupervised_def), run_time=2)
        self.wait(1)

        # Clustering Example
        clustering_title = Text("a. Clustering", font_size=35, color=COLOR_EXAMPLE).shift(UP * 0.5 + LEFT * 3)
        cluster_desc = Text("Grouping similar data points.", font_size=28, color=COLOR_TEXT).next_to(clustering_title, DOWN)
        # Visual: Data points forming natural clusters
        cluster1 = VGroup(*[Dot(point=[random.uniform(-4, -2.5), random.uniform(-1, 1), 0], color=BLUE) for _ in range(12)])
        cluster2 = VGroup(*[Dot(point=[random.uniform(0.5, 2), random.uniform(-1.5, 0.5), 0], color=ORANGE) for _ in range(12)])
        cluster3 = VGroup(*[Dot(point=[random.uniform(-1.5, 0), random.uniform(1, 2), 0], color=GREEN) for _ in range(12)])

        self.play(FadeIn(clustering_title, cluster_desc), run_time=1)
        self.play(Create(cluster1), Create(cluster2), Create(cluster3), run_time=2)
        self.wait(2)

        self.play(FadeOut(unsupervised_heading, unsupervised_def, clustering_title, cluster_desc, cluster1, cluster2, cluster3), run_time=1.5)
        self.wait(0.5)

        # 3. Reinforcement Learning
        rl_heading = Text("3. Reinforcement Learning", font_size=40, color=COLOR_TITLE).to_edge(UP)
        rl_def = Text(
            "Learning by trial and error, through rewards and penalties.",
            font_size=32, color=COLOR_TEXT
        ).next_to(rl_heading, DOWN, buff=0.7)

        self.play(Write(rl_heading), run_time=1.5)
        self.play(Write(rl_def), run_time=2)
        self.wait(1)

        # RL Components
        agent_box = Rectangle(width=2, height=1.5, color=COLOR_MODEL, fill_opacity=0.5).shift(LEFT * 3)
        agent_text = Text("Agent", color=BLACK).move_to(agent_box)
        env_box = Rectangle(width=2.5, height=1.5, color=COLOR_DATA, fill_opacity=0.5).shift(RIGHT * 3)
        env_text = Text("Environment", color=BLACK).move_to(env_box)

        arrow_action = Arrow(agent_box.get_right(), env_box.get_left(), color=COLOR_ARROW)
        action_label = Text("Action", font_size=24, color=COLOR_TEXT).next_to(arrow_action, UP)

        arrow_reward = Arrow(env_box.get_left(), agent_box.get_right(), color=COLOR_ARROW).rotate(PI) # Rotated arrow for reverse
        reward_label = Text("Reward/State", font_size=24, color=COLOR_TEXT).next_to(arrow_reward, DOWN)

        rl_example = Text("Example: A robot learning to walk.", font_size=30, color=COLOR_EXAMPLE).next_to(rl_def, DOWN, buff=1.5)

        self.play(FadeIn(agent_box, agent_text, env_box, env_text), run_time=1.5)
        self.play(Create(arrow_action), Write(action_label), run_time=1)
        self.play(Create(arrow_reward), Write(reward_label), run_time=1)
        self.play(Write(rl_example), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(rl_heading, rl_def, agent_box, agent_text, env_box, env_text, arrow_action, action_label, arrow_reward, reward_label, rl_example), run_time=1.5)
        self.wait(0.5)

        # Conclusion
        conclusion_heading = Text("Conclusion", font_size=45, color=COLOR_HEADING)
        self.play(Write(conclusion_heading), run_time=1)
        self.wait(1)

        summary1 = Text(
            "Machine Learning empowers computers to learn complex patterns.",
            font_size=36, color=COLOR_TEXT
        ).next_to(conclusion_heading, DOWN, buff=0.8)
        summary2 = Text(
            "It's driving innovation in many fields.",
            font_size=36, color=COLOR_TEXT
        ).next_to(summary1, DOWN)

        self.play(Write(summary1), run_time=2)
        self.play(Write(summary2), run_time=2)
        self.wait(2)

        # End scene
        self.play(FadeOut(*self.mobjects), run_time=1.5)