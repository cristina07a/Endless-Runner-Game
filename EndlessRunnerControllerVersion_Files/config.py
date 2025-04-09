# config.py
import os
import pygame
from constants import ASSETS_DIR

def load_image(*path, scale=None):
    full_path = os.path.join(ASSETS_DIR, *path)
    image = pygame.image.load(full_path)
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

def load_character_images(character_name):
    base_path = os.path.join(ASSETS_DIR, "Animal", character_name)
    running = [
        load_image("Animal", character_name, "run1.png"),
        load_image("Animal", character_name, "run2.png")
    ]
    jumping = load_image("Animal", character_name, "jump.png")
    ducking = [
        load_image("Animal", character_name, "duck1.png"),
        load_image("Animal", character_name, "duck2.png")
    ]
    return {"running": running, "jumping": jumping, "ducking": ducking}