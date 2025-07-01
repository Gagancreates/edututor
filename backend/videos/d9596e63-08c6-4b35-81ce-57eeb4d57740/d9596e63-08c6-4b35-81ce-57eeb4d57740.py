from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Text("What is Machine Learning?", font_size=48)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # Define Machine Learning
        definition = Tex("Machine Learning: ",
                       "Algorithms that allow computers to learn from data without being explicitly programmed.",
                       font_size=36)
        definition[0].set_color(YELLOW)
        self.play(Transform(title, definition), run_time=1.5)
        self.wait(2)

        # Components of Machine Learning
        components_title = Text("Key Components", font_size=42)
        self.play(Transform(definition, components_title))
        self.wait(1)

        data_text = Text("Data", font_size=36).shift(UP * 2)
        algorithm_text = Text("Algorithm", font_size=36).shift(DOWN * 0)
        model_text = Text("Model", font_size=36).shift(DOWN * 2)

        self.play(Create(data_text), Create(algorithm_text), Create(model_text), run_time=1)
        self.wait(1.5)

        # Explanation of Data
        data_explanation = Tex("Data: Input to the algorithm.", font_size=30)
        data_explanation.move_to(data_text.get_center() + RIGHT * 4)
        self.play(Write(data_explanation), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(data_explanation), run_time=1)

        # Explanation of Algorithm
        algorithm_explanation = Tex("Algorithm: Procedure for learning.", font_size=30)
        algorithm_explanation.move_to(algorithm_text.get_center() + RIGHT * 4)
        self.play(Write(algorithm_explanation), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(algorithm_explanation), run_time=1)

        # Explanation of Model
        model_explanation = Tex("Model: Output of the learning process.", font_size=30)
        model_explanation.move_to(model_text.get_center() + RIGHT * 4)
        self.play(Write(model_explanation), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(model_explanation), run_time=1)

        self.play(FadeOut(components_title))

        # Types of Machine Learning
        types_title = Text("Types of Machine Learning", font_size=42)
        self.play(Transform(data_text, types_title))
        self.play(FadeOut(algorithm_text), FadeOut(model_text))
        self.wait(1)

        supervised_text = Text("Supervised Learning", font_size=36).shift(UP * 1.5)
        unsupervised_text = Text("Unsupervised Learning", font_size=36).shift(DOWN * 0)
        reinforcement_text = Text("Reinforcement Learning", font_size=36).shift(DOWN * 1.5)

        self.play(ReplacementTransform(data_text, supervised_text), Create(unsupervised_text), Create(reinforcement_text), run_time=1.5)
        self.wait(1.5)

        # Supervised Learning
        supervised_explanation = Tex("Supervised: Labeled data.", font_size=30)
        supervised_explanation.move_to(supervised_text.get_center() + RIGHT * 4)
        self.play(Write(supervised_explanation), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(supervised_explanation), run_time=1)

        # Unsupervised Learning
        unsupervised_explanation = Tex("Unsupervised: Unlabeled data.", font_size=30)
        unsupervised_explanation.move_to(unsupervised_text.get_center() + RIGHT * 4)
        self.play(Write(unsupervised_explanation), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(unsupervised_explanation), run_time=1)

        # Reinforcement Learning
        reinforcement_explanation = Tex("Reinforcement: Learning through trial and error.", font_size=30)
        reinforcement_explanation.move_to(reinforcement_text.get_center() + RIGHT * 4)
        self.play(Write(reinforcement_explanation), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(reinforcement_explanation), run_time=1)

        # Applications
        applications_title = Text("Applications", font_size=42)
        self.play(Transform(supervised_text, applications_title))
        self.play(FadeOut(unsupervised_text), FadeOut(reinforcement_text))
        self.wait(1)

        app1 = Text("Image Recognition", font_size=30).shift(UP * 1.5)
        app2 = Text("Natural Language Processing", font_size=30).shift(DOWN * 0)
        app3 = Text("Recommendation Systems", font_size=30).shift(DOWN * 1.5)

        self.play(ReplacementTransform(supervised_text, app1), Create(app2), Create(app3), run_time=1.5)
        self.wait(2)

        # Conclusion
        conclusion = Text("Machine Learning is powerful!", font_size=48)
        self.play(Transform(app1, conclusion))
        self.play(FadeOut(app2), FadeOut(app3))
        self.wait(2)

        self.play(FadeOut(*self.mobjects), run_time=1)