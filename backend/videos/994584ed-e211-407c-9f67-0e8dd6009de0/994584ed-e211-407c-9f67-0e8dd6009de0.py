from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Text("How does the Internet work?", font_size=48)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)

        # User's computer
        computer = Rectangle(width=2, height=1.5, color=BLUE)
        computer_text = Text("Your Computer", font_size=24).move_to(computer.get_center())
        self.play(Create(computer), Write(computer_text), run_time=1)
        self.wait(0.5)

        # Router
        router = Circle(radius=0.7, color=GREEN)
        router_text = Text("Router", font_size=24).move_to(router.get_center())
        self.play(Create(router), Write(router_text), run_time=1)
        self.wait(0.5)

        # Connection line
        line1 = Line(computer.get_right(), router.get_left(), color=WHITE)
        self.play(Create(line1), run_time=1)
        data_packet_text_to_router = Text("Data Packet", font_size=18, color=YELLOW).move_to(line1.get_center()).shift(UP * 0.5)
        self.play(Write(data_packet_text_to_router), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(data_packet_text_to_router), run_time=0.5)

        # Internet cloud
        internet_cloud = Ellipse(width=4, height=2, color=RED)
        internet_cloud_text = Text("Internet", font_size=24).move_to(internet_cloud.get_center())
        self.play(Create(internet_cloud), Write(internet_cloud_text), run_time=1)
        self.wait(0.5)

        # Connection to internet
        line2 = Line(router.get_right(), internet_cloud.get_left(), color=WHITE)
        self.play(Create(line2), run_time=1)
        data_packet_text_to_internet = Text("Data Packet", font_size=18, color=YELLOW).move_to(line2.get_center()).shift(UP * 0.5)
        self.play(Write(data_packet_text_to_internet), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(data_packet_text_to_internet), run_time=0.5)

        # Server
        server = Square(side_length=1.5, color=PURPLE)
        server_text = Text("Server", font_size=24).move_to(server.get_center())
        self.play(Create(server), Write(server_text), run_time=1)
        self.wait(0.5)

        # Connection from internet
        line3 = Line(internet_cloud.get_right(), server.get_left(), color=WHITE)
        self.play(Create(line3), run_time=1)
        data_packet_text_to_server = Text("Data Packet", font_size=18, color=YELLOW).move_to(line3.get_center()).shift(UP * 0.5)
        self.play(Write(data_packet_text_to_server), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(data_packet_text_to_server), run_time=0.5)

        # Explanation
        explanation = Text("You -> Router -> Internet -> Server", font_size=32).to_edge(DOWN)
        self.play(Write(explanation), run_time=2)
        self.wait(2)

        reverse_explanation = Text("Server -> Internet -> Router -> You", font_size=32).to_edge(DOWN)
        self.play(Transform(explanation, reverse_explanation), run_time=2)
        self.wait(2)

        # Fade out
        self.play(FadeOut(*self.mobjects))