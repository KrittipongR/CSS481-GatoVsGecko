import pygame, sys
import random
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

        self.player_inventory = None
        self.last_item_bought = None
        self.item_display_time = 0
        self.insufficient_funds = False
        self.insufficient_funds_time = 0

    def Enter(self, params):
        self.player_inventory = params.get('inventory')

    def update(self, dt, events):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    g_state_machine.Change('play', {
                        'LIFE': self.player_inventory['LIFE'],
                        'SWORD': self.player_inventory['SWORD'],
                        'ARROW': self.player_inventory['ARROW'],
                        'BOMB': self.player_inventory['BOMB'],
                        'SNIPER': self.player_inventory['SNIPER'],
                        'BLOCK': self.player_inventory['BLOCK'],
                        'LOOT BOX': self.player_inventory['LOOT BOX'],
                        'MONEY': self.player_inventory['MONEY'],
                        'RESET': False
                    })

        for i, button in enumerate(self.item_buttons):
            if button.rect.collidepoint(mouse_x, mouse_y):
                button.hover = True
            else:
                button.hover = False

            if button.update():
                selected_item = self.items[i]
                if self.player_inventory["MONEY"] >= selected_item["cost"]:
                    self.player_inventory["MONEY"] -= selected_item["cost"]
                    if selected_item["name"] == "Loot Box":
                        loot_item = random.choice(self.loot_box_pool)
                        print(f"Congratulations! You won a {loot_item['name']} from the Loot Box!")
                        self.player_inventory[loot_item["name"]] += 1
                        self.last_item_bought = loot_item
                    else:
                        print(f"Purchased {selected_item['name']} for {selected_item['cost']} coins.")
                        self.player_inventory[selected_item["name"]] += 1
                        self.last_item_bought = selected_item
                    self.item_display_time = pygame.time.get_ticks()
                    self.insufficient_funds = False
                    gSounds['buy'].play()
                else:
                    print("Not enough money to buy this item.")
                    self.insufficient_funds = True
                    self.insufficient_funds_time = pygame.time.get_ticks()
                    self.last_item_bought = None
                    gSounds['broke'].play()

        if self.back_button.update():
            g_state_machine.Change('play', {
                        'LIFE': self.player_inventory['LIFE'],
                        'SWORD': self.player_inventory['SWORD'],
                        'ARROW': self.player_inventory['ARROW'],
                        'BOMB': self.player_inventory['BOMB'],
                        'SNIPER': self.player_inventory['SNIPER'],
                        'BLOCK': self.player_inventory['BLOCK'],
                        'LOOT BOX': self.player_inventory['LOOT BOX'],
                        'MONEY': self.player_inventory['MONEY'],
                        'RESET': False
                    })

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))

        # Display player's current money
        money_text = draw_text(f"Money: {self.player_inventory['MONEY']} coin(s)", 'small', (255, 255, 0))
        screen.blit(money_text, (20, 20))

        life_text = draw_text(f"Lives: {self.player_inventory['LIFE']}", 'small', (255, 255, 0))
        screen.blit(life_text, (20, 40))

        for i, button in enumerate(self.item_buttons):
            if button.hover:
                button.image = draw_text(f"{self.items[i]['name']} - {self.items[i]['cost']} coins", 'small', (255, 255, 0))
            else:
                button.image = draw_text(f"{self.items[i]['name']} - {self.items[i]['cost']} coins", 'small', (255, 255, 255))
            button.render(screen)

        if self.back_button.hover:
            self.back_button.image = draw_text("BACK", 'small', (255, 255, 0))
        else:
            self.back_button.image = draw_text("BACK", 'small', (255, 255, 255))
        self.back_button.render(screen)

        # Display feedback (either bought item or error message)
        if self.insufficient_funds:
            time_elapsed = pygame.time.get_ticks() - self.insufficient_funds_time
            if time_elapsed < 3000:
                warning_text = draw_text("Not Enough Geckoin", 'medium', (255, 0, 0))
                warning_rect = warning_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
                screen.blit(warning_text, warning_rect)
            else:
                self.insufficient_funds = False
        elif self.last_item_bought:
            time_elapsed = pygame.time.get_ticks() - self.item_display_time
            if time_elapsed < 3000:
                item_text = draw_text(f"You got: {self.last_item_bought['name']}", 'medium', (255, 255, 0))
                item_rect = item_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
                screen.blit(item_text, item_rect)

    def Exit(self):
        pass
