import pygame
import math
from src.Util import SpriteManager, Template, convertGridToCoords, convertCoordsToGrid, calculateAngle
from src.Constants import *
from src.Resources import *
from src.world.Projectile import *

class Gato:

    templates = {}
    
    for i in range(1, 5):
        send_help = Template("gato", i)
        templates[i] = send_help.data


    def __init__(self, row, col, template_id=1, lvl=1):
        self.template_id = template_id
        self.template = Gato.templates[template_id]
        self.x, self.y = convertGridToCoords((row, col))
        self.row = row
        self.col = col
        self.lvl = lvl
        self.direction=90
        self.setDirection(90)

        self.dmgNumbers = []
        self.targets = []
        self.projectiles=[]
        self.attackRadius: float = self.template["range"][self.lvl-1] * TILE_SIZE
        try:
            self.targeting: str = self.template["targeting"]
        except KeyError:
            self.targeting: str = "first"
        self.damage: int = self.template["damage"][self.lvl-1]
        self.period: float = self.template["period"][self.lvl-1]
        self.aoe: float = self.template["aoe"][self.lvl-1]
        self.attackTimer: float = 0
        self.exclamationTimer = 0
        self.isAttacking = False

        self.exclamation_font_size = gFonts['small'].size("!")                    
        self.exclamation = gFonts['small'].render("!", False, (255, 255, 255))

        self.show = True

    names = {
        1: "sniper_cat",
        2: "arrow_cat",
        3: "bomb_kitty",
        4: "sameowrai"
    }

    def moveToGrid(self, grid: tuple[int, int]):
        self.row, self.col = grid
        self.x, self.y = convertGridToCoords(grid)

    def setDirection(self, direction):
        direction = direction % 360
        self.direction=direction
        path = "./sprites/gato_UpLeft.json"
        self.sprite_collection = SpriteManager([path]).spriteCollection
        self.sprite_name = Gato.names[self.template_id] + "_left_" + str(self.lvl)
        self.sprite = pygame.transform.smoothscale(self.sprite_collection[self.sprite_name].image, (TILE_SIZE, TILE_SIZE))
        self.wpn_sprite_name = Gato.names[self.template_id] + "_left_weapon"
        self.wpn_sprite = self.sprite_collection[self.wpn_sprite_name].image
        if 0 <= direction < 180:            
            wpn_rotation = direction - 90
            self.wpn_sprite = pygame.transform.rotate(self.wpn_sprite, wpn_rotation)
        else:
            wpn_rotation = direction - 270
            self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.wpn_sprite = pygame.transform.flip(self.wpn_sprite, True, False)

        self.wpn_sprite = pygame.transform.smoothscale(self.wpn_sprite, (TILE_SIZE, TILE_SIZE))
        

    def clearTargets(self):
        self.targets = []

    def addTarget(self, gecko):
        self.targets.append(gecko)
    
    def updatePosition(self, row, col):
        """Update Gato's position based on grid coordinates."""
        self.row = row
        self.col = col
        (self.x, self.y) = convertGridToCoords((row, col))  # Update world coordinates


    def update(self, dt, events):

        for dmgNumber in self.dmgNumbers:
            if dmgNumber[2] <= 0:
                self.dmgNumbers.remove(dmgNumber)
            else:
                dmgNumber[2] -= dt
        
        for projectile in self.projectiles:
            projectile.update(dt)
            if not projectile.active:
                self.projectiles.remove(projectile)



        if self.exclamationTimer <= 0:
            self.isAttacking = False
        else:
            self.isAttacking = True
        self.exclamationTimer -= dt

        # Attacking        
        if self.targets:
            if self.attackTimer <= 0:
                match self.targeting:
                    case "first":
                        self.targets = sorted(self.targets, key=lambda x: x.floatingPathProgress)
                        target = self.targets.pop()

                        # Create a projectile targeting the gecko
                        self.projectiles.append(Projectile(self.x, self.y, target, 300, self.damage))

                        # Play sound effect
                        gSounds["hurt"].play()

                        # Damage number rendering logic (unchanged)
                        font_size = gFonts['small'].size(f'-{self.damage}')
                        number = gFonts['small'].render(f'-{self.damage}', False, (255, 255, 255))
                        self.dmgNumbers.append([number, (target.x - font_size[0] / 2, target.y - (TILE_SIZE + font_size[1]) / 2), 0.5])
                        self.exclamation_coords = (self.x - self.exclamation_font_size[0] / 2, self.y - (TILE_SIZE + self.exclamation_font_size[1] / 2))
                        self.attackTimer = self.period
                        self.exclamationTimer = 0.1
                        # self.setDirection(calculateAngle((self.x, self.y), (target.x, target.y)))
            else:
                self.attackTimer -= dt

    def render(self, screen: pygame.Surface):
        for projectile in self.projectiles:
            projectile.render(screen)

        self.sprite.set_colorkey(self.sprite.get_at((0, 0)),pygame.RLEACCEL)
        self.wpn_sprite.set_colorkey(self.wpn_sprite.get_at((0, 0)),pygame.RLEACCEL)
        if self.show:
            screen.blit(self.sprite, (self.x - (TILE_SIZE / 2), self.y - (TILE_SIZE / 2)))
            screen.blit(self.wpn_sprite, (self.x - (TILE_SIZE / 2), self.y - (TILE_SIZE / 2)))

        for dmgNumber in self.dmgNumbers:
            screen.blit(dmgNumber[0], dmgNumber[1])
        
        if self.isAttacking:
            screen.blit(self.exclamation, self.exclamation_coords)

