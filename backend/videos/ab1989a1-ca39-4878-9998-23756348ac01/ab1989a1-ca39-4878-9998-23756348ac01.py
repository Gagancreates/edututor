from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Text("What is Machine Learning?", font_size=48)
        self.play(Write(title), run_time=2)
        self.wait(1)

        definition = Text("Machine learning (ML) is a field of study that gives computers the ability to learn without being explicitly programmed.", font_size=24)
        definition.move_to(DOWN)
        self.play(Write(definition), run_time=3)
        self.wait(2)

        self.play(FadeOut(title, definition), run_time=1)

        # Data and Examples
        data_title = Text("Data is Key!", font_size=36)
        self.play(Write(data_title), run_time=1)
        self.wait(1)

        example_image = ImageMobject("example_image.png") #Replace with path to an actual image file!
        example_image.scale(0.5).move_to(LEFT * 3)
        example_label = Text("Images of Cats", font_size=24).next_to(example_image, DOWN)
        
        example_text = Text("Labels: Cat or Not Cat", font_size=24).move_to(RIGHT * 3)
        self.play(FadeIn(example_image, example_label), Write(example_text), run_time=2)
        self.wait(2)

        # Algorithm
        algorithm_title = Text("Learning Algorithm", font_size=36).move_to(UP * 2)
        self.play(ReplacementTransform(data_title, algorithm_title), FadeOut(example_image, example_label, example_text), run_time=1)
        self.wait(1)

        algorithm_box = Rectangle(width=4, height=2).move_to(DOWN)
        algorithm_text = Text("Machine Learning Algorithm", font_size=20).move_to(algorithm_box.get_center())
        self.play(Create(algorithm_box), Write(algorithm_text), run_time=2)
        self.wait(1)

        input_arrow = Arrow(UP, algorithm_box.get_top(), buff=0.1)
        input_text = Text("Input Data", font_size=24).next_to(input_arrow, UP)
        self.play(Create(input_arrow), Write(input_text), run_time=1)

        output_arrow = Arrow(algorithm_box.get_bottom(), DOWN, buff=0.1)
        output_text = Text("Output Prediction", font_size=24).next_to(output_arrow, DOWN)
        self.play(Create(output_arrow), Write(output_text), run_time=1)
        self.wait(2)

        # Examples of ML in use
        self.play(FadeOut(algorithm_title, algorithm_box, algorithm_text, input_arrow, input_text, output_arrow, output_text), run_time=1)

        applications_title = Text("Applications of Machine Learning", font_size=36)
        self.play(Write(applications_title), run_time=1)
        self.wait(1)

        application1 = Text("1. Image Recognition", font_size=24).move_to(UP * 2)
        application2 = Text("2. Natural Language Processing", font_size=24).move_to(UP * 0.5)
        application3 = Text("3. Recommendation Systems", font_size=24).move_to(DOWN * 1)
        application4 = Text("4. Fraud Detection", font_size=24).move_to(DOWN * 2.5)

        self.play(Write(application1), Write(application2), Write(application3), Write(application4), run_time=2)
        self.wait(3)
        
        # Conclusion
        conclusion = Text("Machine learning empowers machines to learn from data and make predictions, impacting numerous aspects of our lives.", font_size=24)
        conclusion.move_to(DOWN * 3)
        self.play(Write(conclusion), run_time=3)
        self.wait(2)

        self.play(FadeOut(applications_title, application1, application2, application3, application4, conclusion), run_time=1)
        final_text = Text("Thank You!", font_size=48)
        self.play(Write(final_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(final_text))
        
        self.play(FadeOut(*self.mobjects), run_time=1)