import pygame
import os
import random


pygame.init()

pygame.mixer.init() # for songs

pygame.mixer.music.load(os.path.join("Assets/Sound_effects", "nyanCat_theme.mp3")) 

pygame.mixer.music.play(-1)

pygame.joystick.init()

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"controller detected: {joystick.get_name()}")
else:
    print("Error: NO CONTROLLER")

pygame.mixer.init()  # pentru sunete
pygame.mixer.music.load(os.path.join("Assets/Sound_effects", "nyanCat_theme.mp3"))
pygame.mixer.music.play(-1)

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Runner")

BG = pygame.image.load(os.path.join("Assets/Other", "fundal2.png"))
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
BLACK = (0, 0, 0)
font = pygame.font.Font('freesansbold.ttf', 40)

# MENU
menu_options = ["Play", "Options", "Quit"]
selected_option = 0

def draw_menu():
    SCREEN.blit(BG, (0, 0))
    title = font.render("Endless Runner", True, BLACK)
    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    
    for i, option in enumerate(menu_options):
        color = (200, 0, 0) if i == selected_option else BLACK
        text = font.render(option, True, color)
        SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 60))
    
    pygame.display.update()

selected_index = 0
characters = ["Frog", "Parrot", "Pig", "Sheep"]
character_images = [pygame.image.load(os.path.join("Assets/Animal", char, "run1.png")) for char in characters]
IMAGE_PATH = f"Assets/Animal/{characters[selected_index]}"

def draw_options_menu(selected_index):
    SCREEN.blit(BG, (0, 0))
    title = font.render("Choose Your Character:", True, BLACK)
    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    spacing = 180  
    total_width = spacing * len(characters)
    start_x = (SCREEN_WIDTH - total_width) // 2
    for i, char in enumerate(characters):
        char_img = pygame.transform.scale(character_images[i], (100, 100))
        img_x = start_x + i * spacing
        img_y = 250
        SCREEN.blit(char_img, (img_x, img_y))
        name_color = (200, 0, 0) if i == selected_index else BLACK
        char_name = font.render(char, True, name_color)
        SCREEN.blit(char_name, (img_x + 50 - char_name.get_width() // 2, img_y + 110))
    pygame.display.update()

def options():
    global selected_index, IMAGE_PATH, RUNNING, JUMPING, DUCKING
    run = True
    while run:
        draw_options_menu(selected_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # CONTROLLER
            elif event.type == pygame.JOYBUTTONDOWN:                                                                         
                if event.button == 1:  #circle
                    print(f"Button {event.button} pressed")
                    selected_index = (selected_index + 1) % len(characters)
                elif event.button == 2:  #square
                    print(f"Button {event.button} pressed")
                    selected_index = (selected_index - 1) % len(characters)
                elif event.button == 9:  #L1
                    print(f"Button {event.button} pressed")
                    IMAGE_PATH = f"Assets/Animal/{characters[selected_index]}" 
                    RUNNING = [pygame.image.load(os.path.join(IMAGE_PATH, "run1.png")),
                               pygame.image.load(os.path.join(IMAGE_PATH, "run2.png"))]
                    JUMPING = pygame.image.load(os.path.join(IMAGE_PATH, "jump.png"))
                    DUCKING = [pygame.image.load(os.path.join(IMAGE_PATH, "duck1.png")),
                               pygame.image.load(os.path.join(IMAGE_PATH, "duck2.png"))]
                    print(f"Character selected: {characters[selected_index]}, IMAGE_PATH set to {IMAGE_PATH}")
                    run = False
        pygame.display.update()

RUNNING = [pygame.image.load(os.path.join(IMAGE_PATH, "run1.png")),
           pygame.image.load(os.path.join(IMAGE_PATH, "run2.png"))]
JUMPING = pygame.image.load(os.path.join(IMAGE_PATH, "jump.png"))
DUCKING = [pygame.image.load(os.path.join(IMAGE_PATH, "duck1.png")),
           pygame.image.load(os.path.join(IMAGE_PATH, "duck2.png"))]

ROCK = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Other", "box.png")), (100, 100)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Other", "rock1.PNG")), (100, 100)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Other", "rock2.png")), (120, 100))]

CRYSTAL = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Other", "barrel3.png")), (100, 100)),
           pygame.transform.scale(pygame.image.load(os.path.join("Assets/Crystal", "crystal1.png")), (120, 110)),
           pygame.transform.scale(pygame.image.load(os.path.join("Assets/Crystal", "crystal2.png")), (120, 110))]

BIRD = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bird", "bird3.png")), (90, 70)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bird", "bird4.png")), (90, 70))]

# Scrolling background and ground
BG_SCROLL = pygame.image.load(os.path.join("Assets/Other", "fundal.png")).convert()
BG_SCROLL = pygame.transform.scale(BG_SCROLL, (SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND = pygame.image.load(os.path.join("Assets/Other", "dirt4.png")).convert_alpha()
GROUND_HEIGHT = 210
GROUND = pygame.transform.scale(GROUND, (SCREEN_WIDTH, GROUND_HEIGHT))
scroll = 0
ground_scroll = 0
tiles = SCREEN_WIDTH // BG_SCROLL.get_width() + 2

class Dinosaur:
    X_POS = 80
    Y_POS = SCREEN_HEIGHT - GROUND_HEIGHT + 45 
    Y_POS_DUCK = SCREEN_HEIGHT - GROUND_HEIGHT + 50  
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, controller):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if controller["K_UP"] and not self.dino_jump:
            print(f"Button 3 pressed")
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif controller["K_DOWN"] and not self.dino_jump:
            if not self.duck_message_shown:
                print(f"Button 0 pressed")
                self.duck_message_shown = True
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or controller["K_DOWN"]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
            self.duck_message_shown = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class rock(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT + 40 

class crystal(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT + 30

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 20
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def background():
    global scroll, ground_scroll
    for i in range(tiles):
        SCREEN.blit(BG_SCROLL, (i * BG_SCROLL.get_width() + scroll, 0))
    for i in range(tiles):
        SCREEN.blit(GROUND, (i * GROUND.get_width() + ground_scroll, SCREEN_HEIGHT - GROUND_HEIGHT))
    scroll -= game_speed // 2
    ground_scroll -= game_speed
    if abs(scroll) > BG_SCROLL.get_width():
        scroll = 0
    if abs(ground_scroll) > GROUND.get_width():
        ground_scroll = 0

def main():
    global game_speed, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 20
    points = 0
    score_font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = score_font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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

        background()
        player.draw(SCREEN)
        player.update(controller)

        if len(obstacles) == 0:
            rand = random.randint(0, 2)
            if rand == 0:
                obstacles.append(rock(ROCK))
            elif rand == 1:
                obstacles.append(crystal(CRYSTAL))
            elif rand == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(10)
                death_count += 1
                menu(death_count)

        score()
        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global selected_option
    run = True
    game_options = ["Try Again", "Back to Menu", "Quit"]
    while run:
        if death_count == 0:  # main menu
            draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        print(f"Button {event.button} pressed")
                        selected_option = (selected_option + 1) % len(game_options)
                    elif event.button == 3: 
                        print(f"Button {event.button} pressed")
                        selected_option = (selected_option - 1) % len(game_options)
                    elif event.button == 9: 
                        print(f"Button {event.button} pressed") 
                        if selected_option == 0:  # play
                            main()
                        elif selected_option == 1:  # options
                            options()
                        elif selected_option == 2:
                            pygame.quit()
                            exit()
            pygame.display.update()

        elif death_count > 0:  # after losing
            text = font.render("You lost!", True, (0, 0, 0))
            score_text = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score_text.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            SCREEN.blit(score_text, scoreRect)
            
            for i, option in enumerate(game_options):
                color = (200, 0, 0) if i == selected_option else BLACK
                opt_text = font.render(option, True, color)
                SCREEN.blit(opt_text, (SCREEN_WIDTH // 2 - opt_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150 + i * 45))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        print(f"Button {event.button} pressed")
                        selected_option = (selected_option + 1) % len(game_options)
                    elif event.button == 3: 
                        print(f"Button {event.button} pressed")
                        selected_option = (selected_option - 1) % len(game_options)
                    elif event.button == 9:  
                        print(f"Button {event.button} pressed")
                        if selected_option == 0:  # try again
                            main()
                        elif selected_option == 1:  # menu
                            menu(0)
                        elif selected_option == 2:
                            pygame.quit()
                            exit()
            pygame.display.update()

menu(death_count=0)
