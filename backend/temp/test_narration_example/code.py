
from manim import *

class CreateScene(Scene):
    def construct(self):
        # NARRATION: Welcome to this lesson on the quadratic formula. 
        # We'll explore how to solve quadratic equations step by step.
        title = Text("The Quadratic Formula", color=BLUE).scale(1.2)
        self.play(Write(title))
        self.wait(2)
        
        # NARRATION: A quadratic equation has the standard form ax² + bx + c = 0,
        # where a, b, and c are constants and a is not equal to zero.
        equation = MathTex(r"ax^2 + bx + c = 0").scale(1.2)
        self.play(FadeOut(title))
        self.play(Write(equation))
        self.wait(2)
        
        # NARRATION: The quadratic formula gives us the solutions to this equation.
        # The formula is x equals negative b plus or minus the square root of b squared minus 4ac,
        # all divided by 2a.
        formula = MathTex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}").scale(1.2)
        self.play(Transform(equation, formula))
        self.wait(3)
        
        # NARRATION: Let's break down each part of this formula to understand it better.
        self.play(FadeOut(equation))
        self.wait(1)
        
        # NARRATION: First, we start with our quadratic equation in standard form.
        # Let's use a specific example: x² + 5x + 6 = 0
        example = MathTex(r"x^2 + 5x + 6 = 0").scale(1.2)
        self.play(Write(example))
        self.wait(2)
        
        # NARRATION: In this example, a equals 1, b equals 5, and c equals 6.
        values = MathTex(r"a = 1, b = 5, c = 6").scale(1.2).next_to(example, DOWN)
        self.play(Write(values))
        self.wait(2)
        
        # NARRATION: Now we substitute these values into the quadratic formula.
        # x equals negative 5 plus or minus the square root of 5 squared minus 4 times 1 times 6,
        # all divided by 2 times 1.
        substitution = MathTex(r"x = \frac{-5 \pm \sqrt{5^2 - 4 \cdot 1 \cdot 6}}{2 \cdot 1}").scale(1.2)
        self.play(FadeOut(example, values))
        self.play(Write(substitution))
        self.wait(3)
        
        # NARRATION: Let's simplify. 5 squared is 25, and 4 times 1 times 6 is 24.
        # So we have x equals negative 5 plus or minus the square root of 25 minus 24,
        # all divided by 2.
        simplification1 = MathTex(r"x = \frac{-5 \pm \sqrt{25 - 24}}{2}").scale(1.2)
        self.play(Transform(substitution, simplification1))
        self.wait(2)
        
        # NARRATION: Further simplifying, 25 minus 24 equals 1.
        # So we have x equals negative 5 plus or minus the square root of 1,
        # all divided by 2.
        simplification2 = MathTex(r"x = \frac{-5 \pm \sqrt{1}}{2}").scale(1.2)
        self.play(Transform(substitution, simplification2))
        self.wait(2)
        
        # NARRATION: The square root of 1 is 1, so our formula simplifies to
        # x equals negative 5 plus or minus 1, all divided by 2.
        simplification3 = MathTex(r"x = \frac{-5 \pm 1}{2}").scale(1.2)
        self.play(Transform(substitution, simplification3))
        self.wait(2)
        
        # NARRATION: This gives us two solutions:
        # x equals negative 5 plus 1 divided by 2, which is negative 2,
        # or x equals negative 5 minus 1 divided by 2, which is negative 3.
        solutions = MathTex(r"x = -2 \text{ or } x = -3").scale(1.2)
        self.play(Transform(substitution, solutions))
        self.wait(2)
        
        # NARRATION: Let's verify these solutions by substituting them back into the original equation.
        self.play(FadeOut(substitution))
        self.wait(1)
        
        # NARRATION: Thank you for watching this explanation of the quadratic formula.
        # Now you can solve any quadratic equation using this powerful tool.
        conclusion = Text("Quadratic Formula: A Powerful Tool", color=GREEN).scale(1.2)
        self.play(Write(conclusion))
        self.wait(2)
        
        # Clean up
        self.play(FadeOut(*self.mobjects))
