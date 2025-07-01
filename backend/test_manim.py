from manim import *

class CreateScene(Scene):
    def construct(self):
        # Create a simple text
        text = Text("Manim Test")
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))

if __name__ == "__main__":
    print("Manim test script")
    print("This script tests if Manim is properly installed and working") 