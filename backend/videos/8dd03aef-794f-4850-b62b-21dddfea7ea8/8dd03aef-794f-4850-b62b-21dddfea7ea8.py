from manim import *

class CreateScene(Scene):
    def construct(self):
        # 1. Introduction: What is Machine Learning?
        title = Text("What is Machine Learning?", font_size=60)
        self.play(Write(title), run_time=1.5)
        self.wait(2)

        definition = Text("Teaching computers to learn from data,", font_size=40).next_to(title, DOWN, buff=0.8)
        second_part = Text("without being explicitly programmed.", font_size=40).next_to(definition, DOWN, buff=0.4)
        self.play(Write(definition), run_time=1.2)
        self.play(Write(second_part), run_time=1.2)
        self.wait(2.5)

        human_learn = Text("Just like humans learn from experience.", font_size=36).next_to(second_part, DOWN, buff=0.8)
        self.play(FadeIn(human_learn), run_time=1)
        self.wait(2.5)

        # 2. Core Understanding: The Learning Process
        self.play(FadeOut(title, definition, second_part, human_learn), run_time=1.5)
        self.wait(1.5)

        process_title = Text("The Machine Learning Process", font_size=50)
        self.play(Write(process_title), run_time=1.5)
        self.wait(2)

        input_label = Text("Input Data", font_size=40, color=YELLOW).to_edge(LEFT).shift(UP)
        model_label = Text("ML Model", font_size=40, color=BLUE).move_to(ORIGIN)
        output_label = Text("Prediction/Output", font_size=40, color=GREEN).to_edge(RIGHT).shift(UP)

        input_box = Rectangle(width=3, height=1.5, color=YELLOW).next_to(input_label, DOWN, buff=0.5)
        model_box = Rectangle(width=3, height=1.5, color=BLUE).next_to(model_label, DOWN, buff=0.5)
        output_box = Rectangle(width=3, height=1.5, color=GREEN).next_to(output_label, DOWN, buff=0.5)

        arrow_1 = Arrow(input_box.get_right(), model_box.get_left(), buff=0.1)
        arrow_2 = Arrow(model_box.get_right(), output_box.get_left(), buff=0.1)

        self.play(FadeIn(input_label, input_box), run_time=1)
        self.play(Create(arrow_1), run_time=0.8)
        self.play(FadeIn(model_label, model_box), run_time=1)
        self.play(Create(arrow_2), run_time=0.8)
        self.play(FadeIn(output_label, output_box), run_time=1)
        self.wait(2.5)

        # Data flow demonstration
        data_point_1 = Square(side_length=0.5, color=WHITE).move_to(input_box.get_center())
        data_point_text = Text("Data Point", font_size=25).next_to(data_point_1, UP, buff=0.2)
        self.play(Create(data_point_1), FadeIn(data_point_text), run_time=1)
        self.wait(1.5)
        self.play(
            ReplacementTransform(data_point_1, Square(side_length=0.5, color=WHITE).move_to(model_box.get_center())),
            FadeOut(data_point_text),
            run_time=1.5
        )
        prediction_point = Circle(radius=0.3, color=GREEN).move_to(output_box.get_center())
        prediction_text = Text("Prediction", font_size=25).next_to(prediction_point, UP, buff=0.2)
        self.play(
            ReplacementTransform(Square(side_length=0.5, color=WHITE).move_to(model_box.get_center()), prediction_point),
            FadeIn(prediction_text),
            run_time=1.5
        )
        self.wait(2)

        # Feedback loop
        feedback_label = Text("Feedback / Error", font_size=35, color=RED).next_to(output_box, DOWN, buff=1.5).to_edge(RIGHT)
        feedback_arrow_1 = Arrow(output_box.get_bottom(), feedback_label.get_top(), buff=0.1, color=RED)
        feedback_arrow_2 = Arrow(feedback_label.get_left(), model_box.get_bottom(), buff=0.1, color=RED)
        feedback_arrow_2.set_points_as_corners([feedback_label.get_left(), feedback_label.get_left() + LEFT*2, model_box.get_bottom() + LEFT*2, model_box.get_bottom()])

        self.play(FadeIn(feedback_label), Create(feedback_arrow_1), run_time=1.2)
        self.play(Create(feedback_arrow_2), run_time=1.5)
        self.wait(2.5)

        # Refine/Train the model
        train_text = Text("Train (Adjust Model)", font_size=38, color=BLUE).move_to(model_box.get_center())
        self.play(ReplacementTransform(model_label, train_text), run_time=1.5)
        self.wait(2.5)

        # Analogy: Learning to Identify Apples
        self.play(FadeOut(process_title, input_label, input_box, arrow_1, train_text, model_box, arrow_2, output_label, output_box, prediction_point, prediction_text, feedback_label, feedback_arrow_1, feedback_arrow_2), run_time=1.5)
        self.wait(1.5)

        analogy_title = Text("Analogy: Learning to Identify Apples", font_size=48)
        self.play(Write(analogy_title), run_time=1.5)
        self.wait(1.5)

        features_text = Text("Input: Features (Color, Shape, Size)", font_size=36).to_edge(LEFT).shift(UP*1.5)
        apple_circle = Circle(radius=0.5, color=RED).next_to(features_text, DOWN, buff=0.5).set_fill(RED, opacity=0.8)
        apple_text = Text("Is it an Apple?", font_size=28, color=BLACK).move_to(apple_circle.get_center())
        apple_group = VGroup(apple_circle, apple_text)

        brain_model = Rectangle(width=4, height=3, color=GREEN).move_to(ORIGIN)
        brain_text = Text("Brain (Model)", font_size=36, color=GREEN).move_to(brain_model.get_center())

        prediction_output = Text("Output: 'Apple' or 'Not Apple'", font_size=36).to_edge(RIGHT).shift(UP*1.5)

        arrow1_analogy = Arrow(apple_group.get_right(), brain_model.get_left(), buff=0.1)
        arrow2_analogy = Arrow(brain_model.get_right(), prediction_output.get_left(), buff=0.1)

        self.play(FadeIn(features_text), Create(apple_group), run_time=1.5)
        self.play(Create(arrow1_analogy), run_time=0.8)
        self.play(Create(brain_model), FadeIn(brain_text), run_time=1.5)
        self.play(Create(arrow2_analogy), run_time=0.8)
        self.play(FadeIn(prediction_output), run_time=1)
        self.wait(2.5)

        # Correction/Feedback loop for the analogy
        correction_label = Text("Correction: 'It's a Tomato!'", font_size=32, color=RED).next_to(prediction_output, DOWN, buff=1.5).to_edge(RIGHT)
        correction_arrow_1 = Arrow(prediction_output.get_bottom(), correction_label.get_top(), buff=0.1, color=RED)
        correction_arrow_2 = Arrow(correction_label.get_left(), brain_model.get_bottom(), buff=0.1, color=RED)
        correction_arrow_2.set_points_as_corners([correction_label.get_left(), correction_label.get_left() + LEFT*2, brain_model.get_bottom() + LEFT*2, brain_model.get_bottom()])

        self.play(FadeIn(correction_label), Create(correction_arrow_1), run_time=1.2)
        self.play(Create(correction_arrow_2), run_time=1.5)
        self.wait(3)

        learn_more_text = Text("The model learns by adjusting itself based on feedback.", font_size=36).move_to(ORIGIN).shift(DOWN*2.5)
        self.play(FadeIn(learn_more_text), run_time=1.5)
        self.wait(2.5)

        # 3. Examples: ML Tasks & Examples
        self.play(FadeOut(analogy_title, features_text, apple_group, arrow1_analogy, brain_model, brain_text, arrow2_analogy, prediction_output, correction_label, correction_arrow_1, correction_arrow_2, learn_more_text), run_time=1.5)
        self.wait(1.5)

        examples_title = Text("Machine Learning Tasks & Examples", font_size=50)
        self.play(Write(examples_title), run_time=1.5)
        self.wait(2)

        # Supervised Learning
        supervised_title = Text("Supervised Learning", font_size=45, color=BLUE).next_to(examples_title, DOWN, buff=1.0)
        supervised_def = Text("Learning from labeled data (input-output pairs).", font_size=35).next_to(supervised_title, DOWN, buff=0.5)
        self.play(Write(supervised_title), run_time=1.2)
        self.play(FadeIn(supervised_def), run_time=1)
        self.wait(2.5)

        # Classification
        classification_title = Text("1. Classification (e.g., Spam Detection)", font_size=38, color=YELLOW).next_to(supervised_def, DOWN, buff=0.8).to_edge(LEFT)
        classification_def = Text("Predicting a category or label.", font_size=32).next_to(classification_title, DOWN, buff=0.3).to_edge(LEFT)
        self.play(FadeIn(classification_title), run_time=1)
        self.play(FadeIn(classification_def), run_time=1)
        self.wait(2)

        # Regression
        regression_title = Text("2. Regression (e.g., House Prices)", font_size=38, color=ORANGE).next_to(classification_title, RIGHT, buff=2)
        regression_def = Text("Predicting a continuous value.", font_size=32).next_to(regression_title, DOWN, buff=0.3)
        self.play(FadeIn(regression_title), run_time=1)
        self.play(FadeIn(regression_def), run_time=1)
        self.wait(2.5)

        self.play(FadeOut(supervised_title, supervised_def, classification_title, classification_def, regression_title, regression_def), run_time=1.5)
        self.wait(1.5)

        # Unsupervised Learning
        unsupervised_title = Text("Unsupervised Learning", font_size=45, color=PURPLE).next_to(examples_title, DOWN, buff=1.0)
        unsupervised_def = Text("Finding patterns in unlabeled data.", font_size=35).next_to(unsupervised_title, DOWN, buff=0.5)
        self.play(ReplacementTransform(examples_title, unsupervised_title), run_time=1.5)
        self.play(FadeIn(unsupervised_def), run_time=1)
        self.wait(2.5)

        # Clustering
        clustering_title = Text("1. Clustering (e.g., Customer Segmentation)", font_size=38, color=PINK).next_to(unsupervised_def, DOWN, buff=0.8).to_edge(LEFT)
        clustering_def = Text("Grouping similar data points.", font_size=32).next_to(clustering_title, DOWN, buff=0.3).to_edge(LEFT)
        self.play(FadeIn(clustering_title), run_time=1)
        self.play(FadeIn(clustering_def), run_time=1)
        self.wait(2.5)

        # 4. Applications & Summary
        self.play(FadeOut(unsupervised_title, unsupervised_def, clustering_title, clustering_def), run_time=1.5)
        self.wait(1.5)

        applications_title = Text("Where is ML Used?", font_size=50)
        self.play(Write(applications_title), run_time=1.5)
        self.wait(1.5)

        app1 = Text("• Self-driving cars", font_size=38).next_to(applications_title, DOWN, buff=0.8).to_edge(LEFT)
        app2 = Text("• Recommendation systems (Netflix, Amazon)", font_size=38).next_to(app1, DOWN, buff=0.4).to_edge(LEFT)
        app3 = Text("• Medical diagnosis", font_size=38).next_to(app2, DOWN, buff=0.4).to_edge(LEFT)
        app4 = Text("• Fraud detection", font_size=38).next_to(app3, DOWN, buff=0.4).to_edge(LEFT)

        self.play(FadeIn(app1), run_time=1)
        self.play(FadeIn(app2), run_time=1)
        self.play(FadeIn(app3), run_time=1)
        self.play(FadeIn(app4), run_time=1)
        self.wait(2.5)

        summary_text = Text("In essence, ML empowers computers to learn and adapt,", font_size=40).move_to(ORIGIN)
        summary_text_2 = Text("finding patterns and making predictions from data.", font_size=40).next_to(summary_text, DOWN, buff=0.4)
        self.play(Transform(applications_title, summary_text), FadeOut(app1, app2, app3, app4), run_time=1.5)
        self.play(FadeIn(summary_text_2), run_time=1)
        self.wait(3)

        self.play(FadeOut(*self.mobjects), run_time=1.5)