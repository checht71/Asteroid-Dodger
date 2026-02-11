# Example file showing a circle moving on screen
import pygame
from random import randint
from utils.meteor import meteor, star
from utils.gamestates import show_go_screen, highscores
from utils.constants import *

# pygame setup
pygame.init()
pygame.display.set_caption('Asteroid Belt v0.5.7')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
score = 0.0
running = True
dt = 0
screen_height = screen.get_height() -100
screen_width = screen.get_width() -100
game_difficulty_speed = GAME_DIFFICULTY_SPEED_STARTING
# player init
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
player_color = PLAYER_COLOR_DEFAULT
speed_boost = 1
FONT = pygame.font.SysFont(FONT_TYPE, FONT_SIZE)
# sprite init
enemy = [meteor(screen) for i in range(METEORS_MAX)]
num_enemies = METEORS_MINIMUM
stars = [star(screen) for i in range(MAX_STARS)]

while running:
    screen.fill("black")
    player = pygame.draw.rect(screen, player_color, (player_pos.x, player_pos.y, PLAYER_SIZE_X, PLAYER_SIZE_Y))
    score_text = FONT.render(str(round(score)*10), True, FONT_COLOR)
    screen.blit(score_text, (10, 10))

    for astar in stars:
        astar.draw()
        astar.move(dt, game_difficulty_speed)


    for x in range(num_enemies):
        enemy[x].draw()
        enemy[x].move(dt, game_difficulty_speed)

        #END GAME AND RESTART ON COLLISION
    if player.collidelist([enemy[x].drawing]) != -1:
        scoreinfo, highscore_spot = highscores(score, screen)
        show_go_screen(screen, scoreinfo, highscore_spot, FONT)
        score = 0
        for y in range(num_enemies):
            enemy[y].reset()
        game_difficulty_speed = GAME_DIFFICULTY_SPEED_STARTING
        num_enemies = METEORS_MINIMUM
        player_color = PLAYER_COLOR_DEFAULT
        speed_boost = 1


    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if 'left shift'==pygame.key.name(event.key):
                player_color = PLAYER_COLOR_DEFAULT
                speed_boost = 1

    #Input/Movement
    keys = pygame.key.get_pressed()
    PLAYER_SPEED = PLAYER_SPEED_DEFAULT * dt * speed_boost + game_difficulty_speed
    if keys[pygame.K_w]:
        if player_pos.y >= 0:
            player_pos.y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        if player_pos.y <= screen_height:
            player_pos.y += PLAYER_SPEED
    if keys[pygame.K_a]:
        if player_pos.x >= 0:
            player_pos.x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        if player_pos.x <= screen_width:
            player_pos.x += PLAYER_SPEED
    if keys[pygame.K_LSHIFT]:
        speed_boost = 3
        player_color = PLAYER_COLOR_BOOSTED
            

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    score += SCORE_PER_SECOND
    game_difficulty_speed += GAME_SPEED_INCREASE_PER_SECOND
    if round(score,1)%50 == 0.0 and score >= 10.0 and num_enemies < METEORS_MAX:
        num_enemies +=1

pygame.quit()
