from stable_baselines3 import PPO
from gym_env import PlayerControlEnv

# Create environment
env = PlayerControlEnv(render_mode='human')

# Create and train agent
model = PPO('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=100000)

# Save model
model.save("player_control_model")

# Test trained model
obs, _ = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    env.render()
    if done:
        obs, _ = env.reset()

env.close()
