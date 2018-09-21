import pygame
import sys
import random
from pygame.locals import *


class Main:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.surface = pygame.image.load(image).convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(x, y)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    @staticmethod
    def initialization(screen_title, screen_width, screen_height):
        global screen
        global screen_w
        global screen_h
        global clock
        global game
        global all_spawned_rect
        global all_spawned
        global objects_owned
        game = True
        screen_h = screen_height
        screen_w = screen_width
        all_spawned = []
        all_spawned_rect = []
        objects_owned = []
        clock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption(screen_title)
        screen = pygame.display.set_mode((screen_width, screen_height))

    def load_rect(self):
        all_spawned_rect.append(self.rect)

    def blit(self):
        screen.blit(self.surface, self.rect)

    @staticmethod
    def update():
        pygame.display.update()


class Characters(Main):
    def __init__(self, image, name_in_maze):
        Main.__init__(self, image, x=0, y=0)

        all_spawned.append(self)
        self.load_rect()

        with open("ressource/maze_overview.txt", "r") as file:
            i = -1  # all -1 for iterations because first x/y is 0/0

            for line in file:
                j = -1  # reset char numbers for each line
                i += 1
                for char in line:
                    j += 1
                    if char == name_in_maze == "G":  # check where the name_in_maze is in maze_overview.txt and spawn accordingly
                        self.rect = self.rect.move(j*32, i*43)
                        self.x = self.x*32
                        self.y = self.y*43
                    elif char == name_in_maze == "M":
                        self.rect = self.rect.move(j*32, i*43)
                        self.x = j*32
                        self.y = i*43

    def moving(self, x, y):
        global game

        self.x += x
        self.y += y
        self.rect = self.rect.move(x, y)  # Moving for real

        for object in objects_spawned:
            if self.rect.colliderect(object.rect):  # checking collision with objects
                objects_spawned.remove(object)
                objects_owned.append("O")  # object owned +1
                print("You have {} object(s) !".format(len(objects_owned)))

        if self.rect.colliderect(boss.rect):  # checking collision with boss
            if len(objects_owned) == 3:  # condition to win - 3 objects owned
                print("You won the game !!")
                game = False
            else:
                print("You lost !!")
                game = False

    def check_future_collision(self, x, y):
        """ Make future rect and see if something will be there"""

        future_x = self.x + x
        future_y = self.y + y
        future_rect = self.rect.move(x, y)

        if future_rect.collidelist(walls) != -1:  # colliding with wall
            pass
        elif screen_w > future_x >= 0 and screen_h > future_y >= 0:  # check if player won't make it out of the screen
            self.moving(x, y)


class Walls(Main):
    def __init__(self, image, x, y):
        Main.__init__(self, image, x, y)

        all_spawned.append(self)

    @classmethod
    def spawn(cls):
        global walls
        walls = []
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
                        wall = Walls("ressource/wall.png", x*32, y*43)  # position itself compared to numbers line/char in maze_overview.txt
                        walls.append(wall)
                        wall.load_rect()


class Object(Main):
    def __init__(self, image, x, y):
        Main.__init__(self, image, x, y)

        global all_spawned
        all_spawned.append(self)

    @classmethod
    def spawn(cls, number_to_spawn):
        global objects_spawned

        objects_images = ["ressource/MacGyver.png", "ressource/MacGyver.png", "ressource/MacGyver.png"]  # all images for objects
        objects_spawned = []

        while len(objects_spawned) < number_to_spawn:
            x = random.randrange(0, 32*14, 32)  # random zone in screen
            y = random.randrange(0, 43*14, 43)
            a = Object(objects_images[len(objects_images) - 1], x, y)  # spawn object with images list
            objects_spawned.append(a)
            if a.rect.collidelist(all_spawned_rect) != -1:
                objects_spawned.pop()  # delete if collision with something
                del a
            else:
                a.load_rect()  # add self.rect to avoid 2 objects in the same place


#### PYGAME INITIALIZATION ####


Main.initialization("MacGyver", 32*15, 43*15)

boss = Characters("ressource/Gardien.png", name_in_maze="G")
player = Characters("ressource/MacGyver.png", name_in_maze="M")

Walls.spawn()
Object.spawn(3)


#### GAME LOOP ####


while game is True:

    clock.tick(60)
    Main.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_RIGHT:  # KEYDOWN = can't move more than once with one keypress
            player.check_future_collision(player.width, 0)
        elif event.type == pygame.KEYDOWN and event.key == K_DOWN:
            player.check_future_collision(0, player.height)
        elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
            player.check_future_collision(-player.width, 0)
        elif event.type == pygame.KEYDOWN and event.key == K_UP:
            player.check_future_collision(0, -player.height)

    pressedKeys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))

    for wall in walls:
        wall.blit()
    for object in objects_spawned:
        object.blit()

    boss.blit()
    player.blit()

    Main.update()
