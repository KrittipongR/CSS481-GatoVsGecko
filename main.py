import pygame
from game import Game

def main():
    pygame.init() # initialize pygame
    game = Game() # create game object
    game.run() # game loop

if __name__ == "__main__":
    main() #run main program
