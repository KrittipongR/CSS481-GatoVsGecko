import pygame
import math

class Bloon:
    def __init__(self, path, player):
        self.path = path.points
        self.position = 0
        self.x, self.y = self.path[self.position]
        self.speed = 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.hp = 3
        self.player = player
        self.calculate_velocity()

    def calculate_velocity(self):
        if self.position < len(self.path) - 1:
            target_x, target_y = self.path[self.position + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed

    def move(self):
        if self.position < len(self.path) - 1:
            self.x += self.velocity_x
            self.y += self.velocity_y

            target_x, target_y = self.path[self.position + 1]
            if (self.x, self.y) == (target_x, target_y):
                self.position += 1
                self.calculate_velocity()

        # If the bloon reaches the end of the path, reduce player HP and despawn the bloon
        if self.position >= len(self.path) - 1:
            self.player.hp -= self.hp
            self.hp = 0  # Mark as despawned

    def take_damage(self, damage):
        self.hp -= damage

    def is_dead(self):
        return self.hp <= 0

    def draw(self, screen):
        if self.hp > 0:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 10)
