from AI.model import RocketNet, hard_update, soft_update
from AI.buffer import ReplayBuffer
import torch
import torch.optim as optim
import torch.nn.functional as F
import datetime
import time
import random
import os
from core.game import AsteroidDodger
from pympler import asizeof
from AI.hyperparameters import buffer_max_size
import csv


class Agent():

    def __init__(self, env : AsteroidDodger, dropout, hidden_layer, learning_rate, step_repeat, gamma):
        """Initialize the DQN agent with one model, optimizers, and a replay buffer."""
        self.env = env

        self.step_repeat = step_repeat

        self.gamma = gamma

        observation, info = self.env.reset_game()

        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

        print("Model loaded on: ", self.device)

        self.memory = ReplayBuffer(max_size=buffer_max_size, input_shape=observation.shape, n_actions=env.action_space.n, device=self.device)

        self.model = RocketNet(action_dim=env.action_space.n, hidden_dim=hidden_layer, dropout=dropout, observation_shape=observation.shape).to(self.device)
        self.target_model = RocketNet(action_dim=env.action_space.n, hidden_dim=hidden_layer, dropout=dropout, observation_shape=observation.shape).to(self.device)  

        hard_update(self.target_model, self.model)

        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

        self.learning_rate = learning_rate

        print(f"Memory Size: {asizeof.asizeof(self.memory) / (1024 * 1024 * 1024):2f} Gb")

    
    def train(self, episodes, max_episode_steps, batch_size, epsilon, epsilon_decay, min_epsilon, 
              validation_interval=4, patience=100, min_delta=0.0):
        """Train the DDQN agent for a specified number of episodes with early stopping.
        
        Args:
            episodes: Maximum number of episodes to train
            max_episode_steps: Maximum steps per episode
            batch_size: Batch size for training
            epsilon: Initial exploration rate
            epsilon_decay: Decay factor for epsilon
            min_epsilon: Minimum epsilon value
            validation_interval: Evaluate every N episodes (default: 25)
            patience: Number of validation checks without improvement before stopping (default: 100)
            min_delta: Minimum improvement threshold for validation metric (default: 0.0)
        """

        if not os.path.exists('models'):
            os.makedirs('models')
        
        total_steps = 0

        for episode in range(episodes):

            done = False
            episode_reward = 0
            state, info = self.env.reset_game()
            episode_steps = 0

            episode_start_time = time.time()

            while not done and episode_steps < max_episode_steps:

                if random.random() < epsilon:
                    action = self.env.action_space.sample()
                else:
                    q_values = self.model.forward(state.unsqueeze(0).to(self.device))[0]
                    action = torch.argmax(q_values, dim=-1).item()
                
                next_state, reward, done, _ = self.env.ai_step(action=action, repeat=self.step_repeat)

                self.memory.store_transition(state, action, reward, next_state, done)

                state = next_state

                episode_reward += reward
                episode_steps += 1
                total_steps += 1

                if self.memory.can_sample(batch_size):
                    states, actions, rewards, next_states, dones = self.memory.sample_buffer(batch_size)

                    dones = dones.unsqueeze(1).float()

                    # Current Q values from both models
                    q_values = self.model(states)
                    actions = actions.unsqueeze(1).long()
                    qsa_b = q_values.gather(1, actions)

                    # Action selection using main models. 
                    next_actions = torch.argmax(self.model(next_states), dim=1, keepdim=True)

                    next_q_values = self.target_model(next_states).gather(1, next_actions)

                    # Compute the target value using DQN
                    target_b = rewards.unsqueeze(1) + (1 - done) * self.gamma * next_q_values

                    # Compute Loss
                    loss = F.smooth_l1_loss(qsa_b, target_b.detach())

                    # Backprop
                    self.model.zero_grad()
                    loss.backward()
                    self.optimizer.step()
                    
                    if episode_steps % 4 == 0:
                        soft_update(self.target_model, self.model)

            self.model.save_the_model(filename=f'models/dqn_{AI.hyperparameters.agent_batch}_{episode}.pt')

            if epsilon > min_epsilon:
                epsilon *= epsilon_decay

            episode_time = time.time() - episode_start_time

            print(f"Completed episode {episode} with score {episode_reward}")
            print(f"Episode Time: {episode_time:1f} seconds")
            print(f"Episode Steps: {episode_steps}")
            print(f"Loss: {loss}")
                
            # Write to CSV
            with open(f'episode_results_{AI.hyperparameters.agent_batch}.csv', 'a', newline='\n') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Episode', 'Score', 'Loss', 'Time (seconds)', 'Steps'])
                writer.writerow({
                    'Episode': episode,
                    'Score': episode_reward,
                    'Loss': loss,
                    'Time (seconds)': episode_time,
                    'Steps': episode_steps,
                })

        print(f"\nTraining completed!")
        print(f"Total episodes trained: {episode + 1}")
