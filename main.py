import pygame
from random import randint
from core.entities import Meteor, Star, Player, Coin
from core.gamestates import show_highscore_screen, update_highscores
import core.constants as constants
from core.music import change_music
from core.functions import (draw_game_state, handle_coin_logic, handle_meteor_logic, 
                       reset_game_state, handle_events, update_game_difficulty)


# pygame setup
pygame.init()
pygame.display.set_caption('Asteroid Belt')
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
clock = pygame.time.Clock()
score = 0.0
running = True
dt = 0
game_difficulty_speed = constants.GAME_DIFFICULTY_SPEED_STARTING

# Music setup
pygame.mixer.init()
pygame.mixer.music.load(constants.INGAME_MUSIC)
pygame.mixer.music.play(-1)

# Player init
player_human = Player(screen)
FONT = pygame.font.SysFont(constants.FONT_TYPE, constants.FONT_SIZE)

# Sprite init
meteor = [Meteor(screen) for i in range(constants.METEORS_MAX)]
num_meteors = constants.METEORS_MINIMUM
stars = [Star(screen) for i in range(constants.MAX_STARS)]
coin_spawned = False
points_coin = None

# AI setup
TRAINING_AI = False
if TRAINING_AI:
    log_location_scores = constants.SCORES_LOG_AI
    log_location_highscores = constants.HIGHSCORES_LOG_AI
else:
    log_location_scores = constants.SCORES_LOG_HUMAN
    log_location_highscores = constants.HIGHSCORES_LOG_HUMAN

# Main game loop
while running:
    # Draw game state
    draw_game_state(screen, player_human, stars, meteor, num_meteors, points_coin, coin_spawned, score, FONT, dt, game_difficulty_speed)

    # Handle coin logic
    score, coin_spawned = handle_coin_logic(coin_spawned, points_coin, player_human, dt, game_difficulty_speed, score)

    # Handle meteor collision
    if handle_meteor_logic(meteor, num_meteors, player_human, dt, game_difficulty_speed, score):
        score = reset_game_state(player_human, meteor, num_meteors, score, screen, FONT, TRAINING_AI, log_location_scores, log_location_highscores)
        game_difficulty_speed = constants.GAME_DIFFICULTY_SPEED_STARTING
        num_meteors = constants.METEORS_MINIMUM
        coin_spawned = False

    # Poll for events
    for event in pygame.event.get():
        running = handle_events(event, player_human)

    # Input/Movement
    keys = pygame.key.get_pressed()
    player_human.check_movement(keys, dt, game_difficulty_speed)

    # Update display and timing
    pygame.display.flip()
    dt = clock.tick(60) / 1000

    # Update game difficulty and spawn coins
    score, game_difficulty_speed, num_meteors, coin_spawned, points_coin = update_game_difficulty(
        score, num_meteors, game_difficulty_speed, dt, coin_spawned, points_coin, screen
    )

""" TODO: Create seperate while loop for menu to fix bug where ship drifts during menu screen
menu = True
while menu:
    highscores_list, highscore_rank = update_highscores(score, screen,
    log_location_scores, log_location_highscores)
    show_highscore_screen(screen, highscores_list, highscore_rank, FONT)
"""

#pygame.quit()
