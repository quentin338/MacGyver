import random

from constants import *


class Object:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.surface = pygame.transform.scale((pygame.image.load(image).convert_alpha()),
                                              (SPRITE_WIDTH, SPRITE_HEIGHT))
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(x, y)

    @classmethod
    def spawn(cls, number_to_spawn, dico):
        """ Unpacking a random coords tuple from "EMPTY" key from
            maze.coords dict and spawn with it """

        for i in range(0, number_to_spawn):
            x, y = random.choice(dico["Empty"])
            dico["Empty"].remove((x, y))  # Removing tuple to avoid 2 objects stacked
            o = Object(OBJECTS_IMAGES[i], x, y)
            dico["Objects"].append(o)
