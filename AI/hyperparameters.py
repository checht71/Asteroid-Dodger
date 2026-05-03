# Model parameters
episodes = 10
max_episode_steps = 5000
total_steps = 0
step_repeat = 4
max_episode_steps = max_episode_steps / step_repeat

batch_size = 64
learning_rate = 0.001
epsilon = 1
min_epsilon = 0.1
epsilon_decay = 0.995
gamma = 0.99

hidden_layer = 1024
dropout = 0.2

# Replay Buffer
buffer_max_size = 100000 # bytes 

# Rewards
reward_punishment = -10

# testing
HIDE_SCREEN = False