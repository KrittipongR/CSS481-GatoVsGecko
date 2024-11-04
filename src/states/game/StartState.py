from src.states.BastState import BaseState
import pygame, sys

from src.Constants import *
from src.Recourses import *

class StartState(BaseState):
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
                    g_state_machine.Change('play')

    def render(self, screen):
        t_title = gFonts['large'].render("Gato vs Gecko", False, (255,255,255))
        rect = t_title.get_rect(center = (WIDTH/2, HEIGHT/2))
        screen.blit(t_title,rect)

        t_press_enter = gFonts['small'].render("Press Enter", False, (255,255,255))
        rect = t_press_enter.get_rect(center=(WIDTH/2, HEIGHT/2 + 96))
        screen.blit(t_press_enter,rect)

    def Exit(self):
        pass