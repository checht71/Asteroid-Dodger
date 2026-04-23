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


player_ai = False
player_human = True



game = AsteroidDodger(player_ai, player_human)

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

    """
    if keys[pygame.K_w]:
        action = 1
    if keys[pygame.K_s]:
        action = 2
    if keys[pygame.K_a]:
        action = 3
    if keys[pygame.K_d]:
        action = 4
    """

    game.player_human.check_movement(keys, game.dt, game.game_difficulty_speed)


    game.step(action=action)
