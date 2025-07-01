from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        intro_text = Text("From Polygons to Circles: An Infinite Journey", font_size=48)
        self.play(Write(intro_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(intro_text))

        # Start with a triangle
        triangle = RegularPolygon(n=3, start_angle=PI/2, color=BLUE)
        triangle_text = Text("Triangle (3 sides)", font_size=24)
        triangle_text.next_to(triangle, DOWN)
        self.play(Create(triangle), Write(triangle_text))
        self.wait(1)

        # Transition to a square
        square = RegularPolygon(n=4, start_angle=PI/4, color=GREEN)
        square_text = Text("Square (4 sides)", font_size=24)
        square_text.next_to(square, DOWN)
        self.play(Transform(triangle, square), Transform(triangle_text, square_text))
        self.wait(1)

        # Transition to a pentagon
        pentagon = RegularPolygon(n=5, start_angle=PI/10, color=YELLOW)
        pentagon_text = Text("Pentagon (5 sides)", font_size=24)
        pentagon_text.next_to(pentagon, DOWN)
        self.play(Transform(square, pentagon), Transform(square_text, pentagon_text))
        self.wait(1)

        # Transition to a hexagon
        hexagon = RegularPolygon(n=6, start_angle=0, color=ORANGE)
        hexagon_text = Text("Hexagon (6 sides)", font_size=24)
        hexagon_text.next_to(hexagon, DOWN)
        self.play(Transform(pentagon, hexagon), Transform(pentagon_text, hexagon_text))
        self.wait(1)

        # Increasing the number of sides rapidly
        heptagon = RegularPolygon(n=7, start_angle=PI/14, color=PURPLE)
        octagon = RegularPolygon(n=8, start_angle=PI/8, color=RED)
        nonagon = RegularPolygon(n=9, start_angle=PI/18, color=TEAL)
        decagon = RegularPolygon(n=10, start_angle=PI/20, color=PINK)

        heptagon_text = Text("Heptagon (7 sides)", font_size=24)
        heptagon_text.next_to(heptagon, DOWN)

        octagon_text = Text("Octagon (8 sides)", font_size=24)
        octagon_text.next_to(octagon, DOWN)

        nonagon_text = Text("Nonagon (9 sides)", font_size=24)
        nonagon_text.next_to(nonagon, DOWN)

        decagon_text = Text("Decagon (10 sides)", font_size=24)
        decagon_text.next_to(decagon, DOWN)

        self.play(Transform(hexagon, heptagon), Transform(hexagon_text, heptagon_text))
        self.wait(0.5)
        self.play(Transform(heptagon, octagon), Transform(heptagon_text, octagon_text))
        self.wait(0.5)
        self.play(Transform(octagon, nonagon), Transform(octagon_text, nonagon_text))
        self.wait(0.5)
        self.play(Transform(nonagon, decagon), Transform(nonagon_text, decagon_text))
        self.wait(0.5)

        # Show a polygon with a large number of sides
        n_gon = RegularPolygon(n=50, color=WHITE)
        n_gon_text = Text("50 sides", font_size=24)
        n_gon_text.next_to(n_gon, DOWN)
        self.play(Transform(decagon, n_gon), Transform(decagon_text, n_gon_text))
        self.wait(1)

        # Show an even larger number of sides
        n_gon2 = RegularPolygon(n=100, color=WHITE)
        n_gon_text2 = Text("100 sides", font_size=24)
        n_gon_text2.next_to(n_gon2, DOWN)
        self.play(Transform(n_gon, n_gon2), Transform(n_gon_text, n_gon_text2))
        self.wait(1)

        # Zoom in and show sides becoming smaller
        self.play(
            n_gon2.animate.scale(2).move_to(ORIGIN),
            n_gon_text2.animate.move_to(DOWN * 2),
            run_time=2
        )
        self.wait(1)

        # Focus on a small section of the polygon to show the small straight lines
        focus_box = Square(side_length=1, color=YELLOW, stroke_width=2).move_to(n_gon2.get_vertices()[0]).scale(0.5)
        self.play(Create(focus_box), run_time=1)
        self.wait(0.5)

        zoomed_scene = ZoomedScene(
            zoom_factor=3,
            zoomed_display_height=3,
            zoomed_display_width=3,
            zoomed_display_center=focus_box.get_center(),
            display_frame=False,
            scene_mobject=self
        )
        self.play(zoomed_scene.zoom_in(), run_time=2)
        self.wait(1)

        # Show the straight lines more clearly
        line1 = Line(start=focus_box.get_vertices()[0], end=focus_box.get_vertices()[1], color=RED, stroke_width=4)
        line2 = Line(start=focus_box.get_vertices()[1], end=focus_box.get_vertices()[2], color=RED, stroke_width=4)

        self.play(Create(line1), Create(line2))
        self.wait(1)

        # Transition to Circle
        circle = Circle(color=WHITE)
        circle_text = Text("Circle (Infinite sides)", font_size=36)
        circle_text.next_to(circle, DOWN)

        self.play(zoomed_scene.zoom_out(), FadeOut(focus_box), FadeOut(line1), FadeOut(line2))
        self.wait(1)

        self.play(
            Transform(n_gon2, circle),
            Transform(n_gon_text2, circle_text),
            run_time = 2
        )

        # Equation
        equation = MathTex(r"\lim_{n \to \infty} \text{Regular Polygon}(n) = \text{Circle}", font_size=48)
        equation.move_to(UP * 2)
        self.play(Write(equation))
        self.wait(2)

        # Circumference formula
        circumference_formula = MathTex(r"C = 2\pi r", font_size=48)
        circumference_formula.move_to(DOWN * 2)
        self.play(Write(circumference_formula))
        self.wait(2)

        # Outro
        outro_text = Text("Circles are polygons with infinitely many sides!", font_size=36)
        outro_text.move_to(DOWN * 3.5)
        self.play(Write(outro_text))
        self.wait(3)

        self.play(FadeOut(circle, circle_text, equation, circumference_formula, outro_text))
        self.wait(1)