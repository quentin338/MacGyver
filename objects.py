import random
from constants import *


class Object:

    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.surface = pygame.transform.scale(pygame.image.load(image).convert_alpha(),
                                              (SPRITE_WIDTH, SPRITE_HEIGHT))
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(self.x, self.y)

    @staticmethod
    def spawn(number_to_spawn, dict_to_store):
        x = -1
        y = -1
        i = 0
        line = []
        empty_coords = []
        with open("ressource/maze_overview.txt", "r") as file:
            for lines in file:
                y += 1
                for char in lines:
                    line.append(char)
                    x += 1
                    if len(line) > NUMBER_OF_SPRITES:
                        line = []
                        x = -1
                    if char == " ":
                        empty_coords.append((x*SPRITE_WIDTH, y*SPRITE_HEIGHT))
        while i < number_to_spawn:
            object_x, object_y = random.choice(empty_coords)
            empty_coords.remove((object_x, object_y))         # remove the coords chosen in the list
            object = Object(OBJECTS_IMAGES[i], object_x, object_y)   # spawn the object with random tuple
            dict_to_store["Objects"].append(object)
            i += 1
