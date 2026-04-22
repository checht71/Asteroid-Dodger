import pygame
from random import randint
from core.entities import Meteor, Star, Player, Coin
from core.gamestates import show_highscore_screen, update_highscores
import core.constants as constants
from core.music import change_music
from game import AsteroidDodger

game = AsteroidDodger()

while True:
    """Handle pygame events (quit, key press, etc.)."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYUP:
            if pygame.key.name(event.key) == 'left shift':
                game.player_human.set_default_speed()
    game.step()
