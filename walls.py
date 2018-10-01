from constants import *


class Wall:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.surface = pygame.transform.scale(pygame.image.load(image).convert_alpha(),
                                              (SPRITE_WIDTH, SPRITE_HEIGHT))
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(self.x, self.y)

    @classmethod
    def spawn_zones(cls, dict_to_store):
        x = -1
        y = -1
        line = []
        with open("ressource/maze_overview.txt", "r") as file:
            for lines in file:
                y += 1
                for char in lines:
                    line.append(char)
                    x += 1
                    if len(line) > NUMBER_OF_SPRITES:
                        line = []
                        x = -1
                    if char == "#":
                        wall = Wall(IMAGES["Walls"], x*SPRITE_WIDTH, y*SPRITE_HEIGHT)
                        dict_to_store["Walls"].append(wall)
