from time import sleep
from collections import defaultdict

from constants import *
from walls2 import Wall


class Maze:
    def __init__(self):
        self.coords = defaultdict(list)
        self.font = pygame.font.Font(None, 20)

    def getting_coords(self):
        """ Creating walls objects / empty zones coords / Characters coords
            and stocking them in self.coords defaultdict """

        with open("maze_overview.txt", "r") as file:
            for y, lines in enumerate(file):
                for x, chars in enumerate(lines):
                    if chars == "#":
                        self.coords["Walls"].append(Wall(x*SPRITE_WIDTH, y*SPRITE_HEIGHT))
                    elif chars == " ":
                        self.coords["Empty"].append((x*SPRITE_WIDTH, y*SPRITE_HEIGHT))
                    elif chars == "G":
                        self.coords["G"].append((x*SPRITE_WIDTH, y*SPRITE_HEIGHT))
                    elif chars == "M":
                        self.coords["M"].append((x*SPRITE_WIDTH, y*SPRITE_HEIGHT))
                    else:
                        pass
            return self.coords

    def check_collision(self, x, y):
        actual_x, actual_y = self.coords["M"][0]

        # COLLISION WITH WALL

        for walls in self.coords["Walls"]:
            if (actual_x + x, actual_y + y) == (walls.x, walls.y):
                pass

        # COLLISION WITH - EMPTY

        if (actual_x + x, actual_y + y) in self.coords["Empty"][:]:
            self.coords["Empty"].append((actual_x, actual_y))
            self._moving(x, y)

        # COLLISION WITH OBJECT

        for object in self.coords["Objects"]:
            if (actual_x + x, actual_y + y) == (object.x, object.y):
                screen.fill((0, 0, 0), (object.x, object.y, SPRITE_WIDTH, SPRITE_HEIGHT))  # Filling object zone with black
                self.coords["Empty"].append((actual_x + x, actual_y + y))  # Declaring object zone as empty zone
                self.coords["Objects"].remove(object)
                self.coords["Objects_owned"].append(object)
                self.update()                    # Update needed for the score
                self._moving(x, y)

        # COLLISION WITH BOSS - GAME ENDING

            # GAME WON / BOSS DYING

        if (actual_x + x, actual_y + y) == self.coords["G"][0] and len(self.coords["Objects_owned"]) == 3:
            screen.blit(self.image_scaling("ressource/death.png"),
                        (actual_x + x, actual_y + y, SPRITE_WIDTH, SPRITE_HEIGHT))
            pygame.display.update()
            sleep(2)
            self.game_won()

            # GAME LOST / MAC DYING

        elif (actual_x + x, actual_y + y) == self.coords["G"][0] and len(self.coords["Objects_owned"]) != 3:
            screen.blit(self.image_scaling("ressource/death.png"),
                        (actual_x, actual_y, SPRITE_WIDTH, SPRITE_HEIGHT))
            pygame.display.update()
            sleep(2)
            self.game_lost()

    def _moving(self, x, y):
        a, b = self.coords["M"][0]
        self.coords["M"] = [(a + x, b + y)]  # Actually moving

        # Drawing Mac on the new zone / filling ancient zone with black

        screen.blit(self.image_scaling("ressource/MacGyver.png"), self.coords["M"][0])
        screen.fill((0, 0, 0), (a, b, SPRITE_WIDTH, SPRITE_HEIGHT))

        pygame.display.update()

    def update(self):
        # UPDATING EVERYTHING ON SCREEN ONLY @ LAUNCH/OBJECT GOT

        screen.fill((0, 0, 0))

        for walls in self.coords["Walls"]:
            screen.blit(walls.surface, walls.rect)
        for object in self.coords["Objects"]:
            screen.blit(object.surface, object.rect)
        for mac in self.coords["M"]:
            screen.blit(self.image_scaling("ressource/MacGyver.png"), mac)
        for boss in self.coords["G"]:
            screen.blit(self.image_scaling("ressource/Gardien.png"), boss)

        screen.blit(self.font.render("Objects : {}".format(len(self.coords["Objects_owned"])),
                                     True, (255, 255, 255)), (0, 0))

        pygame.display.update()

    def game_won(self):
        # ENDING SCREEN

        screen.fill((0, 0, 0))
        screen.blit(self.font.render("CONGRATULATIONS, you escaped the maze !", True,
                                (255, 255, 255)), (SCREEN_WIDTH/2 - 140, SCREEN_HEIGHT/4))
        screen.blit(pygame.transform.scale2x(self.image_scaling("ressource/MacGyver.png")),
                    (SCREEN_WIDTH/2 - SPRITE_WIDTH, SCREEN_HEIGHT/3))
        pygame.display.update()
        sleep(3)
        exit()

    def game_lost(self):
        # ENDING SCREEN

        screen.fill((0, 0, 0))
        screen.blit(self.font.render("You failed to escape ! TRY AGAIN !", True, (255, 255, 255)),
                    (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/4))
        screen.blit(pygame.transform.scale2x(self.image_scaling("ressource/Gardien.png")),
                    (SCREEN_WIDTH/2 - SPRITE_WIDTH, SCREEN_HEIGHT/3))
        pygame.display.update()
        sleep(3)
        exit()

    @staticmethod
    def image_scaling(image):
        # SCALING IMAGE WITH CONSTANTS.PY SPRITES VALUES

        image_scaled = pygame.transform.scale(pygame.image.load(image),
                                              (SPRITE_WIDTH, SPRITE_HEIGHT))
        return image_scaled
