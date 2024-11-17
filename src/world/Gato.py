import pygame
import math
from src.Util import SpriteManager, Template, convertGridToCoords, convertCoordsToGrid
from src.Constants import *

class Gato:
    def __init__(self, row, col, template_id=1):
        self.template = Template("gato", template_id)
        self.row = row
        self.col = col
        print("gato placed at grid: " + str(self.row) + ", " + str(self.col))

    names = {
        1: "sniper_cat_left_1",
        2: "arrow_cat_left_1",
        3: "bomb_kitty_left_1",
        4: "sameowrai_1"
    }

    def update(self, dt, events):
        pass

    def render(self, screen):
        self.sprite = pygame.transform.scale(self.sprite_collection[self.sprite_name].image, (TILE_SIZE, TILE_SIZE))
        screen.blit(self.sprite, (self.x - (TILE_SIZE / 2), self.y - (TILE_SIZE / 2)))