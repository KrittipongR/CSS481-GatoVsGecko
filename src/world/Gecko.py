import pygame
from src.Util import SpriteManager, Template

class Gecko:
    directions = {
        "up": 0,
        "left": 1,
        "down": 2,
        "right": 3
    }
    names = {
        1: "gecko",
        2: "gigaGecko",
        3: "chameleon",
        4: "jinglen"
    }

    def __init__(self, template_id=1, pos=(0,0)):
        self.template_id = template_id
        self.template = Template("gecko", self.template_id)
        self.x, self.y = pos
        self.hp = self.template.data["maxHP"]
        self.setDirection("right")
        print("gecko generated at: " + str(self.x) + ", " + str(self.y))

    def setDirection(self, direction):
        self.direction = Gecko.directions[direction]
        if self.direction < 2:
            self.path = "./sprites/gecko_UpLeft.json"
            self.sprite_name = Gecko.names[self.template_id] + "_walk_up"
        else:
            self.path = "./sprites/gecko_DownRight.json"
            self.sprite_name = Gecko.names[self.template_id] + "_walk_down"
        self.sprite_collection = SpriteManager(path=self.path).spriteCollection
        

    def update(self, dt, events):
        # Move left to right, nothing more
        self.x += self.template.data["movement"] * dt
        self.sprite_collection[self.sprite_name].animation.update(dt)

    def render(self, screen):
        self.sprite = self.sprite_collection[self.sprite_name].animation.image
        screen.blit(self.sprite, (self.x, self.y))