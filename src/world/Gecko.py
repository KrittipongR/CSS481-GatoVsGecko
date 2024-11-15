import pygame
from src.Util import Template

class Gecko:
    def __init__(self, template_id=1, pos=(0,0)):
        self.template = Template("gecko", template_id)
        self.x, self.y = pos
        self.hp = self.template.data["maxHP"]
        print("gecko generated at: " + str(self.x) + ", " + str(self.y))

    def update(self, dt, events):
        # Move left to right, nothing more
        self.x += self.template.data["movement"] * dt

    def render(self, screen):
        screen.blit(self.template.sprite, (self.x, self.y))