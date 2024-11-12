from src.Constants import *
from src.Resources import *

class Doorway:
    def __init__(self, direction, open, room):
        self.direction = direction
        self.open = open
        self.room = room

        if direction == 'left':
            self.x = MAP_RENDER_OFFSET_X
            self.y = MAP_RENDER_OFFSET_Y + (MAP_HEIGHT / 2 * TILE_SIZE) - TILE_SIZE
            self.height = 96
            self.width = 48
        elif direction == 'right':
            self.x = MAP_RENDER_OFFSET_X + (MAP_WIDTH * TILE_SIZE) - TILE_SIZE
            self.y = MAP_RENDER_OFFSET_Y + (MAP_HEIGHT / 2 * TILE_SIZE) - TILE_SIZE
            self.height = 96
            self.width = 48


    def render(self, screen, offset_x, offset_y):
        transparent_door_image = gDoor_image_list
        door_image = gStage_image_list

        self.x = self.x + offset_x
        self.y = self.y + offset_y

        if self.direction == 'left':
            if self.open:
                index = 180
            else:
                index = 218
            screen.blit(transparent_door_image[index], (self.x-TILE_SIZE, self.y))
            screen.blit(door_image[index+1], (self.x, self.y))
            screen.blit(transparent_door_image[index+19], (self.x - TILE_SIZE, self.y + TILE_SIZE))
            screen.blit(door_image[index+20], (self.x, self.y + TILE_SIZE))
        elif self.direction == 'right':
            if self.open:
                index = 171
            else:
                index = 173
            screen.blit(door_image[index], (self.x, self.y))
            screen.blit(transparent_door_image[index + 1], (self.x + TILE_SIZE, self.y))
            screen.blit(door_image[index + 19], (self.x, self.y + TILE_SIZE))
            screen.blit(transparent_door_image[index + 20], (self.x + TILE_SIZE, self.y + TILE_SIZE))
        
            screen.blit(door_image[index], (self.x, self.y))
            screen.blit(door_image[index + 1], (self.x + TILE_SIZE, self.y))
            screen.blit(transparent_door_image[index + 19], (self.x, self.y + TILE_SIZE))
            screen.blit(transparent_door_image[index + 20], (self.x + TILE_SIZE, self.y + TILE_SIZE))

        self.x = self.x - offset_x
        self.y = self.y - offset_y
