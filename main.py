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


AI_PLAYING = True
HUMAN_PLAYING = True


def load_model(game):

    observation, info = game.reset_game()


    agent = Agent(game, dropout=dropout, hidden_layer=hidden_layer,
                learning_rate=learning_rate, step_repeat=step_repeat,
                gamma=gamma)

    device = 'cuda:0' if torch.cuda.is_available() else 'cpu' 

    model1 = RocketNet(action_dim=game.action_space.n, hidden_dim=hidden_layer, observation_shape=observation.shape).to(device)
    model2 = RocketNet(action_dim=game.action_space.n, hidden_dim=hidden_layer, observation_shape=observation.shape).to(device)

    model1.load_the_model(filename='models/dqn1.pt')
    model2.load_the_model(filename='models/dqn2.pt')

    model1.eval()
    model2.eval()

    return model1, model2


game = AsteroidDodger(AI_PLAYING, HUMAN_PLAYING)
model1, model2 = load_model(game)

while True:

    action = 0
    if random.random() < epsilon:
        action = game.action_space.sample()
    else:
        model1_q_values = model1.forward(state.unsqueeze(0).to(device))[0]
        model2_q_values = model2.forward(state.unsqueeze(0).to(device))[0]

        q_values = torch.min(model1_q_values, model2_q_values)

        action = torch.argmax(q_values, dim=-1, keepdim=True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYUP: # Do not give the AI speed boost
            if pygame.key.name(event.key) == 'left shift':
                game.player_human.set_default_speed()

    keys = pygame.key.get_pressed()

    # Handle AI input
    if keys[pygame.K_i]:
        action = 1
    if keys[pygame.K_k]:
        action = 2
    if keys[pygame.K_j]:
        action = 3
    if keys[pygame.K_l]:
        action = 4

    if HUMAN_PLAYING:
        game.player_human.check_movement(keys, game.dt, game.game_difficulty_speed)
    
    if AI_PLAYING:
        game.player_ai.check_movement(action, game.dt, game.game_difficulty_speed)

    reward, done, truncated = game.step(action=action)


