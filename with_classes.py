import random


class Mac:

    def __init__(self):
        self.x = 0
        self.y = 13

    def move(self):
        global game

        while game:
            output_maze()
            user_input = input("Move MacGyver with ZQSD !")
            if user_input == "z":
                if check_movement(self.x, self.y - 1):
                    maze[self.y][self.x], maze[self.y - 1][self.x] = " ", "M"
                    self.y -= 1
                    self.new_turn()
                else:
                    self.new_turn()
            elif user_input == "q":
                if check_movement(self.x - 1, self.y):
                    maze[self.y][self.x], maze[self.y][self.x - 1] = " ", "M"
                    self.x -= 1
                    self.new_turn()
                else:
                    self.new_turn()
            elif user_input == "s":
                if check_movement(self.x, self.y + 1):
                    maze[self.y][self.x], maze[self.y + 1][self.x] = " ", "M"
                    self.y += 1
                    self.new_turn()
                else:
                    self.new_turn()
            elif user_input == "d":
                if check_movement(self.x + 1, self.y):
                    maze[self.y][self.x], maze[self.y][self.x + 1] = " ", "M"
                    self.x += 1
                    self.new_turn()
            else:
                print("Wrong command, try again.")
                self.new_turn()

    def new_turn(self):
        print(maze)
        self.move()


class Guardian:

    def __init__(self):
        self.x = 13
        self.y = 0


class Object:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def spawn(cls, number_objects):
        global objects_spawned

        while len(objects_spawned) < number_objects:
            x = random.randint(0, 14)
            y = random.randint(0, 14)
            if maze[y][x] != "#" and\
                maze[y][x] != "G" and\
                    maze[y][x] != "M" and\
                    maze[y][x] != "O":
                maze[y][x] = "O"
                Object(x, y)
                objects_spawned += "O"
        print(maze)


def get_maze():  # import into maze var
    global maze

    with open("ressource/maze_overview.txt", "r") as file:
        for lines in file:
            line = []
            for char in lines:
                line.append(char)
                if len(line) > 15:
                    del line[15:]  # cut everything if needed
            maze.append(line)

    with open("ressource/maze_output.txt", "w"):  # make sure that the file is empty at launch
        pass


def output_maze():
    global maze
    with open("ressource/maze_output.txt", "a") as file:  # output the maze into .txt
        for i in maze:
            for j in i:
                file.write(j)
            file.write("\n")


def check_movement(x, y):  # check where player wants to go and True if possible
    global game
    global objects_retrieved

    if maze[y][x] == " ":
        return True
    elif maze[y][x] == "O":
        objects_retrieved += "O"
        print("You got an object !")
        print("You currently have {} object(s).".format(len(objects_retrieved)))
        return True
    elif maze[y][x] == "G":
        if len(objects_retrieved) == 3:
            print("You won !")
            game = False
            return True
        else:
            print("You lost !")
            game = False
            return False
    else:
        return False


def main():
    get_maze()
    Object.spawn(3)
    mac.move()


##### MAIN #####

maze = []
objects_spawned = []
objects_retrieved = []
game = True
mac = Mac()
guardian = Guardian()


main()
