# obstacles.py
import random
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT

class Obstacle:
    def __init__(self, image_list, type):
        self.image_list = image_list
        self.type = type
        self.image = self.image_list[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles_list):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles_list.remove(self)

    def draw(self, SCREEN):
        SCREEN.blit(self.image_list[self.type], self.rect)

class Rock(Obstacle):
    def __init__(self, image_list):
        self.type = random.randint(0, len(image_list) - 1)
        super().__init__(image_list, self.type)
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT + 40

class Crystal(Obstacle):
    def __init__(self, image_list):
        self.type = random.randint(0, len(image_list) - 1)
        super().__init__(image_list, self.type)
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT + 30

class Bird(Obstacle):
    def __init__(self, image_list):
        self.type = 0
        super().__init__(image_list, self.type)
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 20
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image_list[self.index // 5], self.rect)
        self.index += 1
