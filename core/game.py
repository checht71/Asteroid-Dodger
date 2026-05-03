import pygame
from random import randint
from core.entities.coin import Coin
from core.entities.star import Star
from core.entities.meteor import Meteor
from core.entities.player import Player, Player_AI
from core.gamestates import show_highscore_screen, update_highscores
import core.constants as constants
from core.music import change_music
import numpy as np
import cv2
import torch
import gymnasium as gym
import os

class AsteroidDodger():

    # init
    def __init__(self, AI_PLAYING, HUMAN_PLAYING, training=False):
        self.AI_TRAINING = training
        self.AI_PLAYING = AI_PLAYING
        if AI_PLAYING or self.AI_TRAINING:
            self._init_ai()
        self._init_pygame()
        self._init_player(AI_PLAYING, HUMAN_PLAYING)
        self._init_sprites()
        self._init_log()
        if HUMAN_PLAYING:
            self._init_audio()

    def _init_pygame(self):
        """Initialize pygame display, clock and game state vars."""
        pygame.init()
        pygame.display.set_caption('Asteroid Belt')
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont(constants.FONT_TYPE, constants.FONT_SIZE)
        self.score = 0.0
        self.running = True
        self.dt = 0
        self.game_difficulty_speed = constants.GAME_DIFFICULTY_SPEED_STARTING

    def _init_audio(self):
        """Initialize audio and load music."""
        pygame.mixer.init()
        pygame.mixer.music.load(constants.INGAME_MUSIC)
        pygame.mixer.music.play(-1)

    def _init_player(self, AI_PLAYING, HUMAN_PLAYING):
        """Initialize human and AI players."""
        self.players = []
        
        if HUMAN_PLAYING:
            self.player_human = Player(self.screen)
            self.players.append(self.player_human)
        
        if AI_PLAYING:
            self.player_ai = Player_AI(self.screen)
            self.players.append(self.player_ai)

    def _init_sprites(self):
        """Initialize obstacles, stars, and coins."""
        self.obstacle = [Meteor(self.screen) for i in range(constants.METEORS_MAX)]
        self.num_obstacles = constants.METEORS_MINIMUM
        self.stars = [Star(self.screen) for i in range(constants.MAX_STARS)]
        self.coin_spawned = False
        self.points_coin = None

    def _init_log(self):
        """Point to the locations we are saving highscores"""
        if self.AI_TRAINING:
            self.log_location_scores = constants.SCORES_LOG_AI
            self.log_location_highscores = constants.HIGHSCORES_LOG_AI
        else:
            self.log_location_scores = constants.SCORES_LOG_HUMAN
            self.log_location_highscores = constants.HIGHSCORES_LOG_HUMAN

    def _init_ai(self):
        self.done = False
        self.total_frames = 0
        self.action_space = gym.spaces.Discrete(4)
        #if self.AI_TRAINING:
            #os.environ["SDL_VIDEODRIVER"] = "dummy"

    
    
    def step(self, action):
        """Main game loop step."""
        if self.AI_PLAYING:
            self.total_frames += 1
        self.done = False

        reward, truncated = 0, False

        self._draw_background_and_score()
        self._update_coin()
        self._draw_and_move_player()
        self._draw_and_move_stars()
        reward = self._draw_move_and_check_obstacles()
        self._update_display()
        self._update_physics()
        self._check_difficulty_progression()

        if self.AI_TRAINING:
            self.player_ai.check_movement(action, self.dt, self.game_difficulty_speed)

        return reward, self.done, truncated


    def ai_step(self, action, repeat=4):
        """This feeds the AI agent 1/repeat frames"""
        total_reward = 0

        for i in range(repeat):
            reward, done, truncated = self.step(action)
        
        total_reward = reward
    
        return self._get_obs(), total_reward, self.done, truncated


    def _draw_background_and_score(self):
        """Draw background and render score text."""
        self.screen.fill("black")
        self.score_text = self.FONT.render(str(round(self.score) * 10), True, constants.FONT_COLOR)
        self.screen.blit(self.score_text, (10, 10))

    def _update_coin(self):
        """Update coin position and check for collision with any player."""
        if self.coin_spawned:
            self.points_coin.draw(self.coin_spawned)
            self.points_coin.move(self.dt, self.game_difficulty_speed)

            for player in self.players:
                if player.drawing.collidelist([self.points_coin.drawing]) != -1:
                    self.score += self.points_coin.SCORE_VALUE
                    self.coin_spawned = False
                    return

    def _draw_and_move_player(self):
        """Draw and update all active players."""
        for player in self.players:
            player.draw()

    def _draw_and_move_stars(self):
        """Draw and move all stars."""
        for astar in self.stars:
            astar.draw()
            astar.move(self.dt, self.game_difficulty_speed)

    def _draw_move_and_check_obstacles(self):
        """Draw, move obstacles, and check for collision with players."""
        reward = 1  # Default reward for no collision
        
        for x in range(self.num_obstacles):
            self.obstacle[x].draw()
            self.obstacle[x].move(self.dt, self.game_difficulty_speed)

            for player in self.players:
                if player.drawing.collidelist([self.obstacle[x].drawing]) != -1:
                    # Collision detected
                    if self.AI_TRAINING:
                        return -1
                    else:
                        self._handle_game_over()
                        return 0
    

    def _handle_game_over(self):
        """Handle collision and game over sequence."""
        if not self.AI_TRAINING:
            change_music(constants.MENU_MUSIC)
        self.done = True
        
        highscores_list, highscore_rank = update_highscores(
            self.score, 
            self.screen,
            self.log_location_scores, 
            self.log_location_highscores
        )
        
        if not self.AI_TRAINING:
            show_highscore_screen(self.screen, highscores_list, highscore_rank, self.FONT)
            change_music(constants.INGAME_MUSIC)

        self.reset_game()


    def reset_game(self):
        """Reset all game state variables and entities."""
        self.score = 0
        self.game_difficulty_speed = constants.GAME_DIFFICULTY_SPEED_STARTING
        self.num_obstacles = constants.METEORS_MINIMUM
        self.coin_spawned = False
        
        for obstacle in self.obstacle:
            obstacle.reset()
        
        for player in self.players:
            player.reset()
        
        self.done = False

        return self._get_obs(), self.score

    def _update_display(self):
        """Update the display."""
        pygame.display.flip()

    def _update_physics(self):
        """Update frame timing and game progression."""
        self.dt = self.clock.tick(60) / 1000
        self.score += constants.SCORE_PER_TICK
        self.game_difficulty_speed += constants.GAME_SPEED_INCREASE_PER_TICK

    def _check_difficulty_progression(self):
        """Check for difficulty increases and spawn coins."""
        self._increase_obstacle_count()
        if constants.COIN_ENABLED: 
            self._spawn_coin()

    def _increase_obstacle_count(self):
        """Increase obstacle count based on score."""
        if (round(self.score, 1) % 50 == 0.0 and 
            self.score >= 10.0 and 
            self.num_obstacles < constants.METEORS_MAX):
            self.num_obstacles += 1

    def _spawn_coin(self):
        """Spawn a coin if conditions are met."""
        if round(self.score, 1) % 50 == 0.0 and not self.coin_spawned:
            self.points_coin = Coin(self.screen)
            self.coin_spawned = True

    def _get_obs(self):
        screen_array = pygame.surfarray.pixels3d(self.screen)
        screen_array = np.transpose(screen_array, (1, 0, 2))
        downscaled_image = cv2.resize(screen_array, (128, 128), interpolation=cv2.INTER_NEAREST)

        # Save the image (Debugging purposes)
        # cv2.imwrite('screenshot.png', downscaled_image)

        grayscale = cv2.cvtColor(downscaled_image, cv2.COLOR_RGB2GRAY)

        observation = torch.from_numpy(grayscale).float().unsqueeze(0)

        return observation