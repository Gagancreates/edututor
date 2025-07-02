from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- 1. Introduction (25% duration) ---
        title = Text("Neural Networks").scale(1.5).to_edge(UP)
        self.play(Write(title), run_time=1.0)
        self.wait(2)

        definition1 = Text("A computational model inspired by the human brain.").scale(0.8).next_to(title, DOWN, buff=0.5)
        self.play(Write(definition1), run_time=1.2)
        self.wait(2)

        definition2 = Text("Excellent at pattern recognition and prediction.").scale(0.8).next_to(definition1, DOWN, buff=0.3)
        self.play(Write(definition2), run_time=1.2)
        self.wait(2.5)

        self.play(FadeOut(title, definition1, definition2), run_time=1.0)
        self.wait(1)

        # --- 2. Core Understanding (40% duration) ---
        # Building Blocks: Neurons and Connections
        heading_blocks = Text("Building Blocks: Neurons & Connections").to_edge(UP)
        self.play(FadeIn(heading_blocks), run_time=1.0)
        self.wait(1)

        neuron1 = Circle(radius=0.5, color=BLUE, fill_opacity=0.8).move_to(LEFT * 2)
        neuron_label = Text("Neuron").scale(0.6).next_to(neuron1, DOWN)
        self.play(Create(neuron1), Write(neuron_label), run_time=1.2)
        self.wait(2)

        neuron2 = Circle(radius=0.5, color=BLUE, fill_opacity=0.8).move_to(RIGHT * 2)
        connection_arrow = Arrow(neuron1.get_right(), neuron2.get_left(), buff=0.1, color=WHITE)
        weight_label = Text("Weight").scale(0.6).next_to(connection_arrow, UP)
        self.play(Create(neuron2), Create(connection_arrow), Write(weight_label), run_time=1.2)
        self.wait(2)

        self.play(FadeOut(neuron_label, weight_label), run_time=0.8)
        self.play(Transform(heading_blocks, Text("Neural Network Architecture").to_edge(UP)), run_time=1.0)
        self.wait(1)

        # Build the network structure
        # Input Layer
        input_neurons = VGroup(*[
            Circle(radius=0.4, color=BLUE, fill_opacity=0.8).shift(LEFT * 4 + UP * 1.5),
            Circle(radius=0.4, color=BLUE, fill_opacity=0.8).shift(LEFT * 4 + DOWN * 0),
            Circle(radius=0.4, color=BLUE, fill_opacity=0.8).shift(LEFT * 4 + DOWN * 1.5)
        ])
        input_label = Text("Input Layer").scale(0.6).next_to(input_neurons, DOWN, buff=0.5)
        self.play(Create(input_neurons), Write(input_label), run_time=1.5)
        self.wait(1)

        # Hidden Layer
        hidden_neurons = VGroup(*[
            Circle(radius=0.4, color=GREEN, fill_opacity=0.8).shift(ORIGIN + UP * 2),
            Circle(radius=0.4, color=GREEN, fill_opacity=0.8).shift(ORIGIN + UP * 0.7),
            Circle(radius=0.4, color=GREEN, fill_opacity=0.8).shift(ORIGIN + DOWN * 0.7),
            Circle(radius=0.4, color=GREEN, fill_opacity=0.8).shift(ORIGIN + DOWN * 2)
        ])
        hidden_label = Text("Hidden Layer").scale(0.6).next_to(hidden_neurons, DOWN, buff=0.5)
        self.play(Create(hidden_neurons), Write(hidden_label), run_time=1.5)
        self.wait(1)

        # Output Layer
        output_neurons = VGroup(*[
            Circle(radius=0.4, color=RED, fill_opacity=0.8).shift(RIGHT * 4 + UP * 0.7),
            Circle(radius=0.4, color=RED, fill_opacity=0.8).shift(RIGHT * 4 + DOWN * 0.7)
        ])
        output_label = Text("Output Layer").scale(0.6).next_to(output_neurons, DOWN, buff=0.5)
        self.play(Create(output_neurons), Write(output_label), run_time=1.5)
        self.wait(1)

        # Connections between layers
        connections1 = VGroup()
        for i_neuron in input_neurons:
            for h_neuron in hidden_neurons:
                connections1.add(Line(i_neuron.get_right(), h_neuron.get_left(), color=GRAY, stroke_width=2))
        self.play(Create(connections1), run_time=1.5)
        self.wait(0.5)

        connections2 = VGroup()
        for h_neuron in hidden_neurons:
            for o_neuron in output_neurons:
                connections2.add(Line(h_neuron.get_right(), o_neuron.get_left(), color=GRAY, stroke_width=2))
        self.play(Create(connections2), run_time=1.5)
        self.wait(1.5)

        self.play(Transform(heading_blocks, Text("How Data Flows Through the Network").to_edge(UP)), run_time=1.0)
        self.wait(1)

        # Data Flow Animation
        data_point = Dot(color=YELLOW).move_to(input_neurons[0].get_center())
        self.play(FadeIn(data_point), run_time=0.5)

        # Animate a simple data flow through the network
        self.play(data_point.animate.move_to(input_neurons[1].get_center()), run_time=0.5)
        self.play(data_point.animate.move_to(input_neurons[2].get_center()), run_time=0.5)

        self.play(data_point.animate.move_to(hidden_neurons[0].get_center()), run_time=0.7)
        self.play(data_point.animate.move_to(hidden_neurons[2].get_center()), run_time=0.7)

        self.play(data_point.animate.move_to(output_neurons[0].get_center()), run_time=0.7)
        self.play(data_point.animate.move_to(output_neurons[1].get_center()), run_time=0.7)
        self.play(FadeOut(data_point), run_time=0.5)
        self.wait(1)

        # Mathematical Intuition
        formula_heading = Text("Processing at Each Neuron:").next_to(input_label, DOWN, buff=1.0)
        self.play(Write(formula_heading), run_time=1.0)
        self.wait(1)

        formula1 = MathTex(r"\text{Input values } (x_i)", r"\times", r"\text{ Weights } (w_i)", r"+ \text{ Bias } (b)").scale(0.7).next_to(formula_heading, DOWN, buff=0.4)
        self.play(Write(formula1), run_time=1.5)
        self.wait(2)

        formula2 = MathTex(r"\sum (x_i w_i) + b").scale(0.7).next_to(formula1, DOWN, buff=0.4)
        self.play(ReplacementTransform(formula1, formula2), run_time=1.0)
        self.wait(1.5)

        formula3 = MathTex(r"f(\sum (x_i w_i) + b)", r"\quad \text{(Activation Function)}").scale(0.7).next_to(formula2, DOWN, buff=0.4)
        self.play(ReplacementTransform(formula2, formula3), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(heading_blocks, input_neurons, hidden_neurons, output_neurons,
                                 input_label, hidden_label, output_label,
                                 connections1, connections2, formula_heading, formula3), run_time=1.0)
        self.wait(1)

        # --- 3. Examples (25% duration) ---
        example_heading = Text("Examples: What can they learn?").to_edge(UP)
        self.play(FadeIn(example_heading), run_time=1.0)
        self.wait(1)

        # Example 1: Image Classification
        ex1_title = Text("1. Image Classification").scale(0.9).next_to(example_heading, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(ex1_title), run_time=1.0)
        self.wait(1)

        input_img = Text("Input: Image Pixels").scale(0.7).next_to(ex1_title, DOWN, buff=0.5)
        output_catdog = Text("Output: 'Dog' or 'Cat'").scale(0.7).next_to(input_img, RIGHT, buff=2)
        arrow_ex1 = Arrow(input_img.get_right(), output_catdog.get_left(), buff=0.2, color=YELLOW)

        self.play(Create(input_img), Create(output_catdog), Create(arrow_ex1), run_time=1.5)
        self.wait(2)

        # Example 2: House Price Prediction
        ex2_title = Text("2. House Price Prediction").scale(0.9).next_to(output_catdog, DOWN, buff=1.0).to_edge(LEFT)
        self.play(Write(ex2_title), run_time=1.0)
        self.wait(1)

        input_house = Text("Input: Size, Location, Age").scale(0.7).next_to(ex2_title, DOWN, buff=0.5)
        output_price = Text("Output: House Price").scale(0.7).next_to(input_house, RIGHT, buff=2)
        arrow_ex2 = Arrow(input_house.get_right(), output_price.get_left(), buff=0.2, color=YELLOW)

        self.play(Create(input_house), Create(output_price), Create(arrow_ex2), run_time=1.5)
        self.wait(2)

        training_text = Text("Neural networks learn by adjusting their 'weights' and 'biases'", color=PURPLE).scale(0.7).move_to(DOWN * 3)
        self.play(Write(training_text), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(example_heading, ex1_title, input_img, output_catdog, arrow_ex1,
                                 ex2_title, input_house, output_price, arrow_ex2, training_text), run_time=1.0)
        self.wait(1)

        # --- 4. Applications (10% duration) ---
        applications_heading = Text("Real-World Applications").to_edge(UP)
        self.play(FadeIn(applications_heading), run_time=1.0)
        self.wait(1)

        app_list = VGroup(
            Text("• Image Recognition (e.g., facial recognition)").scale(0.8),
            Text("• Natural Language Processing (e.g., translation, chatbots)").scale(0.8),
            Text("• Self-Driving Cars").scale(0.8),
            Text("• Medical Diagnosis").scale(0.8)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(applications_heading, DOWN, buff=0.8).shift(LEFT*2)

        self.play(FadeIn(app_list[0]), run_time=1.0)
        self.wait(1)
        self.play(FadeIn(app_list[1]), run_time=1.0)
        self.wait(1)
        self.play(FadeIn(app_list[2]), run_time=1.0)
        self.wait(1)
        self.play(FadeIn(app_list[3]), run_time=1.0)
        self.wait(2.5)

        # End Scene
        self.play(FadeOut(*self.mobjects), run_time=1.5)