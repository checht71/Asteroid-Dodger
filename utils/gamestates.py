import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_COLOR



def highscores(newscore, screen):
    highscore_rank = -1
    newscore = round(newscore)*10
    with open("./assets/scores.csv", "r") as scores:
        highscores_list = scores.readlines()
        for place, highscore in enumerate(highscores_list):
            highscore = int(highscore.rstrip())
            if newscore > highscore:
                if place <= 1:
                    highscores_list[place+1] = highscores_list[place]
                highscores_list[place] = str(newscore)+"\n"
                highscore_rank = place
                break
    
    with open("./assets/scores.csv", "w") as scores:
        for hs in highscores_list:
            scores.write(str(hs))

    return highscores_list, highscore_rank


def show_go_screen(screen, highscores_list, highscore_rank, FONT):
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
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True


