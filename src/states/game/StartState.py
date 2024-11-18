from src.states.BaseState import BaseState
import pygame, sys

from src.Constants import *
from src.Resources import *
from src.Util import Button

def draw_text(text, font, text_col):
    img = gFonts[font].render(text, False, text_col)
    return img

class StartState(BaseState):
    def __init__(self):
        # Initialize the play button
        self.t_play = 'PLAY'
        self.btn_play = Button(draw_text(self.t_play, 'medium', (255, 255, 0)), (WIDTH / 2 - (len(self.t_play) / 2) * 24), (HEIGHT / 2 + 96))
        self.inventory = {
            'LIFE': 12,
            'SWORD': 4,
            'ARROW': 4,
            'BOMB': 4,
            'SNIPER': 4,
            'BLOCK': 30,
            'LOOT BOX': 0,
            'MONEY':100,
            'RESET': True
        }

    def Enter(self, params):
        pass

    def update(self, dt, events):
        # Check if the play button is clicked
        if self.btn_play.update():
            g_state_machine.Change('play',enter_params = self.inventory)

        # Process input events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    g_state_machine.Change('play',enter_params = self.inventory)

    def render(self, screen):
        # Render the title
        t_title = gFonts['large'].render("Gato vs Gecko", False, (255, 255, 255))
        rect = t_title.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(t_title, rect)

        # Render the play button
        self.btn_play.render(screen)

    def Exit(self):
        gSounds['select'].play()
