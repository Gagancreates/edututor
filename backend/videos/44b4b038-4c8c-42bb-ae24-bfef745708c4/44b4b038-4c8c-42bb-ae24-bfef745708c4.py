from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Text("Neural Networks: A Basic Introduction", color=BLUE).scale(0.8)
        self.play(Write(title), run_time=2)
        self.wait(2)

        definition = Text("Loosely inspired by the human brain, neural networks are a set of algorithms designed to recognize patterns.", color=GREEN).scale(0.5)
        definition.next_to(title, DOWN, buff=0.5)
        self.play(Write(definition), run_time=3)
        self.wait(2)

        connection = Text("Think of it like a complex function trying to fit data.", color=YELLOW).scale(0.5)
        connection.next_to(definition, DOWN, buff=0.5)
        self.play(Write(connection), run_time=2)
        self.wait(2)

        self.play(FadeOut(title, definition, connection))
        self.wait()

        # Core Understanding
        neuron_label = Text("Neuron (Node)", color=BLUE).scale(0.6)
        self.play(Write(neuron_label), run_time=1)
        self.wait(1)

        circle = Circle(radius=0.7, color=BLUE)
        self.play(Create(circle), run_time=1)
        self.wait(1)

        inputs_label = Text("Inputs (x1, x2, ...)", color=GREEN).scale(0.5).to_edge(LEFT)
        self.play(Write(inputs_label), run_time=1)
        self.wait(0.5)

        arrow1 = Arrow(inputs_label.get_right() + RIGHT*0.5, circle.get_left())
        arrow2 = Arrow(inputs_label.get_right() + RIGHT*2.5, circle.get_left())
        self.play(Create(arrow1), Create(arrow2), run_time=1)
        self.wait(1)

        weights_label = Text("Weights (w1, w2, ...)", color=YELLOW).scale(0.5).to_edge(UP)
        self.play(Write(weights_label), run_time=1)
        self.wait(0.5)

        text1 = MathTex("x_1", color=GREEN).next_to(arrow1, LEFT)
        text2 = MathTex("x_2", color=GREEN).next_to(arrow2, LEFT)
        text3 = MathTex("w_1", color=YELLOW).next_to(arrow1, UP*0.5)
        text4 = MathTex("w_2", color=YELLOW).next_to(arrow2, UP*0.5)
        self.play(Write(text1), Write(text2), Write(text3), Write(text4), run_time=1)
        self.wait(1)

        summation = MathTex("\sum (x_i * w_i)", color=PURPLE).next_to(circle, RIGHT)
        self.play(Write(summation), run_time=2)
        self.wait(1)

        activation = Text("Activation Function (e.g., ReLU, Sigmoid)", color=ORANGE).scale(0.5).next_to(summation, DOWN)
        self.play(Write(activation), run_time=2)
        self.wait(1)

        output_label = Text("Output", color=RED).scale(0.6).to_edge(RIGHT)
        arrow3 = Arrow(circle.get_right(), output_label.get_left() + LEFT*0.5)
        self.play(Create(arrow3), Write(output_label), run_time=1)
        self.wait(2)

        self.play(FadeOut(neuron_label, circle, inputs_label, arrow1, arrow2, weights_label, text1, text2, text3, text4, summation, activation, arrow3, output_label))
        self.wait()

        # Example Network
        network_label = Text("Simple Neural Network", color=BLUE).scale(0.7)
        self.play(Write(network_label), run_time=1)
        self.wait(1)

        layer1 = VGroup(*[Circle(radius=0.3, color=BLUE) for _ in range(3)])
        layer2 = VGroup(*[Circle(radius=0.3, color=BLUE) for _ in range(2)])
        layer3 = Circle(radius=0.3, color=BLUE)

        layer1.arrange(DOWN).to_edge(LEFT)
        layer2.arrange(DOWN).move_to(ORIGIN)
        layer3.to_edge(RIGHT)

        self.play(Create(layer1), Create(layer2), Create(layer3), run_time=1.5)
        self.wait(1)

        for i in range(3):
            for j in range(2):
                line = Line(layer1[i].get_right(), layer2[j].get_left(), color=GREY)
                self.play(Create(line), run_time=0.5)
        self.wait(1)
        for j in range(2):
            line = Line(layer2[j].get_right(), layer3.get_left(), color=GREY)
            self.play(Create(line), run_time=0.5)
        self.wait(1)

        input_label = Text("Input Layer", color=GREEN).scale(0.4).next_to(layer1, LEFT)
        hidden_label = Text("Hidden Layer", color=YELLOW).scale(0.4).next_to(layer2, UP)
        output_label = Text("Output Layer", color=RED).scale(0.4).next_to(layer3, RIGHT)

        self.play(Write(input_label), Write(hidden_label), Write(output_label), run_time=1)
        self.wait(2)

        self.play(FadeOut(network_label, layer1, layer2, layer3, input_label, hidden_label, output_label))
        self.wait()

        # Applications
        applications_label = Text("Applications", color=BLUE).scale(0.8)
        self.play(Write(applications_label), run_time=1)
        self.wait(1)

        application1 = Text("Image Recognition", color=GREEN).scale(0.5).to_edge(UP)
        application2 = Text("Natural Language Processing", color=YELLOW).scale(0.5).next_to(application1, DOWN, buff=0.5)
        application3 = Text("Recommendation Systems", color=RED).scale(0.5).next_to(application2, DOWN, buff=0.5)

        self.play(Write(application1), run_time=1)
        self.play(Write(application2), run_time=1)
        self.play(Write(application3), run_time=1)
        self.wait(2)

        self.play(FadeOut(applications_label, application1, application2, application3))
        self.wait()

        self.play(FadeOut(*self.mobjects))