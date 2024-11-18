import pygame
import math
from src.Util import SpriteManager, Template, convertGridToCoords, convertCoordsToGrid, calculateAngle
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
        self.setDirection(90)


        self.targets = []
        self.attackRadius: float = self.template.data["range"] * 10
        try:
            self.targeting: str = self.template.data["targeting"]
        except KeyError:
            self.targeting: str = "first"
        #

    names = {
        1: "sniper_cat",
        2: "arrow_cat",
        3: "bomb_kitty",
        4: "sameowrai"
    }

    def setDirection(self, direction):
        direction = direction % 360
        path = "./sprites/gato_UpLeft.json"
        self.sprite_collection = SpriteManager([path]).spriteCollection
        self.sprite_name = Gato.names[self.template_id] + "_left_" + str(self.lvl)
        self.sprite = pygame.transform.smoothscale(self.sprite_collection[self.sprite_name].image, (TILE_SIZE, TILE_SIZE))
        self.wpn_sprite_name = Gato.names[self.template_id] + "_left_weapon"
        self.wpn_sprite = self.sprite_collection[self.wpn_sprite_name].image
        if 0 <= direction < 180:            
            wpn_rotation = direction - 90
            self.wpn_sprite = pygame.transform.rotate(self.wpn_sprite, wpn_rotation)
        else:
            wpn_rotation = direction - 270
            self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.wpn_sprite = pygame.transform.flip(self.wpn_sprite, True, False)

        self.wpn_sprite = pygame.transform.smoothscale(self.wpn_sprite, (TILE_SIZE, TILE_SIZE))
        

    def clearTargets(self):
        self.targets = []

    def addTarget(self, gecko):
        self.targets.append(gecko)

    def update(self, dt, events):
        # Attacking
        if self.targets:
            match self.targeting:
                case "first":
                    self.targets = sorted(self.targets, key=lambda x: x.floatingPathProgress)
                    target = self.targets.pop()
                    # self.setDirection(calculateAngle((self.x, self.y), (target.x, target.y)))
            pass

    def render(self, screen):       
        self.sprite.set_colorkey(self.sprite.get_at((0, 0)),pygame.RLEACCEL)
        self.wpn_sprite.set_colorkey(self.wpn_sprite.get_at((0, 0)),pygame.RLEACCEL)
        screen.blit(self.sprite, (self.x - (TILE_SIZE / 2), self.y - (TILE_SIZE / 2)))
        screen.blit(self.wpn_sprite, (self.x - (TILE_SIZE / 2), self.y - (TILE_SIZE / 2)))