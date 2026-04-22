import pygame
from random import randint
from core.entities import Meteor, Star, Player, Coin
from core.gamestates import show_highscore_screen, update_highscores
import core.constants as constants
from core.music import change_music


class AsteroidDodger():

    def __init__(self):
        self._init_pygame()
        self._init_audio()
        self._init_player()
        self._init_sprites()
        self._init_ai()

    def _init_pygame(self):
        """Initialize pygame display and clock."""
        pygame.init()
        pygame.display.set_caption('Asteroid Belt')
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont(constants.FONT_TYPE, constants.FONT_SIZE)

    def _init_audio(self):
        """Initialize audio and load music."""
        pygame.mixer.init()
        pygame.mixer.music.load(constants.INGAME_MUSIC)
        pygame.mixer.music.play(-1)

    def _init_player(self):
        """Initialize player and game state variables."""
        self.player_human = Player(self.screen)
        self.score = 0.0
        self.running = True
        self.dt = 0
        self.game_difficulty_speed = constants.GAME_DIFFICULTY_SPEED_STARTING

    def _init_sprites(self):
        """Initialize obstacles, stars, and coins."""
        self.obstacle = [Meteor(self.screen) for i in range(constants.METEORS_MAX)]
        self.num_obstacles = constants.METEORS_MINIMUM
        self.stars = [Star(self.screen) for i in range(constants.MAX_STARS)]
        self.coin_spawned = False
        self.points_coin = None

    def _init_ai(self):
        """Initialize AI logging paths."""
        self.TRAINING_AI = False
        if self.TRAINING_AI:
            self.log_location_scores = constants.SCORES_LOG_AI
            self.log_location_highscores = constants.HIGHSCORES_LOG_AI
        else:
            self.log_location_scores = constants.SCORES_LOG_HUMAN
            self.log_location_highscores = constants.HIGHSCORES_LOG_HUMAN

    def step(self):
        """Main game loop step."""
        self._draw_background_and_score()
        self._update_coin()
        self._draw_and_move_player()
        self._draw_and_move_stars()
        self._draw_move_and_check_obstacles()
        self._update_display()
        self._update_physics()
        self._check_difficulty_progression()

    def _draw_background_and_score(self):
        """Draw background and render score text."""
        self.screen.fill("black")
        self.score_text = self.FONT.render(str(round(self.score) * 10), True, constants.FONT_COLOR)
        self.screen.blit(self.score_text, (10, 10))

    def _update_coin(self):
        """Update coin position and check for collision with player."""
        if self.coin_spawned:
            self.points_coin.draw(self.coin_spawned)
            self.points_coin.move(self.dt, self.game_difficulty_speed)

            if self.player_human.drawing.collidelist([self.points_coin.drawing]) != -1:
                self.score += self.points_coin.SCORE_VALUE
                self.coin_spawned = False

    def _draw_and_move_player(self):
        """Draw and update player position."""
        self.player_human.draw()

    def _draw_and_move_stars(self):
        """Draw and move all stars."""
        for astar in self.stars:
            astar.draw()
            astar.move(self.dt, self.game_difficulty_speed)

    def _draw_move_and_check_obstacles(self):
        """Draw, move obstacles, and check for collision with player."""
        for x in range(self.num_obstacles):
            self.obstacle[x].draw()
            self.obstacle[x].move(self.dt, self.game_difficulty_speed)

            if self.player_human.drawing.collidelist([self.obstacle[x].drawing]) != -1:
                self._handle_game_over()

    def _handle_game_over(self):
        """Handle collision and game over sequence."""
        change_music(constants.MENU_MUSIC)
        
        highscores_list, highscore_rank = update_highscores(
            self.score, 
            self.screen,
            self.log_location_scores, 
            self.log_location_highscores
        )
        
        if not self.TRAINING_AI:
            show_highscore_screen(self.screen, highscores_list, highscore_rank, self.FONT)
        
        self._reset_game()
        change_music(constants.INGAME_MUSIC)

    def _reset_game(self):
        """Reset all game state variables and entities."""
        self.score = 0
        self.game_difficulty_speed = constants.GAME_DIFFICULTY_SPEED_STARTING
        self.num_obstacles = constants.METEORS_MINIMUM
        self.coin_spawned = False
        
        for obstacle in self.obstacle:
            obstacle.reset()
        
        self.player_human.reset()

    def _update_display(self):
        """Update the display."""
        pygame.display.flip()

    def _update_physics(self):
        """Update frame timing and game progression."""
        self.dt = self.clock.tick(60) / 1000
        self.score += constants.SCORE_PER_TICK
        self.game_difficulty_speed += constants.GAME_SPEED_INCREASE_PER_TICK

    def _check_difficulty_progression(self):
        """Check for difficulty increases and spawn coins."""
        self._increase_obstacle_count()
        self._spawn_coin()

    def _increase_obstacle_count(self):
        """Increase obstacle count based on score."""
        if (round(self.score, 1) % 50 == 0.0 and 
            self.score >= 10.0 and 
            self.num_obstacles < constants.METEORS_MAX):
            self.num_obstacles += 1

    def _spawn_coin(self):
        """Spawn a coin if conditions are met."""
        if round(self.score, 1) % 50 == 0.0 and not self.coin_spawned:
            self.points_coin = Coin(self.screen)
            self.coin_spawned = True
