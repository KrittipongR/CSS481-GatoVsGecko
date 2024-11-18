import math
import pygame
class Projectile:
    def __init__(self, start_x, start_y, target_x, target_y, speed, damage):
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.damage = damage
        self.angle = math.atan2(target_y - start_y, target_x - start_x)
        self.vx = self.speed * math.cos(self.angle)
        self.vy = self.speed * math.sin(self.angle)
        self.active = True

    def update(self, dt):
        """Update the projectile's position."""
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Check if it reached the target
        if math.hypot(self.target_x - self.x, self.target_y - self.y) < 5:  # Adjust threshold as needed
            self.active = False

    def render(self, screen: pygame.Surface):
        """Render the projectile."""
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)  # Draw a red circle
