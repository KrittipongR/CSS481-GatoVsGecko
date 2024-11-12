import pygame

pygame.init()

from src.Dependencies import *
from src.Constants import *
from src.Resources import *

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        g_state_machine.SetScreen(self.screen)
        #0,1,2 are place holders
        states = {
            'start': StartState(),
            'play' : PlayState(),
            'game_over': GameOverState(),
            'shop': ShopState()
        }

        g_state_machine.SetStates(states)
        

    def PlayGame(self):
        gSounds['music'].play(-1)

        clock = pygame.time.Clock()

        g_state_machine.Change('start')

        while True:
            pygame.display.set_caption("Gato vs Gecko running with {:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            events = pygame.event.get()

            g_state_machine.update(dt,events)

            self.screen.fill((0,0,0))
            g_state_machine.render()

            pygame.display.update()

if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()