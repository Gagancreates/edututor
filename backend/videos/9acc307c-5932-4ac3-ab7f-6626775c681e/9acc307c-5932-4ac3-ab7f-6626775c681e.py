from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Text("What is Machine Learning?", font_size=48)
        self.play(Write(title), run_time=1.5)
        self.wait(1)

        definition_text = Text("Machine Learning (ML) is a field of AI...", font_size=24)
        definition_text.move_to(DOWN * 1)
        self.play(Write(definition_text), run_time=2)
        self.wait(2)

        self.play(FadeOut(title, definition_text), run_time=1)

        # Section 1: Data and Patterns
        data_title = Text("Data is Key!", font_size=36)
        self.play(Write(data_title), run_time=1)
        self.wait(1)

        circles = VGroup(*[Circle(radius=0.2, color=BLUE).move_to([i - 3, 0, 0]) for i in range(7)])
        squares = VGroup(*[Square(side_length=0.3, color=GREEN).move_to([i - 3, 1, 0]) for i in range(7)])
        triangles = VGroup(*[Triangle(color=RED).scale(0.3).move_to([i - 3, -1, 0]) for i in range(7)])
        data_group = VGroup(circles, squares, triangles)

        self.play(Create(data_group), run_time=1.5)
        self.wait(1)

        pattern_text = Text("ML algorithms find patterns in data.", font_size=24)
        pattern_text.move_to(DOWN * 2)
        self.play(Write(pattern_text), run_time=2)
        self.wait(2)

        arrow = Arrow(start=UP * 1.5, end=DOWN * 0.5, color=YELLOW)
        self.play(Create(arrow), run_time=1)
        self.wait(1)

        self.play(FadeOut(data_title, data_group, pattern_text, arrow), run_time=1)

        # Section 2: Algorithms
        algo_title = Text("Algorithms: The Learning Machines", font_size=36)
        self.play(Write(algo_title), run_time=1)
        self.wait(1)

        algo_box = Rectangle(width=4, height=2, color=ORANGE)
        algo_text = Text("ML Algorithm", font_size=24)
        algo_text.move_to(algo_box.get_center())
        algo_group = VGroup(algo_box, algo_text)
        self.play(Create(algo_group), run_time=1.5)
        self.wait(1)

        input_text = Text("Input Data", font_size=20).move_to(LEFT * 3 + UP * 3)
        output_text = Text("Predictions", font_size=20).move_to(RIGHT * 3 + UP * 3)
        arrow_in = Arrow(start=input_text.get_right(), end=algo_box.get_left(), color=BLUE)
        arrow_out = Arrow(start=algo_box.get_right(), end=output_text.get_left(), color=GREEN)

        self.play(Create(input_text), Create(output_text), Create(arrow_in), Create(arrow_out), run_time=1)
        self.wait(1)

        example_algo = Text("Examples: Linear Regression, Decision Trees...", font_size=18).move_to(DOWN * 2)
        self.play(Write(example_algo), run_time=2)
        self.wait(2)

        self.play(FadeOut(algo_title, algo_group, input_text, output_text, arrow_in, arrow_out, example_algo), run_time=1)

        # Section 3: Training and Prediction
        train_title = Text("Training and Prediction", font_size=36)
        self.play(Write(train_title), run_time=1)
        self.wait(1)

        train_box = Rectangle(width=3, height=1.5, color=PURPLE).move_to(LEFT * 3)
        train_text = Text("Training", font_size=24).move_to(train_box.get_center())

        predict_box = Rectangle(width=3, height=1.5, color=TEAL).move_to(RIGHT * 3)
        predict_text = Text("Prediction", font_size=24).move_to(predict_box.get_center())

        self.play(Create(train_box), Create(train_text), Create(predict_box), Create(predict_text), run_time=1.5)
        self.wait(1)

        train_arrow = Arrow(start=ORIGIN + LEFT * 1.5 + DOWN * 2, end=train_box.get_center() + UP * 0.7, color=YELLOW)
        predict_arrow = Arrow(start=ORIGIN + RIGHT * 1.5 + DOWN * 2, end=predict_box.get_center() + UP * 0.7, color=YELLOW)
        new_data_text = Text("New Data", font_size=20).move_to(ORIGIN + RIGHT * 1.5 + DOWN * 2)
        trained_model_text = Text("Trained Model", font_size=20).move_to(ORIGIN + LEFT * 1.5 + DOWN * 2)

        self.play(Create(train_arrow), Create(predict_arrow), Write(new_data_text), Write(trained_model_text), run_time=1)
        self.wait(1)

        self.play(FadeOut(train_title, train_box, train_text, predict_box, predict_text, train_arrow, predict_arrow, new_data_text, trained_model_text), run_time=1)

        # Applications
        applications_title = Text("Applications of Machine Learning", font_size=36)
        self.play(Write(applications_title), run_time=1)
        self.wait(1)

        app1 = Text("Image Recognition", font_size=24).move_to(UP * 2)
        app2 = Text("Natural Language Processing", font_size=24).move_to(UP * 0.5)
        app3 = Text("Recommendation Systems", font_size=24).move_to(DOWN * 1)
        app4 = Text("Fraud Detection", font_size=24).move_to(DOWN * 2.5)

        self.play(Write(app1), Write(app2), Write(app3), Write(app4), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(applications_title, app1, app2, app3, app4), run_time=1)

        # Conclusion
        conclusion = Text("Machine learning empowers computers to learn from data...", font_size=30)
        self.play(Write(conclusion), run_time=2)
        self.wait(3)

        self.play(FadeOut(*self.mobjects), run_time=1)