# audio.py
import os
import pygame
from constants import ASSETS_DIR

def init_audio():
    pygame.mixer.init()
    theme_path = os.path.join(ASSETS_DIR, "Sound_effects", "nyanCat_theme.mp3")
    pygame.mixer.music.load(theme_path)
    pygame.mixer.music.play(-1)

def play_sound(sound_file):
    sound_path = os.path.join(ASSETS_DIR, "Sound_effects", sound_file)
    sound = pygame.mixer.Sound(sound_path)
    sound.play()
