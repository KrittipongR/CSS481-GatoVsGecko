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
        self.t_play = 'PLAY'
        self.btn_play = Button(draw_text(self.t_play, 'medium', (255,255,0)),(WIDTH/2-(len(self.t_play)/2)*24),(HEIGHT/2 + 96))
        pass

    def Enter(self, params):
        pass

    def update(self, dt, events):

        if self.btn_play.clicked:
            g_state_machine.Change('play')

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    g_state_machine.Change('play')

    def render(self, screen):
        t_title = gFonts['large'].render("Gato vs Gecko", False, (255,255,255))
        rect = t_title.get_rect(center = (WIDTH/2, HEIGHT/2))
        screen.blit(t_title,rect)

        self.btn_play.render(screen)

    def Exit(self):
        gSounds['select'].play()