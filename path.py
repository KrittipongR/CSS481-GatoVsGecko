import pygame

class Path:
    def __init__(self):
        self.points = [(50, 100), (200, 100), (200, 300), (400, 300), (400, 500)]

    def draw(self, screen):
        for i in range(len(self.points) - 1):
            pygame.draw.line(screen, (255, 255, 255), self.points[i], self.points[i+1], 5)
