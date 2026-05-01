import pygame
from random import randint
from core.entities.coin import Coin
from core.entities.star import Star
from core.entities.meteor import Meteor
from core.entities.player import Player
from core.gamestates import show_highscore_screen, update_highscores
import core.constants as constants
from core.music import change_music
from game import AsteroidDodger


PLAYER_AI = True
PLAYER_HUMAN = True


game = AsteroidDodger(PLAYER_AI, PLAYER_HUMAN)


observation, reward = game._reset_game()

while True:

    action = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYUP: # Do not give the AI speed boost
            if pygame.key.name(event.key) == 'left shift':
                game.player_human.set_default_speed()

    keys = pygame.key.get_pressed()

    # Handle AI input
    if keys[pygame.K_i]:
        action = 1
    if keys[pygame.K_k]:
        action = 2
    if keys[pygame.K_j]:
        action = 3
    if keys[pygame.K_l]:
        action = 4

    if PLAYER_HUMAN:
        game.player_human.check_movement(keys, game.dt, game.game_difficulty_speed)
    
    if PLAYER_AI:
        game.player_ai.check_movement(action, game.dt, game.game_difficulty_speed)

    observation, reward, done, truncated = game.step(action=action)
    