from src.Constants import *
from src.Resources import *
from src.Util import convertGridToCoords

class Blockade:
    def __init__ (self, row, col):
        self.row = row
        self.col = col
    
    def render(self, screen):
        screen.blit(gDoor_image_list[BLOCKADE[0]-1], convertGridToCoords((self.row, self.col), center=False))