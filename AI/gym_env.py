import gym
from gym import spaces
import numpy as np
import pygame
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class PlayerControlEnv(gym.Env):
    metadata = {'render_modes': ['human']}
    
    def __init__(self, render_mode=None):
        super(PlayerControlEnv, self).__init__()
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.render_mode = render_mode
        
        # Create player
        self.player = Player(self.screen)
        
        # Define action and observation spaces
        # Actions: 0=up, 1=down, 2=left, 3=right, 4=boost, 5=no-op
        self.action_space = spaces.Discrete(6)
        
        # Observations: player x, player y, player speed_boost (normalized)
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0]),
            high=np.array([SCREEN_WIDTH, SCREEN_HEIGHT, 1]),
            dtype=np.float32
        )
        
        self.game_difficulty_speed = 0
        self.step_count = 0
        self.max_steps = 1000
    
    def reset(self):
        self.player.reset()
        self.step_count = 0
        return self._get_observation()
    
    def step(self, action):
        self.step_count += 1
        dt = self.clock.tick(60) / 1000.0
        
        # Convert action to key presses
        keys = [False] * 512
        keys[pygame.K_w] = action == 0
        keys[pygame.K_s] = action == 1
        keys[pygame.K_a] = action == 2
        keys[pygame.K_d] = action == 3
        keys[pygame.K_LSHIFT] = action == 4
        
        # Update player
        self.player.check_movement(keys, dt, self.game_difficulty_speed)
        
        # Calculate reward (example: reward staying in center)
        center_x = SCREEN_WIDTH / 2
        center_y = SCREEN_HEIGHT / 2
        distance_to_center = np.sqrt(
            (self.player.pos.x - center_x)**2 + 
            (self.player.pos.y - center_y)**2
        )
        reward = -distance_to_center / 1000  # Negative distance as reward
        
        # Check if episode is done
        done = self.step_count >= self.max_steps
        
        # Render if needed
        if self.render_mode == 'human':
            self.render()
        
        return self._get_observation(), reward, done, False, {}
    
    def _get_observation(self):
        return np.array([
            self.player.pos.x,
            self.player.pos.y,
            self.player.speed_boost
        ], dtype=np.float32)
    
    def render(self):
        self.screen.fill((0, 0, 0))
        self.player.draw()
        pygame.display.flip()
    
    def close(self):
        pygame.quit()
