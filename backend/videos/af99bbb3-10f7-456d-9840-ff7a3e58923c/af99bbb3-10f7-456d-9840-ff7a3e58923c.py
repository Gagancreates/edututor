from manim import *

class CreateScene(Scene):
    def construct(self):
        # --- Section 1: Introduction (approx. 45 seconds) ---

        title = Text("Understanding Linked Lists", font_size=50).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(2)

        definition_text = Text(
            "A Linked List is a linear data structure.",
            font_size=36
        ).next_to(title, DOWN, buff=0.8)
        self.play(Write(definition_text), run_time=1.5)
        self.wait(2)

        definition_cont = Text(
            "Elements are not stored at contiguous memory locations.",
            font_size=36
        ).next_to(definition_text, DOWN, buff=0.5)
        self.play(Write(definition_cont), run_time=1.5)
        self.wait(2)

        array_concept = Text("Think about Arrays:", font_size=36).next_to(definition_cont, DOWN, buff=1.0)
        self.play(Write(array_concept), run_time=1.5)
        self.wait(1)

        # Visualizing an Array
        array_rects = VGroup(*[
            Square(side_length=1).set_fill(BLUE_A, opacity=0.7).set_stroke(WHITE)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.1).next_to(array_concept, DOWN, buff=0.5)

        array_indices = VGroup(*[
            Text(str(i), font_size=24).next_to(array_rects[i], DOWN, buff=0.1)
            for i in range(5)
        ])

        array_data = VGroup(*[
            Text(char, font_size=28).move_to(array_rects[i].get_center())
            for i, char in enumerate(["A", "B", "C", "D", "E"])
        ])

        array_group = VGroup(array_rects, array_indices, array_data)
        self.play(Create(array_group), run_time=2)
        self.wait(2)

        array_desc = Text(
            "Arrays: contiguous memory, fixed size.",
            font_size=32
        ).next_to(array_group, DOWN, buff=0.5)
        self.play(Write(array_desc), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(array_concept, array_group, array_desc, definition_text, definition_cont), run_time=1.5)
        self.wait(1)

        # --- Section 2: Core Understanding (approx. 72 seconds) ---

        linked_list_intro = Text(
            "Linked Lists overcome array limitations.",
            font_size=36
        ).next_to(title, DOWN, buff=0.8)
        self.play(Write(linked_list_intro), run_time=1.5)
        self.wait(2)

        component_text = Text("Key Components: Node", font_size=40).next_to(linked_list_intro, DOWN, buff=1.0)
        self.play(Write(component_text), run_time=1.5)
        self.wait(2)

        # Node Structure
        data_rect = Rectangle(width=2, height=1, color=YELLOW_B, fill_opacity=0.7).move_to(ORIGIN + LEFT*2)
        data_label = Text("Data", font_size=30).move_to(data_rect.get_center())

        pointer_rect = Rectangle(width=1, height=1, color=PURPLE_B, fill_opacity=0.7).next_to(data_rect, RIGHT, buff=0)
        pointer_label = Text("Next\nPointer", font_size=20).move_to(pointer_rect.get_center())

        node_box = VGroup(data_rect, pointer_rect)
        node_labels = VGroup(data_label, pointer_label)
        node_group = VGroup(node_box, node_labels)

        self.play(Create(node_group), run_time=2)
        self.wait(2)

        node_explanation = Text(
            "Each Node stores data and a pointer to the next node.",
            font_size=32
        ).next_to(node_group, DOWN, buff=0.7)
        self.play(Write(node_explanation), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(node_explanation, component_text), run_time=1.5)
        self.wait(1)

        # Build a Linked List
        node1_data = Rectangle(width=2, height=1, color=YELLOW_B, fill_opacity=0.7).shift(LEFT*5 + UP*0.5)
        node1_val = Text("10", font_size=30).move_to(node1_data.get_center())
        node1_ptr = Rectangle(width=1, height=1, color=PURPLE_B, fill_opacity=0.7).next_to(node1_data, RIGHT, buff=0)
        node1 = VGroup(node1_data, node1_val, node1_ptr)

        node2_data = Rectangle(width=2, height=1, color=YELLOW_B, fill_opacity=0.7).shift(LEFT*0.5 + UP*0.5)
        node2_val = Text("20", font_size=30).move_to(node2_data.get_center())
        node2_ptr = Rectangle(width=1, height=1, color=PURPLE_B, fill_opacity=0.7).next_to(node2_data, RIGHT, buff=0)
        node2 = VGroup(node2_data, node2_val, node2_ptr)

        node3_data = Rectangle(width=2, height=1, color=YELLOW_B, fill_opacity=0.7).shift(RIGHT*4 + UP*0.5)
        node3_val = Text("30", font_size=30).move_to(node3_data.get_center())
        node3_ptr = Rectangle(width=1, height=1, color=PURPLE_B, fill_opacity=0.7).next_to(node3_data, RIGHT, buff=0)
        node3 = VGroup(node3_data, node3_val, node3_ptr)

        arrow1 = Arrow(node1_ptr.get_right(), node2_data.get_left(), buff=0.1, color=WHITE)
        arrow2 = Arrow(node2_ptr.get_right(), node3_data.get_left(), buff=0.1, color=WHITE)

        head_label = Text("HEAD", font_size=30, color=GREEN_B).next_to(node1, UP, buff=0.5)
        null_label = Text("NULL", font_size=30, color=RED_B).next_to(node3_ptr, RIGHT, buff=0.5)
        null_line = Line(node3_ptr.get_center() + DOWN*0.25 + RIGHT*0.25, node3_ptr.get_center() + UP*0.25 + LEFT*0.25, color=RED_B, stroke_width=4)

        self.play(FadeOut(node_group), run_time=1)
        self.wait(1)

        self.play(Create(node1), Create(node2), Create(node3), run_time=2)
        self.wait(1)
        self.play(Create(arrow1), Create(arrow2), run_time=1.5)
        self.wait(1)
        self.play(Write(head_label), run_time=1)
        self.play(Write(null_label), Create(null_line), run_time=1.5)
        self.wait(2)

        chain_analogy = Text("Like a chain, each link knows the next.", font_size=32).next_to(node1, DOWN, buff=1.5)
        self.play(Write(chain_analogy), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(linked_list_intro, chain_analogy), run_time=1.5)
        self.wait(1)

        # --- Section 3: Examples (approx. 45 seconds) ---

        example_title = Text("Linked List Operations", font_size=45).next_to(title, DOWN, buff=0.8)
        self.play(ReplacementTransform(title, example_title), run_time=1.5) # Transform title to new title
        self.wait(2)

        # Traversal
        traversal_text = Text("1. Traversal: Visiting each node.", font_size=36).next_to(example_title, DOWN, buff=0.8)
        self.play(Write(traversal_text), run_time=1.5)
        self.wait(1)

        self.play(node1_val.animate.set_color(GREEN_C), run_time=0.8)
        self.wait(0.5)
        self.play(arrow1.animate.set_color(GREEN_C), run_time=0.8)
        self.wait(0.5)
        self.play(node2_val.animate.set_color(GREEN_C), run_time=0.8)
        self.wait(0.5)
        self.play(arrow2.animate.set_color(GREEN_C), run_time=0.8)
        self.wait(0.5)
        self.play(node3_val.animate.set_color(GREEN_C), run_time=0.8)
        self.wait(1.5)

        self.play(
            node1_val.animate.set_color(WHITE),
            arrow1.animate.set_color(WHITE),
            node2_val.animate.set_color(WHITE),
            arrow2.animate.set_color(WHITE),
            node3_val.animate.set_color(WHITE),
            run_time=1
        )
        self.wait(1)

        self.play(FadeOut(traversal_text), run_time=1)
        self.wait(0.5)

        # Insertion
        insertion_text = Text("2. Insertion: Adding a new node.", font_size=36).next_to(example_title, DOWN, buff=0.8)
        self.play(Write(insertion_text), run_time=1.5)
        self.wait(1)

        new_node_data = Rectangle(width=2, height=1, color=YELLOW_B, fill_opacity=0.7)
        new_node_val = Text("25", font_size=30).move_to(new_node_data.get_center())
        new_node_ptr = Rectangle(width=1, height=1, color=PURPLE_B, fill_opacity=0.7).next_to(new_node_data, RIGHT, buff=0)
        new_node = VGroup(new_node_data, new_node_val, new_node_ptr).shift(UP*2.5 + RIGHT*1.75) # Start above the list

        self.play(Create(new_node), run_time=1.5)
        self.wait(1)

        # Animate insertion between node2 and node3
        self.play(FadeOut(arrow2), run_time=1) # Fade out original arrow
        self.wait(0.5)

        # Shift node3 and null to make space
        self.play(
            node3.animate.shift(RIGHT*3),
            null_label.animate.shift(RIGHT*3),
            null_line.animate.shift(RIGHT*3),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Move new node into position
        new_node.move_to(node2_ptr.get_right() + RIGHT*1.5)

        new_arrow_from_node2 = Arrow(node2_ptr.get_right(), new_node_data.get_left(), buff=0.1, color=ORANGE_C)
        new_arrow_from_new_node = Arrow(new_node_ptr.get_right(), node3_data.get_left(), buff=0.1, color=ORANGE_C)

        self.play(
            Create(new_arrow_from_node2),
            Create(new_arrow_from_new_node),
            run_time=1.5
        )
        self.wait(2)

        self.play(FadeOut(insertion_text, new_node, new_arrow_from_node2, new_arrow_from_new_node), run_time=1.5)
        self.wait(0.5)

        # Deletion
        # Fade out existing list elements to reset for deletion demo
        self.play(
            FadeOut(head_label, node1, node2, node3, arrow1, null_label, null_line),
            run_time=1.5
        )
        self.wait(1)

        # Re-create the initial list for deletion demo
        node1_data_d = Rectangle(width=2, height=1, color=YELLOW_B, fill_opacity=0.7).shift(LEFT*5 + UP*0.5)
        node1_val_d = Text("10", font_size=30).move_to(node1_data_d.get_center())
        node1_ptr_d = Rectangle(width=1, height=1, color=PURPLE_B, fill_opacity=0.7).next_to(node1_data_d, RIGHT, buff=0)
        node1_d = VGroup(node1_data_d, node1_val_d, node1_ptr_d)

        node2_data_d = Rectangle(width=2, height=1, color=YELLOW_B, fill_opacity=0.7).shift(LEFT*0.5 + UP*0.5)
        node2_val_d = Text("20", font_size=30).move_to(node2_data_d.get_center())
        node2_ptr_d = Rectangle(width=1, height=1, color=PURPLE_B, fill_opacity=0.7).next_to(node2_data_d, RIGHT, buff=0)
        node2_d = VGroup(node2_data_d, node2_val_d, node2_ptr_d)

        node3_data_d = Rectangle(width=2, height=1, color=YELLOW_B, fill_opacity=0.7).shift(RIGHT*4 + UP*0.5)
        node3_val_d = Text("30", font_size=30).move_to(node3_data_d.get_center())
        node3_ptr_d = Rectangle(width=1, height=1, color=PURPLE_B, fill_opacity=0.7).next_to(node3_data_d, RIGHT, buff=0)
        node3_d = VGroup(node3_data_d, node3_val_d, node3_ptr_d)

        arrow1_d = Arrow(node1_ptr_d.get_right(), node2_data_d.get_left(), buff=0.1, color=WHITE)
        arrow2_d = Arrow(node2_ptr_d.get_right(), node3_data_d.get_left(), buff=0.1, color=WHITE)

        head_label_d = Text("HEAD", font_size=30, color=GREEN_B).next_to(node1_d, UP, buff=0.5)
        null_label_d = Text("NULL", font_size=30, color=RED_B).next_to(node3_ptr_d, RIGHT, buff=0.5)
        null_line_d = Line(node3_ptr_d.get_center() + DOWN*0.25 + RIGHT*0.25, node3_ptr_d.get_center() + UP*0.25 + LEFT*0.25, color=RED_B, stroke_width=4)

        self.play(Create(VGroup(node1_d, node2_d, node3_d, arrow1_d, arrow2_d, head_label_d, null_label_d, null_line_d)), run_time=2)
        self.wait(1)

        deletion_text = Text("3. Deletion: Removing a node.", font_size=36).next_to(example_title, DOWN, buff=0.8)
        self.play(Write(deletion_text), run_time=1.5)
        self.wait(1)

        # Animate deletion of node2_d
        self.play(FadeOut(node2_d, arrow1_d, arrow2_d), run_time=1.5)
        self.wait(0.5)

        # Create new arrow bypassing deleted node
        new_arrow_d = Arrow(node1_ptr_d.get_right(), node3_data_d.get_left(), buff=0.1, color=ORANGE_C)
        self.play(Create(new_arrow_d), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(deletion_text, node1_d, node3_d, head_label_d, null_label_d, null_line_d, new_arrow_d), run_time=1.5)
        self.wait(1)

        # --- Section 4: Applications (approx. 18 seconds) ---

        applications_title = Text("Applications", font_size=45).next_to(example_title, DOWN, buff=0.8)
        self.play(ReplacementTransform(example_title, applications_title), run_time=1.5)
        self.wait(1)

        app_list1 = Text("- Music Playlists", font_size=32).next_to(applications_title, DOWN, buff=0.8).to_edge(LEFT)
        app_list2 = Text("- Undo/Redo features", font_size=32).next_to(app_list1, DOWN, buff=0.5).to_edge(LEFT)
        app_list3 = Text("- Web Browser History", font_size=32).next_to(app_list2, DOWN, buff=0.5).to_edge(LEFT)

        self.play(Write(app_list1), run_time=1)
        self.wait(1)
        self.play(Write(app_list2), run_time=1)
        self.wait(1)
        self.play(Write(app_list3), run_time=1)
        self.wait(2)

        advanced_concepts = Text("Also fundamental for Stacks, Queues, Graphs.", font_size=32).next_to(app_list3, DOWN, buff=1.0)
        self.play(Write(advanced_concepts), run_time=1.5)
        self.wait(2)

        # End of Scene
        self.play(FadeOut(*self.mobjects), run_time=2)