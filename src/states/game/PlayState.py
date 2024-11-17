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
            'SWORD': 0,
            'ARROW': 0,
            'BOMB': 0,
            'SNIPER': 0,
            'BLOCK': 0,
            'LIFE': 0,
            'LOOT BOX': 0
        }

        # Initialize buttons for each item with dynamic text
        self.btn_sword = Button(draw_text(f'SWORD ({self.inventory["SWORD"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 4))
        self.btn_arrow = Button(draw_text(f'ARROW ({self.inventory["ARROW"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 5))
        self.btn_bomb = Button(draw_text(f'BOMB ({self.inventory["BOMB"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 6))
        self.btn_sniper = Button(draw_text(f'SNIPER ({self.inventory["SNIPER"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 7))
        self.btn_block = Button(draw_text(f'BLOCK ({self.inventory["BLOCK"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 8))
        self.btn_life = Button(draw_text(f'LIFE ({self.inventory["LIFE"]})', 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10) - 24), (48 * 9))
        
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
        if self.btn_ready.hover:
            self.btn_ready.image = draw_text(self.t_ready, 'small', (255, 255, 0))
        else:
            self.btn_ready.image = draw_text(self.t_ready, 'small', (255, 255, 255))

        if self.btn_shop.hover:
            self.btn_shop.image = draw_text(self.t_shop, 'small', (255, 255, 0))
        else:
            self.btn_shop.image = draw_text(self.t_shop, 'small', (255, 255, 255))

        if self.btn_sword.hover:
            self.btn_sword.image = draw_text(f'SWORD ({self.inventory["SWORD"]})', 'small', (255, 255, 0))
        else:
            self.btn_sword.image = draw_text(f'SWORD ({self.inventory["SWORD"]})', 'small', (255, 255, 255))

        if self.btn_arrow.hover:
            self.btn_arrow.image = draw_text(f'ARROW ({self.inventory["ARROW"]})', 'small', (255, 255, 0))
        else:
            self.btn_arrow.image = draw_text(f'ARROW ({self.inventory["ARROW"]})', 'small', (255, 255, 255))

        if self.btn_bomb.hover:
            self.btn_bomb.image = draw_text(f'BOMB ({self.inventory["BOMB"]})', 'small', (255, 255, 0))
        else:
            self.btn_bomb.image = draw_text(f'BOMB ({self.inventory["BOMB"]})', 'small', (255, 255, 255))

        if self.btn_sniper.hover:
            self.btn_sniper.image = draw_text(f'SNIPER ({self.inventory["SNIPER"]})', 'small', (255, 255, 0))
        else:
            self.btn_sniper.image = draw_text(f'SNIPER ({self.inventory["SNIPER"]})', 'small', (255, 255, 255))

        if self.btn_block.hover:
            self.btn_block.image = draw_text(f'BLOCK ({self.inventory["BLOCK"]})', 'small', (255, 255, 0))
        else:
            self.btn_block.image = draw_text(f'BLOCK ({self.inventory["BLOCK"]})', 'small', (255, 255, 255))

        if self.btn_life.hover:
            self.btn_life.image = draw_text(f'LIFE ({self.inventory["LIFE"]})', 'small', (255, 255, 0))
        else:
            self.btn_life.image = draw_text(f'LIFE ({self.inventory["LIFE"]})', 'small', (255, 255, 255))

        if self.btn_setting.hover:
            self.btn_setting.image = draw_text(self.t_setting, 'small', (255, 255, 0))
        else:
            self.btn_setting.image = draw_text(self.t_setting, 'small', (255, 255, 255))

    def update(self, dt, events):
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
            self.inventory["SWORD"] -= 1
            print("Sword used, remaining:", self.inventory["SWORD"])

        if self.btn_arrow.update() and self.inventory["ARROW"] > 0:
            gSounds['select'].play()
            self.inventory["ARROW"] -= 1
            print("Arrow used, remaining:", self.inventory["ARROW"])

        if self.btn_bomb.update() and self.inventory["BOMB"] > 0:
            gSounds['select'].play()
            self.inventory["BOMB"] -= 1
            print("Bomb used, remaining:", self.inventory["BOMB"])

        if self.btn_sniper.update() and self.inventory["SNIPER"] > 0:
            gSounds['select'].play()
            self.inventory["SNIPER"] -= 1
            print("Sniper used, remaining:", self.inventory["SNIPER"])

        if self.btn_block.update() and self.inventory["BLOCK"] > 0:
            gSounds['select'].play()
            self.inventory["BLOCK"] -= 1
            print("Block used, remaining:", self.inventory["BLOCK"])
        
        if self.btn_life.update() and self.inventory["LIFE"] > 0:
            gSounds['select'].play()
            self.inventory["LIFE"] -= 1
            print("Life used, remaining:", self.inventory["LIFE"])

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
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.selectedPlaceable is not None and (grid := convertCoordsToGrid(event.pos)) is not None:
                    if self.stage.placeObject(grid[0], grid[1], self.selectedPlaceable):
                        pass
                    else:
                        print("Placement rejected")

        self.buttonHover()
        self.stage.update(dt, events)
    
    def render(self, screen):
        self.stage.render(screen, 0, 0)
        self.btn_ready.render(screen)
        self.btn_shop.render(screen)
        self.btn_sword.render(screen)
        self.btn_arrow.render(screen)
        self.btn_bomb.render(screen)
        self.btn_sniper.render(screen)
        self.btn_block.render(screen)
        self.btn_life.render(screen)
        self.btn_setting.render(screen)

    def Exit(self):
        pass
