import pygame
import random
from sys import exit
from collections import defaultdict
from time import sleep
from pygame.locals import *


class Main:

    WIDTH = 32 * 15
    HEIGHT = 43 * 17

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.launch = pygame.init()
        self.FONT = pygame.font.Font(None, 20)
        self.display = pygame.display.set_caption("MacGyver")

    def update(self):

        self.screen.fill((0, 0, 0))

        self.screen.blit(self.FONT.render("Objects picked :", False, (255, 255, 255)), (self.WIDTH / 2 - 50, 0))
        self.screen.blit(self.FONT.render("You", False, (255, 255, 255)), (18, 0))
        self.screen.blit(self.FONT.render("Boss", False, (255, 255, 255)), (self.WIDTH - 50, 0))
        self.screen.blit(player.surface, ((player.width / 2), 25))
        self.screen.blit(boss.surface, (self.WIDTH - boss.width - (boss.width / 2), 25))

        for all_objects in reversed(all_dict["All_objects"]):  # reversed to blit the player last
            self.screen.blit(all_objects.surface, all_objects.rect)

        pygame.display.update()


class Character:

    def __init__(self, image, name_in_maze):
        self.image = image
        self.surface = pygame.image.load(image).convert_alpha()
        self.rect = self.surface.get_rect()
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.death = pygame.image.load("ressource/death.png").convert_alpha()

        with open("ressource/maze_overview.txt", "r") as file:

            i = -1  # all -1 for iterations because first x/y is 0/0
            for line in file:
                j = -1  # reset char numbers for each line
                i += 1
                for char in line:
                    j += 1
                    if char == name_in_maze:  # check where the name_in_maze is in maze_overview.txt and spawn accordingly
                        self.rect = self.rect.move(j*32, 86 + i*43)
                        self.x = j*32
                        self.y = 86 + i*43

            all_dict["All_objects"].append(self)

    def moving(self, x, y):
        self.x += x
        self.y += y
        self.rect = self.rect.move(x, y)

        for object in all_dict["Objects_spawned"]:
            if self.rect.colliderect(object.rect):
                self.collision_with_object(object)

    def check_collision(self, x, y):

        future_x = self.x + x
        future_y = self.y + y
        future_rect = self.rect.move(x, y)

        if future_rect.collidelist(list(all_dict["Walls"])) != -1:  # colliding with wall
            pass
        elif future_rect.colliderect(boss.rect):
            self.collision_with_boss()
        elif game.WIDTH > future_x >= 0 and game.HEIGHT > future_y >= 86:  # check if player won't make it out of the screen
            self.moving(x, y)

    def collision_with_object(self, object_in_collision):
        object_top = Object(object_in_collision.image, (game.WIDTH / 2) - 50 + len(all_dict["Objects_owned"]) * 32, 25)
        all_dict["All_objects"].remove(object_in_collision)
        all_dict["Objects_spawned"].remove(object_in_collision)
        all_dict["Objects_owned"].append(object_top)
        all_dict["All_objects"].append(object_top)
        print("You have {} object(s) !".format(len(all_dict["Objects_owned"])))

    def collision_with_boss(self):
        global the_show_must_go_on

        if len(all_dict["Objects_owned"]) == 3:  # condition to win - 3 objects owned
                game.screen.blit(boss.death, boss.rect)
                pygame.display.update(boss.rect)
                sleep(2)
                game.screen.fill((0, 0, 0))
                game.screen.blit(game.FONT.render("CONGRATULATIONS, you escaped the maze !",
                                                  False, (255, 255, 255)), (game.WIDTH/2 - 140, game.HEIGHT/4))
                game.screen.blit(pygame.transform.scale2x(self.surface), (game.WIDTH/2 - player.width, game.HEIGHT/3))
                pygame.display.update()
                sleep(3)
                the_show_must_go_on = False
        else:
            game.screen.blit(self.death, self.rect)
            pygame.display.update(self.rect)
            sleep(2)
            game.screen.fill((0, 0, 0))
            game.screen.blit(game.FONT.render("You failed to escape ! TRY AGAIN !",
                                              False, (255, 255, 255)), (game.WIDTH/2 - 100, game.HEIGHT/4))
            game.screen.blit(pygame.transform.scale2x(boss.surface), (game.WIDTH/2 - boss.width, game.HEIGHT/3))
            pygame.display.update()
            sleep(3)
            the_show_must_go_on = False


class Walls:
    def __init__(self, image, x, y):
        self.surface = pygame.image.load(image).convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(x, y)

    @classmethod
    def spawn(cls):
        line = []
        x = -1
        y = -1
        with open("ressource/maze_overview.txt", "r") as file:
            for lines in file:
                y += 1
                for char in lines:
                    line.append(char)
                    x += 1
                    if len(line) > 15:
                        line = []
                        x = -1
                    if char == "#":
                        wall = Walls("ressource/wall.png", x*32, 86 + y*43)
                        all_dict["All_objects"].append(wall)
                        all_dict["Walls"].append(wall.rect)


class Object:
    def __init__(self, image, x, y):
        self.image = image
        self.surface = pygame.image.load(image).convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(self.x, self.y)

    @classmethod
    def spawn(cls, number_to_spawn):
        objects_images = ["ressource/tube_plastique2.png", "ressource/ether2.png", "ressource/seringue2.png"]  # all images for objects
        all_rect = [object.rect for object in all_dict["All_objects"]]

        while len(all_dict["Objects_spawned"]) < number_to_spawn:
            x = random.randrange(0, 32*14, 32)
            y = random.randrange(86, 43*14, 43)
            new_object = Object(objects_images[len(all_dict["Objects_spawned"])], x, y)
            if new_object.rect.collidelist(all_rect) == -1:
                all_dict["All_objects"].append(new_object)
                all_dict["Objects_spawned"].append(new_object)
                all_rect.append(new_object.rect)
            else:
                del new_object


""" INITIALIZATION """


the_show_must_go_on = True
game = Main()
all_dict = defaultdict(list)
player = Character("ressource/MacGyver.png", "M")
boss = Character("ressource/Gardien.png", "G")
Walls.spawn()
Object.spawn(3)

""" GAME LOOP """

while the_show_must_go_on:

    game.clock.tick(60)
    game.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == KEYDOWN and event.key == K_RIGHT:  # KEYDOWN = can't move more than once with one keypress
            player.check_collision(player.width, 0)
        elif event.type == pygame.KEYDOWN and event.key == K_DOWN:
            player.check_collision(0, player.height)
        elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
            player.check_collision(-player.width, 0)
        elif event.type == pygame.KEYDOWN and event.key == K_UP:
            player.check_collision(0, -player.height)

