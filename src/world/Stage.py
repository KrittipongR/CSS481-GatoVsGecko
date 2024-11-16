import pygame, random

from src.Constants import *
from src.Dependencies import *
from src.Resources import *
from src.world.Doorway import Doorway
from src.world.Gecko import Gecko

# from src.states.entity.EntityDieState import EntityDieState
# from src.states.entity.EntityWalkState import EntityWalkState

from src.StateMachine import StateMachine
# from src.GameObject import GameObject
# from src.object_defs import *

from src.world.NodeManager import NodeManager

class Stage:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        self.tiles = []
        self.GenerateWallsAndFloors()

        self.geckos = []
        # self.GenerateEntities()

        self.objects = []
        # self.GenerateObjects()

        self.doorways = []
        #self.doorways.append(Doorway('left', False, self))
        self.doorways.append(Doorway('right', False, self))
        
        # centering the dungeon rendering
        self.render_offset_x = MAP_RENDER_OFFSET_X
        self.render_offset_y = MAP_RENDER_OFFSET_Y

        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0

        self.nodeManager = NodeManager(MAP_HEIGHT, MAP_WIDTH)
        Gecko.setPath(self.nodeManager.currentPath)

    def GenerateWallsAndFloors(self):
        for y in range(1, self.height + 1):
            self.tiles.append([])
            for x in range(1, self.width + 1):
                id = TILE_EMPTY

                # Wall Corner
                if x == 1 and y == 1:
                    id = TILE_TOP_LEFT_CORNER
                elif x == 1 and y == self.height:
                    id = TILE_BOTTOM_LEFT_CORNER
                elif x == self.width and y == 1:
                    id = TILE_TOP_RIGHT_CORNER
                elif x == 1 and y == self.height:
                    id = TILE_BOTTOM_RIGHT_CORNER

                #Wall, Floor
                elif x== 1:
                    id = random.choice(TILE_LEFT_WALLS)
                elif x == self.width:
                    id = random.choice(TILE_RIGHT_WALLS)
                elif y == 1:
                    id = random.choice(TILE_TOP_WALLS)
                elif y == self.height:
                    id = random.choice(TILE_BOTTOM_WALLS)
                else:
                    id = random.choice(TILE_FLOORS)

                self.tiles[y - 1].append(id)

    def GenerateEntities(self, wave=1):
        self.geckos.append(Gecko(template_id=random.randint(1,3)))
        pass

    def placeObject(self, row, col, type):      # Tower and Blockade
        self.nodeManager.addBlock(row, col)
        Gecko.setPath(self.nodeManager.currentPath)
        pass

    def update(self, dt, events):
        for gecko in self.geckos:
            gecko.update(dt, events)
            if gecko.hp <= 0:
                self.geckos.remove(gecko)
        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return

    def render(self, screen, x_mod, y_mod):
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.tiles[y][x]
                if tile_id == 78 or tile_id == 97 or tile_id == 116:
                    screen.blit(gDoor_image_list[tile_id-1], (x * TILE_SIZE + self.render_offset_x + self.adjacent_offset_x + x_mod,
                            y * TILE_SIZE + self.render_offset_y + self.adjacent_offset_y + y_mod))
                else:
                    screen.blit(gStage_image_list[tile_id-1], (x * TILE_SIZE + self.render_offset_x + self.adjacent_offset_x + x_mod,
                            y * TILE_SIZE + self.render_offset_y + self.adjacent_offset_y + y_mod))

        for doorway in self.doorways:
            doorway.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)

        for object in self.objects:
            object.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)

        for entity in self.geckos:
            entity.render(screen)