import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT


def highscores(newscore, screen):
    highscore_spot = -1
    newscore = round(newscore)*10
    with open("./assets/scores.csv", "r") as scores:
        scoreinfo = scores.readlines()
        for place, highscore in enumerate(scoreinfo):
            highscore = int(highscore.rstrip())
            if newscore > highscore:
                if place <= 1:
                    scoreinfo[place+1] = scoreinfo[place]
                scoreinfo[place] = str(newscore)+"\n"
                highscore_spot = place
                break
    
    with open("./assets/scores.csv", "w") as scores:
        for hs in scoreinfo:
            scores.write(str(hs))

    return scoreinfo, highscore_spot

        

def show_go_screen(screen, scoreinfo, highscore_spot, FONT):
    if highscore_spot != -1:
        hsblurb = FONT.render("HIGH SCORE!!!", True, "white")
    else:
        hsblurb = FONT.render("High Scores:", True, "white")
    score1 = FONT.render(f"1. {scoreinfo[0].rstrip()}", True, "white")
    score2 = FONT.render(f"2. {scoreinfo[1].rstrip()}", True, "white")
    score3 = FONT.render(f"3. {scoreinfo[2].rstrip()}", True, "white")
    text_surface = FONT.render("Press space bar to play again", True, "white")
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


def checklevel(score):
    if score >= 1000 and score < 2000:
        level = 2
    if score >= 2000:
        level = 3
    
    return score

