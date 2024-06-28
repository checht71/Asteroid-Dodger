import pygame
from random import randint
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class meteor():
    def __init__(self, screen):
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), randint(-500, 0))
        self.width = randint(30, 100)
        self.height = randint(30, 100)
        self.drift = randint(-5, 5)
        self.screen = screen
        
    def move(self, dt, speed_multiplier):
        self.pos.y += 400 *dt*speed_multiplier
        self.pos.x += randint(-1, 1) + self.drift
        if self.pos.y >= SCREEN_HEIGHT:
            self.pos.y = randint(-500, 0)
            self.pos.x = randint(0, SCREEN_WIDTH)
            self.width = randint(50, 250)
            self.height = randint(50, 250)

    def draw(self):
        self.drawing = pygame.draw.rect(self.screen, "red", (self.pos.x, self.pos.y, self.width, self.height))
    
    def reset(self):
        self.pos.y = randint(-500, 0)

