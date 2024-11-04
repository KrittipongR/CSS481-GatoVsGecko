import pygame, sys
from src.Resources import *
from src.Dependencies import *
from src.Constants import *
from src.StateMachine import *
from src.states.BaseState import *


class GameOverState(BaseState):

    def __init__(self):
        pass

    def Enter(self, params):
        pass
    
    def update(self, dt, events):
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
    
    def Exit(self):
        pass