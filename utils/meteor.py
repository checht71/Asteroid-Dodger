import pygame
from random import randint, random
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class meteor():
    def __init__(self, screen):
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), randint(-500, 0))
        self.width = randint(30, 100)
        self.height = randint(30, 100)
        self.drift = randint(-5, 5)
        self.screen = screen
        self.ydrift = randint(-5, 3)
        
    def move(self, dt, speed_multiplier):
        self.pos.y += 400 *dt*speed_multiplier+self.ydrift
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



class star():
    def __init__(self, screen):
        self.pos = pygame.Vector2(randint(0, SCREEN_WIDTH), randint(-2000, 0))
        self.diamteter = randint(1, 10)
        self.screen = screen
        self.alpha = randint(1, 255)
        self.distance = random()/2
        
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

