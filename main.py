# Example file showing a circle moving on screen
import pygame
from random import randint
from utils.meteor import meteor, star
from utils.gamestates import show_go_screen, highscores
import utils.constants as constants

# pygame setup
pygame.init()
pygame.display.set_caption('Asteroid Belt v0.5.7')
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
clock = pygame.time.Clock()
score = 0.0
running = True
dt = 0
screen_height = screen.get_height() - constants.SCREEN_BORDER_LENGTH
screen_width = screen.get_width() - constants.SCREEN_BORDER_LENGTH
game_difficulty_speed = constants.GAME_DIFFICULTY_SPEED_STARTING
# player init
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
player_color = constants.PLAYER_COLOR_DEFAULT
speed_boost = constants.PLAYER_SPEED_MULTIPLIER_DEFAULT
FONT = pygame.font.SysFont(constants.FONT_TYPE, constants.FONT_SIZE)
# sprite init
enemy = [meteor(screen) for i in range(constants.METEORS_MAX)]
num_enemies = constants.METEORS_MINIMUM
stars = [star(screen) for i in range(constants.MAX_STARS)]

while running:
    screen.fill("black")
    player = pygame.draw.rect(screen, player_color, (player_pos.x, player_pos.y, constants.PLAYER_SIZE_X, constants.PLAYER_SIZE_Y))
    score_text = FONT.render(str(round(score)*10), True, constants.FONT_COLOR)
    screen.blit(score_text, (10, 10))

    for astar in stars:
        astar.draw()
        astar.move(dt, game_difficulty_speed)


    for x in range(num_enemies):
        enemy[x].draw()
        enemy[x].move(dt, game_difficulty_speed)


        #END GAME AND RESTART ON COLLISION
        if player.collidelist([enemy[x].drawing]) != -1:
            highscores_list, highscore_rank = highscores(score, screen)
            show_go_screen(screen, highscores_list, highscore_rank, FONT)
            score = 0
            for y in range(num_enemies):
                enemy[y].reset()
            game_difficulty_speed = constants.GAME_DIFFICULTY_SPEED_STARTING
            num_enemies = constants.METEORS_MINIMUM
            player_color = constants.PLAYER_COLOR_DEFAULT
            speed_boost = constants.PLAYER_SPEED_MULTIPLIER_DEFAULT


    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if 'left shift'==pygame.key.name(event.key):
                player_color = constants.PLAYER_COLOR_DEFAULT
                speed_boost = constants.PLAYER_SPEED_MULTIPLIER_DEFAULT

    #Input/Movement
    keys = pygame.key.get_pressed()
    player_speed = constants.PLAYER_SPEED_DEFAULT * dt * speed_boost + game_difficulty_speed
    if keys[pygame.K_w]:
        if player_pos.y >= 0:
            player_pos.y -= player_speed
    if keys[pygame.K_s]:
        if player_pos.y <= screen_height:
            player_pos.y += player_speed
    if keys[pygame.K_a]:
        if player_pos.x >= 0:
            player_pos.x -= player_speed
    if keys[pygame.K_d]:
        if player_pos.x <= screen_width:
            player_pos.x += player_speed
    if keys[pygame.K_LSHIFT]:
        speed_boost = constants.PLAYER_SPEED_MULTIPLIER_BOOSTED
        player_color = constants.PLAYER_COLOR_BOOSTED
            

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    score += constants.SCORE_PER_SECOND
    game_difficulty_speed += constants.GAME_SPEED_INCREASE_PER_SECOND
    if round(score,1)%50 == 0.0 and score >= 10.0 and num_enemies < constants.METEORS_MAX:
        num_enemies +=1

pygame.quit()
