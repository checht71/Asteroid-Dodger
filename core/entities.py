import pygame
from random import randint, random
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from math import sqrt

class player():

    COLOR_DEFAULT = "white"
    COLOR_BOOSTED = "blue"
    SIZE_X = 50
    SIZE_Y = 60
    SPEED_DEFAULT = 300
    SPEED_MULTIPLIER_BOOSTED = 3
    SPEED_MULTIPLIER_DEFAULT = 1
    SCREEN_BORDER_MARGIN = 50

    def __init__(self, screen):
        self.pos = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.color = player.COLOR_DEFAULT
        self.speed_boost = player.SPEED_MULTIPLIER_DEFAULT
        self.screen = screen

    def draw(self):
        self.drawing = pygame.draw.rect(self.screen, self.color, (self.pos.x, self.pos.y, player.SIZE_X, player.SIZE_Y))

    def reset(self):
        self.pos = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.set_default_speed()

    def set_default_speed(self):
        self.color = player.COLOR_DEFAULT
        self.speed_boost = player.SPEED_MULTIPLIER_DEFAULT

    def check_movement(self, keys, dt, game_difficulty_speed):
        player_speed = player.SPEED_DEFAULT * dt * self.speed_boost + game_difficulty_speed
        if keys[pygame.K_w]:
            if self.pos.y >= 0:
                self.pos.y -= player_speed
        if keys[pygame.K_s]:
            if self.pos.y <= SCREEN_HEIGHT - player.SCREEN_BORDER_MARGIN:
                self.pos.y += player_speed
        if keys[pygame.K_a]:
            if self.pos.x >= 0:
                self.pos.x -= player_speed
        if keys[pygame.K_d]:
            if self.pos.x <= SCREEN_WIDTH - player.SCREEN_BORDER_MARGIN:
                self.pos.x += player_speed
        if keys[pygame.K_LSHIFT]:
            self.speed_boost = player.SPEED_MULTIPLIER_BOOSTED
            self.color = player.COLOR_BOOSTED


class meteor():
    """Meteors are the objects you have to dodge to progress thru the game.
    If they collide with the player, it's game over."""

    DEFAULT_SPEED_DOWN = 400

    def __init__(self, screen):
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), randint(-500, 0))
        self.screen = screen
        self.spawn()
        
    def move(self, dt, speed_multiplier):
        """Move the position of the meteor down the screen"""
        self.pos.y += meteor.DEFAULT_SPEED_DOWN *dt*speed_multiplier+self.ydrift
        self.pos.x += self.drift
        if self.pos.y >= SCREEN_HEIGHT: # Reset position
            self.spawn()

    def draw(self):
        """Display the meteor on screen"""
        self.drawing = pygame.draw.rect(self.screen, "red", (self.pos.x, self.pos.y, self.width, self.height))
    
    def reset(self):
        """Reset all meteors at game's end"""
        self.pos.y = randint(-1000, -500)

    def spawn(self):
        self.pos.y = randint(-1000, -500)
        self.pos.x = randint(0, SCREEN_WIDTH)
        self.width = randint(50, 250)
        self.height = self.width + randint(-30, 30)
        self.drift = randint(-5, 5)
        self.ydrift = randint(-5, 3)


class star():
    """Stars are background objects with no collision. For visual purposes only"""
    def __init__(self, screen):
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), randint(-1000, 1000))
        self.diamteter = randint(1, 10)
        self.screen = screen
        self.alpha = randint(1, 255)
        
    def move(self, dt, speed_multiplier):
        """Move the position of the star down the screen"""
        self.pos.y += 350*dt*speed_multiplier
        if self.pos.y >= SCREEN_HEIGHT:
            self.pos.y = randint(-2000, 0)
            self.pos.x = randint(0, SCREEN_WIDTH)
            self.diamteter = randint(2, 12)
            self.alpha = self.diamteter*20

    def draw(self):
        """Display each star on screen"""
        self.drawing = pygame.draw.rect(self.screen, (self.alpha,self.alpha,self.alpha,self.alpha), (self.pos.x, self.pos.y, self.diamteter, self.diamteter))
    
    def reset(self):
        """Reset all stars at game's end"""
        self.pos.y = randint(-500, 0)

