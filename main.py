import pygame
from random import randint
from core.entities.coin import Coin
from core.entities.star import Star
from core.entities.meteor import Meteor
from core.entities.player import Player
from core.gamestates import show_highscore_screen, update_highscores
import core.constants as constants
from core.music import change_music
from core.game import AsteroidDodger
from AI.agent import Agent
from AI.model import RocketNet
from AI.hyperparameters import *
import torch
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--solo', action='store_true')
args = parser.parse_args()

if args.solo:
    AI_PLAYING = False
else:
    AI_PLAYING = True


HUMAN_PLAYING = True


def load_model(game):

    observation, info = game.reset_game()


    agent = Agent(game, dropout=dropout, hidden_layer=hidden_layer,
                learning_rate=learning_rate, step_repeat=step_repeat,
                gamma=gamma)

    device = 'cuda:0' if torch.cuda.is_available() else 'cpu' 

    model = RocketNet(action_dim=game.action_space.n, hidden_dim=hidden_layer, observation_shape=observation.shape).to(device)

    model.load_the_model(filename='models/dqn1.pt')

    model.eval()

    return model


game = AsteroidDodger(AI_PLAYING, HUMAN_PLAYING)
if AI_PLAYING:
    model = load_model(game)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYUP: # Do not give the AI speed boost
            if pygame.key.name(event.key) == 'left shift':
                game.player_human.set_default_speed()

    keys = pygame.key.get_pressed()

    if AI_PLAYING:
        action = 0
        if random.random() < epsilon:
            action = game.action_space.sample()
        else:
            q_values = model.forward(state.unsqueeze(0).to(device))[0]


            action = torch.argmax(q_values, dim=-1, keepdim=True)

        # Handle AI input
        if keys[pygame.K_i]:
            action = 1
        if keys[pygame.K_k]:
            action = 2
        if keys[pygame.K_j]:
            action = 3
        if keys[pygame.K_l]:
            action = 4

        game.player_ai.check_movement(action, game.dt, game.game_difficulty_speed)

    if HUMAN_PLAYING:
        game.player_human.check_movement(keys, game.dt, game.game_difficulty_speed)

    if not AI_PLAYING:
        action = 0
   
    reward, done, truncated = game.step(action=action)


