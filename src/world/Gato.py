import pygame
import math
from src.Util import SpriteManager, Template, convertGridToCoords, convertCoordsToGrid
from src.Constants import *

class Gato:
    def __init__(self, row, col, template_id=1, lvl=1):
        self.template_id = template_id
        self.template = Template("gato", self.template_id)
        (self.x, self.y) = convertGridToCoords((row, col))
        self.row = row
        self.col = col
        self.lvl = lvl
        print("gato placed at grid: " + str(self.row) + ", " + str(self.col))
        self.setDirection(1)

    names = {
        1: "sniper_cat",
        2: "arrow_cat",
        3: "bomb_kitty",
        4: "sameowrai"
    }

    def setDirection(self, direction):
        direction = direction % 4
        match direction:
            case 0 | 1 | 2:
                directionStr = "_left_"
                self.path = "./sprites/gato_UpLeft.json"
            case 3:
                directionStr = "_right_"
                self.path = "./sprites/gato_DownRight.json"

        self.currentDirection = direction

        self.sprite_collection = SpriteManager([self.path]).spriteCollection

        self.sprite_name = Gato.names[self.template_id] + directionStr + str(self.lvl)
        self.sprite = pygame.transform.smoothscale(self.sprite_collection[self.sprite_name].image, (TILE_SIZE, TILE_SIZE))
        self.wpn_sprite_name = Gato.names[self.template_id] + directionStr + "weapon"
        wpn_rotation = (direction-1)*90 if direction != 3 else 0
        self.wpn_sprite = pygame.transform.smoothscale(pygame.transform.rotate(self.sprite_collection[self.wpn_sprite_name].image, wpn_rotation), (TILE_SIZE, TILE_SIZE))

    def update(self, dt, events):
        pass

    def render(self, screen):       
        self.sprite.set_colorkey(self.sprite.get_at((0, 0)),pygame.RLEACCEL)
        self.wpn_sprite.set_colorkey(self.wpn_sprite.get_at((0, 0)),pygame.RLEACCEL)
        screen.blit(self.sprite, (self.x - (TILE_SIZE / 2), self.y - (TILE_SIZE / 2)))
        screen.blit(self.wpn_sprite, (self.x - (TILE_SIZE / 2), self.y - (TILE_SIZE / 2)))