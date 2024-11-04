import pygame, sys
from src.Recourses import *
from src.Dependencies import *
from src.Constants import *
from src.StateMachine import *
from src.states.BastState import *


class PlayState(BaseState):

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
                    g_state_machine.Change('game_over')
    
    def render(self, screen):
        t_title = gFonts['large'].render("This is the play state", False, (255,255,255))
        rect = t_title.get_rect(center = (WIDTH/2, HEIGHT/2))
        screen.blit(t_title,rect)
    
    def Exit(self):
        pass