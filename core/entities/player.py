import pygame
from random import randint, random
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Player():

    COLOR_DEFAULT = "white"
    COLOR_BOOSTED = "blue"
    SIZE_X = 50
    SIZE_Y = 60
    SPEED_DEFAULT = 900
    SPEED_MULTIPLIER_BOOSTED = 2
    SPEED_MULTIPLIER_DEFAULT = 1
    SCREEN_BORDER_MARGIN = 100

    def __init__(self, screen):
        self.pos = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.color = Player.COLOR_DEFAULT
        self.speed_boost = Player.SPEED_MULTIPLIER_DEFAULT
        self.screen = screen

    def draw(self):
        self.drawing = pygame.draw.rect(self.screen, self.color, (self.pos.x, self.pos.y, Player.SIZE_X, Player.SIZE_Y))

    def reset(self):
        self.pos = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.set_default_speed()

    def set_default_speed(self):
        self.color = Player.COLOR_DEFAULT
        self.speed_boost = Player.SPEED_MULTIPLIER_DEFAULT

    def check_movement(self, keys, dt, game_difficulty_speed):
        Player_speed = Player.SPEED_DEFAULT * dt * self.speed_boost + game_difficulty_speed
        if keys[pygame.K_w]:
            if self.pos.y >= 0:
                self.pos.y -= Player_speed
        if keys[pygame.K_s]:
            if self.pos.y <= SCREEN_HEIGHT - Player.SCREEN_BORDER_MARGIN:
                self.pos.y += Player_speed
        if keys[pygame.K_a]:
            if self.pos.x >= 0:
                self.pos.x -= Player_speed
        if keys[pygame.K_d]:
            if self.pos.x <= SCREEN_WIDTH - Player.SCREEN_BORDER_MARGIN:
                self.pos.x += Player_speed
        if keys[pygame.K_LSHIFT]:
            self.speed_boost = Player.SPEED_MULTIPLIER_BOOSTED
            self.color = Player.COLOR_BOOSTED



class Player_AI(Player):
    COLOR_DEFAULT = "red"
    SPAWN_OFFSET_X = 50
    SPAWN_LOCATION_X = SCREEN_WIDTH/2 + SPAWN_OFFSET_X
    SPAWN_LOCATION_Y = SCREEN_HEIGHT/2

    def __init__(self, screen):
        self.pos = pygame.Vector2(Player_AI.SPAWN_LOCATION_X, Player_AI.SPAWN_LOCATION_Y)
        self.color = Player_AI.COLOR_DEFAULT
        self.screen = screen

    def check_movement(self, action, dt, game_difficulty_speed):

        up = True if action == 1 else False
        down = True if action == 2 else False
        left = True if action == 3 else False
        right = True if action == 4 else False


        Player_speed = Player.SPEED_DEFAULT * dt + game_difficulty_speed
        if up:
            if self.pos.y >= 0:
                self.pos.y -= Player_speed
        if down:
            if self.pos.y <= SCREEN_HEIGHT - Player.SCREEN_BORDER_MARGIN:
                self.pos.y += Player_speed
        if left:
            if self.pos.x >= 0:
                self.pos.x -= Player_speed
        if right:
            if self.pos.x <= SCREEN_WIDTH - Player.SCREEN_BORDER_MARGIN:
                self.pos.x += Player_speed