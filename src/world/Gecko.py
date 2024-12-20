import pygame
import math
from src.Util import SpriteManager, Template, convertGridToCoords, convertCoordsToGrid, calculateDistance
from src.Constants import *

class Gecko:

    @staticmethod
    def setPath(path: list):    # Path is given as a list of nodes
        # Goal: Minimize turns by finding the row that yields the longest straight line in each step
        currentNode = 0
        Gecko.waypoints = []
        while currentNode < len(path) - 1:
            maxLength = 0
            bestRow = 0
            
            for row in range(path[currentNode].row1, path[currentNode].row2 + 1):
                i = 1
                while currentNode + i < len(path) and row in range(path[currentNode + i].row1, path[currentNode + i].row2 + 1):
                    i += 1
                if i > maxLength or (i == maxLength and abs(row - (path[currentNode].row1 + path[currentNode].row2 // 2)) < abs(bestRow - (path[currentNode].row1 + path[currentNode].row2 // 2))):
                    maxLength = i
                    bestRow = row
            Gecko.waypoints.append(convertGridToCoords((bestRow, path[currentNode].col)))
            if maxLength > 1:
                Gecko.waypoints.append(convertGridToCoords((bestRow, path[currentNode + maxLength - 1].col)))
            currentNode += maxLength - 1
            # previousRow = bestRow
        if convertGridToCoords((7, 21)) not in Gecko.waypoints:
            Gecko.waypoints.insert(-1, convertGridToCoords((7, 21)))

    waypoints = []      # Convert path to absolute coordinates [(x1,y1), (x2,y2), (x3,y3), ...]
                        # Gecko only move in cardinal directions so there can be multiple waypoints per node when turning
    
    templates = {}
    
    for i in range(1, 5):
        send_help = Template("gecko", i)
        templates[i] = send_help.data

    names = {
        1: "gecko",
        2: "jinglen",
        3: "gigaGecko",
        4: "chameleon"
    }

    def __init__(self, template_id=1):
        self.template_id = template_id
        self.template: dict = Gecko.templates[self.template_id]
        
        self.x, self.y = Gecko.waypoints[0]
        self.pathProgress = 0   # Index for waypoints
        self.floatingPathProgress: float = 0
        self.hp = self.template["maxHP"]
        self.money = self.template["money"]
        self.xMod = 0
        self.yMod = 0
        self.setDirection(3)
        self.currentDirection = 3
        self.updateWaypoint()
        self.reached = False
        self.geckoDoor = False

    def setDirection(self, direction):
        if direction < 2:
            self.path = "./sprites/gecko_UpLeft.json"
            self.sprite_name = Gecko.names[self.template_id] + "_walk_up"
        else:
            self.path = "./sprites/gecko_DownRight.json"
            self.sprite_name = Gecko.names[self.template_id] + "_walk_down"
        self.currentDirection = direction
        self.sprite_collection = SpriteManager([self.path]).spriteCollection
        
    def updateWaypoint(self):
        self.waypoint = Gecko.waypoints[self.pathProgress + 1]
        grid = convertCoordsToGrid((self.x, self.y))
        if convertCoordsToGrid(self.waypoint)[1] != grid[1]:
            self.xMod = math.copysign(1, self.waypoint[0] - self.x)
            self.yMod = 0
            if self.currentDirection != (2 + self.xMod):
                self.setDirection(2 + self.xMod)  # Magic
        elif convertCoordsToGrid(self.waypoint)[0] != grid[0]:
            self.xMod = 0
            self.yMod = math.copysign(1, self.waypoint[1] - self.y)
            if self.currentDirection != (1 + self.yMod):
                self.setDirection(1 + self.yMod)  # Magic


    def update(self, dt, events):
        self.x += self.template["movement"] * dt * self.xMod
        self.y += self.template["movement"] * dt * self.yMod

        if self.pathProgress < len(Gecko.waypoints) - 1:
            self.floatingPathProgress = self.pathProgress + 1 - (
                calculateDistance((self.x, self.y), Gecko.waypoints[self.pathProgress + 1]) / calculateDistance(Gecko.waypoints[self.pathProgress], Gecko.waypoints[self.pathProgress + 1])
            )

        if  (self.x >= self.waypoint[0] and self.xMod == 1) or \
            (self.x <= self.waypoint[0] and self.xMod == -1) or \
            (self.y >= self.waypoint[1] and self.yMod == 1) or \
            (self.y <= self.waypoint[1] and self.yMod == -1):
            self.pathProgress += 1
            if self.pathProgress == len(Gecko.waypoints) - 1:   # End of the line
                # DO SOMETHING HERE TO MAKE THE PLAYER LOSE LIVES
                self.reached = True
                self.hp = 0     # Set own HP to 0 afterwards to get deleted by Stage on the next update cycle
            else:
                if self.pathProgress == len(Gecko.waypoints) - 2:
                    self.geckoDoor = True
                self.updateWaypoint()

        self.sprite_collection[self.sprite_name].animation.update(dt)

    def render(self, screen):
        self.sprite = pygame.transform.smoothscale(self.sprite_collection[self.sprite_name].animation.image, (TILE_SIZE, TILE_SIZE))
        self.sprite.set_colorkey(self.sprite.get_at((0, 0)),pygame.RLEACCEL)
        screen.blit(self.sprite, (self.x - (TILE_SIZE / 2), self.y - (TILE_SIZE / 2)))