from sys import exit
from collections import defaultdict
from pygame.locals import *

from characters import *
from objects import *
from walls import *


def main():

    all_purpose_dict = defaultdict(list)

    pygame.init()
    Wall.spawn_zones(all_purpose_dict)
    Object.spawn(3, all_purpose_dict)
    player = Character("M", all_purpose_dict)
    boss = Character("G", all_purpose_dict)

    objects_to_blit = all_purpose_dict.copy()

    for _, v in objects_to_blit.items():
        for all_values in v:
            all_purpose_dict["All_objects"].append(all_values)

    while 1:

        CLOCK.tick(60)

        screen.fill((0, 0, 0))

        for object in all_purpose_dict["All_objects"]:
            screen.blit(object.surface, object.rect)

        screen.blit(FONT.render("Objects : {}".format(len(all_purpose_dict["Objects_owned"])),
                                True, (255, 255, 255)), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == KEYDOWN and event.key == K_RIGHT:
                player.check_collision(SPRITE_WIDTH, 0, all_purpose_dict)
            elif event.type == pygame.KEYDOWN and event.key == K_DOWN:
                player.check_collision(0, SPRITE_HEIGHT, all_purpose_dict)
            elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
                player.check_collision(-SPRITE_WIDTH, 0, all_purpose_dict)
            elif event.type == pygame.KEYDOWN and event.key == K_UP:
                player.check_collision(0, -SPRITE_HEIGHT, all_purpose_dict)

        pygame.display.update()


if __name__ == "__main__":
    main()
