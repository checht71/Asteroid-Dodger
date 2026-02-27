import pygame
from random import randint, random
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from math import sqrt

class Player():

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


class Meteor():
    """Meteors are the objects you have to dodge to progress thru the game.
    If they collide with the Player, it's game over."""

    DEFAULT_SPEED_DOWN = 400
    SPAWN_Y_MIN = -1000
    SPAWN_Y_MAX = -500

    def __init__(self, screen):
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), randint(-500, 0))
        self.screen = screen
        self.spawn()
        
    def move(self, dt, speed_multiplier):
        """Move the position of the Meteor down the screen"""
        self.pos.y += Meteor.DEFAULT_SPEED_DOWN *dt*speed_multiplier+self.ydrift
        self.pos.x += self.drift
        if self.pos.y >= SCREEN_HEIGHT: # Reset position
            self.spawn()

    def draw(self):
        """Display the Meteor on screen"""
        self.drawing = pygame.draw.rect(self.screen, "red", (self.pos.x, self.pos.y, self.width, self.height))
    
    def reset(self):
        """Reset all Meteors at game's end"""
        self.pos.y = randint(Meteor.SPAWN_Y_MIN, Meteor.SPAWN_Y_MAX)

    def spawn(self):
        self.pos.y = randint(Meteor.SPAWN_Y_MIN, Meteor.SPAWN_Y_MAX)
        self.pos.x = randint(0, SCREEN_WIDTH)
        self.width = randint(50, 250)
        self.height = self.width + randint(-30, 30)
        self.drift = randint(-5, 5)
        self.ydrift = randint(-5, 3)


class Star():
    SPAWN_Y_MIN = -1000
    SPAWN_Y_MAX = 1000
    DEFAULT_SPEED_DOWN = 350

    """Stars are background objects with no collision. For visual purposes only"""
    def __init__(self, screen):
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), randint(Star.SPAWN_Y_MIN, Star.SPAWN_Y_MAX))
        self.diameter = randint(1, 10)
        self.screen = screen
        self.alpha = randint(1, 255)
        
    def move(self, dt, speed_multiplier):
        """Move the position of the star down the screen"""
        self.pos.y += Star.DEFAULT_SPEED_DOWN*speed_multiplier*dt
        if self.pos.y >= SCREEN_HEIGHT:
            self.pos.y = randint(-2000, 0)
            self.pos.x = randint(0, SCREEN_WIDTH)
            self.diameter = randint(2, 12)
            self.alpha = self.diameter*20

    def draw(self):
        """Display each star on screen"""
        self.drawing = pygame.draw.rect(self.screen, (self.alpha,self.alpha,self.alpha,self.alpha), (self.pos.x, self.pos.y, self.diameter, self.diameter))
    
    def reset(self):
        """Reset all stars at game's end"""
        self.pos.y = randint(-500, 0)


class Coin():
    """Collect the coins to earn more points. Encourages player risk."""
    DEFAULT_SPEED_DOWN = 300
    SCORE_VALUE = 50


    def __init__(self, screen):
        self.spawn_y = -randint(750, 1250)
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), self.spawn_y)
        self.diameter = 50
        self.screen = screen
        
    def move(self, dt, speed_multiplier):
        """Move the position of the coin down the screen"""
        self.pos.y += Coin.DEFAULT_SPEED_DOWN*speed_multiplier*dt
            
    def draw(self, coin_spawned):
        """Display each star on screen"""
        if coin_spawned:
            self.drawing = pygame.draw.rect(self.screen, "yellow", (self.pos.x, self.pos.y, self.diameter, self.diameter))
    
    def reset(self):
        """Move coin out of range at the game's end"""
        self.pos.y = self.spawn_y


    def is_touched(self, score):
        score += 50
