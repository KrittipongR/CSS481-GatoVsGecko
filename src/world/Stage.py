import pygame, random

from src.Constants import *
from src.Dependencies import *
from src.Resources import *
from src.world.Doorway import Doorway
from src.world.Gecko import Gecko
from src.world.Blockade import Blockade
from src.world.Gato import Gato

# from src.states.entity.EntityDieState import EntityDieState
# from src.states.entity.EntityWalkState import EntityWalkState

from src.StateMachine import StateMachine
# from src.GameObject import GameObject
# from src.object_defs import *

from src.world.NodeManager import NodeManager
from src.Util import calculateRadius

class Stage:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        self.tiles = []
        self.GenerateWallsAndFloors()

        self.geckoQueue = []
        self.geckos: list[Gecko] = []
        # self.GenerateEntities()

        self.objects: list[Blockade] = []
        # self.placeObjects()

        self.gatos: list[Gato] = []
        # self.placeGatos()

        self.doorways = []
        #self.doorways.append(Doorway('left', False, self))
        self.doorways.append(Doorway('right', False, self))
        
        # centering the dungeon rendering
        self.render_offset_x = MAP_RENDER_OFFSET_X
        self.render_offset_y = MAP_RENDER_OFFSET_Y

        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0

        self.state = 0

        self.nodeManager = NodeManager(MAP_HEIGHT, MAP_WIDTH)
        Gecko.setPath(self.nodeManager.currentPath[::-1])

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
        #self.geckoQueue.append(...)
        self.state = 1
        self.geckos.append(Gecko(template_id=random.randint(1,3)))
        pass

    def placeObject(self, row, col, type):      # Blockade
        if self.state == 0 and self.nodeManager.addBlock(row, col):
            Gecko.setPath(self.nodeManager.currentPath[::-1])
            match type:
                case "BLOCK":
                    self.objects.append(Blockade(row, col))
                case "SNIPER" | "ARROW" | "BOMB" | "SWORD":
                    templates = {
                        "SNIPER": 1,
                        "ARROW": 2,
                        "BOMB": 3,
                        "SWORD": 4                        
                    }
                    self.gatos.append(Gato(row,col, template_id=templates[type]))
                case _:
                    return False

            return True
        else:
            return False
        
    # def placeGatos(self, row, col, type):       # Towers
    #     if self.state == 0 and self.nodeManager.addBlock(row, col):
    #         self.gatos.append(Gato(row, col))
    # def rotateGato(self, grid):
    #     for gato in self.gatos:
    #         if (gato.row, gato.col) == grid and self.state == 0:
    #             gato.setDirection(gato.currentDirection + 1)
    #             break

    def update(self, dt, events):
        if not self.geckoQueue and not self.geckos:
            self.state = 0
        else:            
            for gecko in self.geckos:
                gecko.update(dt, events)

                for doorway in self.doorways:
                    gecko_coords = (gecko.x, gecko.y)
                    
                if gecko_coords == (1080, 360) and not doorway.open:
                    doorway.open_door()  # Open the door
                    
        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return
        
        for gato in self.gatos:
            gato.clearTargets()
            for gecko in self.geckos:
                if calculateRadius((gato.x, gato.y), (gecko.x, gecko.y), gato.attackRadius):                    
                    gato.addTarget(gecko)

            gato.update(dt, events)

    def render(self, screen, x_mod, y_mod):
        for row in range(self.height):
            for col in range(self.width):
                tile_id = self.tiles[row][col]
                x = col * TILE_SIZE + self.render_offset_x + self.adjacent_offset_x + x_mod
                y = row * TILE_SIZE + self.render_offset_y + self.adjacent_offset_y + y_mod
                if tile_id == 78 or tile_id == 97 or tile_id == 116:
                    tileImageList = gDoor_image_list
                else:
                    tileImageList = gStage_image_list
                screen.blit(tileImageList[tile_id-1], (x, y))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), 1) # Grid outlines

        for doorway in self.doorways:
            doorway.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)

        for object in self.objects:
            object.render(screen)

        for entity in self.geckos:
            entity.render(screen)

        for gato in self.gatos:
            gato.render(screen)