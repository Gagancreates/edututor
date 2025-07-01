from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Text("What is Machine Learning?")
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title), run_time=0.75)

        # Defining Machine Learning
        definition = Tex("Machine Learning: ", "A field of computer science ", "that allows computers to learn ", "from data without being explicitly programmed.")
        definition[0].set_color(YELLOW)
        definition[1].set_color(BLUE)
        definition[2].set_color(GREEN)
        definition[3].set_color(RED)
        definition.scale(0.75)
        self.play(Write(definition), run_time=3)
        self.wait(2)
        self.play(FadeOut(definition), run_time=0.75)

        # Examples of Machine Learning
        examples_title = Text("Examples of Machine Learning")
        self.play(Write(examples_title), run_time=1)
        self.wait(1)

        example1 = Tex("1. Email Spam Detection")
        example2 = Tex("2. Image Recognition")
        example3 = Tex("3. Recommendation Systems")

        example1.move_to(UP)
        example2.move_to(ORIGIN)
        example3.move_to(DOWN)

        self.play(Write(example1), run_time=1)
        self.play(Write(example2), run_time=1)
        self.play(Write(example3), run_time=1)
        self.wait(2)

        self.play(FadeOut(examples_title, example1, example2, example3), run_time=0.75)

        # The Learning Process
        learning_title = Text("The Learning Process")
        self.play(Write(learning_title), run_time=1)
        self.wait(1)

        data = Tex("Data")
        model = Tex("Model")
        prediction = Tex("Prediction")

        arrow1 = Arrow(data.get_right(), model.get_left(), buff=0.2)
        arrow2 = Arrow(model.get_right(), prediction.get_left(), buff=0.2)

        data.move_to(LEFT * 3)
        prediction.move_to(RIGHT * 3)

        self.play(Write(data), run_time=0.75)
        self.play(Create(arrow1), run_time=1)
        self.play(Write(model), run_time=0.75)
        self.play(Create(arrow2), run_time=1)
        self.play(Write(prediction), run_time=0.75)
        self.wait(2)

        # Supervised Learning
        supervised_title = Text("Supervised Learning")
        supervised_title.move_to(UP * 3)
        self.play(Write(supervised_title), run_time=1)

        labeled_data = Tex("Labeled Data", color=GREEN)
        algorithm = Tex("Algorithm")
        trained_model = Tex("Trained Model")

        arrow3 = Arrow(labeled_data.get_right(), algorithm.get_left(), buff=0.2)
        arrow4 = Arrow(algorithm.get_right(), trained_model.get_left(), buff=0.2)

        labeled_data.move_to(LEFT * 3)
        trained_model.move_to(RIGHT * 3)

        self.play(Write(labeled_data), run_time=0.75)
        self.play(Create(arrow3), run_time=1)
        self.play(Write(algorithm), run_time=0.75)
        self.play(Create(arrow4), run_time=1)
        self.play(Write(trained_model), run_time=0.75)
        self.wait(2)

        self.play(FadeOut(learning_title, data, model, prediction, arrow1, arrow2, supervised_title, labeled_data, algorithm, trained_model, arrow3, arrow4), run_time=0.75)

        # Unsupervised Learning
        unsupervised_title = Text("Unsupervised Learning")
        unsupervised_title.move_to(UP * 3)
        self.play(Write(unsupervised_title), run_time=1)

        unlabeled_data = Tex("Unlabeled Data", color=RED)
        discovery = Tex("Pattern Discovery")

        arrow5 = Arrow(unlabeled_data.get_right(), discovery.get_left(), buff=0.2)

        unlabeled_data.move_to(LEFT * 3)
        discovery.move_to(RIGHT * 3)

        self.play(Write(unlabeled_data), run_time=0.75)
        self.play(Create(arrow5), run_time=1)
        self.play(Write(discovery), run_time=0.75)
        self.wait(2)

        self.play(FadeOut(unsupervised_title, unlabeled_data, discovery, arrow5), run_time=0.75)

        # Reinforcement Learning
        reinforcement_title = Text("Reinforcement Learning")
        reinforcement_title.move_to(UP * 3)
        self.play(Write(reinforcement_title), run_time=1)
        self.wait(1)

        agent = Tex("Agent")
        environment = Tex("Environment")
        action = Tex("Action")
        reward = Tex("Reward")

        agent.move_to(LEFT * 3 + UP)
        environment.move_to(RIGHT * 3 + UP)
        action.move_to(DOWN)
        reward.move_to(DOWN + RIGHT*3)

        arrow_env_agent = Arrow(environment.get_left(), agent.get_right(), buff=0.2)
        arrow_agent_action = Arrow(agent.get_bottom(), action.get_top(), buff=0.2)
        arrow_action_env = Arrow(action.get_right(), environment.get_bottom(), buff=0.2)
        arrow_env_reward = Arrow(environment.get_bottom(), reward.get_top(), buff=0.2)

        self.play(Write(agent), run_time=0.75)
        self.play(Write(environment), run_time=0.75)
        self.play(Create(arrow_env_agent), run_time=1)
        self.play(Write(action), run_time=0.75)
        self.play(Create(arrow_agent_action), run_time=1)
        self.play(Create(arrow_action_env), run_time=1)
        self.play(Write(reward), run_time=0.75)
        self.play(Create(arrow_env_reward), run_time=1)

        self.wait(3)

        self.play(FadeOut(reinforcement_title, agent, environment, action, reward, arrow_agent_action, arrow_env_agent, arrow_action_env, arrow_env_reward), run_time=0.75)

        # Conclusion
        conclusion = Text("Machine Learning is a powerful tool!", color=GREEN)
        self.play(Write(conclusion), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(*self.mobjects), run_time=1)