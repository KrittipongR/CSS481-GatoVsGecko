import pygame
import json
from src.Resources import *
from src.Constants import *

def GenerateTiles(file_name, tile_width, tile_height, scale=3, colorkey=None):
    image = pygame.image.load(file_name)

    (img_width, img_height) = image.get_size()

    sheet_width = img_width//tile_width
    sheet_height = img_height//tile_height

    sheet_counter = 1
    tile_sheet = []

    for y in range(sheet_height):
        for x in range(sheet_width):
            tile = pygame.Surface((tile_width, tile_height))

            # surface, location, area of surface
            tile.blit(image, (0, 0), (x*tile_width, y*tile_height, tile_width, tile_height))

            # transparency
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                tile.set_colorkey(colorkey, pygame.RLEACCEL)

            tile = pygame.transform.scale(
                tile, (tile_width * scale, tile_height * scale)
            )

            tile_sheet.append(tile)

            sheet_counter += 1

    return tile_sheet

class Animation:
    def __init__(self, images, idleSprite=None, looping=True, interval_time=0.15):
        self.images = images
        self.timer = 0
        self.index = 0
        if idleSprite is None:
            self.image = self.images[self.index]
        else:
            self.image = idleSprite
        self.idleSprite = idleSprite

        self.interval_time = interval_time

        self.looping = looping #default loop

        self.times_played = 0

    def Refresh(self):
        self.timer=0
        self.index = 0
        self.times_played=0

    def update(self, dt):
        # one time animation check
        if self.looping is False and self.times_played>0:
            return

        self.timer = self.timer + dt

        if self.timer > self.interval_time:
            self.timer = self.timer % self.interval_time

            self.index = (self.index+1) % len(self.images)

            if self.index == 0:
                self.times_played += 1

        self.image = self.images[self.index]

    def Idle(self):
        self.image = self.idleSprite

class Sprite:
    def __init__(self, image, animation=None):
        self.image = image
        self.animation = animation

class SpriteManager:
    def __init__(self, path):
        self.spriteCollection = self.loadSprites(path)

    def loadSprites(self, urlList):
        resDict = {}
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData)
                mySpritesheet = SpriteSheet(data["spriteSheetURL"])
                dic = {}
                spriteList = data["sprites"]
                (xTileSize, yTileSize) = data["size"]

                if data["type"] == "animation":
                    for sprite in spriteList:
                        images = []
                        for image in sprite["images"]:
                            images.append(
                                mySpritesheet.image_at(
                                    image["x"],
                                    image["y"],
                                    xTileSize,
                                    yTileSize
                                )
                            )
                        try:
                            idle_info = sprite['idle_image']
                            idle_img = mySpritesheet.image_at(
                                idle_info["x"],
                                idle_info["y"],
                                xTileSize,
                                yTileSize
                            )
                        except KeyError:
                            idle_img = None
                        try:
                            loop = sprite['loop']
                        except KeyError:
                            loop = True

                        dic[sprite["name"]] = Sprite(
                            None,
                            animation=Animation(images, idleSprite=idle_img, looping=loop, interval_time=sprite["interval_time"]),
                        )

                    resDict.update(dic)
                    continue
                else:
                    for sprite in spriteList:
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                xTileSize,
                                yTileSize
                            ),
                        )
                    resDict.update(dic)
                    continue
        return resDict

class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            # if not self.sheet.get_alpha():
            #     self.sheet.set_colorkey((0, 0, 0))
        except pygame.error:
            print("Unable to load spritesheet image:", filename)
            raise SystemExit

    def image_at(self, x, y, xTileSize=512, yTileSize=512):
        rect = pygame.Rect(x, y, xTileSize, yTileSize)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        # if colorkey is not None:
        #     if colorkey == -1:
        #         colorkey = image.get_at((0, 0))
        #     image.set_colorkey(colorkey, pygame.RLEACCEL)
        return pygame.transform.scale(
            image, (xTileSize, yTileSize)
        )
    
class Button():
    def __init__(self, image, x, y):
        self.image = image
        width = image.get_width()
        height = image.get_height()  # Add parentheses to call get_height()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.hover = False

    def update(self):
        action = False
        pos = pygame.mouse.get_pos()

        # Check if mouse is over button
        if self.rect.collidepoint(pos):
            self.hover = True
            # Check if the button is clicked
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.hover = False

        # Reset clicked state when mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

    def render(self, screen):
        # Draw the button image on the screen
        screen.blit(self.image, self.rect.topleft)

import json

class Template:
    def __init__(self, type, template_id=1):
        self.type = type
        match self.type:
            case "gecko":
                self.path = "./src/data/Gecko.json"
            case "gato":
                self.path = "./src/data/Gato.json"

        self.load_template(template_id)


        # Loads JSON object as a dictionary
    def load_template(self, template_id):
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)

            # Iterating through the json list
            for template in data["templates"]:
                if self.type + str(template_id) == template["name"]:
                    self.data = template
                    break

        except FileNotFoundError:
            print(f"Error: The file {self.path} was not found.")
            return None

        except json.decoder.JSONDecodeError:
            print(f"Error: Failed to decode the template {self.path} file.")
            return None

def convertGridToCoords(grid: tuple[int, int], center=True) -> tuple[int, int]:  # Default: The output coordinates will be at the center of the grid, NOT TOP-LEFT
    if center:
        mod = TILE_SIZE / 2
    else:
        mod = 0
    y = grid[0] * TILE_SIZE + mod
    x = grid[1] * TILE_SIZE + mod
    return (int(x), int(y))

def convertCoordsToGrid(coords: tuple[int, int]) -> tuple[int, int]:
    if int(coords[0]) in range(0, MAP_WIDTH * TILE_SIZE) and int(coords[1]) in range(0, MAP_HEIGHT * TILE_SIZE):
        row = coords[1] // TILE_SIZE
        col = coords[0] // TILE_SIZE
        return (row, col)
    else:
        return (-1, -1)
    
def calculateRadius(origin: tuple[float, float], target: tuple[float, float], radius: float) -> bool:
    return True