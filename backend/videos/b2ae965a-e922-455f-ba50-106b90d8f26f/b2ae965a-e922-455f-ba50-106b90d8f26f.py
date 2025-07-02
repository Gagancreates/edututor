from manim import *

class CreateScene(Scene):
    def construct(self):
        # 1. Introduction (25%)
        title = Text("Neural Networks Explained", font_size=50).to_edge(UP)
        definition = Text("Computational models inspired by the human brain.", font_size=30).next_to(title, DOWN, buff=0.5)
        importance = Text("Powerful tools for complex pattern recognition and prediction.", font_size=30).next_to(definition, DOWN, buff=0.3)

        self.play(Write(title, run_time=1.5))
        self.wait(2)
        self.play(Write(definition, run_time=1.5))
        self.wait(2)
        self.play(Write(importance, run_time=1.5))
        self.wait(2)

        brain_center = Circle(radius=0.5, color=BLUE_E, fill_opacity=0.7).move_to(ORIGIN)
        brain_lobes = []
        for i in range(5):
            lobe = Circle(radius=0.3, color=BLUE_D, fill_opacity=0.5).move_to(brain_center.get_center() + 1.5 * UP * np.cos(i * 2 * PI / 5) + 1.5 * RIGHT * np.sin(i * 2 * PI / 5))
            brain_lobes.append(lobe)
        brain_group = VGroup(brain_center, *brain_lobes)

        self.play(FadeOut(definition, importance, run_time=1))
        self.wait(0.5)
        self.play(ReplacementTransform(title, Text("How do they work?", font_size=50).to_edge(UP), run_time=1.5))
        self.play(Create(brain_group, run_time=2))
        self.wait(2)
        self.play(FadeOut(brain_group, run_time=1))
        self.wait(0.5)

        # 2. Core Understanding (40%)
        # Neuron
        neuron_text = Text("1. The Neuron", font_size=40, color=YELLOW).to_edge(UP)
        self.play(Write(neuron_text, run_time=1.5))
        self.wait(1.5)

        neuron_circle = Circle(radius=0.8, color=GREEN_B, fill_opacity=0.7).move_to(ORIGIN)
        neuron_label = Text("Neuron", font_size=30).move_to(neuron_circle.get_center())
        self.play(Create(neuron_circle, run_time=1))
        self.play(Write(neuron_label, run_time=1))
        self.wait(2)

        inputs_text = Text("Takes inputs, processes them, produces an output.", font_size=28).next_to(neuron_circle, DOWN, buff=0.7)
        self.play(Write(inputs_text, run_time=1.5))
        self.wait(2)

        # Inputs and Weights
        input1_label = MathTex("x_1", font_size=40).move_to(neuron_circle.get_left() + 2 * LEFT + UP * 0.5)
        input2_label = MathTex("x_2", font_size=40).move_to(neuron_circle.get_left() + 2 * LEFT + DOWN * 0.5)
        input_group = VGroup(input1_label, input2_label)

        arrow1 = Arrow(input1_label.get_right(), neuron_circle.get_left() + UP * 0.2, buff=0.1, color=ORANGE)
        arrow2 = Arrow(input2_label.get_right(), neuron_circle.get_left() + DOWN * 0.2, buff=0.1, color=ORANGE)

        weight1_label = MathTex("w_1", font_size=30).next_to(arrow1, UP, buff=0.1)
        weight2_label = MathTex("w_2", font_size=30).next_to(arrow2, DOWN, buff=0.1)
        weights_group = VGroup(weight1_label, weight2_label)

        self.play(FadeOut(inputs_text, run_time=1))
        self.play(FadeIn(input_group, run_time=1))
        self.play(Create(arrow1, run_time=1), Create(arrow2, run_time=1))
        self.play(Write(weights_group, run_time=1))
        self.wait(2)

        weights_explanation = Text("2. Weights (w): Strength of connections.", font_size=30).to_edge(UP)
        self.play(ReplacementTransform(neuron_text, weights_explanation, run_time=1.5))
        self.wait(2)

        # Bias
        bias_label = MathTex("+ b", font_size=40, color=RED).move_to(neuron_circle.get_center() + DOWN * 0.3)
        self.play(Write(bias_label, run_time=1))
        self.wait(1)

        bias_explanation = Text("3. Bias (b): An offset value.", font_size=30).to_edge(UP)
        self.play(ReplacementTransform(weights_explanation, bias_explanation, run_time=1.5))
        self.wait(2)

        # Summation
        summation_eq_initial = MathTex("z = (x_1 \\cdot w_1) + (x_2 \\cdot w_2) + b", font_size=35).next_to(neuron_circle, DOWN, buff=0.7)
        self.play(Write(summation_eq_initial, run_time=1.5))
        self.wait(2)

        summation_explanation = Text("4. Summation: Weighted sum of inputs plus bias.", font_size=30).to_edge(UP)
        self.play(ReplacementTransform(bias_explanation, summation_explanation, run_time=1.5))
        self.wait(2)

        # Activation Function
        activation_text = Text("5. Activation Function (f): Adds non-linearity.", font_size=30).to_edge(UP)
        self.play(ReplacementTransform(summation_explanation, activation_text, run_time=1.5))
        self.wait(1.5)

        activation_eq = MathTex("a = f(z)", font_size=35).next_to(summation_eq_initial, DOWN, buff=0.5)
        self.play(Write(activation_eq, run_time=1.5))
        self.wait(2)

        output_label = MathTex("a", font_size=40).move_to(neuron_circle.get_right() + 2 * RIGHT)
        arrow_out = Arrow(neuron_circle.get_right(), output_label.get_left(), buff=0.1, color=BLUE_C)
        self.play(Create(arrow_out, run_time=1))
        self.play(Write(output_label, run_time=1))
        self.wait(2)

        # Clear neuron, prepare for layers
        self.play(FadeOut(neuron_circle, neuron_label, input_group, arrow1, arrow2, weights_group, bias_label, arrow_out, output_label, summation_eq_initial, activation_eq, run_time=1.5))
        self.wait(0.5)

        # Layers
        layers_text = Text("6. Layers of Neurons", font_size=40, color=YELLOW).to_edge(UP)
        self.play(ReplacementTransform(activation_text, layers_text, run_time=1.5))
        self.wait(1.5)

        input_layer_nodes = VGroup(*[Circle(radius=0.4, color=GRAY, fill_opacity=0.7).shift(LEFT*5 + UP*y) for y in [-1, 1]])
        input_labels = VGroup(MathTex("x_1", font_size=30).move_to(input_layer_nodes[0]), MathTex("x_2", font_size=30).move_to(input_layer_nodes[1]))
        input_layer_label = Text("Input Layer", font_size=25).next_to(input_layer_nodes, DOWN)

        self.play(Create(input_layer_nodes, run_time=1))
        self.play(Write(input_labels, run_time=0.8), Write(input_layer_label, run_time=0.8))
        self.wait(1.5)

        hidden_layer_nodes = VGroup(*[Circle(radius=0.4, color=PURPLE, fill_opacity=0.7).shift(ORIGIN + UP*y) for y in [-1.5, 0, 1.5]])
        hidden_layer_label = Text("Hidden Layer", font_size=25).next_to(hidden_layer_nodes, DOWN)
        self.play(Create(hidden_layer_nodes, run_time=1))
        self.play(Write(hidden_layer_label, run_time=0.8))
        self.wait(1.5)

        connections_in_hidden = VGroup()
        for input_node in input_layer_nodes:
            for hidden_node in hidden_layer_nodes:
                connections_in_hidden.add(Arrow(input_node.get_right(), hidden_node.get_left(), buff=0.1, color=ORANGE, stroke_width=2))
        self.play(Create(connections_in_hidden, run_time=1.5))
        self.wait(1.5)

        output_layer_node = Circle(radius=0.4, color=GREEN_C, fill_opacity=0.7).shift(RIGHT*5)
        output_label_node = MathTex("y", font_size=30).move_to(output_layer_node)
        output_layer_label = Text("Output Layer", font_size=25).next_to(output_layer_node, DOWN)
        self.play(Create(output_layer_node, run_time=1))
        self.play(Write(output_label_node, run_time=0.8), Write(output_layer_label, run_time=0.8))
        self.wait(1.5)

        connections_hidden_out = VGroup()
        for hidden_node in hidden_layer_nodes:
            connections_hidden_out.add(Arrow(hidden_node.get_right(), output_layer_node.get_left(), buff=0.1, color=ORANGE, stroke_width=2))
        self.play(Create(connections_hidden_out, run_time=1.5))
        self.wait(2)

        network_group = VGroup(input_layer_nodes, input_labels, input_layer_label, hidden_layer_nodes, hidden_layer_label, connections_in_hidden, output_layer_node, output_label_node, output_layer_label, connections_hidden_out)
        self.play(FadeOut(layers_text, run_time=1))
        self.play(network_group.animate.scale(0.8).to_edge(LEFT), run_time=1.5)
        self.wait(0.5)

        # 3. Examples (25%)
        forward_pass_title = Text("Example: The Forward Pass", font_size=40, color=YELLOW).to_edge(UP)
        self.play(Write(forward_pass_title, run_time=1.5))
        self.wait(1.5)

        self.play(FadeOut(network_group, run_time=1))
        self.wait(0.5)

        input_eg_nodes = VGroup(*[Circle(radius=0.4, color=GRAY, fill_opacity=0.7).shift(LEFT*4 + UP*y) for y in [-0.7, 0.7]])
        x1_val_text = MathTex("x_1 = 0.5", font_size=35).move_to(input_eg_nodes[0].get_center())
        x2_val_text = MathTex("x_2 = 0.8", font_size=35).move_to(input_eg_nodes[1].get_center())
        input_eg_labels = VGroup(x1_val_text, x2_val_text)

        hidden_eg_nodes = VGroup(*[Circle(radius=0.4, color=PURPLE, fill_opacity=0.7).shift(ORIGIN + UP*y) for y in [-0.7, 0.7]])
        output_eg_node = Circle(radius=0.4, color=GREEN_C, fill_opacity=0.7).shift(RIGHT*4)

        arrows_ih = VGroup()
        weights_ih = VGroup()
        arrows_ih.add(Arrow(input_eg_nodes[0].get_right(), hidden_eg_nodes[0].get_left(), buff=0.1, color=ORANGE))
        weights_ih.add(MathTex("w_{11}=0.1", font_size=25).next_to(arrows_ih[0], UP * 0.5 + RIGHT * 0.1))
        arrows_ih.add(Arrow(input_eg_nodes[0].get_right(), hidden_eg_nodes[1].get_left(), buff=0.1, color=ORANGE))
        weights_ih.add(MathTex("w_{12}=0.3", font_size=25).next_to(arrows_ih[1], UP * 0.5 + LEFT * 0.1))
        arrows_ih.add(Arrow(input_eg_nodes[1].get_right(), hidden_eg_nodes[0].get_left(), buff=0.1, color=ORANGE))
        weights_ih.add(MathTex("w_{21}=0.2", font_size=25).next_to(arrows_ih[2], DOWN * 0.5 + RIGHT * 0.1))
        arrows_ih.add(Arrow(input_eg_nodes[1].get_right(), hidden_eg_nodes[1].get_left(), buff=0.1, color=ORANGE))
        weights_ih.add(MathTex("w_{22}=0.4", font_size=25).next_to(arrows_ih[3], DOWN * 0.5 + LEFT * 0.1))

        b_h1 = MathTex("b_1 = 0.05", font_size=25).move_to(hidden_eg_nodes[0].get_center() + DOWN*0.2)
        b_h2 = MathTex("b_2 = 0.03", font_size=25).move_to(hidden_eg_nodes[1].get_center() + DOWN*0.2)
        biases_h = VGroup(b_h1, b_h2)

        arrows_ho = VGroup()
        weights_ho = VGroup()
        arrows_ho.add(Arrow(hidden_eg_nodes[0].get_right(), output_eg_node.get_left(), buff=0.1, color=ORANGE))
        weights_ho.add(MathTex("w_{1O}=0.6", font_size=25).next_to(arrows_ho[0], UP * 0.5))
        arrows_ho.add(Arrow(hidden_eg_nodes[1].get_right(), output_eg_node.get_left(), buff=0.1, color=ORANGE))
        weights_ho.add(MathTex("w_{2O}=0.7", font_size=25).next_to(arrows_ho[1], DOWN * 0.5))

        b_out = MathTex("b_O = 0.01", font_size=25).move_to(output_eg_node.get_center() + DOWN*0.2)
        
        example_network_elements = VGroup(input_eg_nodes, input_eg_labels, hidden_eg_nodes, output_eg_node,
                                          arrows_ih, weights_ih, biases_h, arrows_ho, weights_ho, b_out)
        
        self.play(Create(input_eg_nodes, run_time=0.8), Write(input_eg_labels, run_time=0.8))
        self.play(Create(hidden_eg_nodes, run_time=0.8), Create(output_eg_node, run_time=0.8))
        self.play(Create(arrows_ih, run_time=1), Write(weights_ih, run_time=1), Write(biases_h, run_time=1))
        self.play(Create(arrows_ho, run_time=1), Write(weights_ho, run_time=1), Write(b_out, run_time=1))
        self.wait(1.5)

        calc_h1_text = MathTex("z_{h1} = (0.5 \\cdot 0.1) + (0.8 \\cdot 0.2) + 0.05", font_size=30).to_edge(DOWN)
        calc_h1_result = MathTex("z_{h1} = 0.05 + 0.16 + 0.05 = 0.26", font_size=30).to_edge(DOWN)
        self.play(Write(calc_h1_text, run_time=1.5))
        self.wait(1.5)
        self.play(Transform(calc_h1_text, calc_h1_result, run_time=1))
        self.wait(1.5)

        act_h1_text = Text("Apply Activation Function (e.g., Sigmoid)", font_size=25).next_to(calc_h1_result, UP, buff=0.5)
        a_h1_text = MathTex("a_{h1} = \\text{sigmoid}(0.26) \\approx 0.56", font_size=30).next_to(calc_h1_result, UP, buff=0.2)
        self.play(Write(act_h1_text, run_time=1))
        self.play(ReplacementTransform(act_h1_text, a_h1_text, run_time=1))
        self.wait(1.5)
        
        h1_output_label = MathTex("a_{h1} \\approx 0.56", font_size=35).move_to(hidden_eg_nodes[0].get_center())
        self.play(Transform(hidden_eg_nodes[0].copy(), h1_output_label, run_time=1))
        self.wait(0.5)
        self.play(FadeOut(h1_output_label, run_time=0.5))
        self.play(Transform(hidden_eg_nodes[0], hidden_eg_nodes[0].copy().set_color(BLUE_C).move_to(hidden_eg_nodes[0].get_center()), run_time=0.5))

        calc_h2_text = MathTex("z_{h2} = (0.5 \\cdot 0.3) + (0.8 \\cdot 0.4) + 0.03", font_size=30).to_edge(DOWN)
        calc_h2_result = MathTex("z_{h2} = 0.15 + 0.32 + 0.03 = 0.50", font_size=30).to_edge(DOWN)
        self.play(Transform(calc_h1_result, calc_h2_text, run_time=1))
        self.wait(1.5)
        self.play(Transform(calc_h1_result, calc_h2_result, run_time=1))
        self.wait(1.5)

        act_h2_text = MathTex("a_{h2} = \\text{sigmoid}(0.50) \\approx 0.62", font_size=30).next_to(calc_h2_result, UP, buff=0.2)
        self.play(Transform(a_h1_text, act_h2_text, run_time=1))
        self.wait(1.5)
        
        h2_output_label = MathTex("a_{h2} \\approx 0.62", font_size=35).move_to(hidden_eg_nodes[1].get_center())
        self.play(Transform(hidden_eg_nodes[1].copy(), h2_output_label, run_time=1))
        self.wait(0.5)
        self.play(FadeOut(h2_output_label, run_time=0.5))
        self.play(Transform(hidden_eg_nodes[1], hidden_eg_nodes[1].copy().set_color(BLUE_C).move_to(hidden_eg_nodes[1].get_center()), run_time=0.5))
        
        self.wait(1)
        self.play(FadeOut(calc_h1_result, a_h1_text, run_time=1))
        self.wait(0.5)

        calc_out_text = MathTex("z_{out} = (0.56 \\cdot 0.6) + (0.62 \\cdot 0.7) + 0.01", font_size=30).to_edge(DOWN)
        calc_out_result = MathTex("z_{out} = 0.336 + 0.434 + 0.01 = 0.78", font_size=30).to_edge(DOWN)
        self.play(Write(calc_out_text, run_time=1.5))
        self.wait(1.5)
        self.play(Transform(calc_out_text, calc_out_result, run_time=1))
        self.wait(1.5)

        act_out_text = MathTex("y = \\text{sigmoid}(0.78) \\approx 0.69", font_size=30).next_to(calc_out_result, UP, buff=0.2)
        self.play(Write(act_out_text, run_time=1))
        self.wait(1.5)

        final_output_label = MathTex("y \\approx 0.69", font_size=40).move_to(output_eg_node.get_center())
        self.play(Transform(output_eg_node.copy(), final_output_label, run_time=1))
        self.wait(0.5)
        self.play(FadeOut(final_output_label, run_time=0.5))
        self.play(Transform(output_eg_node, output_eg_node.copy().set_color(BLUE_C).move_to(output_eg_node.get_center()), run_time=0.5))

        self.wait(1)
        self.play(FadeOut(forward_pass_title, example_network_elements, calc_out_text, act_out_text, run_time=1.5))
        self.wait(0.5)

        # 4. Applications (10%)
        applications_title = Text("Applications & Learning", font_size=40, color=YELLOW).to_edge(UP)
        self.play(Write(applications_title, run_time=1.5))
        self.wait(1.5)

        app1 = Text("Image Recognition", font_size=30).shift(UP*1.5)
        app2 = Text("Natural Language Processing", font_size=30).next_to(app1, DOWN, buff=0.5)
        app3 = Text("Medical Diagnosis", font_size=30).next_to(app2, DOWN, buff=0.5)
        
        self.play(Write(app1, run_time=1))
        self.play(Write(app2, run_time=1))
        self.play(Write(app3, run_time=1))
        self.wait(2)

        learning_text = Text("Neural networks learn by adjusting weights and biases.", font_size=30).to_edge(DOWN)
        self.play(Write(learning_text, run_time=1.5))
        self.wait(2)

        summary_text = Text("This process allows them to find complex patterns in data.", font_size=30).next_to(learning_text, UP, buff=0.5)
        self.play(Write(summary_text, run_time=1.5))
        self.wait(2)

        self.play(FadeOut(*self.mobjects, run_time=2))