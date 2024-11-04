import pygame
import math

class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.speed = 5
        self.radius = 5
        self.target = target

        self.predict_target_position()

    def predict_target_position(self):
        target_velocity_x = self.target.velocity_x
        target_velocity_y = self.target.velocity_y

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        time_to_hit = distance / self.speed

        future_x = self.target.x + target_velocity_x * time_to_hit
        future_y = self.target.y + target_velocity_y * time_to_hit

        dx = future_x - self.x
        dy = future_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        self.velocity_x = (dx / distance) * self.speed
        self.velocity_y = (dy / distance) * self.speed

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def has_hit_target(self):
        distance = math.sqrt((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
        return distance < self.radius + 10

    def deal_damage(self):
        self.target.take_damage(1)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius)
