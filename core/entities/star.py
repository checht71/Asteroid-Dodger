import pygame
from random import randint, random
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT



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
