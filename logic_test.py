import random


maze = []
guardian_x = 0
guardian_y = 0
mac_x = 0
mac_y = 0
objects_spawned = []
objects_collected = []


###### MAKING THE MAZE INTO LIST ######


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


###### GETTING COORDINATES ######


for i in maze:
    if "G" in i:
        guardian_x = i.index("G")
        guardian_y = maze.index(i)

for i in maze:
    if "M" in i:
        mac_x = i.index("M")
        mac_y = maze.index(i)


###### SPAWN OBJECTS ######

while len(objects_spawned) < 3:

    object_x = random.randint(0, 14)
    object_y = random.randint(0, 14)

    if maze[object_y][object_x] != "#" and\
        maze[object_y][object_x] != "G" and\
            maze[object_y][object_x] != "M" and\
            maze[object_y][object_x] != "O":
        maze[object_y][object_x] = "O"
        objects_spawned += "O"


###### MAIN LOOP ######


while 1:

    with open("ressource/maze_output.txt", "a") as file:  # output the maze into .txt
        for i in maze:
            for j in i:
                file.write(j)
            file.write("\n")

    print(maze)

    move_mac = input("Move Mac : ")

    if move_mac == "d":
        if maze[mac_y][mac_x + 1] == "#":  # when you move into a wall
            pass
        elif maze[mac_y][mac_x + 1] == maze[guardian_y][guardian_x]:  # when walk to the guardian
            if len(objects_collected) == 3:  # all objects collected
                mac_x += 1
                maze[mac_y][mac_x], maze[mac_y][mac_x - 1] = "M", " "
                print("You won !!")
            else:
                maze[mac_y][mac_x] = " "
                print("You lost !!")
                break
        elif maze[mac_y][mac_x + 1] == 15:  # can't get out of the screen even if no wall !
            pass
        else:  # walk into a space or an object
            mac_x += 1
            if maze[mac_y][mac_x] == " ":
                maze[mac_y][mac_x], maze[mac_y][mac_x - 1] = "M", " "
            else:
                maze[mac_y][mac_x], maze[mac_y][mac_x - 1] = "M", " "
                objects_collected += "O"
                print("You got {} object(s) !".format(len(objects_collected)))
    if move_mac == "q":
        break
