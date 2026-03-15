import pygame
from core.entities import Meteor, Star, Player, Coin
from core.gamestates import show_highscore_screen, update_highscores
import core.constants as constants
from core.music import change_music


def draw_game_state(screen, player_human, stars, meteor, num_meteors, points_coin, coin_spawned, score, FONT, dt, game_difficulty_speed):
    """Draw all game entities and UI elements."""
    screen.fill("black")
    score_text = FONT.render(str(round(score)*10), True, constants.FONT_COLOR)
    screen.blit(score_text, (10, 10))
    
    player_human.draw()
    for star in stars:
        star.draw()
        star.move(dt, game_difficulty_speed)

    for x in range(num_meteors):
        meteor[x].draw()


def handle_coin_logic(coin_spawned, points_coin, player_human, dt, game_difficulty_speed, score):
    """Handle coin movement and collision detection."""
    if coin_spawned:
        points_coin.draw(coin_spawned)
        points_coin.move(dt, game_difficulty_speed)

        if player_human.drawing.collidelist([points_coin.drawing]) != -1:
            score += points_coin.SCORE_VALUE
            coin_spawned = False
    
    return score, coin_spawned


def handle_meteor_logic(meteor, num_meteors, player_human, dt, game_difficulty_speed, score):
    """Handle meteor movement and collision detection."""
    for x in range(num_meteors):
        meteor[x].move(dt, game_difficulty_speed)

        if player_human.drawing.collidelist([meteor[x].drawing]) != -1:
            return True  # Collision detected
    
    return False


def reset_game_state(player_human, meteor, num_meteors, score, screen, FONT, TRAINING_AI, log_location_scores, log_location_highscores):
    """Reset all game variables after collision."""
    change_music(constants.MENU_MUSIC)
    highscores_list, highscore_rank = update_highscores(score, screen,
        log_location_scores, log_location_highscores)
    if TRAINING_AI == False:
        show_highscore_screen(screen, highscores_list, highscore_rank, FONT)
    
    score = 0
    for y in range(num_meteors):
        meteor[y].reset()
    player_human.reset()
    change_music(constants.INGAME_MUSIC)
    
    return score


def handle_events(event, player_human):
    """Handle keyboard input events."""
    if event.type == pygame.QUIT:    # Stop game if browser is closed
        return False
    if event.type == pygame.KEYUP:      # Reset player speed if LSHIFT is up
        if 'left shift' == pygame.key.name(event.key):
            player_human.set_default_speed()

    return True     # Loop keeps running


def update_game_difficulty(score, num_meteors, game_difficulty_speed, dt):
    """Update score, difficulty, and spawn coins."""
    score += constants.SCORE_PER_TICK
    game_difficulty_speed += constants.GAME_SPEED_INCREASE_PER_TICK

    if round(score, 1) %constants.METEOR_SPAWN_TIME_INTERVAL == 0.0 and score >= 10.0 and num_meteors < constants.METEORS_MAX:
        num_meteors += 1
    
    return score, game_difficulty_speed, num_meteors


def check_coin_spawn(score, coin_spawned, points_coin, screen):
    """If score is a certain amount, spawn coin if it is not already spawned."""
    if round(score, 1) % constants.COIN_SPAWN_TIME_INTERVAL == 0.0:
        if coin_spawned == False:
            points_coin = Coin(screen)
            coin_spawned = True

    return coin_spawned, points_coin