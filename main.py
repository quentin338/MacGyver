import pygame
import sys
import random

# Classes, Functions, etc

# class creation => pygame.sprite.Sprite()
#   class walls
#   class player/boss ?
#   class objects
#   class boss ?

# group creation => pygame.sprite.Group()
#   walls
#   player => player_group = pygame.sprite.Group() => player_group.add(player)
#   objects
#   boss
#   all_sprites ? => all_sprites.draw(screen) / all_sprites.update()

# collision creation => pygame.sprite.spritecollideany(sprite, group) / detection between sprite and sprites in group
#   Player/Walls
#   Player/Objects
#   Player/Boss ? => boss.kill() when len(group_objects) == 3 / player.kill() when len(group_objects) < 3 ?
#   Walls/Objects => to spawn objects without collision ?


clock = pygame.time.Clock()
FPS = 120

#### PYGAME INITIALIZATION

pygame.init()

width, height = 900, 700
pygame.display.set_caption("MacGyver")
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

player = pygame.image.load("ressource/MacGyver.png").convert_alpha()  # should load from class init
boss = pygame.image.load("ressource/Gardien.png").convert_alpha()  # should load from class init
background = pygame.image.load("ressource/structures.png").convert()

player_rect = player.get_rect()
boss_pos = boss.get_rect()

# object => screen.blit(object, (object.x = random.randint(0, screen.width) if spritecollideany(object, all_sprites) == None
#                                object.y = random.randint(0, screen.height) if spritecollideany(object, all_sprites) == None)
#                                       BLIT RANDOM AND ONLY IN EMPTY SPACES

screen.blit(background, (0, 0))
screen.blit(boss, (0, 0))  # start position
screen.blit(player, (0, 0))  # start position


### GAME LOOP / Test pressedkeys()


while 1:

    clock.tick(FPS)

    pygame.display.update()
    pressedKeys = pygame.key.get_pressed()
    rect_list = [player_rect, boss_pos, screen_rect]


    for event in pygame.event.get():
        if pressedKeys == pygame.QUIT:
            sys.exit()


    if pressedKeys[pygame.K_ESCAPE] == 1:
        pygame.quit()
        sys.exit()
    elif pressedKeys[pygame.K_RIGHT]:
        screen.blit(background, (0, 0))
        screen.blit(boss, (random.randint(0, 200), random.randint(0, 200)))  # Random spawn : OK
        player_rect = player_rect.move(1, 0)
        screen.blit(player, player_rect)
    elif pressedKeys[pygame.K_DOWN]:
        screen.blit(background, (0, 0))
        player_rect = player_rect.move(0, 1)
        screen.blit(player, player_rect)
    elif pressedKeys[pygame.K_LEFT]:
        screen.blit(background, (0, 0))
        player_rect = player_rect.move(-1, 0)
        screen.blit(player, player_rect)
    elif pressedKeys[pygame.K_UP]:
        screen.blit(background, (0, 0))
        player_rect = player_rect.move(0, -1)
        screen.blit(player, player_rect)

    pygame.display.update(rect_list)
