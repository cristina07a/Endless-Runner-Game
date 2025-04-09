# main.py
import os
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INITIAL_GAME_SPEED, GROUND_HEIGHT, BLACK, RED, FONT_PATH, SCORE_FONT_SIZE, ASSETS_DIR
from audio import init_audio
from config import load_character_images, load_image
from background import load_background, load_scrolling_background, draw_scrolling_background
from player import Dinosaur
from obstacles import Rock, Crystal, Bird
from menu import main_menu, options_menu, death_menu, draw_text


pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Runner")


init_audio()
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("Error: NO CONTROLLER")


bg = load_background()
bg_scroll, ground = load_scrolling_background()
scroll = 0
ground_scroll = 0


characters = ["Frog", "Parrot", "Pig", "Sheep"]
selected_char_index = 0

def game_loop():
    global scroll, ground_scroll
    clock = pygame.time.Clock()
    game_speed = INITIAL_GAME_SPEED
    points = 0
    obstacles = []

    # incarcare resurse personaj selectat
    character_images = load_character_images(characters[selected_char_index])
    player = Dinosaur(character_images)
    score_font = pygame.font.Font(FONT_PATH, SCORE_FONT_SIZE)

    death_count = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        controller = {
            "K_UP": False,
            "K_DOWN": False,
            "K_LEFT": False,
            "K_RIGHT": False,
            "K_RETURN": False
        }
        if joystick:
            controller["K_UP"] = joystick.get_button(3)
            controller["K_DOWN"] = joystick.get_button(0)
            controller["K_LEFT"] = joystick.get_button(2)
            controller["K_RIGHT"] = joystick.get_button(1)
            controller["K_RETURN"] = joystick.get_button(9)

        scroll, ground_scroll = draw_scrolling_background(SCREEN, bg_scroll, ground, scroll, ground_scroll, game_speed)
        player.draw(SCREEN)
        player.update(controller)

        
        if len(obstacles) == 0:
            rand = random.randint(0, 2)
            if rand == 0:
                rock_images = [
                    pygame.transform.scale(load_image("Other", "box.png"), (100, 100)),
                    pygame.transform.scale(load_image("Other", "rock1.PNG"), (100, 100)),
                    pygame.transform.scale(load_image("Other", "rock2.png"), (120, 100))
                ]
                obstacles.append(Rock(rock_images))
            elif rand == 1:
                crystal_images = [
                    pygame.transform.scale(load_image("Other", "barrel3.png"), (100, 100)),
                    pygame.transform.scale(load_image("Crystal", "crystal1.png"), (120, 110)),
                    pygame.transform.scale(load_image("Crystal", "crystal2.png"), (120, 110))
                ]
                obstacles.append(Crystal(crystal_images))
            elif rand == 2:
                bird_images = [
                    pygame.transform.scale(load_image("Bird", "bird3.png"), (90, 70)),
                    pygame.transform.scale(load_image("Bird", "bird4.png"), (90, 70))
                ]
                obstacles.append(Bird(bird_images))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(game_speed, obstacles)
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(10)
                death_count += 1
                game_over(death_count, points)

        points += 1
        if points % 100 == 0:
            game_speed += 1

        #scorul
        score_text = score_font.render("Points: " + str(points), True, BLACK)
        score_rect = score_text.get_rect(center=(1000, 40))
        SCREEN.blit(score_text, score_rect)

        pygame.display.update()
        clock.tick(30)

def game_over(death_count, points):
    selected_option = 0
    game_options = ["Try Again", "Back to Menu", "Quit"]
    font = pygame.font.Font(FONT_PATH, 40)
    run = True

    while run:
        death_menu(SCREEN, font, points, selected_option, game_options)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    selected_option = (selected_option + 1) % len(game_options)
                elif event.button == 3:
                    selected_option = (selected_option - 1) % len(game_options)
                elif event.button == 9:
                    if selected_option == 0:
                        game_loop()
                    elif selected_option == 1:
                        main_run()
                    elif selected_option == 2:
                        pygame.quit()
                        exit()
        pygame.time.delay(100)

def main_run():
    # meniul principal
    option = main_menu(SCREEN, bg, joystick)
    if option == 0:  # Play
        game_loop()
    elif option == 1:  # Options
        global selected_char_index
        selected_char_index = options_menu(SCREEN, bg, joystick, characters, selected_char_index)
        main_run()
    else:  # Quit
        pygame.quit()
        exit()

if __name__ == '__main__':
    main_run()
