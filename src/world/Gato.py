import pygame
from src.Util import Template

class Gato:
    def __init__(self, template_id=1, pos=(0,0)):
        self.template = Template("gato", template_id)
        self.row, self.col = pos
        print("gato placed at grid: " + str(self.row) + ", " + str(self.col))

    def update(self, dt, events):
        pass

    def render(self, screen):
        screen.blit(self.template.sprite, (self.x, self.y))