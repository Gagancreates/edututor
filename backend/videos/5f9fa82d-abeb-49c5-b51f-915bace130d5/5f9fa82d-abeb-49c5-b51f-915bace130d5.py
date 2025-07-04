from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- 1. Introduction (25%) ---
        title = Text("Understanding Linked Lists", font_size=50).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(2)

        intro_text1 = Text("A fundamental data structure...", font_size=30).next_to(title, DOWN, buff=0.8).to_edge(LEFT)
        intro_text2 = Text("Unlike arrays, linked lists are dynamic.", font_size=30).next_to(intro_text1, DOWN, buff=0.5)
        intro_text3 = Text("They allow efficient insertions and deletions.", font_size=30).next_to(intro_text2, DOWN, buff=0.5)

        self.play(Write(intro_text1), run_time=1.0)
        self.wait(1.5)
        self.play(Write(intro_text2), run_time=1.0)
        self.wait(1.5)
        self.play(Write(intro_text3), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(intro_text1, intro_text2, intro_text3), run_time=1.0)
        
        definition_title = Text("What is a Linked List?", font_size=40).next_to(title, DOWN, buff=0.5)
        definition_text = Text("A sequence of 'nodes' connected by 'pointers'.", font_size=35).next_to(definition_title, DOWN, buff=0.5)
        
        self.play(Transform(title, definition_title), FadeIn(definition_text), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(definition_text, title), run_time=1.0)

        # --- 2. Core Understanding (40%) ---
        core_title = Text("Core Components", font_size=50).to_edge(UP)
        self.play(Write(core_title), run_time=1.5)
        self.wait(1.5)

        # Node Structure
        node_rect = Rectangle(width=2.5, height=1.5, color=BLUE)
        node_rect_left_edge_x = node_rect.get_left()[0]
        node_rect_right_edge_x = node_rect.get_right()[0]
        mid_x = (node_rect_left_edge_x + node_rect_right_edge_x) / 2
        
        vertical_line_correct = Line(
            [mid_x, node_rect.get_top()[1], 0],
            [mid_x, node_rect.get_bottom()[1], 0],
            color=WHITE
        )
        
        data_text = Text("Data", font_size=30).next_to(vertical_line_correct, LEFT, buff=0.2)
        pointer_text = Text("Next", font_size=30).next_to(vertical_line_correct, RIGHT, buff=0.2)

        node_group = VGroup(node_rect, vertical_line_correct, data_text, pointer_text)
        node_label = Text("Node", font_size=35).next_to(node_group, DOWN, buff=0.5)

        self.play(Create(node_group), Write(node_label), run_time=1.5)
        self.wait(2.5)

        # Head and Tail
        head_text = Text("Head: Start of the list", font_size=30).to_edge(LEFT).shift(UP*1.5)
        tail_text = Text("Tail: End of the list (points to None)", font_size=30).next_to(head_text, DOWN, buff=0.5)

        self.play(FadeOut(node_group, node_label), run_time=1.0)
        self.play(Write(head_text), run_time=1.0)
        self.wait(1.5)
        self.play(Write(tail_text), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(head_text, tail_text, core_title), run_time=1.0)

        # --- 3. Examples (25%) ---
        example_title = Text("Building a Linked List", font_size=40).to_edge(UP)
        self.play(Write(example_title), run_time=1.5)
        self.wait(1.5)

        # Helper function to create a node for examples
        def create_example_node(value, pos, color=BLUE):
            rect = Rectangle(width=2, height=1, color=color).move_to(pos)
            line = Line(
                [rect.get_left()[0] + rect.width/2, rect.get_top()[1], 0],
                [rect.get_left()[0] + rect.width/2, rect.get_bottom()[1], 0],
                color=WHITE
            )
            value_text = Text(str(value), font_size=35).move_to(rect.get_center() + LEFT * 0.5)
            pointer_slot = Text("->", font_size=35).move_to(rect.get_center() + RIGHT * 0.5) # Represent pointer visually

            return VGroup(rect, line, value_text, pointer_slot)

        # Node 1
        node1_val = 10
        node1_pos = ORIGIN + LEFT * 4
        node1 = create_example_node(node1_val, node1_pos)
        head_label = Text("Head", font_size=30).next_to(node1, UP)
        
        self.play(Create(node1), Write(head_label), run_time=1.0)
        self.wait(1.5)

        # Node 2
        node2_val = 20
        node2_pos = node1_pos + RIGHT * 3
        node2 = create_example_node(node2_val, node2_pos)
        arrow1_2 = Arrow(node1[0].get_right(), node2[0].get_left(), buff=0.1, max_stroke_width_to_length_ratio=4)
        
        self.play(Create(node2), Create(arrow1_2), run_time=1.0)
        self.wait(1.5)

        # Node 3
        node3_val = 30
        node3_pos = node2_pos + RIGHT * 3
        node3 = create_example_node(node3_val, node3_pos)
        arrow2_3 = Arrow(node2[0].get_right(), node3[0].get_left(), buff=0.1, max_stroke_width_to_length_ratio=4)
        
        self.play(Create(node3), Create(arrow2_3), run_time=1.0)
        self.wait(2.5)
        
        # Traversing
        traverse_label = Text("Traversing the List", font_size=35).next_to(example_title, DOWN, buff=0.5)
        self.play(Write(traverse_label), run_time=1.0)
        self.wait(1.5)
        
        current_arrow = Arrow(node1[0].get_top() + UP, node1[0].get_top() + UP*0.1, color=YELLOW, buff=0.1).set_length(0.5)
        current_text = Text("Current", font_size=25, color=YELLOW).next_to(current_arrow, UP)
        
        self.play(Create(current_arrow), Write(current_text), run_time=0.8)
        self.wait(1.5)
        
        self.play(
            current_arrow.animate.next_to(node2[0].get_top(), UP, buff=0.1),
            current_text.animate.next_to(node2[0].get_top(), UP, buff=0.1 + 0.5),
            run_time=1.0
        )
        self.wait(1.5)
        
        self.play(
            current_arrow.animate.next_to(node3[0].get_top(), UP, buff=0.1),
            current_text.animate.next_to(node3[0].get_top(), UP, buff=0.1 + 0.5),
            run_time=1.0
        )
        self.wait(2.5)

        self.play(FadeOut(current_arrow, current_text, traverse_label, node1, node2, node3, arrow1_2, arrow2_3, head_label), run_time=1.5)
        
        # Insertion Example
        insertion_title = Text("Insertion Example", font_size=40).to_edge(UP)
        self.play(ReplacementTransform(example_title, insertion_title), run_time=1.0)
        self.wait(1.5)

        # Re-create two nodes for insertion
        nodeA = create_example_node("A", ORIGIN + LEFT * 3.5)
        nodeB = create_example_node("B", ORIGIN + RIGHT * 3.5)
        arrowAB = Arrow(nodeA[0].get_right(), nodeB[0].get_left(), buff=0.1, max_stroke_width_to_length_ratio=4)

        self.play(Create(nodeA), Create(nodeB), Create(arrowAB), run_time=1.0)
        self.wait(1.5)

        # New node to insert
        nodeX = create_example_node("X", ORIGIN, color=GREEN)
        self.play(Create(nodeX), run_time=1.0)
        self.wait(1.5)

        # Animate pointer changes for insertion
        # 1. New node points to Node B
        new_arrow_X_B = Arrow(nodeX[0].get_right(), nodeB[0].get_left(), buff=0.1, color=GREEN, max_stroke_width_to_length_ratio=4)
        self.play(Transform(nodeX[3], new_arrow_X_B.copy()), run_time=1.0)
        self.play(Create(new_arrow_X_B), FadeOut(nodeX[3]), run_time=0.1)
        self.wait(1.5)

        # 2. Node A points to New Node X
        self.play(FadeOut(arrowAB), run_time=0.5)
        new_arrow_A_X = Arrow(nodeA[0].get_right(), nodeX[0].get_left(), buff=0.1, color=YELLOW, max_stroke_width_to_length_ratio=4)
        self.play(Create(new_arrow_A_X), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(nodeA, nodeB, nodeX, new_arrow_A_X, new_arrow_X_B, insertion_title), run_time=1.5)

        # Deletion Example (Similar setup to insertion)
        deletion_title = Text("Deletion Example", font_size=40).to_edge(UP)
        self.play(Write(deletion_title), run_time=1.0)
        self.wait(1.5)

        # Nodes for deletion: A -> B (to be deleted) -> C
        node_del_A = create_example_node("A", ORIGIN + LEFT * 4.5)
        node_del_B = create_example_node("B", ORIGIN + 0)
        node_del_C = create_example_node("C", ORIGIN + RIGHT * 4.5)
        
        arrow_del_AB = Arrow(node_del_A[0].get_right(), node_del_B[0].get_left(), buff=0.1, max_stroke_width_to_length_ratio=4)
        arrow_del_BC = Arrow(node_del_B[0].get_right(), node_del_C[0].get_left(), buff=0.1, max_stroke_width_to_length_ratio=4)

        self.play(Create(VGroup(node_del_A, node_del_B, node_del_C, arrow_del_AB, arrow_del_BC)), run_time=1.5)
        self.wait(1.5)

        node_to_delete_label = Text("Node to Delete", font_size=30, color=RED).next_to(node_del_B, UP)
        self.play(FadeIn(node_to_delete_label), run_time=0.8)
        self.wait(1.5)

        # Animate pointer change for deletion: A -> C
        self.play(FadeOut(arrow_del_AB, arrow_del_BC, node_to_delete_label), run_time=0.8)
        new_arrow_A_C = Arrow(node_del_A[0].get_right(), node_del_C[0].get_left(), buff=0.1, color=YELLOW, max_stroke_width_to_length_ratio=4)
        self.play(Create(new_arrow_A_C), run_time=1.0)
        self.wait(1.5)

        self.play(FadeOut(node_del_B), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(node_del_A, node_del_C, new_arrow_A_C, deletion_title), run_time=1.5)

        # --- 4. Applications (10%) ---
        applications_title = Text("Applications", font_size=40).to_edge(UP)
        self.play(Write(applications_title), run_time=1.0)
        self.wait(1.5)

        app1 = Text("• Implementing Stacks and Queues", font_size=30).next_to(applications_title, DOWN, buff=0.7).to_edge(LEFT)
        app2 = Text("• Music Playlists & Browser History", font_size=30).next_to(app1, DOWN, buff=0.5)
        app3 = Text("• Dynamic memory allocation", font_size=30).next_to(app2, DOWN, buff=0.5)

        self.play(Write(app1), run_time=0.8)
        self.wait(1.2)
        self.play(Write(app2), run_time=0.8)
        self.wait(1.2)
        self.play(Write(app3), run_time=0.8)
        self.wait(2.5)

        conclusion_text = Text("Linked lists are versatile for dynamic data!", font_size=40, color=GREEN).move_to(ORIGIN)
        self.play(FadeOut(applications_title, app1, app2, app3), run_time=1.0)
        self.play(Write(conclusion_text), run_time=1.5)
        self.wait(2.5)

        # --- End Scene ---
        self.play(FadeOut(*self.mobjects), run_time=1.5)