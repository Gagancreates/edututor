from manim import *

class CreateScene(Scene):
    def construct(self):
        # Helper function to create a node Mobject
        def create_node_mobject(data_val, position=ORIGIN, data_color=BLUE_B, pointer_color=PURPLE_B):
            data_rect = Rectangle(width=1.5, height=0.8, color=data_color, fill_opacity=0.8)
            pointer_rect = Rectangle(width=1.5, height=0.8, color=pointer_color, fill_opacity=0.8)
            
            # Combine the rectangles first, then position them
            node_boxes = VGroup(data_rect, pointer_rect).arrange(RIGHT, buff=0).scale(0.8)
            node_data_value = Text(str(data_val), font_size=36).move_to(node_boxes[0].get_center()) # node_boxes[0] is the data_rect
            
            # Create a larger VGroup for the whole node, including text
            node_full = VGroup(node_boxes, node_data_value).move_to(position)
            
            # Expose components for easier access
            node_full.data_rect_component = node_boxes[0]
            node_full.pointer_rect_component = node_boxes[1]
            node_full.data_value_component = node_data_value
            
            return node_full

        # --- Part 1: Introduction (25%) ---
        intro_title = Text("What are Linked Lists?", font_size=56).to_edge(UP)
        self.play(Write(intro_title, run_time=1.5))
        self.wait(2)

        definition_text = Text("A fundamental data structure for sequential storage.", font_size=36).next_to(intro_title, DOWN, buff=0.8)
        self.play(Write(definition_text, run_time=1.5))
        self.wait(2.5)

        analogy_text = Text("Think of a treasure hunt:", font_size=36).next_to(definition_text, DOWN, buff=0.8).to_edge(LEFT)
        analogy_detail = Text("Each clue points to the NEXT location.", font_size=36).next_to(analogy_text, DOWN, aligned_edge=LEFT)
        
        self.play(Write(analogy_text, run_time=1))
        self.wait(1.5)
        self.play(Write(analogy_detail, run_time=1.5))
        self.wait(2.5)

        intro_group = VGroup(intro_title, definition_text, analogy_text, analogy_detail)
        self.play(FadeOut(intro_group, run_time=1.5))
        self.wait(1)

        # --- Part 2: Core Understanding (40%) ---

        # Node Structure
        node_concept_title = Text("The Building Block: A Node", font_size=48).to_edge(UP)
        self.play(FadeIn(node_concept_title, run_time=1))
        self.wait(1)

        node_data_rect_proto = Rectangle(width=2.5, height=1, color=BLUE_B, fill_opacity=0.8)
        node_pointer_rect_proto = Rectangle(width=2.5, height=1, color=PURPLE_B, fill_opacity=0.8)
        
        proto_node_group = VGroup(node_data_rect_proto, node_pointer_rect_proto).arrange(RIGHT, buff=0).move_to(ORIGIN)
        
        data_text_label = Text("Data (Value)", font_size=36).move_to(node_data_rect_proto.get_center())
        pointer_text_label = Text("Next (Pointer)", font_size=36).move_to(node_pointer_rect_proto.get_center())

        self.play(Create(proto_node_group, run_time=1.5))
        self.wait(1)
        self.play(Write(data_text_label, run_time=1), Write(pointer_text_label, run_time=1))
        self.wait(2.5)
        
        node_structure_group = VGroup(node_concept_title, proto_node_group, data_text_label, pointer_text_label)
        self.play(FadeOut(node_structure_group, run_time=1.5))
        self.wait(1)

        # Building a Simple List
        list_building_title = Text("Building a Linked List", font_size=48).to_edge(UP)
        self.play(FadeIn(list_building_title, run_time=1))
        self.wait(1)

        head_text = Text("Head", font_size=36).shift(LEFT*6.5 + UP*1)
        
        node1 = create_node_mobject("10", position=LEFT*3 + UP*1)
        node2 = create_node_mobject("20", position=ORIGIN + UP*1)
        node3 = create_node_mobject("30", position=RIGHT*3 + UP*1)
        
        null_text = Text("Null", font_size=36).next_to(node3.pointer_rect_component, RIGHT, buff=0.5)

        head_arrow = Arrow(head_text.get_right(), node1.get_left(), buff=0.1, color=ORANGE)
        conn_arrow1_2 = Arrow(node1.pointer_rect_component.get_right(), node2.get_left(), buff=0.1, color=YELLOW)
        conn_arrow2_3 = Arrow(node2.pointer_rect_component.get_right(), node3.get_left(), buff=0.1, color=YELLOW)

        self.play(FadeIn(head_text, run_time=0.8), Create(node1, run_time=1.2))
        self.play(Create(head_arrow, run_time=1))
        self.wait(1.5)

        self.play(Create(node2, run_time=1.2))
        self.play(Create(conn_arrow1_2, run_time=1))
        self.wait(1.5)

        self.play(Create(node3, run_time=1.2))
        self.play(Create(conn_arrow2_3, run_time=1), Write(null_text, run_time=0.8))
        self.wait(2.5)
        
        list_elements_group = VGroup(head_text, head_arrow, node1, node2, node3, null_text, conn_arrow1_2, conn_arrow2_3)
        
        self.play(FadeOut(list_building_title, run_time=1.5))
        self.wait(1)

        # --- Part 3: Examples & Properties (25%) ---

        # Adding a Node
        add_node_title = Text("Adding a Node (e.g., Value 40)", font_size=48).to_edge(UP)
        self.play(FadeIn(add_node_title, run_time=1))
        self.wait(1)
        
        # Shift existing list up
        self.play(list_elements_group.animate.shift(UP*1.5), run_time=1.5)
        self.wait(1)

        new_node = create_node_mobject("40", position=RIGHT*3 + DOWN*1.5)
        new_node_null_text = Text("Null", font_size=36).next_to(new_node.pointer_rect_component, RIGHT, buff=0.5)
        
        self.play(Create(new_node, run_time=1.2), Write(new_node_null_text, run_time=0.8))
        self.wait(1.5)

        # Re-route pointer from node3 to new_node
        self.play(FadeOut(null_text, run_time=0.8)) # Fade out the old Null
        new_conn_arrow3_4 = Arrow(node3.pointer_rect_component.get_right(), new_node.get_left(), buff=0.1, color=YELLOW)
        self.play(ReplacementTransform(conn_arrow2_3, new_conn_arrow3_4, run_time=1.5)) # Transform arrow
        self.wait(2)
        
        # Keep track of all objects to fade out later
        current_list_elements = VGroup(list_elements_group, new_node, new_node_null_text, new_conn_arrow3_4)
        self.play(FadeOut(add_node_title, run_time=1.5))
        self.wait(1)


        # Deleting a Node (Value 20)
        delete_node_title = Text("Deleting a Node (e.g., Value 20)", font_size=48).to_edge(UP)
        self.play(FadeIn(delete_node_title, run_time=1))
        self.wait(1)
        
        # Re-set list for deletion
        # Fade out current_list_elements and reset list to original 10-20-30 state (shifted for space)
        self.play(FadeOut(current_list_elements, run_time=1.5))
        self.wait(1)

        head_text_del = Text("Head", font_size=36).shift(LEFT*6.5 + UP*1)
        node1_del = create_node_mobject("10", position=LEFT*3 + UP*1)
        node2_del = create_node_mobject("20", position=ORIGIN + UP*1, data_color=RED_B, pointer_color=RED_B) # This one will be deleted
        node3_del = create_node_mobject("30", position=RIGHT*3 + UP*1)
        null_text_del = Text("Null", font_size=36).next_to(node3_del.pointer_rect_component, RIGHT, buff=0.5)
        
        head_arrow_del = Arrow(head_text_del.get_right(), node1_del.get_left(), buff=0.1, color=ORANGE)
        conn_arrow1_2_del = Arrow(node1_del.pointer_rect_component.get_right(), node2_del.get_left(), buff=0.1, color=YELLOW)
        conn_arrow2_3_del = Arrow(node2_del.pointer_rect_component.get_right(), node3_del.get_left(), buff=0.1, color=YELLOW)

        list_for_del_group = VGroup(head_text_del, head_arrow_del, node1_del, node2_del, node3_del, null_text_del, conn_arrow1_2_del, conn_arrow2_3_del)
        self.play(FadeIn(list_for_del_group, run_time=1.5))
        self.wait(1.5)

        # Reroute pointer from node1 to node3, fading out the node2 and its connections
        new_conn_arrow1_3 = Arrow(node1_del.pointer_rect_component.get_right(), node3_del.get_left(), buff=0.1, color=YELLOW)
        self.play(
            ReplacementTransform(conn_arrow1_2_del, new_conn_arrow1_3, run_time=1.5),
            FadeOut(conn_arrow2_3_del, run_time=0.8),
            FadeOut(node2_del, run_time=1.5)
        )
        self.wait(2)

        properties_title = Text("Key Properties:", font_size=40).next_to(delete_node_title, DOWN, buff=1).to_edge(LEFT)
        property1 = Text("- Dynamic size (can grow or shrink)", font_size=32).next_to(properties_title, DOWN, buff=0.5, aligned_edge=LEFT)
        property2 = Text("- Non-contiguous memory allocation", font_size=32).next_to(property1, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.play(FadeIn(properties_title, run_time=1))
        self.wait(0.5)
        self.play(Write(property1, run_time=1.2))
        self.wait(1)
        self.play(Write(property2, run_time=1.2))
        self.wait(2.5)

        deletion_and_properties_group = VGroup(delete_node_title, list_for_del_group, new_conn_arrow1_3, properties_title, property1, property2)
        self.play(FadeOut(deletion_and_properties_group, run_time=1.5))
        self.wait(1)

        # --- Part 4: Applications (10%) ---
        applications_title = Text("Real-World Applications", font_size=48).to_edge(UP)
        self.play(FadeIn(applications_title, run_time=1))
        self.wait(1)

        app1 = Text("- Implementing Stacks and Queues", font_size=36).next_to(applications_title, DOWN, buff=0.8).to_edge(LEFT)
        app2 = Text("- Memory Management in Operating Systems", font_size=36).next_to(app1, DOWN, buff=0.5, aligned_edge=LEFT)
        app3 = Text("- Image Viewers (next/previous image functionality)", font_size=36).next_to(app2, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(app1, run_time=1.2))
        self.wait(1.5)
        self.play(Write(app2, run_time=1.2))
        self.wait(1.5)
        self.play(Write(app3, run_time=1.2))
        self.wait(2)

        conclusion_text = Text("Linked Lists: Flexible, Powerful, Foundational.", font_size=44, color=YELLOW_B).to_edge(DOWN)
        self.play(Write(conclusion_text, run_time=1.5))
        self.wait(2.5)

        # --- End Scene ---
        self.play(FadeOut(*self.mobjects, run_time=1.5))
        self.wait(0.5)