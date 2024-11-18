import pygame, sys
from src.Resources import *
from src.Dependencies import *
from src.Constants import *
from src.StateMachine import *
from src.states.BaseState import *
from src.Util import Button
from src.world.Stage import Stage

from src.Util import convertGridToCoords, convertCoordsToGrid

def draw_text(text, font, text_col):
    img = gFonts[font].render(text, False, text_col)
    return img

class PlayState(BaseState):

    def __init__(self):
        # Button initializations
        self.t_ready = 'READY'
        self.btn_ready = Button(draw_text(self.t_ready, 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 2))
        self.t_shop = 'SHOP'
        self.btn_shop = Button(draw_text(self.t_shop, 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 3))
        
        # Items available to buy
        self.inventory = {
            'LIFE': 0,
            'SWORD': 1,
            'ARROW': 1,
            'BOMB': 1,
            'SNIPER': 1,
            'BLOCK': 10,
            'LOOT BOX': 0
        }

        # Initialize buttons for each item with dynamic text
        self.btn_sword = Button(draw_text(f'SWORD ({self.inventory["SWORD"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 4))
        self.btn_arrow = Button(draw_text(f'ARROW ({self.inventory["ARROW"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 5))
        self.btn_bomb = Button(draw_text(f'BOMB ({self.inventory["BOMB"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 6))
        self.btn_sniper = Button(draw_text(f'SNIPER ({self.inventory["SNIPER"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 7))
        self.btn_block = Button(draw_text(f'BLOCK ({self.inventory["BLOCK"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 8))
        # self.btn_life = Button(draw_text(f'LIFE ({self.inventory["LIFE"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 9))
        
        self.t_setting = 'SETTINGS'
        self.btn_setting = Button(draw_text(self.t_setting, 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (HEIGHT - 48))

        # Init Stage
        self.wave = 1
        self.stage = Stage()

        self.selectedPlaceable = None

    def Enter(self, params):
        pass
    
    def buttonHover(self):
        # Change button color based on hover status
        if self.btn_ready.hover or self.stage.state == 1:
            self.btn_ready.image = draw_text(self.t_ready, 'small', (255, 255, 0))
        else:
            self.btn_ready.image = draw_text(self.t_ready, 'small', (255, 255, 255))

        if self.btn_shop.hover:
            self.btn_shop.image = draw_text(self.t_shop, 'small', (255, 255, 0))
        else:
            self.btn_shop.image = draw_text(self.t_shop, 'small', (255, 255, 255))

        if self.btn_sword.hover or self.selectedPlaceable == "SWORD":
            self.btn_sword.image = draw_text(f'SWORD ({self.inventory["SWORD"]})', 'small', (255, 255, 0))
        else:
            self.btn_sword.image = draw_text(f'SWORD ({self.inventory["SWORD"]})', 'small', (255, 255, 255))

        if self.btn_arrow.hover or self.selectedPlaceable == "ARROW":
            self.btn_arrow.image = draw_text(f'ARROW ({self.inventory["ARROW"]})', 'small', (255, 255, 0))
        else:
            self.btn_arrow.image = draw_text(f'ARROW ({self.inventory["ARROW"]})', 'small', (255, 255, 255))

        if self.btn_bomb.hover or self.selectedPlaceable == "BOMB":
            self.btn_bomb.image = draw_text(f'BOMB ({self.inventory["BOMB"]})', 'small', (255, 255, 0))
        else:
            self.btn_bomb.image = draw_text(f'BOMB ({self.inventory["BOMB"]})', 'small', (255, 255, 255))

        if self.btn_sniper.hover or self.selectedPlaceable == "SNIPER":
            self.btn_sniper.image = draw_text(f'SNIPER ({self.inventory["SNIPER"]})', 'small', (255, 255, 0))
        else:
            self.btn_sniper.image = draw_text(f'SNIPER ({self.inventory["SNIPER"]})', 'small', (255, 255, 255))

        if self.btn_block.hover or self.selectedPlaceable == "BLOCK":
            self.btn_block.image = draw_text(f'BLOCK ({self.inventory["BLOCK"]})', 'small', (255, 255, 0))
        else:
            self.btn_block.image = draw_text(f'BLOCK ({self.inventory["BLOCK"]})', 'small', (255, 255, 255))

        # if self.btn_life.hover or self.selectedPlaceable == "LIFE":
        #     self.btn_life.image = draw_text(f'LIFE ({self.inventory["LIFE"]})', 'small', (255, 255, 0))
        # else:
        #     self.btn_life.image = draw_text(f'LIFE ({self.inventory["LIFE"]})', 'small', (255, 255, 255))

        if self.btn_setting.hover:
            self.btn_setting.image = draw_text(self.t_setting, 'small', (255, 255, 0))
        else:
            self.btn_setting.image = draw_text(self.t_setting, 'small', (255, 255, 255))

    def update(self, dt, events):
        # Lives display

        # Check if each button is clicked by calling `update`
        if self.btn_ready.update():
            gSounds['select'].play()
            print("Ready button clicked")
            self.stage.GenerateEntities(wave=self.wave)
        
        if self.btn_shop.update():
            gSounds['select'].play()
            g_state_machine.Change('shop', {"inventory": self.inventory})
        
        if self.btn_sword.update() and self.inventory["SWORD"] > 0:
            gSounds['select'].play()
            self.selectedPlaceable = "SWORD"

        if self.btn_arrow.update() and self.inventory["ARROW"] > 0:
            gSounds['select'].play()
            self.selectedPlaceable = "ARROW"

        if self.btn_bomb.update() and self.inventory["BOMB"] > 0:
            gSounds['select'].play()
            self.selectedPlaceable = "BOMB"

        if self.btn_sniper.update() and self.inventory["SNIPER"] > 0:
            gSounds['select'].play()
            self.selectedPlaceable = "SNIPER"

        if self.btn_block.update() and self.inventory["BLOCK"] > 0:
            gSounds['select'].play()
            self.selectedPlaceable = "BLOCK"
        
        # if self.btn_life.update() and self.inventory["LIFE"] > 0:
        #     gSounds['select'].play()
        #     self.inventory["LIFE"] -= 1

        if self.btn_setting.update():
            gSounds['select'].play()
            print("Settings button clicked")

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
                if event.key == pygame.K_r and (grid := convertCoordsToGrid(pygame.mouse.get_pos())) is not None and grid[1] < MAP_WIDTH - 1:
                    self.stage.rotateGato(grid)
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.selectedPlaceable is not None and (grid := convertCoordsToGrid(event.pos)) is not None and grid[1] < MAP_WIDTH - 1:
                    if self.stage.placeObject(grid[0], grid[1], self.selectedPlaceable):
                        self.inventory[self.selectedPlaceable] -= 1
                    else:
                        print("Placement rejected")
                    self.selectedPlaceable = None

        self.buttonHover()
        self.stage.update(dt, events)
    
    def render(self, screen):
        self.stage.render(screen, 0, 0)

        self.lives_text = draw_text(f'LIVES: {self.inventory["LIFE"]}', 'small', (255, 255, 255))
        self.lives_text_rect = self.lives_text.get_rect()
        self.lives_text_rect.topleft = ((WIDTH - (WIDTH / 10) - 24), (48 * 1))
        screen.blit(self.lives_text, self.lives_text_rect.topleft)

        self.btn_ready.render(screen)
        self.btn_shop.render(screen)
        self.btn_sword.render(screen)
        self.btn_arrow.render(screen)
        self.btn_bomb.render(screen)
        self.btn_sniper.render(screen)
        self.btn_block.render(screen)
        self.btn_setting.render(screen)

        # Sanity Check
        # image = pygame.image.load("./graphics/gato_DownRight.png")
        # screen.blit(image, (0,0))

    def Exit(self):
        pass
