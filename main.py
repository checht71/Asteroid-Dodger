# Example file showing a circle moving on screen
import pygame
from random import randint
from utils.meteor import meteor, star
from utils.gamestates import show_go_screen, checklevel, highscores
from utils.constants import *

# pygame setup
pygame.init()
pygame.display.set_caption('Asteroid Belt v0.5.5')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
score = 0.0
running = True
dt = 0
screen_height = screen.get_height() -100
screen_width = screen.get_width() -100
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_color = "white"
speed_multiplier = 1
speed_boost = 1
FONT = pygame.font.SysFont('mats bold', 40)

enemy = [meteor(screen) for i in range(MAX_METEORS)]
num_enemies = STARTING_METEORS
stars = [star(screen) for i in range(50)]

while running:
    screen.fill("black")
    player = pygame.draw.rect(screen, player_color, (player_pos.x, player_pos.y, 50, 60))
    text_surface = FONT.render(str(round(score))+'0', True, "white")
    screen.blit(text_surface, (10, 10))

    for astar in stars:
        astar.draw()
        astar.move(dt, speed_multiplier)


    for x in range(num_enemies):
        enemy[x].draw()
        enemy[x].move(dt, speed_multiplier)

        if player.collidelist([enemy[x].drawing]) != -1:
            scoreinfo, highscore_spot = highscores(score, screen)
            show_go_screen(screen, scoreinfo, highscore_spot, FONT)
            score = 0
            for y in range(num_enemies):
                enemy[y].reset()
            speed_multiplier = 1
            num_enemies = 5



    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            player_color = "red"
        if event.type == pygame.MOUSEBUTTONUP:
            player_color = "white"
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if 'left shift'==pygame.key.name(event.key):
                player_color = "white"
                speed_boost = 1

    # fill the screen with a color to wipe away anything from last frame

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if player_pos.y >= 0:
            player_pos.y -= 300 * dt * speed_boost + speed_multiplier
    if keys[pygame.K_s]:
        if player_pos.y <= screen_height:
            player_pos.y += 300 * dt * speed_boost + speed_multiplier
    if keys[pygame.K_a]:
        if player_pos.x >= 0:
            player_pos.x -= 300 * dt * speed_boost + speed_multiplier
    if keys[pygame.K_d]:
        if player_pos.x <= screen_width:
            player_pos.x += 300 * dt * speed_boost + speed_multiplier
    if keys[pygame.K_LSHIFT]:
        speed_boost = 3
        player_color = "blue"
            

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    score += 0.1
    speed_multiplier += 0.0005
    if round(score,1)%50 == 0.0 and score >= 10.0 and num_enemies < MAX_METEORS:
        print("new meteor")
        num_enemies +=1

pygame.quit()
