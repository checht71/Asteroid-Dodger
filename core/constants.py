#Window & Fonts
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_CENTER_Y = SCREEN_HEIGHT/2
SCREEN_CENTER_X = SCREEN_WIDTH/2
FONT_SIZE = 50
FONT_TYPE = 'mats bold'
FONT_COLOR = 'darkgoldenrod1'
SCREEN_BORDER_LENGTH = 100

# Environmental Behavior
SCORE_PER_TICK = 0.1
GAME_SPEED_INCREASE_PER_TICK = 0.0005
GAME_DIFFICULTY_SPEED_STARTING = 1

# Asteroid Behavior
METEORS_MAX = 10
METEORS_MINIMUM = 6
METEOR_SPAWN_TIME_INTERVAL = 50 # score/10 before meteor spawns

# Entity Behavior
MAX_STARS = 50
COIN_SPAWN_TIME_INTERVAL = 50 # score/10 before coin has chance to spawn

# Score log locations
HIGHSCORES_LOG_HUMAN = "./highscores/highscores_human.csv"
HIGHSCORES_LOG_AI = "./highscores/highscores_ai.csv"
SCORES_LOG_HUMAN = "./highscores/scores_human.csv"
SCORES_LOG_AI = "./highscores/scores_ai.csv"


# Music
INGAME_MUSIC = "./assets/music/arcade_2.mp3"
MENU_MUSIC = "./assets/music/star_crusader.mp3"