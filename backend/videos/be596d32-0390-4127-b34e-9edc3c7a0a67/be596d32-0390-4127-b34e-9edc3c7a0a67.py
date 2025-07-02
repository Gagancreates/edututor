from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- Section 1: Introduction ---

        title = Text("What are Proxy Servers?").scale(1.2).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(2)

        definition = Text("A Proxy Server acts as an intermediary", font_size=36).next_to(title, DOWN, buff=0.8)
        definition_line2 = Text("between a client and another server.", font_size=36).next_to(definition, DOWN, buff=0.2)
        self.play(Write(definition), run_time=1)
        self.play(Write(definition_line2), run_time=1)
        self.wait(2.5)

        user_text = Text("You (Client)", font_size=30).move_to(LEFT * 4 + DOWN * 0.5)
        user_box = Rectangle(width=2, height=1.5, color=BLUE).move_to(user_text)
        user_group = VGroup(user_box, user_text)

        proxy_text = Text("Proxy Server", font_size=30).move_to(ORIGIN + DOWN * 0.5)
        proxy_box = Rectangle(width=2, height=1.5, color=YELLOW).move_to(proxy_text)
        proxy_group = VGroup(proxy_box, proxy_text)

        internet_text = Text("Internet (Server)", font_size=30).move_to(RIGHT * 4 + DOWN * 0.5)
        internet_box = Rectangle(width=2, height=1.5, color=GREEN).move_to(internet_text)
        internet_group = VGroup(internet_box, internet_text)

        arrow1 = Arrow(user_box.get_right(), proxy_box.get_left(), buff=0.1, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.2)
        arrow2 = Arrow(proxy_box.get_right(), internet_box.get_left(), buff=0.1, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.2)

        self.play(FadeIn(user_group), FadeIn(internet_group), run_time=1)
        self.wait(1)
        self.play(Create(arrow1), FadeIn(proxy_group), run_time=1)
        self.wait(1)
        self.play(Create(arrow2), run_time=1)
        self.wait(2.5)

        benefits_text = Text("Key Benefits:", font_size=36).next_to(definition_line2, DOWN, buff=1.0).to_edge(LEFT, buff=1.0)
        benefit1 = Text("• Privacy (hide IP address)", font_size=32).next_to(benefits_text, DOWN, buff=0.4).to_edge(LEFT, buff=1.5)
        benefit2 = Text("• Security (filter malicious content)", font_size=32).next_to(benefit1, DOWN, buff=0.2).to_edge(LEFT, buff=1.5)
        benefit3 = Text("• Speed (caching)", font_size=32).next_to(benefit2, DOWN, buff=0.2).to_edge(LEFT, buff=1.5)

        self.play(Write(benefits_text), run_time=0.8)
        self.play(Write(benefit1), run_time=1)
        self.play(Write(benefit2), run_time=1)
        self.play(Write(benefit3), run_time=1)
        self.wait(3)

        self.play(FadeOut(user_group, proxy_group, internet_group, arrow1, arrow2, benefits_text, benefit1, benefit2, benefit3, definition, definition_line2), run_time=1.5)
        self.wait(0.5)

        # --- Section 2: Core Understanding ---

        core_title = Text("How They Work: The Flow", font_size=48).to_edge(UP)
        self.play(Transform(title, core_title), run_time=1)
        self.wait(2)

        client_rect = Rectangle(width=2.5, height=2, color=BLUE).move_to(LEFT * 4.5)
        client_label = Text("Client Device", font_size=30).move_to(client_rect.get_top() + DOWN*0.4)
        client_ip = Text("IP: 192.168.1.100", font_size=28).next_to(client_label, DOWN, buff=0.1)
        client_obj = VGroup(client_rect, client_label, client_ip)

        proxy_rect = Rectangle(width=2.5, height=2, color=YELLOW).move_to(ORIGIN)
        proxy_label = Text("Proxy Server", font_size=30).move_to(proxy_rect.get_top() + DOWN*0.4)
        proxy_ip = Text("IP: 203.0.113.50", font_size=28).next_to(proxy_label, DOWN, buff=0.1)
        proxy_obj = VGroup(proxy_rect, proxy_label, proxy_ip)

        dest_rect = Rectangle(width=2.5, height=2, color=GREEN).move_to(RIGHT * 4.5)
        dest_label = Text("Destination Server", font_size=30).move_to(dest_rect.get_top() + DOWN*0.4)
        dest_ip = Text("IP: 93.184.216.34", font_size=28).next_to(dest_label, DOWN, buff=0.1)
        dest_obj = VGroup(dest_rect, dest_label, dest_ip)

        self.play(FadeIn(client_obj), FadeIn(proxy_obj), FadeIn(dest_obj), run_time=1.5)
        self.wait(2)

        request_arrow1 = Arrow(client_rect.get_right(), proxy_rect.get_left(), buff=0.1, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.2, color=RED)
        request_text1 = Text("Request (my IP)", font_size=28).next_to(request_arrow1, UP, buff=0.1)
        self.play(Create(request_arrow1), Write(request_text1), run_time=1)
        self.wait(1.5)

        temp_client_ip = client_ip.copy().next_to(proxy_ip, UP, buff=0.5)
        self.play(
            ReplacementTransform(client_ip.copy(), temp_client_ip),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            FadeOut(temp_client_ip),
            FadeIn(proxy_ip.copy().next_to(proxy_ip, UP, buff=0.5)), # Showing the proxy IP is used
            run_time=1
        )
        self.wait(1)
        self.play(FadeOut(self.mobjects[-1]), run_time=0.5) # Fade out the temporary proxy IP

        request_arrow2 = Arrow(proxy_rect.get_right(), dest_rect.get_left(), buff=0.1, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.2, color=RED)
        request_text2 = Text("Request (proxy's IP)", font_size=28).next_to(request_arrow2, UP, buff=0.1)
        self.play(Create(request_arrow2), Write(request_text2), run_time=1)
        self.wait(2.5)

        response_arrow1 = Arrow(dest_rect.get_left(), proxy_rect.get_right(), buff=0.1, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.2, color=GREEN)
        response_text1 = Text("Response", font_size=28).next_to(response_arrow1, DOWN, buff=0.1)
        self.play(Create(response_arrow1), Write(response_text1), run_time=1)
        self.wait(1.5)

        response_arrow2 = Arrow(proxy_rect.get_left(), client_rect.get_right(), buff=0.1, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.2, color=GREEN)
        response_text2 = Text("Response", font_size=28).next_to(response_arrow2, DOWN, buff=0.1)
        self.play(Create(response_arrow2), Write(response_text2), run_time=1)
        self.wait(3)

        self.play(FadeOut(client_obj, proxy_obj, dest_obj, request_arrow1, request_text1, request_arrow2, request_text2, response_arrow1, response_text1, response_arrow2, response_text2), run_time=1.5)
        self.wait(0.5)

        # --- Section 3: Examples / Types ---

        examples_title = Text("Types of Proxies", font_size=48).to_edge(UP)
        self.play(Transform(title, examples_title), run_time=1)
        self.wait(2)

        forward_title = Text("1. Forward Proxy", font_size=40).to_edge(UL)
        self.play(Write(forward_title), run_time=1)
        self.wait(1)

        f_client_rect = Rectangle(width=2.5, height=1.5, color=BLUE).move_to(LEFT * 4)
        f_client_label = Text("Your Device", font_size=28).move_to(f_client_rect)

        f_proxy_rect = Rectangle(width=2.5, height=1.5, color=YELLOW).move_to(ORIGIN)
        f_proxy_label = Text("Forward Proxy", font_size=28).move_to(f_proxy_rect)

        f_internet_rect = Rectangle(width=2.5, height=1.5, color=GREEN).move_to(RIGHT * 4)
        f_internet_label = Text("Internet", font_size=28).move_to(f_internet_rect)

        f_arrow1 = Arrow(f_client_rect.get_right(), f_proxy_rect.get_left(), buff=0.1, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.2)
        f_arrow2 = Arrow(f_proxy_rect.get_right(), f_internet_rect.get_left(), buff=0.1, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.2)

        self.play(FadeIn(f_client_rect, f_client_label), run_time=0.8)
        self.play(Create(f_arrow1), FadeIn(f_proxy_rect, f_proxy_label), run_time=0.8)
        self.play(Create(f_arrow2), FadeIn(f_internet_rect, f_internet_label), run_time=0.8)
        self.wait(1.5)

        forward_explanation = Text("Clients access the Internet through the proxy.", font_size=32).next_to(f_proxy_rect, DOWN, buff=0.8)
        forward_benefits = Text("Used for: Access Control, Caching, Privacy.", font_size=32).next_to(forward_explanation, DOWN, buff=0.2)
        self.play(Write(forward_explanation), run_time=1)
        self.play(Write(forward_benefits), run_time=1)
        self.wait(2)

        self.play(FadeOut(f_client_rect, f_client_label, f_proxy_rect, f_proxy_label, f_internet_rect, f_internet_label, f_arrow1, f_arrow2, forward_explanation, forward_benefits, forward_title), run_time=1.5)
        self.wait(0.5)

        reverse_title = Text("2. Reverse Proxy", font_size=40).to_edge(UL)
        self.play(Write(reverse_title), run_time=1)
        self.wait(1)

        r_internet_rect = Rectangle(width=2.5, height=1.5, color=BLUE).move_to(LEFT * 4)
        r_internet_label = Text("Internet Users", font_size=28).move_to(r_internet_rect)

        r_proxy_rect = Rectangle(width=2.5, height=1.5, color=YELLOW).move_to(ORIGIN)
        r_proxy_label = Text("Reverse Proxy", font_size=28).move_to(r_proxy_rect)

        r_servers_rect = Rectangle(width=2.5, height=1.5, color=GREEN).move_to(RIGHT * 4)
        r_servers_label = Text("Web Servers", font_size=28).move_to(r_servers_rect)

        r_arrow1 = Arrow(r_internet_rect.get_right(), r_proxy_rect.get_left(), buff=0.1, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.2)
        r_arrow2 = Arrow(r_proxy_rect.get_right(), r_servers_rect.get_left(), buff=0.1, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.2)

        self.play(FadeIn(r_internet_rect, r_internet_label), run_time=0.8)
        self.play(Create(r_arrow1), FadeIn(r_proxy_rect, r_proxy_label), run_time=0.8)
        self.play(Create(r_arrow2), FadeIn(r_servers_rect, r_servers_label), run_time=0.8)
        self.wait(1.5)

        reverse_explanation = Text("Protects web servers from direct Internet access.", font_size=32).next_to(r_proxy_rect, DOWN, buff=0.8)
        reverse_benefits = Text("Used for: Load Balancing, Security, SSL Offloading.", font_size=32).next_to(reverse_explanation, DOWN, buff=0.2)
        self.play(Write(reverse_explanation), run_time=1)
        self.play(Write(reverse_benefits), run_time=1)
        self.wait(3)

        self.play(FadeOut(r_internet_rect, r_internet_label, r_proxy_rect, r_proxy_label, r_servers_rect, r_servers_label, r_arrow1, r_arrow2, reverse_explanation, reverse_benefits, reverse_title), run_time=1.5)
        self.wait(0.5)

        # --- Section 4: Applications ---

        applications_title = Text("Common Applications", font_size=48).to_edge(UP)
        self.play(Transform(title, applications_title), run_time=1)
        self.wait(2)

        app_list_text = Text("Proxy servers are widely used for:", font_size=36).next_to(applications_title, DOWN, buff=0.8).to_edge(LEFT, buff=1.0)
        app1 = Text("• Corporate Network Security & Filtering", font_size=32).next_to(app_list_text, DOWN, buff=0.4).to_edge(LEFT, buff=1.5)
        app2 = Text("• Content Filtering (e.g., parental controls)", font_size=32).next_to(app1, DOWN, buff=0.2).to_edge(LEFT, buff=1.5)
        app3 = Text("• Anonymity and Privacy", font_size=32).next_to(app2, DOWN, buff=0.2).to_edge(LEFT, buff=1.5)
        app4 = Text("• Bypassing Geo-restrictions", font_size=32).next_to(app3, DOWN, buff=0.2).to_edge(LEFT, buff=1.5)

        self.play(Write(app_list_text), run_time=1)
        self.play(Write(app1), run_time=1)
        self.play(Write(app2), run_time=1)
        self.play(Write(app3), run_time=1)
        self.play(Write(app4), run_time=1)
        self.wait(4)

        # Final Fade Out
        self.play(FadeOut(*self.mobjects), run_time=2)