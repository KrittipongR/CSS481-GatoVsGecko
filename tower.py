import pygame
from projectile import Projectile

class Tower:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.range = 100
        self.reload_time = 30
        self.reload_counter = 0
        self.projectiles = []
        self.player = player

    def shoot(self, bloons):
        if self.reload_counter == 0:
            for bloon in bloons:
                if self.in_range(bloon):
                    projectile = Projectile(self.x, self.y, bloon)
                    self.projectiles.append(projectile)
                    self.reload_counter = self.reload_time
                    break

    def in_range(self, bloon):
        return (bloon.x - self.x) ** 2 + (bloon.y - self.y) ** 2 <= self.range ** 2

    def update(self, bloons):

        # reload projectile
        if self.reload_counter > 0:
            self.reload_counter -= 1
        self.shoot(bloons) # shoot projectile

        # move projectile
        for projectile in self.projectiles[:]:
            projectile.move()
            if projectile.has_hit_target():
                projectile.deal_damage()
                if projectile.target.is_dead():
                    self.player.money += 1
                self.projectiles.remove(projectile)

        for bloon in bloons[:]:
            if bloon.is_dead():
                bloons.remove(bloon)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 15)
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.range, 1)
        for projectile in self.projectiles:
            projectile.draw(screen)
