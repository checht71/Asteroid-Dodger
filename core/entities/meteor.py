import pygame
from random import randint, random
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT



class Meteor():
    """Meteors are the objects you have to dodge to progress thru the game.
    If they collide with the Player, it's game over."""

    DEFAULT_SPEED_DOWN = 400
    SPAWN_Y_MIN = -1000
    SPAWN_Y_MAX = -500
    COLOR = "azure4"

    def __init__(self, screen):
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), randint(Meteor.SPAWN_Y_MAX, 0))
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
        self.drawing = pygame.draw.rect(self.screen, Meteor.COLOR, (self.pos.x, self.pos.y, self.width, self.height))
        self.drawing2 = pygame.draw.rect(self.screen, Meteor.COLOR, (self.pos.x-20, self.pos.y-20, self.height, self.width))
        self.drawing3 = pygame.draw.rect(self.screen, Meteor.COLOR, (self.pos.x+10, self.pos.y-10, self.height+10, self.width-10))
    
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