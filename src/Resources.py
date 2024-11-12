import pygame
from src.Util import SpriteManager, Animation
import src.Util as Util
from src.StateMachine import *

g_state_machine = StateMachine()

sprite_collection = SpriteManager().spriteCollection

gIcon_image_list = [sprite_collection["arrow_left"].image, sprite_collection["arrow_right"].image,
                    sprite_collection["arrow_up"].image, sprite_collection["arrow_down"].image]

gStage_image_list = Util.GenerateTiles("./graphics/tilesheet.png", 16, 16)
gDoor_image_list = Util.GenerateTiles("./graphics/tilesheet.png", 16, 16, colorkey=(13, 7, 17, 255))

gFonts ={
    'small': pygame.font.Font('fonts/font.ttf', 24),
    'medium': pygame.font.Font('fonts/font.ttf', 48),
    'large': pygame.font.Font('fonts/font.ttf', 96),
}

gSounds = {
    'music': pygame.mixer.Sound('sounds/dawn-of-war-DSTechnician.mp3'),
    'select': pygame.mixer.Sound('sounds/select.wav'),
    'game_over': pygame.mixer.Sound('sounds/game over.wav')
}