
from manim import *

class CreateScene(Scene):
    def construct(self):
        # Create a title with potential Unicode characters
        title = Text("Neural Networks Explained", font_size=48)
        title.to_edge(UP)
        
        # Create some complex mathematical equations with symbols
        eq1 = MathTex(r"f(x) = \frac{1}{1 + e^{-x}}")
        eq2 = MathTex(r"\nabla_{\theta} J(\theta) = \frac{1}{m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)}) x^{(i)}")
        
        # Create a neural network diagram
        network = VGroup()
        layers = [3, 4, 4, 2]  # Number of neurons in each layer
        
        # Create neurons for each layer
        neurons = []
        for i, layer_size in enumerate(layers):
            layer_neurons = VGroup()
            for j in range(layer_size):
                neuron = Circle(radius=0.2, color=BLUE)
                neuron.move_to([i*2, (j - (layer_size-1)/2)*0.8, 0])
                layer_neurons.add(neuron)
            neurons.append(layer_neurons)
            network.add(layer_neurons)
        
        # Create connections between neurons
        connections = VGroup()
        for i in range(len(layers)-1):
            for neuron1 in neurons[i]:
                for neuron2 in neurons[i+1]:
                    connection = Line(neuron1.get_center(), neuron2.get_center(), stroke_width=1)
                    connections.add(connection)
        network.add(connections)
        
        # Animation sequence
        self.play(Write(title))
        self.wait(1)
        
        self.play(Create(network))
        self.wait(2)
        
        self.play(network.animate.shift(DOWN*2))
        self.wait(1)
        
        self.play(Write(eq1))
        self.wait(2)
        
        self.play(ReplacementTransform(eq1, eq2))
        self.wait(2)
        
        self.play(FadeOut(network), FadeOut(eq2), FadeOut(title))
        self.wait(1)
