from constants import *


class Wall:
    def __init__(self, x, y):
        self.surface = pygame.transform.scale((pygame.image.load(IMAGES["Walls"]).convert_alpha()),
                                              (SPRITE_WIDTH, SPRITE_HEIGHT))
        self.x = x
        self.y = y
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(x, y)
