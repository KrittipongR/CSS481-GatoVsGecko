import pygame, sys
import random  # Import random for selecting a loot item
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
        # Define the items in the shop (Including Loot Box)
        self.items = [
            {"name": "SWORD", "cost": 15},
            {"name": "ARROW", "cost": 15},
            {"name": "BOMB", "cost": 15},
            {"name": "SNIPER", "cost": 20},
            {"name": "BLOCK", "cost": 5},
            {"name": "LIFE", "cost": 100},
            {"name": "Loot Box", "cost": 10}
        ]

        raw_bg_image = pygame.image.load('graphics/shop.png')
        self.bg_image = pygame.transform.scale(raw_bg_image, (WIDTH, HEIGHT))
        
        # Define the pool of items that can be awarded from the Loot Box
        self.loot_box_pool = [
            {"name": "SWORD", "cost": 100},
            {"name": "ARROW", "cost": 50},
            {"name": "BOMB", "cost": 75},
            {"name": "SNIPER", "cost": 150}
        ]
        
        self.item_buttons = [
            Button(draw_text(f"{item['name']} - {item['cost']} coins", 'small', (255, 255, 255)), 200, 250 + i * 50)
            for i, item in enumerate(self.items)
        ]
        self.back_button = Button(draw_text("BACK", 'small', (255, 255, 255)), WIDTH - 80, HEIGHT - 50)

        # Player's inventory reference
        self.player_inventory = None  # Will be set in Enter

        self.last_item_bought = None
        self.item_display_time = 0

    def Enter(self, params):
        # Assign player's inventory passed from PlayState
        self.player_inventory = params.get('inventory')

    def update(self, dt, events):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    g_state_machine.Change('play')

        for i, button in enumerate(self.item_buttons):
            if button.rect.collidepoint(mouse_x, mouse_y):
                button.hover = True
            else:
                button.hover = False

            if button.update():
                selected_item = self.items[i]
                if selected_item["name"] == "Loot Box":
                    loot_item = random.choice(self.loot_box_pool)
                    print(f"Congratulations! You won a {loot_item['name']} from the Loot Box!")
                    self.player_inventory[loot_item["name"]] += 1  # Update inventory
                    self.last_item_bought = loot_item
                    self.item_display_time = pygame.time.get_ticks()
                    gSounds['select'].play()
                else:
                    print(f"Attempting to purchase {selected_item['name']} for {selected_item['cost']} coins.")
                    self.player_inventory[selected_item["name"]] += 1  # Update inventory
                    self.last_item_bought = selected_item
                    self.item_display_time = pygame.time.get_ticks()
                    gSounds['select'].play()

        if self.back_button.update():
            g_state_machine.Change('play')

    def render(self, screen):

        screen.blit(self.bg_image, (0, 0))

        for i, button in enumerate(self.item_buttons):
            if button.hover:
                button.image = draw_text(f"{self.items[i]['name']} - {self.items[i]['cost']} coins", 'small', (255, 255, 0))
            else:
                button.image = draw_text(f"{self.items[i]['name']} - {self.items[i]['cost']} coins", 'small', (255, 255, 255))
            button.render(screen)

        self.back_button.render(screen)

        if self.last_item_bought:
            time_elapsed = pygame.time.get_ticks() - self.item_display_time
            if time_elapsed < 3000:
                item_text = draw_text(f"You got: {self.last_item_bought['name']}", 'medium', (255, 255, 0))
                item_rect = item_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
                screen.blit(item_text, item_rect)

    def Exit(self):
        pass
