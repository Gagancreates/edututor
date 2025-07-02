from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- 1. Introduction (25%) ---
        title = Text("Laplace Transforms", font_size=72).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(2)

        intro_text1 = Text("A powerful tool to solve differential equations", font_size=36)
        intro_text2 = Text("Transforms problems from Time Domain (t) to s-Domain (s)", font_size=36)
        intro_text3 = Text("Simplifies calculus into algebra!", font_size=36)

        intro_text1.next_to(title, DOWN, buff=1.0)
        self.play(Write(intro_text1), run_time=1.5)
        self.wait(1.5)

        intro_text2.next_to(intro_text1, DOWN, buff=0.5)
        self.play(Write(intro_text2), run_time=1.5)
        self.wait(1.5)

        intro_text3.next_to(intro_text2, DOWN, buff=0.5)
        self.play(Write(intro_text3), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(intro_text1, intro_text2, intro_text3), run_time=1.0)

        # --- 2. Core Understanding (40%) ---
        definition_label = Text("The Definition:", font_size=48).move_to(LEFT * 4 + UP * 2)
        self.play(Write(definition_label), run_time=1.0)
        self.wait(1)

        laplace_def = MathTex(
            r"\mathcal{L}\{f(t)\}",
            r"=",
            r"\int_{0}^{\infty} e^{-st} f(t) \,dt",
            r"=",
            r"F(s)",
            font_size=60
        ).next_to(definition_label, DOWN, buff=0.7).set_color_by_tex_to_color_map({
            r"\mathcal{L}\{f(t)\}": YELLOW,
            r"e^{-st}": BLUE,
            r"f(t)": GREEN,
            r"F(s)": RED
        })

        self.play(Write(laplace_def[0]), run_time=1.0) # L{f(t)}
        self.wait(0.5)
        self.play(Write(laplace_def[1]), run_time=0.5) # =
        self.wait(0.5)
        self.play(Write(laplace_def[2]), run_time=1.5) # integral part
        self.wait(0.5)
        self.play(Write(laplace_def[3]), run_time=0.5) # =
        self.wait(0.5)
        self.play(Write(laplace_def[4]), run_time=1.0) # F(s)
        self.wait(2)

        ft_text = Text("f(t): Function in Time Domain", font_size=32).next_to(laplace_def, DOWN, buff=0.5).to_edge(LEFT)
        Fs_text = Text("F(s): Function in s-Domain", font_size=32).next_to(ft_text, RIGHT, buff=1.0)
        kernel_text = Text("e^(-st): The Kernel (weighting function)", font_size=32).next_to(ft_text, DOWN, buff=0.5).to_edge(LEFT)

        ft_text.set_color(GREEN)
        Fs_text.set_color(RED)
        kernel_text.set_color(BLUE)

        self.play(Write(ft_text), run_time=1.0)
        self.play(Write(Fs_text), run_time=1.0)
        self.play(Write(kernel_text), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(definition_label, laplace_def, ft_text, Fs_text, kernel_text), run_time=1.0)

        # Analogy
        analogy_title = Text("Think of it as a dictionary:", font_size=48).to_edge(UP)
        self.play(Write(analogy_title), run_time=1.0)
        self.wait(1)

        time_domain_word = Text("Difficult Time Domain (t) words", font_size=36, color=GREEN).next_to(analogy_title, DOWN, buff=1.0).to_edge(LEFT)
        s_domain_word = Text("Easier s-Domain (s) words", font_size=36, color=RED).next_to(time_domain_word, RIGHT, buff=2.0)

        dictionary_icon = Tex(r"$\mathcal{L}$", font_size=90, color=YELLOW).move_to(ORIGIN)
        arrow_to_s = Arrow(time_domain_word.get_right(), dictionary_icon.get_left(), buff=0.1)
        arrow_from_s = Arrow(dictionary_icon.get_right(), s_domain_word.get_left(), buff=0.1)

        self.play(Write(time_domain_word), run_time=1.0)
        self.wait(0.5)
        self.play(Write(s_domain_word), run_time=1.0)
        self.wait(0.5)
        self.play(Create(dictionary_icon), run_time=1.0)
        self.play(GrowArrow(arrow_to_s), GrowArrow(arrow_from_s), run_time=1.0)
        self.wait(2.5)

        self.play(
            FadeOut(analogy_title, time_domain_word, s_domain_word,
                    dictionary_icon, arrow_to_s, arrow_from_s),
            run_time=1.0
        )

        # --- 3. Examples and Properties (25%) ---
        examples_title = Text("Common Laplace Transforms & Properties", font_size=54).to_edge(UP)
        self.play(Write(examples_title), run_time=1.5)
        self.wait(1)

        ex1_label = Text("Example 1:", font_size=36).next_to(examples_title, DOWN, buff=0.8).to_edge(LEFT)
        ex1_math = MathTex(r"\mathcal{L}\{1\} = \frac{1}{s}", font_size=50).next_to(ex1_label, RIGHT, buff=0.5)
        self.play(Write(ex1_label), run_time=0.8)
        self.play(Write(ex1_math), run_time=1.2)
        self.wait(1.5)

        ex2_label = Text("Example 2:", font_size=36).next_to(ex1_label, DOWN, buff=0.5)
        ex2_math = MathTex(r"\mathcal{L}\{e^{at}\} = \frac{1}{s-a}", font_size=50).next_to(ex2_label, RIGHT, buff=0.5)
        self.play(Write(ex2_label), run_time=0.8)
        self.play(Write(ex2_math), run_time=1.2)
        self.wait(1.5)

        prop_linearity_label = Text("Property: Linearity", font_size=36).next_to(ex2_label, DOWN, buff=0.7).to_edge(LEFT)
        prop_linearity_math = MathTex(r"\mathcal{L}\{af(t) + bg(t)\} = aF(s) + bG(s)", font_size=45).next_to(prop_linearity_label, RIGHT, buff=0.5)
        self.play(Write(prop_linearity_label), run_time=0.8)
        self.play(Write(prop_linearity_math), run_time=1.5)
        self.wait(2)

        prop_derivative_label = Text("Property: Derivative", font_size=36).next_to(prop_linearity_label, DOWN, buff=0.7).to_edge(LEFT)
        prop_derivative_math = MathTex(r"\mathcal{L}\{f'(t)\} = sF(s) - f(0)", font_size=45).next_to(prop_derivative_label, RIGHT, buff=0.5)
        self.play(Write(prop_derivative_label), run_time=0.8)
        self.play(Write(prop_derivative_math), run_time=1.5)
        self.wait(2.5)

        self.play(
            FadeOut(examples_title, ex1_label, ex1_math, ex2_label, ex2_math,
                    prop_linearity_label, prop_linearity_math,
                    prop_derivative_label, prop_derivative_math),
            run_time=1.0
        )

        # --- 4. Applications (10%) ---
        applications_title = Text("Key Applications", font_size=54).to_edge(UP)
        self.play(Write(applications_title), run_time=1.5)
        self.wait(1)

        app1 = Text("1. Solving Ordinary Differential Equations (ODEs)", font_size=36).next_to(applications_title, DOWN, buff=0.8).to_edge(LEFT)
        app2 = Text("2. Circuit Analysis (R, L, C circuits)", font_size=36).next_to(app1, DOWN, buff=0.5).to_edge(LEFT)
        app3 = Text("3. Control Systems and Signal Processing", font_size=36).next_to(app2, DOWN, buff=0.5).to_edge(LEFT)

        self.play(Write(app1), run_time=1.2)
        self.wait(1.5)
        self.play(Write(app2), run_time=1.2)
        self.wait(1.5)
        self.play(Write(app3), run_time=1.2)
        self.wait(2)

        # Final Fade Out
        self.play(FadeOut(*self.mobjects), run_time=1.5)

# To render this scene, save it as a Python file (e.g., laplace_transform.py)
# and run from your terminal:
# manim -pql laplace_transform.py CreateScene
# or manim -pqm laplace_transform.py CreateScene for medium quality.