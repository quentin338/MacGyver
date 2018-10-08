import pygame
import os

os.environ["SDL_VIDEO_CENTERED"] = "1"

SPRITE_WIDTH = 40
SPRITE_HEIGHT = 40
NUMBER_OF_SPRITES = 15

SCREEN_WIDTH = NUMBER_OF_SPRITES * SPRITE_WIDTH
SCREEN_HEIGHT = NUMBER_OF_SPRITES * SPRITE_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CLOCK = pygame.time.Clock()

OBJECTS_IMAGES = ["ressource/ether2.png", "ressource/seringue2.png",
                  "ressource/tube_plastique2.png"]

IMAGES = {"M": "ressource/MacGyver.png",
          "G": "ressource/Gardien.png",
          "Walls": "ressource/wall.png",
          "Death": "ressource/death.png"}
