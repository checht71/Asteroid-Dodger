import pygame
from random import randint
from core.entities import Meteor, Star, Player
from core.gamestates import show_highscore_screen, update_highscores
import core.constants as constants

# pygame setup
pygame.init()
pygame.display.set_caption('Asteroid Belt')
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
clock = pygame.time.Clock()
score = 0.0
running = True
dt = 0
game_difficulty_speed = constants.GAME_DIFFICULTY_SPEED_STARTING
# Player init
Player = Player(screen)
FONT = pygame.font.SysFont(constants.FONT_TYPE, constants.FONT_SIZE)
# sprite init
obstacle = [Meteor(screen) for i in range(constants.METEORS_MAX)]
num_obstacles = constants.METEORS_MINIMUM
stars = [Star(screen) for i in range(constants.MAX_STARS)]
log_location_scores = constants.SCORES_LOG_HUMAN
log_location_highscores = constants.HIGHSCORES_LOG_HUMAN



while running:
    # draw screen and score text
    screen.fill("black")
    score_text = FONT.render(str(round(score)*10), True, constants.FONT_COLOR)
    screen.blit(score_text, (10, 10))

    # draw and move entities
    Player.draw()
    for astar in stars:
        astar.draw()
        astar.move(dt, game_difficulty_speed)

    for x in range(num_obstacles):
        obstacle[x].draw()
        obstacle[x].move(dt, game_difficulty_speed)

        # END GAME AND RESTART ON COLLISION
        if Player.drawing.collidelist([obstacle[x].drawing]) != -1:
            # update then show highscores
            highscores_list, highscore_rank = update_highscores(score, screen, log_location_scores, log_location_highscores)
            show_highscore_screen(screen, highscores_list, highscore_rank, FONT)
            # reset player and meteors
            score = 0
            for y in range(num_obstacles):
                obstacle[y].reset()
            game_difficulty_speed = constants.GAME_DIFFICULTY_SPEED_STARTING
            num_obstacles = constants.METEORS_MINIMUM
            Player.reset()


    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if 'left shift'==pygame.key.name(event.key):
                Player.set_default_speed()
    
    #Input/Movement
    keys = pygame.key.get_pressed()
    Player.check_movement(keys, dt, game_difficulty_speed)
            
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    score += constants.SCORE_PER_TICK
    game_difficulty_speed += constants.GAME_SPEED_INCREASE_PER_TICK

    # increase meteors every 500 points
    if round(score,1)%50 == 0.0 and score >= 10.0 and num_obstacles < constants.METEORS_MAX:
        num_obstacles +=1

pygame.quit()
