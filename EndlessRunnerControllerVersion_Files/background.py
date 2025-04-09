# background.py
import os
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT, ASSETS_DIR

def load_background():
    bg = pygame.image.load(os.path.join(ASSETS_DIR, "Other", "fundal2.png"))
    return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

def load_scrolling_background():
    bg_scroll = pygame.image.load(os.path.join(ASSETS_DIR, "Other", "fundal.png")).convert()
    bg_scroll = pygame.transform.scale(bg_scroll, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ground = pygame.image.load(os.path.join(ASSETS_DIR, "Other", "dirt4.png")).convert_alpha()
    ground = pygame.transform.scale(ground, (SCREEN_WIDTH, GROUND_HEIGHT))
    return bg_scroll, ground

def draw_scrolling_background(SCREEN, bg_scroll, ground, scroll, ground_scroll, game_speed):
    tiles = SCREEN_WIDTH // bg_scroll.get_width() + 2
    for i in range(tiles):
        SCREEN.blit(bg_scroll, (i * bg_scroll.get_width() + scroll, 0))
    for i in range(tiles):
        SCREEN.blit(ground, (i * ground.get_width() + ground_scroll, SCREEN_HEIGHT - GROUND_HEIGHT))
    scroll -= game_speed // 2
    ground_scroll -= game_speed
    if abs(scroll) > bg_scroll.get_width():
        scroll = 0
    if abs(ground_scroll) > ground.get_width():
        ground_scroll = 0
    return scroll, ground_scroll
