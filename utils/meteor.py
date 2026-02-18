import pygame
from random import randint, random
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from math import sqrt

class meteor():
    def __init__(self, screen):
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), randint(-500, 0))
        self.screen = screen
        self.spawn()
        
    def move(self, dt, speed_multiplier):
        self.pos.y += 400 *dt*speed_multiplier+self.ydrift
        self.pos.x += self.drift
        if self.pos.y >= SCREEN_HEIGHT: # Reset position
            self.spawn()

    def draw(self):
        self.drawing = pygame.draw.rect(self.screen, "red", (self.pos.x, self.pos.y, self.width, self.height))
    
    def reset(self):
        # Reset all meteors at game's end
        self.pos.y = randint(-1000, -500)

    def spawn(self):
        self.pos.y = randint(-1000, -500)
        self.pos.x = randint(0, SCREEN_WIDTH)
        self.width = randint(50, 250)
        self.height = self.width + randint(-30, 30)
        self.drift = randint(-5, 5)
        self.ydrift = randint(-5, 3)


class star():
    def __init__(self, screen):
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), randint(-1000, 1000))
        self.diamteter = randint(1, 10)
        self.screen = screen
        self.alpha = randint(1, 255)
        
    def move(self, dt, speed_multiplier):
        self.pos.y += 350*dt*speed_multiplier
        if self.pos.y >= SCREEN_HEIGHT:
            self.pos.y = randint(-2000, 0)
            self.pos.x = randint(0, SCREEN_WIDTH)
            self.diamteter = randint(2, 12)
            self.alpha = self.diamteter*20

    def draw(self):
        self.drawing = pygame.draw.rect(self.screen, (self.alpha,self.alpha,self.alpha,self.alpha), (self.pos.x, self.pos.y, self.diamteter, self.diamteter))
    
    def reset(self):
        self.pos.y = randint(-500, 0)

