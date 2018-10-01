from constants import *
from time import sleep


class Character:

    def __init__(self, name_in_maze, dict_to_store):
        self.surface = pygame.transform.scale(pygame.image.load(IMAGES[name_in_maze]).convert_alpha(),
                                              (SPRITE_WIDTH, SPRITE_HEIGHT))
        self.rect = self.surface.get_rect()
        self.death = pygame.transform.scale(pygame.image.load(IMAGES["Death"]).convert_alpha(),
                                            (SPRITE_WIDTH, SPRITE_HEIGHT))

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
                    if char == name_in_maze:
                        self.x = x*SPRITE_WIDTH
                        self.y = y*SPRITE_HEIGHT
                        self.rect = self.rect.move(self.x, self.y)

                        dict_to_store[name_in_maze].append(self)

    def moving(self, x, y, all_purpose_dict):
        if SCREEN_WIDTH > self.x + x >= 0 and SCREEN_HEIGHT > self.y + y >= 0:  # Can't move outside the screen
            self.x += x
            self.y += y
            self.rect = self.rect.move(x, y)

            for object in all_purpose_dict["Objects"]:
                if self.rect.colliderect(object.rect):
                    all_purpose_dict["Objects_owned"].append("O")
                    all_purpose_dict["Objects"].remove(object)
                    all_purpose_dict["All_objects"].remove(object)

    def check_collision(self, x, y, all_purpose_dict):
        future_rect = self.rect.move(x, y)

        for boss in all_purpose_dict["G"]:
            if future_rect.colliderect(boss.rect):
                if len(all_purpose_dict["Objects_owned"]) == 3:
                    screen.blit(boss.death, boss.rect)
                    pygame.display.update()
                    sleep(2)
                    self.game_winning_window()
                else:
                    screen.blit(self.death, self.rect)
                    pygame.display.update()
                    sleep(2)
                    self.game_losing_window(boss)

        if future_rect.collidelist(all_purpose_dict["Walls"]) != -1:
            pass
        else:
            self.moving(x, y, all_purpose_dict)

    def game_winning_window(self):
        screen.fill((0, 0, 0))
        screen.blit(FONT.render("CONGRATULATIONS, you escaped the maze !", True,
                                (255, 255, 255)), (SCREEN_WIDTH/2 - 140, SCREEN_HEIGHT/4))
        screen.blit(pygame.transform.scale2x(self.surface), (SCREEN_WIDTH/2 -
                                                             SPRITE_WIDTH, SCREEN_HEIGHT/3))
        pygame.display.update()

        sleep(3)
        exit()

    @staticmethod
    def game_losing_window(boss):
        screen.fill((0, 0, 0))
        screen.blit(FONT.render("You failed to escape ! TRY AGAIN !", True, (255, 255, 255)),
                    (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/4))
        screen.blit(pygame.transform.scale2x(boss.surface), (SCREEN_WIDTH/2 -
                                                             SPRITE_WIDTH, SCREEN_HEIGHT/3))

        pygame.display.update()

        sleep(3)
        exit()
