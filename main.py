from maze import *
from objects2 import *
from pygame.locals import *


def main():

    pygame.init()

    maze = Maze()
    maze.getting_coords()
    Object.spawn(3, maze.coords)
    maze.update()

    while 1:

        CLOCK.tick(60)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and event.key == K_RIGHT:
                    maze.check_collision(SPRITE_WIDTH, 0)
                elif event.type == pygame.KEYDOWN and event.key == K_DOWN:
                    maze.check_collision(0, SPRITE_HEIGHT)
                elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
                    maze.check_collision(-SPRITE_WIDTH, 0)
                elif event.type == pygame.KEYDOWN and event.key == K_UP:
                    maze.check_collision(0, -SPRITE_HEIGHT)


if __name__ == "__main__":
    main()
