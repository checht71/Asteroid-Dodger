import time
import random
import torch
from core.game import AsteroidDodger
from AI.agent import Agent
import core.constants
from AI.model import RocketNet
from AI.hyperparameters import *


env = AsteroidDodger(AI_PLAYING=True, HUMAN_PLAYING=False, training=True)

observation, info = env.reset_game()


agent = Agent(env, dropout=dropout, hidden_layer=hidden_layer,
              learning_rate=learning_rate, step_repeat=step_repeat,
              gamma=gamma)

device = 'cuda:0' if torch.cuda.is_available() else 'cpu' 

model = RocketNet(action_dim=env.action_space.n, hidden_dim=hidden_layer, observation_shape=observation.shape).to(device)
model.load_state_dict(torch.load('models/dqn_C_42.pt', map_location=device))
model.to(device)


model.eval()

for episode in range(episodes):
    done = False
    episode_reward = 0
    state, info = env.reset_game()
    episode_steps = 0

    episode_start_time = time.time()

    while not done and episode_steps < max_episode_steps:
        if random.random() < epsilon:
            action = env.action_space.sample()
        else:
            model1_q_values = model.forward(state.unsqueeze(0).to(device))[0]

            q_values = torch.min(model1_q_values, model2_q_values)

            action = torch.argmax(q_values, dim=-1, keepdim=True)
        
        next_state, reward, done, truncated = env.ai_step(action=action, repeat=step_repeat)

        state = next_state

        episode_reward += reward
        episode_steps += 1
    
    episode_time = time.time() - episode_start_time


    print(f"Completed episode {episode} with score {episode_reward}")
    print(f"Episode Time: {episode_time:1f} seconds")
    print(f"Episode Steps: {episode_steps}") 