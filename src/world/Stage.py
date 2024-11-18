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
from src.Util import calculateDistance

class Stage:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        self.tiles = []
        self.GenerateWallsAndFloors()

        # self.geckoQueue = []
        self.geckos: list[Gecko] = []
        # self.GenerateEntities()

        self.objects: list[Blockade] = []
        # self.placeObjects()

        self.gatos: list[Gato] = []
        # self.placeGatos()

        self.doorways = []
        #self.doorways.append(Doorway('left', False, self))
        self.doorways.append(Doorway(False, self))
        
        # centering the dungeon rendering
        self.render_offset_x = MAP_RENDER_OFFSET_X
        self.render_offset_y = MAP_RENDER_OFFSET_Y

        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0

        self.state = 0
        self.timer = 0  # Timer to track time for spawn delay
        self.spawn_interval = 1  # Delay in seconds (1 second)
        self.spawn_queue = []  # Queue of entities to spawn with delay

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

    def GenerateEntities(self, gecko=None, num=1):
        # Add the specified number of entities to the spawn queue
        for _ in range(num):
            if gecko == "Normal":
                self.spawn_queue.append(Gecko(template_id=1))
            elif gecko == "Fast":
                self.spawn_queue.append(Gecko(template_id=2))
            elif gecko == "Chad":
                self.spawn_queue.append(Gecko(template_id=3))
            elif gecko == "Jagras":
                self.spawn_queue.append(Gecko(template_id=4))
            else:
                self.spawn_queue.append(Gecko(template_id=random.randint(1, 4)))
        

    def GenerateWaves(self, difficulty=1):
        if difficulty == 1:
            self.GenerateEntities(gecko="Normal", num=5)
            self.GenerateEntities(gecko="Chad")
            self.GenerateEntities(gecko="Normal", num=3)
            self.GenerateEntities(gecko="Chad")
        elif difficulty == 2:
            self.GenerateEntities(gecko="Normal", num=3)
            self.GenerateEntities(gecko="Fast")
            self.GenerateEntities(gecko="Normal", num=3)
            self.GenerateEntities(gecko="Fast")
            self.GenerateEntities(gecko="Chad", num=2)
        elif difficulty == 3:
            self.GenerateEntities(gecko="Jagras", num=1)
            self.GenerateEntities(gecko="Normal", num=3)
            self.GenerateEntities(gecko="Chad", num=1)
            self.GenerateEntities(gecko="Jagras", num=2)
        else:
            for i in range(math.ceil(difficulty)):
                self.GenerateEntities(num=random.randint(1,difficulty))
        print(difficulty)


    def placeObject(self, row, col, type):      # Blockade
        merged=False
        if self.state == 0 and self.nodeManager.addBlock(row, col):
            Gecko.setPath(self.nodeManager.currentPath[::-1])
            match type:
                
                case "BLOCK":
                    for object in self.objects:
                        if object.row == row and object.col == col:
                            return False
                    
                    for gato in self.gatos:
                        if gato.row == row and gato.col == col:
                            return False

                    self.objects.append(Blockade(row, col))
                case "SNIPER" | "ARROW" | "BOMB" | "SWORD":
                    templates = {
                        "SNIPER": 1,
                        "ARROW": 2,
                        "BOMB": 3,
                        "SWORD": 4                        
                    }
                    for object in self.objects:
                        if object.row == row and object.col == col:
                            return False
                    
                    for gato in self.gatos:
                        if gato.row == row and gato.col == col:
                            # print(gato.template_id)
                            if templates[type]==gato.template_id:
                                
                                if gato.lvl ==1: 
                                    gato.lvl += 1
                                    print("Upgrade to lvl", gato.lvl)
                                    merged=True
                                    
                                    # Recalculate attributes
                                    gato.damage = gato.template["damage"][gato.lvl - 1]
                                    gato.attackRadius = gato.template["range"][gato.lvl - 1] * TILE_SIZE
                                    gato.period = gato.template["period"][gato.lvl - 1]
                                    
                                    # Update sprite
                                    gato.setDirection(gato.direction)
                                    return True
                                else:
                                    print("Max tier reached!")
                                    return False
                                
                            else:
                                return False
                    if not merged:
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

    def moveTower(self, old_row, old_col, new_row, new_col):
        is_upgrade = False
        for gato in self.gatos:
            if gato.row == old_row and gato.col == old_col:
                for targetGato in self.gatos:
                    if targetGato.row == new_row and targetGato.col == new_col:
                        # Check if the target Gato is of the same type and level, and can be upgraded
                        if gato.template_id == targetGato.template_id and gato.lvl == targetGato.lvl and gato.lvl < 3:
                            targetGato.lvl += 1
                            print("Upgrade to lvl", targetGato.lvl)

                            # Recalculate attributes for the upgraded Gato
                            targetGato.damage = targetGato.template["damage"][targetGato.lvl - 1]
                            targetGato.attackRadius = targetGato.template["range"][targetGato.lvl - 1] * TILE_SIZE
                            targetGato.period = targetGato.template["period"][targetGato.lvl - 1]

                            # Update sprite
                            targetGato.setDirection(targetGato.direction)
                            is_upgrade = True
                            
                        else:
                            print("Invalid move: Target position is occupied or invalid.")
                            gato.show = True
                            return False

                # Validate the new position
                if self.nodeManager.addBlock(new_row, new_col, validateOnly=True):  # Doesn't actually add the block at this step
                    self.nodeManager.removeBlock((old_row, old_col))
                    if not is_upgrade:
                        gato.moveToGrid((new_row, new_col))
                        gato.show = True
                        self.nodeManager.addBlock(new_row, new_col, validateOnly=False)  # Occupy the new position
                    else:
                        self.gatos.remove(gato)  # Only remove gato if upgraded
                    Gecko.setPath(self.nodeManager.currentPath[::-1])
                    return True
                else:
                    print("Invalid move: Target position is occupied or invalid.")
                    gato.show = True  # Ensure show is true if the move is invalid
        
        return False



    def update(self, dt, events):
        self.timer += dt  # Increment timer with delta time

        # Check if enough time has passed to spawn the next entity
        if self.spawn_queue and self.timer >= self.spawn_interval:
            entity_to_spawn = self.spawn_queue.pop(0)  # Get the next entity from the queue
            self.geckos.append(entity_to_spawn)  # Add the entity to the geckos list
            self.timer = 0  # Reset the timer for the next spawn

        # Update existing entities
        for gecko in self.geckos:
            gecko.update(dt, events)

        # Handle other updates (doorway checks, entity health, etc.)
        if not self.spawn_queue and not self.geckos:
            self.state = 0
        else:
            self.state = 1
        for gecko in self.geckos:
            for doorway in self.doorways:
                gecko_coords = (gecko.x, gecko.y)
                if gecko_coords == (1080, 360) and not doorway.open:
                    doorway.open_door()  # Open the door
                if gecko.hp <= 0:
                    self.geckos.remove(gecko)
                    
        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return
        
        for gato in self.gatos:
            gato.clearTargets()
            for gecko in self.geckos:
                if calculateDistance((gato.x, gato.y), (gecko.x, gecko.y)) <= gato.attackRadius:                    
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

        for i in range(len(Gecko.waypoints)-1):
            pygame.draw.line(screen, (255, 0, 0), Gecko.waypoints[i], Gecko.waypoints[i+1], 3)  # Line thickness is 3

        for doorway in self.doorways:
            doorway.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)

        for object in self.objects:
            object.render(screen)

        for entity in self.geckos:
            entity.render(screen)

        for gato in self.gatos:
            gato.render(screen)
        
        # self.nodeManager.renderPath(screen)