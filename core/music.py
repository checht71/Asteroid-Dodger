import pygame

def change_music(new_music_path):
    pygame.mixer.music.stop()  # Stop the current music
    pygame.mixer.music.load(new_music_path)  # Load new music
    pygame.mixer.music.play(-1)