import pygame, sys
from src.Resources import *
from src.Dependencies import *
from src.Constants import *
from src.StateMachine import *
from src.states.BaseState import *
from src.Util import Button
from src.world.Stage import Stage

def draw_text(text, font, text_col):
    img = gFonts[font].render(text, False, text_col)
    return img

class PlayState(BaseState):

    def __init__(self):
        # Button initializations
        self.t_ready = 'READY'
        self.btn_ready = Button(draw_text(self.t_ready, 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10)), (48 * 2))
        self.t_shop = 'SHOP'
        self.btn_shop = Button(draw_text(self.t_shop, 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10)), (48 * 3))
        self.t_inv = 'INV.'
        self.btn_inv = Button(draw_text(self.t_inv, 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10)), (48 * 4))
        self.t_setting = 'SETTINGS'
        self.btn_setting = Button(draw_text(self.t_setting, 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10)), (HEIGHT - 48))

        #Init Stage
        self.wave = 1
        self.stage = Stage()

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

        if self.btn_inv.hover:
            self.btn_inv.image = draw_text(self.t_inv, 'small', (255, 255, 0))
        else:
            self.btn_inv.image = draw_text(self.t_inv, 'small', (255, 255, 255))

        if self.btn_setting.hover:
            self.btn_setting.image = draw_text(self.t_setting, 'small', (255, 255, 0))
        else:
            self.btn_setting.image = draw_text(self.t_setting, 'small', (255, 255, 255))

    def update(self, dt, events):
        # Check if each button is clicked by calling `update`
        if self.btn_ready.update():
            gSounds['select'].play()
            print("Ready button clicked")  # Example action
            self.stage.GenerateEntities(wave=self.wave)
        
        if self.btn_shop.update():
            gSounds['select'].play()
            g_state_machine.Change('shop')
        
        if self.btn_inv.update():
            gSounds['select'].play()
            print("Inventory button clicked")  # Example action
        
        if self.btn_setting.update():
            gSounds['select'].play()
            print("Settings button clicked")  # Example action

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
                    g_state_machine.Change('game_over')
        
        # Button hovering
        self.buttonHover()

        self.stage.update(dt, events)
    
    def render(self, screen):

        self.stage.render(screen, -TILE_SIZE*2, 0)

        # Render the title
        # t_title = gFonts['small'].render("This is the play state", False, (255, 255, 255))
        # rect = t_title.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        # screen.blit(t_title, rect)

        # Side menu bar
        t_wave = 'Wave 1'
        screen.blit(draw_text(t_wave, 'small', (255, 255, 255)), (WIDTH - (WIDTH / 10), 48))

        # Render buttons
        self.btn_ready.render(screen)
        self.btn_shop.render(screen)
        self.btn_inv.render(screen)
        self.btn_setting.render(screen)

        # Example of additional rendering
        # screen.blit(gIcon_image_list[1], (60, 60))  # Render a left arrow icon

    def Exit(self):
        pass
