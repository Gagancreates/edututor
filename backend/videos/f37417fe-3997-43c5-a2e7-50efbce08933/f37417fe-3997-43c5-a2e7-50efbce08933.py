from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Text("What are Proxy Servers?")
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)

        # Defining the components: User, Proxy Server, Web Server
        user = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)
        user_text = Text("User", font_size=24).next_to(user, DOWN)
        user_group = VGroup(user, user_text).to_edge(LEFT)
        self.play(Create(user_group), run_time=1)
        self.wait(0.5)

        proxy_server = Rectangle(width=1, height=1, color=GREEN, fill_opacity=0.5)
        proxy_server_text = Text("Proxy\nServer", font_size=20).next_to(proxy_server, DOWN)
        proxy_group = VGroup(proxy_server, proxy_server_text).move_to(ORIGIN)
        self.play(Create(proxy_group), run_time=1)
        self.wait(0.5)

        web_server = Square(side_length=1, color=RED, fill_opacity=0.5)
        web_server_text = Text("Web\nServer", font_size=20).next_to(web_server, DOWN)
        web_group = VGroup(web_server, web_server_text).to_edge(RIGHT)
        self.play(Create(web_group), run_time=1)
        self.wait(0.5)

        # Explaining the basic flow without proxy
        no_proxy_text = Text("Without Proxy", font_size=28).to_edge(UP)
        self.play(Write(no_proxy_text), run_time=1)
        self.wait(0.5)

        arrow1 = Arrow(user.get_right(), web_server.get_left(), color=BLUE)
        arrow1_text = Text("Request", font_size=18).move_to(arrow1.get_center() + UP*0.3)
        self.play(Create(arrow1), Write(arrow1_text), run_time=1)
        self.wait(0.5)

        arrow2 = Arrow(web_server.get_left(), user.get_right(), color=RED)
        arrow2_text = Text("Response", font_size=18).move_to(arrow2.get_center() + DOWN*0.3)
        self.play(Create(arrow2), Write(arrow2_text), run_time=1)
        self.wait(1)

        self.play(FadeOut(arrow1, arrow1_text, arrow2, arrow2_text, no_proxy_text), run_time=1)
        self.wait(0.5)

        # Explaining the flow with proxy
        with_proxy_text = Text("With Proxy", font_size=28).to_edge(UP)
        self.play(Write(with_proxy_text), run_time=1)
        self.wait(0.5)

        arrow3 = Arrow(user.get_right(), proxy_server.get_left(), color=BLUE)
        arrow3_text = Text("Request", font_size=18).move_to(arrow3.get_center() + UP*0.3)
        self.play(Create(arrow3), Write(arrow3_text), run_time=1)
        self.wait(0.5)

        arrow4 = Arrow(proxy_server.get_right(), web_server.get_left(), color=GREEN)
        arrow4_text = Text("Request", font_size=18).move_to(arrow4.get_center() + UP*0.3)
        self.play(Create(arrow4), Write(arrow4_text), run_time=1)
        self.wait(0.5)

        arrow5 = Arrow(web_server.get_left(), proxy_server.get_right(), color=RED)
        arrow5_text = Text("Response", font_size=18).move_to(arrow5.get_center() + DOWN*0.3)
        self.play(Create(arrow5), Write(arrow5_text), run_time=1)
        self.wait(0.5)

        arrow6 = Arrow(proxy_server.get_left(), user.get_right(), color=GREEN)
        arrow6_text = Text("Response", font_size=18).move_to(arrow6.get_center() + DOWN*0.3)
        self.play(Create(arrow6), Write(arrow6_text), run_time=1)
        self.wait(1)

        # What a Proxy Server is
        proxy_definition = Text("A proxy server acts as an intermediary between your device and the internet.", font_size=22).to_edge(DOWN)
        self.play(Write(proxy_definition), run_time=2)
        self.wait(2)
        self.play(FadeOut(arrow3, arrow3_text, arrow4, arrow4_text, arrow5, arrow5_text, arrow6, arrow6_text, with_proxy_text, proxy_definition), run_time=1)
        self.wait(0.5)

        # Advantages of Proxy Servers
        advantages_title = Text("Advantages of Proxy Servers", font_size=28).to_edge(UP)
        self.play(Write(advantages_title), run_time=1)
        self.wait(0.5)

        anonymity = Text("Anonymity: Hides your IP address", font_size=22).to_edge(LEFT)
        security = Text("Security: Adds a layer of protection", font_size=22).next_to(anonymity, DOWN, aligned_edge=LEFT)
        content_filtering = Text("Content Filtering: Blocks access to specific sites", font_size=22).next_to(security, DOWN, aligned_edge=LEFT)
        caching = Text("Caching: Improves loading speeds", font_size=22).next_to(content_filtering, DOWN, aligned_edge=LEFT)

        self.play(Write(anonymity), run_time=1)
        self.wait(0.5)
        self.play(Write(security), run_time=1)
        self.wait(0.5)
        self.play(Write(content_filtering), run_time=1)
        self.wait(0.5)
        self.play(Write(caching), run_time=1)
        self.wait(1)

        self.play(FadeOut(advantages_title, anonymity, security, content_filtering, caching), run_time=1)
        self.wait(0.5)

        # Conclusion
        conclusion = Text("Proxy servers provide anonymity, security, and content control.", font_size=24)
        self.play(Write(conclusion), run_time=2)
        self.wait(2)

        self.play(FadeOut(*self.mobjects), run_time=1)