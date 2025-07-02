from manim import *

class CreateScene(Scene):
    def construct(self):
        # 1. Introduction: What is Machine Learning?
        title = Text("What is Machine Learning?").scale(1.2).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(2)

        ml_def_text = Text("Teaching computers to learn from data.").next_to(title, DOWN, buff=0.8)
        self.play(Write(ml_def_text), run_time=2)
        self.wait(2.5)

        # Contrast with Traditional Programming
        traditional_prog = Text("Traditional Programming", font_size=36).to_edge(LEFT).shift(UP*1.5)
        ml_prog = Text("Machine Learning", font_size=36).to_edge(RIGHT).shift(UP*1.5)

        # Traditional Programming Diagram
        program_box = Rectangle(width=3, height=1.5, color=BLUE).next_to(traditional_prog, DOWN, buff=0.5)
        program_text = Text("Rules (explicit)", font_size=24).move_to(program_box.center())
        data_box_trad = Rectangle(width=3, height=1.5, color=GREEN).next_to(program_box, DOWN, buff=0.5)
        data_text_trad = Text("Data", font_size=24).move_to(data_box_trad.center())
        output_box_trad = Rectangle(width=3, height=1.5, color=RED).next_to(data_box_trad, DOWN, buff=0.5)
        output_text_trad = Text("Output", font_size=24).move_to(output_box_trad.center())

        arrow_rules_data_trad = Arrow(program_box.get_bottom(), data_box_trad.get_top(), buff=0.1)
        arrow_data_output_trad = Arrow(data_box_trad.get_bottom(), output_box_trad.get_top(), buff=0.1)
        
        trad_group = VGroup(traditional_prog, program_box, program_text, data_box_trad, data_text_trad, 
                            output_box_trad, output_text_trad, arrow_rules_data_trad, arrow_data_output_trad).scale(0.8).move_to(LEFT*3)

        # ML side Diagram
        ml_model_box = Rectangle(width=3, height=1.5, color=ORANGE).next_to(ml_prog, DOWN, buff=0.5)
        ml_model_text = Text("Model (learned)", font_size=24).move_to(ml_model_box.center())
        data_box_ml = Rectangle(width=3, height=1.5, color=GREEN).next_to(ml_model_box, DOWN, buff=0.5)
        data_text_ml = Text("Data", font_size=24).move_to(data_box_ml.center())
        output_box_ml = Rectangle(width=3, height=1.5, color=RED).next_to(data_box_ml, DOWN, buff=0.5)
        output_text_ml = Text("Output", font_size=24).move_to(output_box_ml.center())

        arrow_data_to_model = Arrow(data_box_ml.get_top(), ml_model_box.get_bottom(), buff=0.1)
        arrow_model_to_output = Arrow(ml_model_box.get_bottom(), output_box_ml.get_top(), buff=0.1)
        
        ml_group = VGroup(ml_prog, ml_model_box, ml_model_text, data_box_ml, data_text_ml, 
                          output_box_ml, output_text_ml, arrow_data_to_model, arrow_model_to_output).scale(0.8).move_to(RIGHT*3)

        self.play(
            FadeOut(title, ml_def_text),
            FadeIn(trad_group, ml_group),
            run_time=1.5
        )
        self.wait(2.5)

        key_idea = Text("Instead of explicit rules, computers find patterns.", font_size=36).to_edge(DOWN)
        self.play(FadeIn(key_idea), run_time=1)
        self.wait(2.5)

        self.play(
            FadeOut(trad_group, ml_group, key_idea),
            run_time=1.5
        )
        self.wait(1)

        # 2. Core Understanding: The Learning Process
        process_title = Text("The Learning Process").scale(1).to_edge(UP)
        self.play(Write(process_title), run_time=1.5)
        self.wait(2)

        # Components: Data, Model, Output
        data_text = Text("Data (Input)", color=BLUE).shift(LEFT*4)
        model_text = Text("Model", color=ORANGE)
        output_text = Text("Output (Prediction)", color=RED).shift(RIGHT*4)

        arrow_data_model = Arrow(data_text.get_right(), model_text.get_left())
        arrow_model_output = Arrow(model_text.get_right(), output_text.get_left())

        self.play(
            FadeIn(data_text, model_text, output_text, arrow_data_model, arrow_model_output),
            run_time=1.5
        )
        self.wait(2.5)

        # Add "Learning/Training" as a feedback loop
        feedback_loop_text = Text("Feedback / Adjust Model", color=PURPLE, font_size=30).next_to(arrow_model_output, DOWN, buff=0.5)
        feedback_arrow_simple = CurvedArrow(output_text.get_bottom(), model_text.get_bottom(), angle=-PI/3)

        self.play(
            FadeIn(feedback_loop_text, feedback_arrow_simple),
            run_time=1.5
        )
        self.wait(3)

        self.play(FadeOut(data_text, model_text, output_text, arrow_data_model, arrow_model_output,
                          feedback_loop_text, feedback_arrow_simple, process_title),
                  run_time=1.5)
        self.wait(1)

        # Analogy: Learning to identify categories
        analogy_title = Text("Analogy: Learning to Classify").scale(1).to_edge(UP)
        self.play(Write(analogy_title), run_time=1.5)
        self.wait(2)

        data_label = Text("Training Data:", font_size=36).to_edge(LEFT).shift(UP*1.5)
        self.play(FadeIn(data_label), run_time=1)

        # Represent images as squares/circles with labels
        cat_img1 = Square(side_length=1, color=YELLOW_A, fill_opacity=0.7).shift(LEFT*4 + DOWN*0.5)
        cat_label1 = Text("CAT", font_size=24, color=YELLOW_D).next_to(cat_img1, DOWN, buff=0.1)
        dog_img1 = Circle(radius=0.5, color=BLUE_A, fill_opacity=0.7).shift(LEFT*2 + DOWN*0.5)
        dog_label1 = Text("DOG", font_size=24, color=BLUE_D).next_to(dog_img1, DOWN, buff=0.1)
        cat_img2 = Square(side_length=1, color=YELLOW_B, fill_opacity=0.7).shift(ORIGIN + DOWN*0.5)
        cat_label2 = Text("CAT", font_size=24, color=YELLOW_D).next_to(cat_img2, DOWN, buff=0.1)
        dog_img2 = Circle(radius=0.5, color=BLUE_B, fill_opacity=0.7).shift(RIGHT*2 + DOWN*0.5)
        dog_label2 = Text("DOG", font_size=24, color=BLUE_D).next_to(dog_img2, DOWN, buff=0.1)
        cat_img3 = Square(side_length=1, color=YELLOW_C, fill_opacity=0.7).shift(RIGHT*4 + DOWN*0.5)
        cat_label3 = Text("CAT", font_size=24, color=YELLOW_D).next_to(cat_img3, DOWN, buff=0.1)

        training_data = VGroup(
            VGroup(cat_img1, cat_label1),
            VGroup(dog_img1, dog_label1),
            VGroup(cat_img2, cat_label2),
            VGroup(dog_img2, dog_label2),
            VGroup(cat_img3, cat_label3)
        ).arrange(RIGHT, buff=0.8).move_to(ORIGIN + DOWN*0.5)

        self.play(FadeIn(training_data), run_time=2)
        self.wait(2.5)

        model_learns_text = Text("Model learns patterns and rules.", font_size=36).to_edge(DOWN)
        self.play(FadeIn(model_learns_text), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(training_data, data_label, model_learns_text), run_time=1.5)
        self.wait(1)

        # Show the model as a black box with prediction
        model_box = Rectangle(width=4, height=2, color=ORANGE).move_to(ORIGIN)
        model_text_inside = Text("ML Model", color=WHITE, font_size=36).move_to(model_box.center())
        model_group = VGroup(model_box, model_text_inside)

        self.play(Transform(analogy_title, Text("Prediction with ML Model").scale(1).to_edge(UP)), run_time=1.5)
        self.wait(1)
        self.play(FadeIn(model_group), run_time=1.5)
        self.wait(2)

        # New, unseen data for prediction
        new_data_input = Square(side_length=1, color=YELLOW_D, fill_opacity=0.7).next_to(model_group, LEFT, buff=1.5)
        input_arrow = Arrow(new_data_input.get_right(), model_box.get_left())
        input_label = Text("New Image", font_size=24).next_to(new_data_input, DOWN)

        predicted_output_label = Text("Prediction:", font_size=36).next_to(model_group, RIGHT, buff=1.5).shift(UP*0.5)
        predicted_class_text = Text("CAT", font_size=48, color=GREEN).next_to(predicted_output_label, DOWN, buff=0.2)
        output_arrow = Arrow(model_box.get_right(), predicted_output_label.get_left())

        self.play(FadeIn(new_data_input, input_arrow, input_label), run_time=1)
        self.wait(1.5)
        self.play(FadeIn(predicted_output_label, predicted_class_text, output_arrow), run_time=1.5)
        self.wait(3)

        self.play(FadeOut(new_data_input, input_arrow, input_label, predicted_output_label,
                          predicted_class_text, output_arrow, model_group, analogy_title),
                  run_time=1.5)
        self.wait(1)

        # 3. Examples: Simple Classification (Apples vs Oranges)
        example_title = Text("Example: Classifying Fruits").scale(1).to_edge(UP)
        self.play(Write(example_title), run_time=1.5)
        self.wait(2)

        # Axes for features: Color (Red/Green/Yellow) vs. Roundness
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY, "stroke_width": 2},
        ).to_edge(LEFT, buff=1).shift(DOWN*0.5)
        x_label = Text("Color (Red to Green)", font_size=24).next_to(axes.x_axis, DOWN)
        y_label = Text("Roundness (Low to High)", font_size=24).next_to(axes.y_axis, LEFT)

        self.play(Create(axes), FadeIn(x_label, y_label), run_time=1.5)
        self.wait(2)

        # Data points for apples (red, less round) and oranges (orange, more round)
        apples = VGroup(
            Dot(axes.c2p(2, 3), color=RED),
            Dot(axes.c2p(3, 2), color=RED),
            Dot(axes.c2p(2.5, 2.5), color=RED),
            Dot(axes.c2p(3.5, 3.5), color=RED),
            Dot(axes.c2p(1.8, 2.8), color=RED),
            Dot(axes.c2p(3.2, 2.1), color=RED)
        )
        oranges = VGroup(
            Dot(axes.c2p(7, 8), color=ORANGE),
            Dot(axes.c2p(8, 7), color=ORANGE),
            Dot(axes.c2p(7.5, 7.5), color=ORANGE),
            Dot(axes.c2p(6.8, 8.2), color=ORANGE),
            Dot(axes.c2p(8.2, 6.9), color=ORANGE),
            Dot(axes.c2p(7.1, 8.5), color=ORANGE)
        )

        apple_label = Text("Apples", font_size=30, color=RED).next_to(apples, RIGHT, buff=1).shift(UP*1.5)
        orange_label = Text("Oranges", font_size=30, color=ORANGE).next_to(oranges, RIGHT, buff=1).shift(DOWN*1.5)


        self.play(FadeIn(apples, oranges, apple_label, orange_label), run_time=2)
        self.wait(2.5)

        # Decision boundary
        decision_boundary = Line(axes.c2p(0, 5), axes.c2p(10, 5), color=WHITE, stroke_width=4, stroke_dash_offset=0)
        boundary_text = Text("Decision Boundary", font_size=30).next_to(decision_boundary, UP, buff=0.5)

        self.play(Create(decision_boundary), FadeIn(boundary_text), run_time=1.5)
        self.wait(2.5)

        # New data point prediction
        new_fruit = Dot(axes.c2p(4, 4.5), color=PURPLE)
        new_fruit_label = Text("New Fruit", font_size=24).next_to(new_fruit, UP)
        prediction_question = Text("Is it an Apple or Orange?", font_size=30).to_edge(RIGHT).shift(UP*2)

        self.play(FadeIn(new_fruit, new_fruit_label), run_time=1)
        self.wait(1.5)
        self.play(FadeIn(prediction_question), run_time=1)
        self.wait(1)

        # Show prediction
        predicted_class_text_example = Text("Prediction: APPLE", font_size=36, color=RED).next_to(prediction_question, DOWN)
        self.play(FadeOut(prediction_question), FadeIn(predicted_class_text_example), run_time=1.5)
        self.wait(3)

        self.play(
            FadeOut(
                axes, x_label, y_label, apples, oranges, apple_label, orange_label,
                decision_boundary, boundary_text, new_fruit, new_fruit_label,
                predicted_class_text_example, example_title
            ),
            run_time=1.5
        )
        self.wait(1)

        # 4. Applications: Real-World Impact
        applications_title = Text("Real-World Applications").scale(1).to_edge(UP)
        self.play(Write(applications_title), run_time=1.5)
        self.wait(2)

        app1 = Text("Image Recognition (e.g., face ID)", font_size=36).shift(UP*1)
        app2 = Text("Natural Language Processing (e.g., spam detection)", font_size=36)
        app3 = Text("Recommendation Systems (e.g., Netflix suggestions)", font_size=36).shift(DOWN*1)

        self.play(FadeIn(app1), run_time=1)
        self.wait(2)
        self.play(FadeIn(app2), run_time=1)
        self.wait(2)
        self.play(FadeIn(app3), run_time=1)
        self.wait(2.5)

        final_thought = Text("ML is about 'learning' functions from data, not programming them.", font_size=36).to_edge(DOWN)
        self.play(FadeIn(final_thought), run_time=1.5)
        self.wait(4)

        # End scene
        self.play(FadeOut(*self.mobjects), run_time=2)