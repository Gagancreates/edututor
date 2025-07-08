
from manim import *

class CircleExample(Scene):
    def construct(self):
        # NARRATION: Welcome to this demonstration of circle properties.
        title = Title("Circle Properties")
        self.play(Write(title))
        self.wait(1)
        
        # NARRATION: Let's start by creating a circle with radius 2.
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        self.wait(1)
        
        # NARRATION: The center of a circle is the point from which all points on the circle are equidistant.
        center_dot = Dot(ORIGIN, color=RED)
        self.play(FadeIn(center_dot))
        self.wait(1)
        
        # NARRATION: The radius is the distance from the center to any point on the circle.
        radius = Line(ORIGIN, circle.point_at_angle(45 * DEGREES), color=YELLOW)
        radius_label = Text("r", font_size=24).next_to(radius.get_center(), UP)
        self.play(Create(radius), Write(radius_label))
        self.wait(1.5)
        
        # NARRATION: The diameter is twice the radius and passes through the center.
        diameter = Line(circle.point_at_angle(225 * DEGREES), circle.point_at_angle(45 * DEGREES), color=GREEN)
        diameter_label = Text("d = 2r", font_size=24).next_to(diameter.get_center(), DOWN)
        self.play(Create(diameter), Write(diameter_label))
        self.wait(1.5)
        
        # NARRATION: The circumference of a circle equals pi times the diameter.
        circumference_formula = MathTex("C = \pi \times d").scale(1.5)
        self.play(
            FadeOut(title),
            FadeOut(radius_label),
            FadeOut(diameter_label),
            Transform(circle, circumference_formula)
        )
        self.wait(1.5)
        
        # NARRATION: The area of a circle equals pi times the radius squared.
        area_formula = MathTex("A = \pi \times r^2").scale(1.5)
        self.play(Transform(circle, area_formula))
        self.wait(1.5)
        
        # NARRATION: Understanding these properties is fundamental to mathematics.
        final_text = Text("Circles are fundamental shapes", font_size=36)
        self.play(Transform(circle, final_text))
        self.wait(2)
