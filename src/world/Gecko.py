import pygame
import math
from src.Util import SpriteManager, Template, convertGridToCoords
from src.Constants import *

class Gecko:

    @staticmethod
    def setPath(path):    # Path is given as a list of nodes
        # Goal: Minimize turns by finding the row that yields the longest straight line in each step
        currentNode = 0
        maxLength = 0
        bestRow = 0
        while currentNode < len(path) - 1:
            for row in range(path[currentNode].row1, path[currentNode].row2 + 1):
                i = 1
                while currentNode + i < len(path) and row in range(path[currentNode + i].row1, path[currentNode + i].row2 + 1):
                    i += 1
                if i > maxLength:
                    maxLength = i
                    bestRow = row
            Gecko.waypoints.append(convertGridToCoords((bestRow, path[currentNode].col)))
            if maxLength > 1:
                Gecko.waypoints.append(convertGridToCoords((bestRow, path[currentNode + maxLength - 1].col)))
            currentNode += maxLength - 1
        print(Gecko.waypoints)

    waypoints = []      # Convert path to absolute coordinates [(x1,y1), (x2,y2), (x3,y3), ...]
                        # Gecko only move in cardinal directions so there can be multiple waypoints per node when turning
    names = {
        1: "gecko",
        2: "jinglen",
        3: "gigaGecko",
        4: "chameleon"
    }

    def __init__(self, template_id=1):
        self.template_id = template_id
        self.template = Template("gecko", self.template_id)
        self.x, self.y = Gecko.waypoints[0]
        self.pathProgress = 0   # Index for waypoints
        self.hp = self.template.data["maxHP"]
        self.setDirection(3)
        self.currentDirection = 3
        self.updateWaypoint()
        print("gecko generated at: " + str(self.x) + ", " + str(self.y))

    def setDirection(self, direction):
        if direction < 2:
            self.path = "./sprites/gecko_UpLeft.json"
            self.sprite_name = Gecko.names[self.template_id] + "_walk_up"
        else:
            self.path = "./sprites/gecko_DownRight.json"
            self.sprite_name = Gecko.names[self.template_id] + "_walk_down"
        self.sprite_collection = SpriteManager(path=self.path).spriteCollection
        
    def updateWaypoint(self):
        self.waypoint = Gecko.waypoints[self.pathProgress + 1]
        if self.waypoint[0] != self.x:
            self.xMod = math.copysign(1, self.waypoint[0] - self.x)
            self.yMod = 0
            if self.currentDirection != (2 + self.xMod):
                self.setDirection(2 + self.xMod)  # Magic
        elif self.waypoint[1] != self.y:
            self.xMod = 0
            self.yMod = math.copysign(1, self.waypoint[1] - self.y)
            if self.currentDirection != (1 + self.yMod):
                self.setDirection(1 + self.yMod)  # Magic

    def update(self, dt, events):
        self.x += self.template.data["movement"] * dt * self.xMod
        self.y += self.template.data["movement"] * dt * self.yMod

        if  (self.x >= self.waypoint[0] and self.xMod == 1) or \
            (self.x <= self.waypoint[0] and self.xMod == -1) or \
            (self.y >= self.waypoint[1] and self.yMod == 1) or \
            (self.y <= self.waypoint[1] and self.yMod == -1):
            self.pathProgress += 1
            if self.pathProgress == len(Gecko.waypoints) - 1:   # End of the line
                # DO SOMETHING HERE TO MAKE THE PLAYER LOSE LIVES
                self.hp = 0     # Set own HP to 0 afterwards to get deleted by Stage on the next update cycle
            else:
                self.updateWaypoint()

        self.sprite_collection[self.sprite_name].animation.update(dt)

    def render(self, screen):
        self.sprite = pygame.transform.scale(self.sprite_collection[self.sprite_name].animation.image, (TILE_SIZE, TILE_SIZE))
        screen.blit(self.sprite, (self.x - (TILE_SIZE / 2), self.y - (TILE_SIZE / 2)))