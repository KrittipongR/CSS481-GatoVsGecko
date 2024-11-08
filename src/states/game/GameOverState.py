import pygame, sys
from src.Resources import *
from src.Dependencies import *
from src.Constants import *
from src.StateMachine import *
from src.states.BaseState import *
from src.Util import Button

def draw_text(text, font, text_col):
    img = gFonts[font].render(text, False, text_col)
    return img

class GameOverState(BaseState):

    def __init__(self):
        pass

    def Enter(self, params):
        gSounds['game_over'].play()
        self.t_retry = 'RETRY'
        self.btn_retry = Button(draw_text(self.t_retry, 'medium', (255,255,0)),(WIDTH/2-(len(self.t_retry)/2)*24),(HEIGHT/2 + 96))
    
    def update(self, dt, events):

        if self.btn_retry.clicked:
            g_state_machine.Change('start')

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    g_state_machine.Change('start')
    
    def render(self, screen):
        t_title = gFonts['large'].render("GAME OVER", False, (255,255,255))
        rect = t_title.get_rect(center = (WIDTH/2, HEIGHT/2))
        screen.blit(t_title,rect)
        self.btn_retry.render(screen)
    
    def Exit(self):
        gSounds['select'].play()