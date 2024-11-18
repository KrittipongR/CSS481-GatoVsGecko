import pygame
import math
class Projectile:
    def __init__(self, start_x, start_y, target, speed, damage):
        self.x = start_x
        self.y = start_y
        self.target = target  # Reference to the target (e.g., a Gecko instance)
        self.target_x = target.x
        self.target_y = target.y
        self.speed = speed
        self.damage = damage
        self.angle = math.atan2(self.target_y - start_y, self.target_x - start_x)
        self.vx = self.speed * math.cos(self.angle)
        self.vy = self.speed * math.sin(self.angle)
        self.active = True

    def update(self, dt):
        """Update the projectile's position and check for collision with the target."""
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Check if the projectile has hit the target
        if math.hypot(self.target_x - self.x, self.target_y - self.y) < 5:  # Adjust threshold as needed
            self.active = False
            self.target.hp -= self.damage  # Apply damage to the target

    def render(self, screen: pygame.Surface):
        """Render the projectile."""
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)  # Draw a red circle
