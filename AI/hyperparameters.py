# Model parameters
episodes = 100
max_episode_steps = 500
total_steps = 0
step_repeat = 2 # frames before action
max_episode_steps = max_episode_steps / step_repeat

batch_size = 128 # smaller = less stability, less memory
learning_rate = 0.0001 # how quick the network readjusts
epsilon = 0.1 # 1 = explore, 0 = exploit
min_epsilon = 0.1
epsilon_decay = 1 # e * decay = e'
gamma = 0.99 # discount factor, 1 =  long term plan, 0 = short term

hidden_layer = 1024
dropout = 0.2

# Replay Buffer
buffer_max_size = 500 # higher = long term planning

# Rewards
reward_punishment = -5
reward_scaling = 0.1 # prevent overly large rewards

# testing
HIDE_SCREEN = False

agent_batch = "E" # model version