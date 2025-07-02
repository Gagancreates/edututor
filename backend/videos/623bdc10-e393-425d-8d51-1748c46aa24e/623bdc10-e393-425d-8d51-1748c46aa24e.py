from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- 1. Introduction (25%) ---
        # Title
        title = Text("What is Machine Learning?", font_size=60).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(2)

        # Definition
        definition_line1 = Text("Machine Learning (ML) is about enabling computers", font_size=38).next_to(title, DOWN, buff=0.8)
        definition_line2 = Text("to learn from data without explicit programming.", font_size=38).next_to(definition_line1, DOWN)
        definition_group = VGroup(definition_line1, definition_line2)

        self.play(FadeIn(definition_group, shift=UP), run_time=1.5)
        self.wait(2.5)

        # Analogy intro
        analogy_intro = Text("Think of it like teaching a child.", font_size=36).next_to(definition_group, DOWN, buff=1.0)
        self.play(FadeIn(analogy_intro), run_time=1.0)
        self.wait(2)

        self.play(FadeOut(title, definition_group, analogy_intro), run_time=1.5)
        self.wait(1)

        # --- 2. Core Understanding - The Analogy (Child Learning) (40% Part 1) ---
        analogy_title = Text("Analogy: Teaching a child to identify fruits", font_size=48).to_edge(UP)
        self.play(Write(analogy_title), run_time=1.5)
        self.wait(2)

        # Data (Input)
        data_text = Text("1. Data (Input)", font_size=38, color=BLUE).shift(2.5*LEFT + UP)
        apple_text = Text("Apple", font_size=30).next_to(data_text, DOWN)
        banana_text = Text("Banana", font_size=30).next_to(apple_text, DOWN)
        
        data_box = Rectangle(width=3, height=2, color=BLUE).move_to(VGroup(data_text, apple_text, banana_text))
        
        self.play(FadeIn(data_box), Write(data_text), run_time=1.0)
        self.play(Write(apple_text), Write(banana_text), run_time=1.0)
        self.wait(2)

        # Model (Learning/Child)
        model_text = Text("2. Model (Learning)", font_size=38, color=GREEN).shift(0.5*UP)
        child_brain = Circle(radius=0.8, color=GREEN).next_to(model_text, DOWN, buff=0.5)
        child_brain_text = Text("Child's Brain", font_size=28).move_to(child_brain)
        
        arrow1 = Arrow(data_box.get_right(), child_brain.get_left(), buff=0.1, color=WHITE)

        self.play(FadeIn(model_text), Create(child_brain), FadeIn(child_brain_text), Create(arrow1), run_time=1.5)
        self.wait(2.5)

        # Prediction (Output)
        prediction_text = Text("3. Prediction (Output)", font_size=38, color=RED).shift(2.5*RIGHT + UP)
        new_fruit_text = Text("New Fruit", font_size=30).next_to(prediction_text, DOWN)
        identified_text = Text("Identified!", font_size=30, color=YELLOW).next_to(new_fruit_text, DOWN)
        
        prediction_box = Rectangle(width=3, height=2, color=RED).move_to(VGroup(prediction_text, new_fruit_text, identified_text))

        arrow2 = Arrow(child_brain.get_right(), prediction_box.get_left(), buff=0.1, color=WHITE)

        self.play(FadeIn(prediction_box), Write(prediction_text), run_time=1.0)
        self.play(Write(new_fruit_text), Write(identified_text), Create(arrow2), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(analogy_title, data_box, data_text, apple_text, banana_text, 
                           model_text, child_brain, child_brain_text, prediction_box, 
                           prediction_text, new_fruit_text, identified_text, 
                           arrow1, arrow2), run_time=1.5)
        self.wait(1)

        # --- 3. Core Understanding - Formal Components (40% Part 2) ---
        components_title = Text("The Core Components of Machine Learning", font_size=50).to_edge(UP)
        self.play(Write(components_title), run_time=1.5)
        self.wait(1.5)

        # Component 1: Data
        data_concept = Text("Data (Input)", font_size=40, color=BLUE).shift(3.5*LEFT + 1*UP)
        data_desc = Text("Observations, examples, features.", font_size=32).next_to(data_concept, DOWN)
        data_block = Square(side_length=1.5, color=BLUE, fill_opacity=0.3).next_to(data_desc, DOWN, buff=0.5)
        data_example = Text("Images, Text, Numbers", font_size=25).move_to(data_block)

        self.play(FadeIn(data_concept), FadeIn(data_desc), Create(data_block), FadeIn(data_example), run_time=1.5)
        self.wait(2)

        # Component 2: Model/Algorithm
        model_concept = Text("Model (Algorithm)", font_size=40, color=GREEN).shift(0*LEFT + 1*UP)
        model_desc = Text("A mathematical representation that learns patterns.", font_size=32).next_to(model_concept, DOWN)
        model_block = Circle(radius=0.9, color=GREEN, fill_opacity=0.3).next_to(model_desc, DOWN, buff=0.5)
        model_example = Text("Neural Network", font_size=25).move_to(model_block)

        arrow_data_model = Arrow(data_block.get_right(), model_block.get_left(), buff=0.1)

        self.play(FadeIn(model_concept), FadeIn(model_desc), Create(model_block), FadeIn(model_example), Create(arrow_data_model), run_time=1.5)
        self.wait(2.5)

        # Component 3: Prediction/Output
        prediction_concept = Text("Prediction (Output)", font_size=40, color=RED).shift(3.5*RIGHT + 1*UP)
        prediction_desc = Text("Inference or decision for new data.", font_size=32).next_to(prediction_concept, DOWN)
        prediction_block = Rectangle(width=2, height=1.5, color=RED, fill_opacity=0.3).next_to(prediction_desc, DOWN, buff=0.5)
        prediction_example = Text("Classification,\nRecommendation", font_size=20, line_spacing=0.8).move_to(prediction_block)


        arrow_model_prediction = Arrow(model_block.get_right(), prediction_block.get_left(), buff=0.1)

        self.play(FadeIn(prediction_concept), FadeIn(prediction_desc), Create(prediction_block), FadeIn(prediction_example), Create(arrow_model_prediction), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(components_title, data_concept, data_desc, data_block, data_example,
                           model_concept, model_desc, model_block, model_example,
                           prediction_concept, prediction_desc, prediction_block, prediction_example,
                           arrow_data_model, arrow_model_prediction), run_time=1.5)
        self.wait(1)

        # --- 4. Examples (25%) ---
        examples_title = Text("Common Machine Learning Examples", font_size=50).to_edge(UP)
        self.play(Write(examples_title), run_time=1.5)
        self.wait(1.5)

        # Example 1: Spam Detection
        spam_title = Text("1. Spam Detection", font_size=38, color=BLUE).shift(2*UP + 3.5*LEFT)
        spam_input = Text("Input: Email Text", font_size=30).next_to(spam_title, DOWN)
        spam_output = Text("Output: Spam / Not Spam", font_size=30).next_to(spam_input, DOWN)
        self.play(FadeIn(spam_title, spam_input, spam_output), run_time=1.5)
        self.wait(2)

        # Example 2: Image Recognition
        image_title = Text("2. Image Recognition", font_size=38, color=GREEN).shift(2*UP + 3.5*RIGHT)
        image_input = Text("Input: Image (e.g., Cat)", font_size=30).next_to(image_title, DOWN)
        image_output = Text("Output: Label (e.g., 'Cat')", font_size=30).next_to(image_input, DOWN)
        self.play(FadeIn(image_title, image_input, image_output), run_time=1.5)
        self.wait(2)

        # Example 3: Recommendation Systems
        recomm_title = Text("3. Recommendation Systems", font_size=38, color=RED).shift(1.5*DOWN)
        recomm_input = Text("Input: User History (purchases, views)", font_size=30).next_to(recomm_title, DOWN)
        recomm_output = Text("Output: Recommended Items (movies, products)", font_size=30).next_to(recomm_input, DOWN)
        self.play(FadeIn(recomm_title, recomm_input, recomm_output), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(examples_title, spam_title, spam_input, spam_output,
                           image_title, image_input, image_output,
                           recomm_title, recomm_input, recomm_output), run_time=1.5)
        self.wait(1)

        # --- 5. Applications (10%) ---
        recap_text = Text("In essence, ML enables systems to learn and adapt.", font_size=45).to_edge(UP)
        self.play(Write(recap_text), run_time=1.5)
        self.wait(2)

        applications_title = Text("Real-World Applications:", font_size=40).shift(1*UP)
        app1 = Text("• Self-Driving Cars", font_size=35, color=YELLOW).next_to(applications_title, DOWN, buff=0.5)
        app2 = Text("• Medical Diagnosis", font_size=35, color=YELLOW).next_to(app1, DOWN)
        app3 = Text("• Financial Trading", font_size=35, color=YELLOW).next_to(app2, DOWN)
        
        self.play(FadeIn(applications_title), run_time=1.0)
        self.play(FadeIn(app1, shift=LEFT), run_time=0.8)
        self.play(FadeIn(app2, shift=LEFT), run_time=0.8)
        self.play(FadeIn(app3, shift=LEFT), run_time=0.8)
        self.wait(3)

        # End Scene
        self.play(FadeOut(*self.mobjects), run_time=1.5)