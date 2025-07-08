from manim import *

class CreateScene(Scene):
    # NARRATION: This method introduces the concept of data structures, comparing linked lists to arrays.
    # We will start by showing a familiar data structure, an array, to set a baseline.
    # Then, we will introduce linked lists as a fundamental alternative, highlighting their sequential nature but non-contiguous memory storage.
    # This segment aims to provide a clear, concise definition and establish the context for why linked lists are important in computer science.
    def introduce_linked_lists(self):
        animations = []
        
        title = Text("Data Structures: Linked Lists", color=BLUE_A).scale(1.2)
        animations.append(Write(title, run_time=1.5))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        # Fade out title and bring in new text
        animations.append(FadeOut(title, run_time=0.8))
        if animations:
            self.play(*animations)
        self.wait(0.5)
        animations.clear()

        intro_text = Text("Imagine organizing information...", font_size=48).to_edge(UP)
        animations.append(Write(intro_text, run_time=1.5))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        array_text = Text("Arrays: Fixed-size, contiguous memory", font_size=36).next_to(intro_text, DOWN, buff=0.8)
        
        # Create an array visualization
        array_elements = VGroup()
        for i in range(5):
            square = Square(side_length=1.2, color=GRAY_D, fill_opacity=0.8).set_stroke(width=3)
            text_num = Text(str(i+1), color=WHITE).scale(0.8)
            element = VGroup(square, text_num)
            if i > 0:
                element.next_to(array_elements[-1], RIGHT, buff=0)
            array_elements.add(element)
        
        array_indices = VGroup()
        for i, element in enumerate(array_elements):
            index_text = Text(f"[{i}]", font_size=24, color=YELLOW).next_to(element, DOWN, buff=0.1)
            array_indices.add(index_text)

        array_container = VGroup(array_elements, array_indices).move_to(ORIGIN)

        animations.append(FadeIn(array_text, shift=UP, run_time=1))
        animations.append(Create(array_elements, run_time=1.5))
        animations.append(Write(array_indices, run_time=1))
        if animations:
            self.play(*animations)
        self.wait(2)
        animations.clear()

        linked_list_intro = Text("Linked Lists: Flexible, non-contiguous", font_size=36, color=YELLOW).next_to(intro_text, DOWN, buff=0.8)
        
        animations.append(ReplacementTransform(array_text, linked_list_intro, run_time=1))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        animations.append(FadeOut(array_container, run_time=0.8))
        animations.append(FadeOut(intro_text, run_time=0.8))
        if animations:
            self.play(*animations)
        self.wait(0.5)
        animations.clear()

        definition_text = Text("A Linked List is a sequence of nodes.", font_size=40).to_edge(UP)
        animations.append(Write(definition_text, run_time=1.5))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        nodes_ref_text = Text("Each node contains data and a reference to the next node.", font_size=36).next_to(definition_text, DOWN, buff=0.5)
        animations.append(Write(nodes_ref_text, run_time=2))
        if animations:
            self.play(*animations)
        self.wait(2)
        animations.clear()
        
        animations.append(FadeOut(definition_text, run_time=0.8))
        animations.append(FadeOut(nodes_ref_text, run_time=0.8))
        if animations:
            self.play(*animations)
        self.wait(0.5)


    # NARRATION: In this section, we will delve into the fundamental building block of a linked list: the Node.
    # We'll visually dissect a node, showing its two essential parts: the data payload and the pointer to the next node.
    # Following this, we will illustrate how multiple nodes are chained together, forming the list, by explicitly showing the 'next' pointers connecting them.
    # The concept of a 'Head' pointer, which marks the beginning of the list, will also be introduced, along with the 'None' pointer at the end of the list.
    def core_understanding_nodes(self):
        animations = []

        node_title = Text("Anatomy of a Node", color=GREEN).scale(1.1).to_edge(UP)
        animations.append(Write(node_title, run_time=1.2))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        # Create a single node
        data_box = Square(side_length=1.5, color=WHITE, fill_opacity=0.2).set_stroke(width=3)
        pointer_box = Rectangle(width=1.5, height=1.5, color=WHITE, fill_opacity=0.2).set_stroke(width=3)
        pointer_box.next_to(data_box, RIGHT, buff=0)
        
        node_box = VGroup(data_box, pointer_box).move_to(ORIGIN)
        
        data_label = Text("Data", font_size=36, color=YELLOW).move_to(data_box.get_center())
        pointer_label = Text("Next", font_size=36, color=ORANGE).move_to(pointer_box.get_center())
        
        node_elements = VGroup(node_box, data_label, pointer_label)

        animations.append(FadeIn(node_elements, shift=UP, run_time=1.5))
        if animations:
            self.play(*animations)
        self.wait(2)
        animations.clear()

        # Connect to "Next"
        next_arrow = Arrow(pointer_box.get_right(), pointer_box.get_right() + RIGHT * 1.5, buff=0)
        animations.append(Create(next_arrow, run_time=1))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()
        
        animations.append(FadeOut(next_arrow, run_time=0.8))
        if animations:
            self.play(*animations)
        self.wait(0.5)
        animations.clear()

        # Build a small list
        nodes = VGroup()
        node_values = ["A", "B", "C"]
        
        for i, val in enumerate(node_values):
            data_rect = Rectangle(width=1.5, height=1.0, color=BLUE_E, fill_opacity=0.8).set_stroke(width=3)
            ptr_rect = Rectangle(width=0.75, height=1.0, color=GREY_E, fill_opacity=0.8).set_stroke(width=3)
            ptr_rect.next_to(data_rect, RIGHT, buff=0)
            
            node_value_text = Text(val, color=WHITE).move_to(data_rect.get_center())
            
            current_node = VGroup(data_rect, ptr_rect, node_value_text)
            
            # Position nodes
            current_node.move_to(ORIGIN + LEFT * 4 + RIGHT * (i * 3))
            
            if len(nodes) > 0: # If not the first node, connect it
                # The VGroup `nodes` contains previous node VGroups AND arrows.
                # The structure is [node_0_VGroup, arrow_0_to_1_Mobject, node_1_VGroup, ...]
                # To get the previous node VGroup, we need to access `nodes[-2]` if the last element added was a node.
                # Careful indexing: after adding node (first element of this loop), it's nodes[-1].
                # If we're drawing arrow to `current_node`, `nodes` is `[node0]` when `i=1`
                # If `nodes` contains `[node_0, arrow_01, node_1]`, then `prev_ptr_box` of `node_1` needs `nodes[-1][1]`
                # However, in this loop, `nodes.add(arrow)` happens before `nodes.add(current_node)` for subsequent nodes.
                # The `current_node` is added to `nodes` after the `arrow`.
                # So, `nodes` contains `[node_0, arrow_01, node_1, arrow_12, node_2]` for `i=2`.
                # For `i=1`: `nodes` is `[node_0]` before arrow and node_1 are added.
                # `prev_node_vgroup` should be `nodes[-1]`
                prev_node_vgroup = nodes[-1] 
                prev_ptr_box = prev_node_vgroup[1] # Get the pointer rectangle of the previous node
                
                arrow = Arrow(prev_ptr_box.get_center(), current_node[0].get_left(), buff=0.1, color=RED, stroke_width=5)
                nodes.add(arrow) # Add arrow to the VGroup holding all elements
                animations.append(Create(arrow, run_time=1))
                if animations:
                    self.play(*animations)
                self.wait(0.5)
                animations.clear()

            nodes.add(current_node) # Add current node VGroup
            animations.append(FadeIn(current_node, shift=UP, run_time=1))
            if animations:
                self.play(*animations)
            self.wait(0.5)
            animations.clear()
        
        # Fade out single node anatomy
        animations.append(FadeOut(node_elements, run_time=1))
        if animations:
            self.play(*animations)
        self.wait(0.5)
        animations.clear()

        # Introduce Head pointer
        head_text = Text("HEAD", color=YELLOW_A).next_to(nodes[0], UP, buff=0.5) # nodes[0] is the first node VGroup
        head_arrow = Arrow(head_text.get_bottom(), nodes[0][0].get_top(), buff=0.1, color=YELLOW_A)
        
        animations.append(FadeIn(head_text, shift=UP, run_time=1))
        animations.append(Create(head_arrow, run_time=1))
        if animations:
            self.play(*animations)
        self.wait(1.5)
        animations.clear()

        # Show None at the end
        none_text = Text("NULL / None", color=WHITE, font_size=30).next_to(nodes[-1][1], RIGHT, buff=0.5) # nodes[-1] is the last node VGroup
        none_arrow = Arrow(nodes[-1][1].get_center(), none_text.get_left(), buff=0.1, color=WHITE)
        animations.append(Write(none_text, run_time=1))
        animations.append(Create(none_arrow, run_time=1))
        if animations:
            self.play(*animations)
        self.wait(2)
        animations.clear()
        
        # Prepare for next scene
        elements_to_fade_out = VGroup(node_title, head_text, head_arrow, none_text, none_arrow, nodes)
        animations.append(FadeOut(elements_to_fade_out, run_time=1.5))
        if animations:
            self.play(*animations)
        self.wait(0.5)

    # NARRATION: This method demonstrates practical operations on a linked list.
    # We will start by visualizing how a new node can be easily added to the end of an existing list, showing the pointer redirection required.
    # Following this, we will illustrate the traversal process, where we move from node to node using their 'next' pointers, effectively accessing each element sequentially.
    # This section aims to solidify the understanding of linked list dynamics and their flexibility compared to static arrays.
    def examples_and_traversal(self):
        animations = []

        example_title = Text("Examples: Building & Traversing", color=PURPLE_A).scale(1.1).to_edge(UP)
        animations.append(Write(example_title, run_time=1.2))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        # Recreate a small list for examples
        # To ensure clean indexing, let's build the VGroup with only nodes and arrows, then add head/null labels separately.
        # This will make `nodes_elements` contain only: [node0, arrow01, node1, arrow12, node2]
        nodes_elements = VGroup()
        node_values_ex = ["10", "20", "30"]
        
        head_ex_text = Text("HEAD", color=YELLOW_A)
        
        # Store actual node VGroups for later reference without mixing in arrows/labels
        actual_nodes = [] 
        
        for i, val in enumerate(node_values_ex):
            data_rect = Rectangle(width=1.5, height=1.0, color=BLUE_E, fill_opacity=0.8).set_stroke(width=3)
            ptr_rect = Rectangle(width=0.75, height=1.0, color=GREY_E, fill_opacity=0.8).set_stroke(width=3)
            ptr_rect.next_to(data_rect, RIGHT, buff=0)
            node_value_text = Text(val, color=WHITE).move_to(data_rect.get_center())
            current_node_vgroup = VGroup(data_rect, ptr_rect, node_value_text)
            
            # Position nodes
            current_node_vgroup.move_to(ORIGIN + LEFT * 3.5 + RIGHT * (i * 3.0)) 
            
            if i == 0:
                head_ex_text.next_to(current_node_vgroup, UP, buff=0.5)
                head_ex_arrow = Arrow(head_ex_text.get_bottom(), current_node_vgroup[0].get_top(), buff=0.1, color=YELLOW_A)
                animations.append(FadeIn(head_ex_text, run_time=0.8))
                animations.append(Create(head_ex_arrow, run_time=0.8))
                
            else:
                prev_ptr_box = actual_nodes[-1][1] # Get pointer rect of previous actual node VGroup
                arrow = Arrow(prev_ptr_box.get_center(), current_node_vgroup[0].get_left(), buff=0.1, color=RED, stroke_width=5)
                nodes_elements.add(arrow) # Add arrow
                animations.append(Create(arrow, run_time=0.8))

            nodes_elements.add(current_node_vgroup) # Add current node
            actual_nodes.append(current_node_vgroup) # Keep track of actual node VGroups
            animations.append(FadeIn(current_node_vgroup, run_time=0.8))
            
            if animations:
                self.play(*animations)
            self.wait(0.5)
            animations.clear()

        # Add initial NULL
        none_ex_text = Text("NULL", color=WHITE, font_size=30).next_to(actual_nodes[-1][1], RIGHT, buff=0.5)
        none_ex_arrow = Arrow(actual_nodes[-1][1].get_center(), none_ex_text.get_left(), buff=0.1, color=WHITE)
        animations.append(Write(none_ex_text, run_time=0.8))
        animations.append(Create(none_ex_arrow, run_time=0.8))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        # Group all initial elements for later fade out
        initial_list_elements = VGroup(nodes_elements, head_ex_text, head_ex_arrow, none_ex_text, none_ex_arrow)

        # Add a new node (e.g., "40")
        add_node_text = Text("Adding a new node ('40')", font_size=36).next_to(example_title, DOWN, buff=0.5)
        animations.append(Write(add_node_text, run_time=1.2))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        new_data_rect = Rectangle(width=1.5, height=1.0, color=BLUE_E, fill_opacity=0.8).set_stroke(width=3)
        new_ptr_rect = Rectangle(width=0.75, height=1.0, color=GREY_E, fill_opacity=0.8).set_stroke(width=3)
        new_ptr_rect.next_to(new_data_rect, RIGHT, buff=0)
        new_node_value_text = Text("40", color=WHITE).move_to(new_data_rect.get_center())
        new_node_vgroup = VGroup(new_data_rect, new_ptr_rect, new_node_value_text).move_to(ORIGIN + RIGHT * 6.5)
        
        animations.append(FadeIn(new_node_vgroup, shift=UP, run_time=1))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()
        
        # Remove old NULL arrow and text
        animations.append(FadeOut(none_ex_text, run_time=0.8))
        animations.append(FadeOut(none_ex_arrow, run_time=0.8))
        if animations:
            self.play(*animations)
        self.wait(0.5)
        animations.clear()

        # Create new arrow from last node to new node
        last_actual_node_ptr_box = actual_nodes[-1][1] # The pointer rect of "30" node
        
        new_connecting_arrow = Arrow(last_actual_node_ptr_box.get_center(), new_node_vgroup[0].get_left(), buff=0.1, color=RED, stroke_width=5)
        animations.append(Create(new_connecting_arrow, run_time=1))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        # New NULL for the added node
        new_none_text = Text("NULL", color=WHITE, font_size=30).next_to(new_node_vgroup[1], RIGHT, buff=0.5)
        new_none_arrow = Arrow(new_node_vgroup[1].get_center(), new_none_text.get_left(), buff=0.1, color=WHITE)
        animations.append(Write(new_none_text, run_time=0.8))
        animations.append(Create(new_none_arrow, run_time=0.8))
        if animations:
            self.play(*animations)
        self.wait(2)
        animations.clear()

        # Fade out adding node text to prepare for traversal
        animations.append(FadeOut(add_node_text, run_time=0.8))
        if animations:
            self.play(*animations)
        self.wait(0.5)
        animations.clear()

        # Now for traversal
        traversal_text = Text("Traversal: Visiting each node", font_size=36).next_to(example_title, DOWN, buff=0.5)
        animations.append(Write(traversal_text, run_time=1.2))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        # Highlight nodes during traversal
        all_nodes_in_order = actual_nodes + [new_node_vgroup] # All actual node VGroups
        
        # Add all new nodes/arrows to a VGroup for easier fadeout later
        full_list_elements = VGroup(initial_list_elements, new_node_vgroup, new_connecting_arrow, new_none_text, new_none_arrow)

        for node_obj in all_nodes_in_order:
            box_to_highlight = node_obj[0] # The data rectangle
            animations.append(box_to_highlight.animate.set_stroke(color=GREEN_A, width=6, run_time=0.8))
            if animations:
                self.play(*animations)
            self.wait(0.8)
            animations.clear()
            animations.append(box_to_highlight.animate.set_stroke(color=BLUE_E, width=3, run_time=0.8)) # Reset color
            if animations:
                self.play(*animations)
            animations.clear() 

        self.wait(1)
        
        # Prepare for next scene
        elements_to_fade_out_ex = VGroup(example_title, traversal_text, full_list_elements)
        animations.append(FadeOut(elements_to_fade_out_ex, run_time=1.5))
        if animations:
            self.play(*animations)
        self.wait(0.5)

    # NARRATION: Finally, let's explore some practical applications of linked lists in real-world scenarios.
    # Linked lists are not just theoretical constructs; they are used in various computing tasks, often when dynamic size and efficient insertions/deletions are paramount.
    # We will briefly touch upon how they are used in everyday software, highlighting their versatility and importance in building robust systems.
    def applications(self):
        animations = []

        app_title = Text("Applications of Linked Lists", color=ORANGE_A).scale(1.1).to_edge(UP)
        animations.append(Write(app_title, run_time=1.2))
        if animations:
            self.play(*animations)
        self.wait(1)
        animations.clear()

        app1 = Text("1. Music Playlists (adding/removing songs)", font_size=36).next_to(app_title, DOWN, buff=0.8).to_edge(LEFT)
        animations.append(Write(app1, run_time=1.5))
        if animations:
            self.play(*animations)
        self.wait(1.5)
        animations.clear()

        app2 = Text("2. Browser History (back/forward navigation)", font_size=36).next_to(app1, DOWN, buff=0.5).to_edge(LEFT)
        animations.append(Write(app2, run_time=1.5))
        if animations:
            self.play(*animations)
        self.wait(1.5)
        animations.clear()

        app3 = Text("3. Undo/Redo Functionality in Software", font_size=36).next_to(app2, DOWN, buff=0.5).to_edge(LEFT)
        animations.append(Write(app3, run_time=1.5))
        if animations:
            self.play(*animations)
        self.wait(1.5)
        animations.clear()

        conclusion_text = Text("Linked Lists: Flexible and Powerful!", color=YELLOW).scale(1.2).move_to(ORIGIN)
        animations.append(ReplacementTransform(VGroup(app1, app2, app3, app_title), conclusion_text, run_time=1.5))
        if animations:
            self.play(*animations)
        self.wait(2)
        animations.clear()


    def construct(self):
        self.introduce_linked_lists()
        self.core_understanding_nodes()
        self.examples_and_traversal()
        self.applications()

        self.play(FadeOut(*self.mobjects), run_time=1.5) # Final fade out of all remaining objects
        self.wait(0.5)