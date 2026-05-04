from core.game import AsteroidDodger
from AI.agent import Agent
import core.constants
from AI.hyperparameters import *



env = AsteroidDodger(AI_PLAYING=True, HUMAN_PLAYING=False, training=True)


agent = Agent(env, dropout=dropout, hidden_layer=hidden_layer,
              learning_rate=learning_rate, step_repeat=step_repeat,
              gamma=gamma)

agent.train(episodes=episodes, max_episode_steps=max_episode_steps,
            batch_size=batch_size, epsilon=epsilon, epsilon_decay=epsilon_decay, min_epsilon=min_epsilon)
