import pygame
from config import WIDTH, HEIGHT
from path import Path
from bloon import Bloon
from tower import Tower

class Player: # Player info
    def __init__(self):
        self.hp = 100
        self.money = 0

class Game: # Game class
    def __init__(self): # Initialize parameters
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.path = Path()
        self.bloons = []
        self.towers = [Tower(150, 150, self.player)]

        # Initialize spawn
        self.bloon_spawn_timer = 0
        self.max_bloons = 10 # number of bloons to spawn
        self.bloons_spawned = 0

    def run(self): # game loop
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self): # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self): #update game

        self.bloon_spawn_timer += 1 # spawn timer

        if self.bloon_spawn_timer >= 60 and self.bloons_spawned < self.max_bloons: # spawn every 60 frames (1 sec)
            self.bloons.append(Bloon(self.path, self.player)) #spawn bloon
            self.bloon_spawn_timer = 0
            self.bloons_spawned += 1

        for bloon in self.bloons: # move bloon
            bloon.move()

        for tower in self.towers: # update every tower
            tower.update(self.bloons)

        if self.player.hp <= 0: # if player dies
            self.running = False
            print("Game Over")

    def draw(self):

        # Draw screen
        self.screen.fill((0, 0, 0))
        self.path.draw(self.screen)

        # Draw bloons
        for bloon in self.bloons:
            bloon.draw(self.screen)

        # Draw towers
        for tower in self.towers:
            tower.draw(self.screen)

        # Draw player HP
        font = pygame.font.SysFont(None, 36)
        hp_text = font.render(f"HP: {self.player.hp}", True, (255, 255, 255))
        self.screen.blit(hp_text, (WIDTH - 100, 20))

        # Draw player money
        money_text = font.render(f"Money: {self.player.money}", True, (255, 255, 255))
        self.screen.blit(money_text, (20, 20))

        pygame.display.flip()
