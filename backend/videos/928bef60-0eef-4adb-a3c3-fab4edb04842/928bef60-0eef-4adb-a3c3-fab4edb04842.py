from manim import *

class CreateScene(Scene):
    def construct(self):
        # Set the theme for the scene
        self.camera.background_color = WHITE

        # Introduction
        title = Text("Blockchain Explained", font_size=60, color=BLUE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Concept of a Block
        block_title = Text("What is a Block?", color=BLACK)
        block_rect = Rectangle(width=4, height=3, color=BLUE, fill_opacity=0.2)
        data_text = Text("Data: Transactions", color=BLACK, font_size=24).move_to(block_rect.get_center() + UP * 0.5)
        hash_text = Text("Hash: SHA256(...) ", color=BLACK, font_size=24).move_to(block_rect.get_center() - DOWN * 0.5)
        block_group = VGroup(block_rect, data_text, hash_text, block_title).arrange(DOWN)

        self.play(Create(block_group))
        self.wait(2)
        self.play(FadeOut(block_group))

        # Concept of Hashing
        hashing_title = Text("Hashing Explained", color=BLACK)
        input_text = Text("Input: 'Hello World'", color=BLACK)
        arrow = Arrow(start=LEFT, end=RIGHT, color=GREEN)
        hash_function_text = Text("SHA256", color=RED)
        output_text = Text("Output: 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'", color=BLACK)

        hashing_group = VGroup(input_text, arrow, hash_function_text, output_text).arrange(RIGHT)
        hashing_group.to_edge(UP)
        self.play(Write(hashing_title.to_edge(UP+LEFT)))
        self.play(Write(hashing_group))
        self.wait(3)
        self.play(FadeOut(hashing_group), FadeOut(hashing_title))


        # Linking Blocks Together (Blockchain)
        blockchain_title = Text("Building the Blockchain", color=BLACK)
        self.play(Write(blockchain_title.to_edge(UP+LEFT)))
        block1 = Rectangle(width=4, height=3, color=BLUE, fill_opacity=0.2)
        block1_data = Text("Data: Txn 1", color=BLACK, font_size=24).move_to(block1.get_center() + UP * 0.5)
        block1_hash = Text("Hash: 0x123...", color=BLACK, font_size=24).move_to(block1.get_center() - DOWN * 0.5)
        block1_group = VGroup(block1, block1_data, block1_hash).move_to(LEFT * 5)

        block2 = Rectangle(width=4, height=3, color=BLUE, fill_opacity=0.2)
        block2_data = Text("Data: Txn 2", color=BLACK, font_size=24).move_to(block2.get_center() + UP * 0.5)
        block2_prev_hash = Text("Prev Hash: 0x123...", color=BLACK, font_size=18).move_to(block2.get_center() - DOWN * 0.7)
        block2_hash = Text("Hash: 0x456...", color=BLACK, font_size=24).move_to(block2.get_center() - DOWN * 0.2)
        block2_group = VGroup(block2, block2_data, block2_prev_hash, block2_hash).move_to(ORIGIN)

        block3 = Rectangle(width=4, height=3, color=BLUE, fill_opacity=0.2)
        block3_data = Text("Data: Txn 3", color=BLACK, font_size=24).move_to(block3.get_center() + UP * 0.5)
        block3_prev_hash = Text("Prev Hash: 0x456...", color=BLACK, font_size=18).move_to(block3.get_center() - DOWN * 0.7)
        block3_hash = Text("Hash: 0x789...", color=BLACK, font_size=24).move_to(block3.get_center() - DOWN * 0.2)
        block3_group = VGroup(block3, block3_data, block3_prev_hash, block3_hash).move_to(RIGHT * 5)

        arrow1 = Arrow(start=block1_group.get_right(), end=block2_group.get_left(), color=GREEN)
        arrow2 = Arrow(start=block2_group.get_right(), end=block3_group.get_left(), color=GREEN)

        self.play(Create(block1_group), Create(block2_group), Create(block3_group))
        self.play(Create(arrow1), Create(arrow2))
        self.wait(3)

        #Highlighting the linking between blocks with the previous hash
        self.play(Indicate(block2_prev_hash, color=YELLOW))
        self.play(Indicate(block1_hash, color=YELLOW))
        self.wait(1)
        self.play(Indicate(block3_prev_hash, color=YELLOW))
        self.play(Indicate(block2_hash, color=YELLOW))

        self.wait(3)
        self.play(FadeOut(block1_group), FadeOut(block2_group), FadeOut(block3_group), FadeOut(arrow1), FadeOut(arrow2), FadeOut(blockchain_title))

        # Distributed Ledger
        distributed_title = Text("Distributed Ledger", color=BLACK)
        self.play(Write(distributed_title.to_edge(UP+LEFT)))

        node1 = Circle(radius=1, color=BLUE, fill_opacity=0.2).move_to(LEFT * 4 + UP * 2)
        node2 = Circle(radius=1, color=BLUE, fill_opacity=0.2).move_to(RIGHT * 4 + UP * 2)
        node3 = Circle(radius=1, color=BLUE, fill_opacity=0.2).move_to(DOWN * 2)

        blockchain_replica1 = Rectangle(width=3, height=2, color=GREEN, fill_opacity=0.2).move_to(node1.get_center())
        blockchain_replica2 = Rectangle(width=3, height=2, color=GREEN, fill_opacity=0.2).move_to(node2.get_center())
        blockchain_replica3 = Rectangle(width=3, height=2, color=GREEN, fill_opacity=0.2).move_to(node3.get_center())

        node1_text = Text("Node 1", color=BLACK, font_size=20).next_to(node1, DOWN)
        node2_text = Text("Node 2", color=BLACK, font_size=20).next_to(node2, DOWN)
        node3_text = Text("Node 3", color=BLACK, font_size=20).next_to(node3, DOWN)
        blockchain_text = Text("Blockchain Copy", color=BLACK, font_size=16).move_to(blockchain_replica1.get_center())

        self.play(Create(node1), Create(node2), Create(node3))
        self.play(Create(node1_text), Create(node2_text), Create(node3_text))
        self.play(Create(blockchain_replica1), Create(blockchain_replica2), Create(blockchain_replica3))
        self.play(Write(blockchain_text.copy().move_to(blockchain_replica2.get_center())), Write(blockchain_text.copy().move_to(blockchain_replica3.get_center())))

        self.wait(3)
        self.play(FadeOut(node1), FadeOut(node2), FadeOut(node3), FadeOut(node1_text), FadeOut(node2_text), FadeOut(node3_text), FadeOut(blockchain_replica1), FadeOut(blockchain_replica2), FadeOut(blockchain_replica3), FadeOut(blockchain_text), FadeOut(distributed_title))

        # Consensus Mechanism
        consensus_title = Text("Consensus Mechanism", color=BLACK)
        self.play(Write(consensus_title.to_edge(UP+LEFT)))

        nodes = [Circle(radius=0.5, color=BLUE, fill_opacity=0.2).move_to(np.array([np.cos(2 * np.pi * i / 5) * 3, np.sin(2 * np.pi * i / 5) * 3, 0])) for i in range(5)]
        node_texts = [Text(f"Node {i+1}", color=BLACK, font_size=16).next_to(nodes[i], DOWN) for i in range(5)]

        self.play(*[Create(node) for node in nodes], *[Write(node_text) for node_text in node_texts])

        # Simulation of a transaction being proposed
        transaction_text = Text("New Transaction", color=GREEN)
        self.play(Write(transaction_text.move_to(UP)))
        self.wait(1)

        # Animate broadcasting to all nodes
        arrows_to_nodes = [Arrow(start=transaction_text.get_bottom(), end=node.get_top(), color=GREEN) for node in nodes]
        self.play(*[Create(arrow) for arrow in arrows_to_nodes])
        self.wait(2)
        self.play(*[FadeOut(arrow) for arrow in arrows_to_nodes])

        # Simulate nodes verifying the transaction and reaching consensus (e.g., Proof of Work)
        verifying_text = Text("Verifying...", color=ORANGE, font_size=24).move_to(DOWN)
        self.play(*[Write(verifying_text.copy().move_to(node.get_center())) for node in nodes])
        self.wait(2)
        self.play(*[FadeOut(Text("Verifying...", color=ORANGE, font_size=24).move_to(node.get_center())) for node in nodes])

        # Simulate block being added
        block_consensus = Rectangle(width=2, height=1.5, color=BLUE, fill_opacity=0.2).move_to(DOWN)
        block_consensus_text = Text("Block Added", color=BLACK, font_size=16).move_to(block_consensus.get_center())

        self.play(Create(block_consensus), Write(block_consensus_text))
        self.wait(2)

        self.play(FadeOut(verifying_text), FadeOut(transaction_text), FadeOut(block_consensus), FadeOut(block_consensus_text))
        self.play(*[FadeOut(node) for node in nodes], *[FadeOut(node_text) for node_text in node_texts], FadeOut(consensus_title))


        # Security and Immutability
        security_title = Text("Security & Immutability", color=BLACK)
        self.play(Write(security_title.to_edge(UP+LEFT)))

        block1_immutability = Rectangle(width=4, height=3, color=BLUE, fill_opacity=0.2).move_to(LEFT * 5)
        block1_data_immutability = Text("Data: Txn 1", color=BLACK, font_size=24).move_to(block1_immutability.get_center() + UP * 0.5)
        block1_hash_immutability = Text("Hash: 0x123...", color=BLACK, font_size=24).move_to(block1_immutability.get_center() - DOWN * 0.5)
        block1_group_immutability = VGroup(block1_immutability, block1_data_immutability, block1_hash_immutability)

        block2_immutability = Rectangle(width=4, height=3, color=BLUE, fill_opacity=0.2).move_to(ORIGIN)
        block2_data_immutability = Text("Data: Txn 2", color=BLACK, font_size=24).move_to(block2_immutability.get_center() + UP * 0.5)
        block2_prev_hash_immutability = Text("Prev Hash: 0x123...", color=BLACK, font_size=18).move_to(block2_immutability.get_center() - DOWN * 0.7)
        block2_hash_immutability = Text("Hash: 0x456...", color=BLACK, font_size=24).move_to(block2_immutability.get_center() - DOWN * 0.2)
        block2_group_immutability = VGroup(block2_immutability, block2_data_immutability, block2_prev_hash_immutability, block2_hash_immutability)

        block3_immutability = Rectangle(width=4, height=3, color=BLUE, fill_opacity=0.2).move_to(RIGHT * 5)
        block3_data_immutability = Text("Data: Txn 3", color=BLACK, font_size=24).move_to(block3_immutability.get_center() + UP * 0.5)
        block3_prev_hash_immutability = Text("Prev Hash: 0x456...", color=BLACK, font_size=18).move_to(block3_immutability.get_center() - DOWN * 0.7)
        block3_hash_immutability = Text("Hash: 0x789...", color=BLACK, font_size=24).move_to(block3_immutability.get_center() - DOWN * 0.2)
        block3_group_immutability = VGroup(block3_immutability, block3_data_immutability, block3_prev_hash_immutability, block3_hash_immutability)

        arrow1_immutability = Arrow(start=block1_group_immutability.get_right(), end=block2_group_immutability.get_left(), color=GREEN)
        arrow2_immutability = Arrow(start=block2_group_immutability.get_right(), end=block3_group_immutability.get_left(), color=GREEN)

        self.play(Create(block1_group_immutability), Create(block2_group_immutability), Create(block3_group_immutability), Create(arrow1_immutability), Create(arrow2_immutability))
        self.wait(2)

        #Attempting to tamper with block 2
        block2_data_tampered = Text("Data: Tampered", color=RED, font_size=24).move_to(block2_immutability.get_center() + UP * 0.5)
        self.play(ReplacementTransform(block2_data_immutability, block2_data_tampered))
        self.wait(1)
        self.play(block2_immutability.animate.set_color(RED), block2_hash_immutability.animate.set_color(RED))
        self.wait(1)
        self.play(arrow2_immutability.animate.set_color(RED), block3_immutability.animate.set_color(RED), block3_prev_hash_immutability.animate.set_color(RED), block3_hash_immutability.animate.set_color(RED))

        self.play(Write(Text("Change detected!", color=RED).to_edge(DOWN)))
        self.wait(3)
        self.play(FadeOut(block1_group_immutability), FadeOut(block2_group_immutability), FadeOut(block3_group_immutability), FadeOut(arrow1_immutability), FadeOut(arrow2_immutability), FadeOut(security_title), FadeOut(Text("Change detected!", color=RED).to_edge(DOWN)))

        # Conclusion
        conclusion_text = Text("Blockchain: Secure, Transparent, Decentralized", color=BLUE, font_size=48)
        self.play(Write(conclusion_text))
        self.wait(3)
        self.play(FadeOut(conclusion_text))

        end_text = Text("Thank you!", color=GREEN, font_size=60)
        self.play(Write(end_text))
        self.wait(2)
        self.play(FadeOut(end_text))
        self.wait(1)