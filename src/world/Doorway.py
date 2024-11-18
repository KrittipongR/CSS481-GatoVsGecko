from src.Constants import *
from src.Resources import *

class Doorway:
    def __init__(self, direction, open, room):
        self.direction = direction
        self.open = open
        self.room = room

        self.x = MAP_RENDER_OFFSET_X + (MAP_WIDTH * TILE_SIZE) - TILE_SIZE
        self.y = MAP_RENDER_OFFSET_Y + (MAP_HEIGHT / 2 * TILE_SIZE) - TILE_SIZE
        self.height = 96
        self.width = 48

        self.DOOR_CLOSE_EVENT = pygame.USEREVENT + 1

    def get_coordinates(self):
        return (MAP_WIDTH - 1, MAP_HEIGHT // 2)
        
    def open_door(self):
        self.open = True
        pygame.time.set_timer(self.DOOR_CLOSE_EVENT, 1000)

    def close_door(self):
        self.open = False
        pygame.time.set_timer(self.DOOR_CLOSE_EVENT, 0)

    def render(self, screen, offset_x, offset_y):
        self.x = self.x + offset_x
        self.y = self.y + offset_y

        
        if self.open:
            screen.blit(gDoor_image_list[171], (self.x, self.y))
            screen.blit(gDoor_image_list[172], (self.x + TILE_SIZE, self.y))
            screen.blit(gDoor_image_list[190], (self.x, self.y + TILE_SIZE))
            screen.blit(gDoor_image_list[191], (self.x + TILE_SIZE, self.y + TILE_SIZE))
        else:
            screen.blit(gDoor_image_list[173], (self.x, self.y))
            screen.blit(gDoor_image_list[174], (self.x + TILE_SIZE, self.y))
            screen.blit(gDoor_image_list[192], (self.x, self.y + TILE_SIZE))
            screen.blit(gDoor_image_list[193], (self.x + TILE_SIZE, self.y + TILE_SIZE))

        self.x = self.x - offset_x
        self.y = self.y - offset_y
