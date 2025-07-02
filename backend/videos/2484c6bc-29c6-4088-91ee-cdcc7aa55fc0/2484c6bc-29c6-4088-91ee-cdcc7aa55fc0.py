from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- Section 1: Introduction (What is Machine Learning?) ---
        title = Text("What is Machine Learning?", font_size=50).to_edge(UP)
        self.play(Write(title, run_time=1.5))
        self.wait(1.5)

        definition_text = Text("Machine Learning (ML) is teaching computers to learn from data", font_size=32).next_to(title, DOWN, buff=0.8)
        definition_text_cont = Text("without being explicitly programmed.", font_size=32).next_to(definition_text, DOWN, buff=0.2)
        self.play(Write(definition_text, run_time=1.5))
        self.play(Write(definition_text_cont, run_time=1.2))
        self.wait(2)

        # Analogy: Child learning vs. explicit instructions
        child_analogy_1 = Text("Imagine teaching a child to recognize a 'cat'.", font_size=30).move_to(LEFT * 3 + UP * 0.5)
        self.play(FadeIn(child_analogy_1, run_time=1))
        self.wait(1)

        child_analogy_2 = Text("You show them many pictures: 'This is a cat,' 'This is NOT a cat.'", font_size=30).next_to(child_analogy_1, DOWN, buff=0.5)
        self.play(Write(child_analogy_2, run_time=1.5))
        self.wait(1.5)

        child_analogy_3 = Text("Eventually, they learn to identify cats on their own.", font_size=30).next_to(child_analogy_2, DOWN, buff=0.5)
        self.play(Write(child_analogy_3, run_time=1.5))
        self.wait(2)

        ml_analogy_1 = Text("Machine Learning works similarly for computers.", font_size=30, color=YELLOW).move_to(RIGHT * 3 + UP * 0.5)
        self.play(FadeIn(ml_analogy_1, run_time=1))
        self.wait(1)

        ml_analogy_2 = Text("We feed them 'data' (pictures, numbers, text)...", font_size=30, color=YELLOW).next_to(ml_analogy_1, DOWN, buff=0.5)
        self.play(Write(ml_analogy_2, run_time=1.5))
        self.wait(1.5)

        ml_analogy_3 = Text("...and they learn patterns to make decisions or predictions.", font_size=30, color=YELLOW).next_to(ml_analogy_2, DOWN, buff=0.5)
        self.play(Write(ml_analogy_3, run_time=1.5))
        self.wait(2)

        self.play(FadeOut(child_analogy_1, child_analogy_2, child_analogy_3,
                           ml_analogy_1, ml_analogy_2, ml_analogy_3,
                           definition_text, definition_text_cont, title, run_time=1.5))
        self.wait(1)

        # --- Section 2: Core Understanding (How does it work?) ---
        core_title = Text("How Does It Work?", font_size=45).to_edge(UP)
        self.play(FadeIn(core_title, run_time=1))
        self.wait(1.5)

        # Basic flow: Data -> ML Model -> Prediction
        data_box = Rectangle(width=2, height=1.5, color=BLUE).move_to(LEFT * 4)
        data_text = Text("Input Data", font_size=28).move_to(data_box.get_center())
        self.play(Create(data_box, run_time=0.8), Write(data_text, run_time=0.8))
        self.wait(0.8)

        ml_model_box = Rectangle(width=2.5, height=1.5, color=GREEN).move_to(ORIGIN)
        ml_model_text = Text("ML Model", font_size=28).move_to(ml_model_box.get_center())
        self.play(Create(ml_model_box, run_time=0.8), Write(ml_model_text, run_time=0.8))
        self.wait(0.8)

        output_box = Rectangle(width=2, height=1.5, color=RED).move_to(RIGHT * 4)
        output_text = Text("Output", font_size=28).move_to(output_box.get_center())
        self.play(Create(output_box, run_time=0.8), Write(output_text, run_time=0.8))
        self.wait(0.8)

        arrow1 = Arrow(data_box.get_right(), ml_model_box.get_left(), buff=0.1, max_stroke_width_to_length_ratio=4)
        arrow2 = Arrow(ml_model_box.get_right(), output_box.get_left(), buff=0.1, max_stroke_width_to_length_ratio=4)
        self.play(GrowArrow(arrow1, run_time=0.8), GrowArrow(arrow2, run_time=0.8))
        self.wait(2)

        # Components: Data, Model, Learning Algorithm
        components_text = Text("Key Components:", font_size=35).to_edge(LEFT).shift(UP * 2)
        self.play(FadeIn(components_text, run_time=1))
        self.wait(1)

        data_comp = Text("1. Data", font_size=30, color=BLUE).next_to(components_text, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(data_comp, run_time=1))
        self.wait(0.5)
        data_desc = Text("Historical examples with patterns.", font_size=25).next_to(data_comp, RIGHT, buff=0.5)
        self.play(Write(data_desc, run_time=1))
        self.wait(1.5)

        model_comp = Text("2. Model", font_size=30, color=GREEN).next_to(data_comp, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(model_comp, run_time=1))
        self.wait(0.5)
        model_desc = Text("A mathematical function that learns from data.", font_size=25).next_to(model_comp, RIGHT, buff=0.5)
        self.play(Write(model_desc, run_time=1))
        self.wait(1.5)

        alg_comp = Text("3. Learning Algorithm", font_size=30, color=ORANGE).next_to(model_comp, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(alg_comp, run_time=1))
        self.wait(0.5)
        alg_desc = Text("Method to adjust the model for better predictions.", font_size=25).next_to(alg_comp, RIGHT, buff=0.5)
        self.play(Write(alg_desc, run_time=1))
        self.wait(2)

        self.play(FadeOut(components_text, data_comp, data_desc, model_comp, model_desc, alg_comp, alg_desc, run_time=1.5))
        self.wait(0.5)

        # Illustrate Learning Algorithm (Feedback Loop)
        arrow_feedback = Arrow(output_box.get_bottom(), ml_model_box.get_bottom(), buff=0.1, max_stroke_width_to_length_ratio=4, color=ORANGE)
        arrow_feedback.set_points_as_corners([output_box.get_bottom() + DOWN * 0.5 + RIGHT * 0.5,
                                             output_box.get_bottom() + DOWN * 1,
                                             ml_model_box.get_bottom() + DOWN * 1,
                                             ml_model_box.get_bottom() + DOWN * 0.5 + LEFT * 0.5])
        
        feedback_text = Text("Learning Algorithm (Adjusts)", font_size=25, color=ORANGE).next_to(arrow_feedback, DOWN, buff=0.2)
        self.play(GrowArrow(arrow_feedback, run_time=1.5), Write(feedback_text, run_time=1.5))
        self.wait(2.5)

        self.play(FadeOut(data_box, data_text, ml_model_box, ml_model_text, output_box, output_text,
                           arrow1, arrow2, arrow_feedback, feedback_text, core_title, run_time=1.5))
        self.wait(1)

        # --- Section 3: Examples (Types of ML) ---
        types_title = Text("Types of Machine Learning", font_size=45).to_edge(UP)
        self.play(FadeIn(types_title, run_time=1))
        self.wait(1.5)

        # Supervised Learning
        supervised_label = Text("1. Supervised Learning", font_size=35, color=BLUE).to_edge(LEFT).shift(UP*2)
        self.play(Write(supervised_label, run_time=1))
        self.wait(0.8)
        supervised_desc = Text("Learning from labeled data (input-output pairs).", font_size=28).next_to(supervised_label, RIGHT, buff=0.5)
        self.play(Write(supervised_desc, run_time=1.5))
        self.wait(1.5)

        # Classification
        classification_label = Text("Classification:", font_size=30, color=GREEN).next_to(supervised_label, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(classification_label, run_time=1))
        self.wait(0.8)
        classification_desc = Text("Predicting a category (e.g., spam/not-spam, cat/dog).", font_size=25).next_to(classification_label, RIGHT, buff=0.5)
        self.play(Write(classification_desc, run_time=1.5))
        self.wait(1.5)

        # Visual for Classification: Circles and Squares
        group1_color = YELLOW
        group2_color = PURPLE
        
        circles = VGroup(*[Circle(radius=0.15, color=group1_color, fill_opacity=0.8).move_to(np.array([x, y, 0]))
                           for x in np.linspace(-3, -1, 3) for y in np.linspace(-1.5, 0.5, 3)])
        squares = VGroup(*[Square(side_length=0.3, color=group2_color, fill_opacity=0.8).move_to(np.array([x, y, 0]))
                           for x in np.linspace(1, 3, 3) for y in np.linspace(-0.5, 1.5, 3)])
        
        self.play(Create(circles, run_time=1), Create(squares, run_time=1))
        self.wait(1)

        line_separator = Line(start=LEFT * 0.5 + DOWN * 2, end=RIGHT * 0.5 + UP * 2, color=WHITE, stroke_width=4)
        self.play(Create(line_separator, run_time=1.5))
        self.wait(2)

        self.play(FadeOut(circles, squares, line_separator,
                           classification_label, classification_desc, run_time=1))
        self.wait(0.8)

        # Regression
        regression_label = Text("Regression:", font_size=30, color=RED).next_to(supervised_label, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(regression_label, run_time=1))
        self.wait(0.8)
        regression_desc = Text("Predicting a continuous value (e.g., house price, temperature).", font_size=25).next_to(regression_label, RIGHT, buff=0.5)
        self.play(Write(regression_desc, run_time=1.5))
        self.wait(1.5)

        # Visual for Regression: Scatter plot and line
        axes = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=6, y_length=4, tips=False).shift(DOWN*0.5)
        x_label = Text("Size", font_size=24).next_to(axes.x_axis, DOWN)
        y_label = Text("Price", font_size=24, rotation=PI/2).next_to(axes.y_axis, LEFT)
        self.play(Create(axes, run_time=1), Write(x_label, run_time=0.8), Write(y_label, run_time=0.8))
        self.wait(0.8)

        points = VGroup(*[Dot(axes.c2p(x, x * 0.8 + np.random.rand() * 0.5), radius=0.08, color=BLUE_A)
                           for x in np.linspace(0.5, 4.5, 10)])
        self.play(Create(points, run_time=1.5))
        self.wait(1.5)

        fit_line = axes.get_graph(lambda x: 0.8 * x + 0.5, color=GREEN)
        self.play(Create(fit_line, run_time=1.5))
        self.wait(2)

        self.play(FadeOut(axes, x_label, y_label, points, fit_line,
                           regression_label, regression_desc, supervised_label, supervised_desc, run_time=1.5))
        self.wait(1)

        # Unsupervised Learning
        unsupervised_label = Text("2. Unsupervised Learning", font_size=35, color=PURPLE).to_edge(LEFT).shift(UP*2)
        self.play(Write(unsupervised_label, run_time=1))
        self.wait(0.8)
        unsupervised_desc = Text("Finding patterns in unlabeled data.", font_size=28).next_to(unsupervised_label, RIGHT, buff=0.5)
        self.play(Write(unsupervised_desc, run_time=1.5))
        self.wait(1.5)

        # Clustering
        clustering_label = Text("Clustering:", font_size=30, color=ORANGE).next_to(unsupervised_label, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(clustering_label, run_time=1))
        self.wait(0.8)
        clustering_desc = Text("Grouping similar data points together.", font_size=25).next_to(clustering_label, RIGHT, buff=0.5)
        self.play(Write(clustering_desc, run_time=1.5))
        self.wait(1.5)

        # Visual for Clustering
        cluster_data = VGroup(*[Dot(np.array([x, y, 0]), radius=0.08, color=LIGHT_GRAY)
                                for x in np.linspace(-3, -1, 5) for y in np.linspace(-0.5, 1.5, 5)] +
                              [Dot(np.array([x, y, 0]), radius=0.08, color=LIGHT_GRAY)
                                for x in np.linspace(1, 3, 5) for y in np.linspace(-1.5, 0.5, 5)])
        self.play(Create(cluster_data, run_time=1.5))
        self.wait(1)

        cluster1_outline = Circle(radius=1, color=YELLOW, stroke_width=4).move_to(LEFT*2 + UP*0.5)
        cluster2_outline = Circle(radius=1, color=PINK, stroke_width=4).move_to(RIGHT*2 + DOWN*0.5)
        self.play(Create(cluster1_outline, run_time=1), Create(cluster2_outline, run_time=1))
        self.wait(2.5)

        self.play(FadeOut(cluster_data, cluster1_outline, cluster2_outline,
                           clustering_label, clustering_desc, unsupervised_label, unsupervised_desc,
                           types_title, run_time=1.5))
        self.wait(1)

        # --- Section 4: Applications & Conclusion ---
        apps_title = Text("Real-World Applications", font_size=45).to_edge(UP)
        self.play(FadeIn(apps_title, run_time=1))
        self.wait(1.5)

        app1 = Text("Recommendation Systems (Netflix, Amazon)", font_size=32, color=BLUE).shift(UP * 1.5)
        self.play(Write(app1, run_time=1.2))
        self.wait(1.5)

        app2 = Text("Spam Detection (Email filters)", font_size=32, color=GREEN).next_to(app1, DOWN, buff=0.8)
        self.play(Write(app2, run_time=1.2))
        self.wait(1.5)

        app3 = Text("Medical Diagnosis (Analyzing patient data)", font_size=32, color=RED).next_to(app2, DOWN, buff=0.8)
        self.play(Write(app3, run_time=1.2))
        self.wait(1.5)

        app4 = Text("Self-Driving Cars (Perceiving environment)", font_size=32, color=ORANGE).next_to(app3, DOWN, buff=0.8)
        self.play(Write(app4, run_time=1.2))
        self.wait(2.5)

        conclusion_text = Text("Machine Learning is transforming industries,", font_size=38).shift(UP*1)
        conclusion_text2 = Text("enabling computers to discover insights and make intelligent decisions.", font_size=38).next_to(conclusion_text, DOWN, buff=0.5)
        self.play(FadeOut(app1, app2, app3, app4, apps_title, run_time=1.5))
        self.play(Write(conclusion_text, run_time=1.5))
        self.play(Write(conclusion_text2, run_time=1.5))
        self.wait(3)

        # Final FadeOut
        self.play(FadeOut(*self.mobjects, run_time=2))