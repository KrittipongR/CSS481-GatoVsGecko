import pygame, sys
from src.Dependencies import *
from src.Resources import *
from src.Constants import *
from src.StateMachine import *
from src.states.BaseState import *
from src.Util import Button

def draw_text(text, font, text_col):
    img = gFonts[font].render(text, False, text_col)
    return img

class ShopState(BaseState):

    def __init__(self):
        # Sample items in the shop
        self.items = [
            {"name": "Extra Life", "cost": 50},
            {"name": "Power Boost", "cost": 100},
            {"name": "Shield", "cost": 75}
        ]
        self.selected_index = 0  # Track which item is selected
        self.back_button = Button(draw_text("BACK", 'small', (255, 255, 255)), WIDTH - 80, HEIGHT - 50)

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
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.items)
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.items)
                elif event.key == pygame.K_RETURN:
                    selected_item = self.items[self.selected_index]
                    print(f"Attempting to purchase {selected_item['name']} for {selected_item['cost']} coins.")

        # Check if back button is clicked
        if self.back_button.update():  # Now using update to check for action
            g_state_machine.Change('play')  # Change state back to play

        # Update back button hover effect
        if self.back_button.hover:
            self.back_button.image = draw_text("BACK", 'small', (255, 255, 0))
        else:
            self.back_button.image = draw_text("BACK", 'small', (255, 255, 255))


    def render(self, screen):
        # Render shop title
        title_text = draw_text("SHOP", 'large', (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        # Render items
        for i, item in enumerate(self.items):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            item_text = draw_text(f"{item['name']} - {item['cost']} coins", 'small', color)
            screen.blit(item_text, (WIDTH // 2 - 100, 150 + i * 40))

        # Render back button
        self.back_button.render(screen)

    def Exit(self):
        gSounds['select'].play()
