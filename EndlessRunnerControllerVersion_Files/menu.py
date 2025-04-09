# menu.py
import pygame
from background import load_background
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, RED, FONT_PATH, MENU_FONT_SIZE
from config import load_character_images
from player import Dinosaur

def draw_text(SCREEN, text, size, x, y, color=BLACK):
    font = pygame.font.Font(FONT_PATH, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    SCREEN.blit(text_surface, text_rect)

def draw_menu(SCREEN, dth, selected_option, menu_options):
    SCREEN.blit(dth, (0, 0))
    draw_text(SCREEN, "Endless Runner", MENU_FONT_SIZE, SCREEN_WIDTH // 2, 100)
    for i, option in enumerate(menu_options):
        color = RED if i == selected_option else BLACK
        draw_text(SCREEN, option, MENU_FONT_SIZE, SCREEN_WIDTH // 2, 250 + i * 60, color)
    pygame.display.update()

def options_menu(SCREEN, bg, joystick, characters, selected_index):
    
    character_images = [load_character_images(char)['running'][0] for char in characters]

    run = True
    font = pygame.font.Font(FONT_PATH, MENU_FONT_SIZE)
    spacing = 180  
    total_width = spacing * len(characters)
    start_x = (SCREEN_WIDTH - total_width) // 2

    while run:
        SCREEN.blit(bg, (0, 0))
        draw_text(SCREEN, "Choose Your Character:", MENU_FONT_SIZE, SCREEN_WIDTH // 2, 100)
        for i, char in enumerate(characters):
            char_img = pygame.transform.scale(character_images[i], (100, 100))
            img_x = start_x + i * spacing
            img_y = 250
            SCREEN.blit(char_img, (img_x, img_y))
            name_color = RED if i == selected_index else BLACK
            text = font.render(char, True, name_color)
            SCREEN.blit(text, (img_x + 50 - text.get_width() // 2, img_y + 110))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:  # Exemplu: avansăm caracterul
                    selected_index = (selected_index + 1) % len(characters)
                elif event.button == 2:
                    selected_index = (selected_index - 1) % len(characters)
                elif event.button == 9:  # Confirmare
                    return selected_index
    return selected_index

def death_menu(SCREEN, font, points, selected_option, game_options):
    bg = load_background()
    SCREEN.blit(bg, (0,0))
    draw_text(SCREEN, "You lost!", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    draw_text(SCREEN, f"Your Score: {points}", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

    for i, option in enumerate(game_options):
        color = RED if i == selected_option else BLACK
        draw_text(SCREEN, option, 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150 + i * 45, color)
    pygame.display.update()

    return selected_option

def main_menu(SCREEN, bg, joystick):
    selected_option = 0
    menu_options = ["Play", "Options", "Quit"]
    while True:
        draw_menu(SCREEN, bg, selected_option, menu_options)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.button == 3:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.button == 9:
                    return selected_option
        pygame.time.delay(100)
