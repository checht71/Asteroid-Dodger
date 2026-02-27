import pygame
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_COLOR, SCREEN_CENTER_X, SCREEN_CENTER_Y

def show_start_screen(screen, FONT):
    text_surface = FONT.render("Press space bar to play again", True, FONT_COLOR)
    screen.blit(text_surface, (SCREEN_CENTER_X - 200,   SCREEN_CENTER_Y))
    pygame.display.flip()
    startscreen_showing = True
    while startscreen_showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                startscreen_showing = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startscreen_showing = False


def update_highscores(newscore, screen, log_location_scores, log_location_highscores):
    highscore_rank = -1
    newscore = round(newscore)*10
    # read highscores, compare new score
    with open(log_location_highscores, "r") as highscores_file:
        highscores_list = highscores_file.readlines()

        # if the highscores list is empty, create list of zeros
        if len(highscores_list) == 0:
            highscores_list = ['0', '0', '0']
        # iterate through highscores, place new highscore in
        for place, highscore in enumerate(highscores_list):
            highscore = int(highscore.rstrip())
            if newscore > highscore:
                if place <= 1:
                    highscores_list[place+1] = highscores_list[place]
                highscores_list[place] = str(newscore)+"\n"
                highscore_rank = place
                break

    # write highschores
    with open(log_location_highscores, "w") as hscores:
        for hs in highscores_list:
            hscores.write(str(hs))
    
    # write scores
    with open(log_location_scores, "a") as scores:
        scores.write(str(newscore)+"\n")

    return highscores_list, highscore_rank


def show_highscore_screen(screen, highscores_list, highscore_rank, FONT):
    """Show all of the highscores on screen. Wait for player input to restart game."""
    # show text and scores
    if highscore_rank != -1:
        hsblurb = FONT.render("HIGH SCORE!!!", True, "green")
    else:
        hsblurb = FONT.render("High Scores:", True, FONT_COLOR)
        screen.blit(hsblurb, (SCREEN_CENTER_X-100, SCREEN_CENTER_Y-200))

    for score_rank in range(0,len(highscores_list)):
        score_display = FONT.render(f"{score_rank+1}. {highscores_list[score_rank].rstrip()}", True, FONT_COLOR)
        screen.blit(score_display, (SCREEN_CENTER_X-50, SCREEN_CENTER_Y+(score_rank*50)-150))

    text_surface = FONT.render("Press space bar to play again", True, FONT_COLOR)
    
    pygame.display.flip()
    higscores_showing = True
    # Wait for player input before restarting game
    while higscores_showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                higscores_showing = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    higscores_showing = False


