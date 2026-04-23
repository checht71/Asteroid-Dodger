import pygame
from random import randint, random
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from math import sqrt



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
