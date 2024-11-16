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
            {"name": "Extra Life", "cost": 50},
            {"name": "Power Boost", "cost": 100},
            {"name": "Shield", "cost": 75},
            {"name": "Loot Box", "cost": 150} 
        ]
        
        # Define the pool of items that can be awarded from the Loot Box
        self.loot_box_pool = [
            {"name": "Extra Life", "cost": 50},
            {"name": "Power Boost", "cost": 100},
            {"name": "Shield", "cost": 75}
        ]
        
        # Initialize buttons for each item
        self.item_buttons = [
            Button(draw_text(f"{item['name']} - {item['cost']} coins", 'small', (255, 255, 255)), WIDTH // 2 - 100, 150 + i * 40)
            for i, item in enumerate(self.items)
        ]
        
        # Back button
        self.back_button = Button(draw_text("BACK", 'small', (255, 255, 255)), WIDTH - 80, HEIGHT - 50)

        # Variables to track the last item purchased and the time to display it
        self.last_item_bought = None
        self.item_display_time = 0  # Store the time when the item was bought

    def Enter(self, params):
        pass

    def update(self, dt, events):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get the mouse position

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Check if any item button is clicked
        for i, button in enumerate(self.item_buttons):
            button_rect = button.rect  # Get the button's rectangle

            # Update hover effect based on mouse position
            if button_rect.collidepoint(mouse_x, mouse_y):
                button.hover = True
            else:
                button.hover = False

            if button.update():
                selected_item = self.items[i]
                if selected_item["name"] == "Loot Box":
                    # Loot Box purchase logic
                    loot_item = random.choice(self.loot_box_pool)
                    print(f"Congratulations! You won a {loot_item['name']} from the Loot Box!")
                    self.last_item_bought = loot_item  # Store the item
                    self.item_display_time = pygame.time.get_ticks()  # Store the time it was bought
                    gSounds['select'].play()  # Play 'select' sound when an item is bought
                else:
                    print(f"Attempting to purchase {selected_item['name']} for {selected_item['cost']} coins.")
                    self.last_item_bought = selected_item  # Store the item
                    self.item_display_time = pygame.time.get_ticks()  # Store the time it was bought
                    gSounds['select'].play()  # Play 'select' sound when an item is bought

        # Check if back button is clicked
        if self.back_button.update():
            g_state_machine.Change('play')

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

        # Render item buttons
        for i, button in enumerate(self.item_buttons):
            # Highlight button on hover
            if button.hover:
                button.image = draw_text(f"{self.items[i]['name']} - {self.items[i]['cost']} coins", 'small', (255, 255, 0))
            else:
                button.image = draw_text(f"{self.items[i]['name']} - {self.items[i]['cost']} coins", 'small', (255, 255, 255))
            
            button.render(screen)

        # Render back button
        self.back_button.render(screen)

        # Render the last item bought for 3 seconds
        if self.last_item_bought:
            time_elapsed = pygame.time.get_ticks() - self.item_display_time
            if time_elapsed < 3000:  # Display item for 3 seconds
                item_text = draw_text(f"You got: {self.last_item_bought['name']}", 'medium', (255, 255, 0))
                item_rect = item_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
                screen.blit(item_text, item_rect)

    def Exit(self):
        pass
