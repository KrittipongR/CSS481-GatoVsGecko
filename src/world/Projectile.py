import math
import pygame
class Projectile:
    def __init__(self, start_x, start_y, target, speed, damage):
        self.x = start_x
        self.y = start_y
        self.target = target  # Reference to the target (e.g., a Gecko instance)
        self.speed = speed
        self.damage = damage
        self.active = True
        self.updateTargetPosition()  # Initial target position
        self.calculateTrajectory()

    def updateTargetPosition(self):
        """Update the target's current position."""
        self.target_x = self.target.x
        self.target_y = self.target.y
        self.calculateTrajectory()

    def calculateTrajectory(self):
        """Recalculate the trajectory based on the updated target position."""
        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)
        self.vx = self.speed * math.cos(self.angle)
        self.vy = self.speed * math.sin(self.angle)

    def update(self, dt):
        """Update the projectile's position and check for collision with the target."""
        # Update target position and trajectory every frame
        self.updateTargetPosition()

        # Move the projectile
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Check if the projectile has hit the target
        if math.hypot(self.target_x - self.x, self.target_y - self.y) < 5:  # Adjust threshold as needed
            self.active = False
            self.target.hp -= self.damage  # Apply damage to the target

    def render(self, screen: pygame.Surface):
        """Render the projectile."""
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)  # Draw a red circle
