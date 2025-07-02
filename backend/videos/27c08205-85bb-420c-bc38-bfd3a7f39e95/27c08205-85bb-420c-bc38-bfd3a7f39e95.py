from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- Introduction (25%) ---
        title = Text("The Rich History of Mysuru", font_size=50, color=BLUE).move_to(UP*2.5)
        intro_desc_1 = Text("A city steeped in centuries of heritage,", font_size=30).next_to(title, DOWN, buff=0.8)
        intro_desc_2 = Text("Mysuru's story is a tapestry of powerful dynasties,", font_size=30).next_to(intro_desc_1, DOWN, buff=0.3)
        intro_desc_3 = Text("cultural flourishing, and significant historical events.", font_size=30).next_to(intro_desc_2, DOWN, buff=0.3)

        self.play(Write(title, run_time=1.5))
        self.wait(1)
        self.play(FadeIn(intro_desc_1, run_time=1))
        self.play(FadeIn(intro_desc_2, run_time=1))
        self.play(FadeIn(intro_desc_3, run_time=1))
        self.wait(2)

        # Fade out intro text, keep title for transformation
        self.play(FadeOut(intro_desc_1, intro_desc_2, intro_desc_3, run_time=1.5))
        self.wait(0.5)

        # --- Core Understanding: Ancient Origins & Wodeyars (40%) ---
        origins_title = Text("Ancient Origins: Mahishuru", font_size=45, color=GREEN).move_to(title)
        legend_text = Text("The city's name is derived from 'Mahishuru',", font_size=30).move_to(ORIGIN + LEFT*0.5)
        legend_text_2 = Text("meaning 'Buffalo Town', linked to the legend", font_size=30).next_to(legend_text, DOWN, buff=0.3)
        legend_text_3 = Text("of Mahishasura, a buffalo demon.", font_size=30).next_to(legend_text_2, DOWN, buff=0.3)

        self.play(Transform(title, origins_title, run_time=1.5))
        self.play(Write(legend_text, run_time=1.5))
        self.play(Write(legend_text_2, run_time=1.5))
        self.play(Write(legend_text_3, run_time=1.5))
        self.wait(2)

        self.play(FadeOut(legend_text, legend_text_2, legend_text_3, run_time=1.5))
        self.wait(0.5)

        wodeyar_title = Text("The Wodeyar Dynasty (1399-1761, 1799-1947)", font_size=45, color=ORANGE).move_to(title)
        wodeyar_founder = Text("Founded by Yaduraya in 1399 AD,", font_size=30).move_to(ORIGIN + LEFT*0.5)
        wodeyar_rule_1 = Text("the Wodeyars ruled Mysuru for centuries,", font_size=30).next_to(wodeyar_founder, DOWN, buff=0.3)
        wodeyar_rule_2 = Text("fostering art, architecture, and administration.", font_size=30).next_to(wodeyar_rule_1, DOWN, buff=0.3)
        wodeyar_palace = Text("Their legacy includes the iconic Mysore Palace.", font_size=30).next_to(wodeyar_rule_2, DOWN, buff=0.3)

        self.play(Transform(title, wodeyar_title, run_time=1.5))
        self.play(Write(wodeyar_founder, run_time=1.5))
        self.play(Write(wodeyar_rule_1, run_time=1.5))
        self.play(Write(wodeyar_rule_2, run_time=1.5))
        self.play(Write(wodeyar_palace, run_time=1.5))
        self.wait(2)

        self.play(FadeOut(wodeyar_founder, wodeyar_rule_1, wodeyar_rule_2, wodeyar_palace, run_time=1.5))
        self.wait(0.5)

        # --- Examples: Hyder Ali & Tipu Sultan (25%) ---
        hyder_tipu_title = Text("Hyder Ali and Tipu Sultan (18th Century)", font_size=45, color=RED).move_to(title)
        hyder_ali_text = Text("In the 18th century, power shifted from Wodeyars", font_size=30).move_to(ORIGIN + LEFT*0.5)
        hyder_ali_text_2 = Text("to the military genius, Hyder Ali.", font_size=30).next_to(hyder_ali_text, DOWN, buff=0.3)

        tipu_sultan_text = Text("His son, Tipu Sultan, the 'Tiger of Mysore',", font_size=30).next_to(hyder_ali_text_2, DOWN, buff=0.5)
        tipu_sultan_text_2 = Text("became a formidable opponent to the British.", font_size=30).next_to(tipu_sultan_text, DOWN, buff=0.3)

        anglo_mysore_wars = Text("Their reigns were marked by the Anglo-Mysore Wars,", font_size=30).next_to(tipu_sultan_text_2, DOWN, buff=0.5)
        anglo_mysore_wars_2 = Text("a period of intense conflict and resistance.", font_size=30).next_to(anglo_mysore_wars, DOWN, buff=0.3)

        self.play(Transform(title, hyder_tipu_title, run_time=1.5))
        self.play(Write(hyder_ali_text, run_time=1))
        self.play(Write(hyder_ali_text_2, run_time=1))
        self.wait(1.5)
        self.play(Write(tipu_sultan_text, run_time=1))
        self.play(Write(tipu_sultan_text_2, run_time=1))
        self.wait(1.5)
        self.play(Write(anglo_mysore_wars, run_time=1))
        self.play(Write(anglo_mysore_wars_2, run_time=1))
        self.wait(2)

        self.play(FadeOut(hyder_ali_text, hyder_ali_text_2, tipu_sultan_text, tipu_sultan_text_2, anglo_mysore_wars, anglo_mysore_wars_2, run_time=1.5))
        self.wait(0.5)

        # --- Applications: British Influence & Modern Era (10%) ---
        modern_mysuru_title = Text("British Influence & Modern Mysuru", font_size=45, color=PURPLE).move_to(title)
        srirangapatna_text = Text("After Tipu Sultan's fall in 1799 (Siege of Srirangapatna),", font_size=30).move_to(ORIGIN + LEFT*0.5)
        wodeyar_restoration = Text("the Wodeyar dynasty was restored under British suzerainty.", font_size=30).next_to(srirangapatna_text, DOWN, buff=0.3)

        cultural_hub = Text("Modern Mysuru evolved into a cultural and educational hub,", font_size=30).next_to(wodeyar_restoration, DOWN, buff=0.5)
        cultural_hub_2 = Text("preserving its royal heritage and vibrant traditions.", font_size=30).next_to(cultural_hub, DOWN, buff=0.3)

        self.play(Transform(title, modern_mysuru_title, run_time=1.5))
        self.play(Write(srirangapatna_text, run_time=1.5))
        self.play(Write(wodeyar_restoration, run_time=1.5))
        self.wait(2)
        self.play(Write(cultural_hub, run_time=1.5))
        self.play(Write(cultural_hub_2, run_time=1.5))
        self.wait(2)

        self.play(FadeOut(srirangapatna_text, wodeyar_restoration, cultural_hub, cultural_hub_2, run_time=1.5))
        self.wait(0.5)

        # --- Conclusion ---
        conclusion_text = Text("Mysuru: A Legacy of Grandeur and Resilience", font_size=45, color=YELLOW).move_to(title)
        self.play(Transform(title, conclusion_text, run_time=1.5))
        self.wait(3)

        # Final fade out
        self.play(FadeOut(*self.mobjects, run_time=1.5))