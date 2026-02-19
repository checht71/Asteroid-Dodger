import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_COLOR



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
    if highscore_rank != -1:
        hsblurb = FONT.render("HIGH SCORE!!!", True, "green")
    else:
        hsblurb = FONT.render("High Scores:", True, FONT_COLOR)
    score1 = FONT.render(f"1. {highscores_list[0].rstrip()}", True, FONT_COLOR)
    score2 = FONT.render(f"2. {highscores_list[1].rstrip()}", True, FONT_COLOR)
    score3 = FONT.render(f"3. {highscores_list[2].rstrip()}", True, FONT_COLOR)
    text_surface = FONT.render("Press space bar to play again", True, FONT_COLOR)
    screen.blit(text_surface, (SCREEN_WIDTH / 2-200, SCREEN_HEIGHT / 2))
    screen.blit(score1, (SCREEN_WIDTH / 2-50, SCREEN_HEIGHT / 2-150))
    screen.blit(score2, (SCREEN_WIDTH / 2-50, SCREEN_HEIGHT / 2-100))
    screen.blit(score3, (SCREEN_WIDTH / 2-50, SCREEN_HEIGHT / 2-50))
    screen.blit(hsblurb, (SCREEN_WIDTH / 2-100, SCREEN_HEIGHT / 2-200))
    pygame.display.flip()
    higscores_showing = True
    while higscores_showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                higscores_showing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    higscores_showing = False


