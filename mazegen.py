import argparse
import random
import sys
from util import Directions
from mazeutil import zeroes, border, pillars, has_dead_ends, fill, maze_contains, replace_all, MAZE_CHARS, PERFECT_MAZE, \
    BRAID_MAZE, RECURSIVE_DIVISION, RECURSIVE_QUADRANTS

ALL_MAZES = [PERFECT_MAZE, BRAID_MAZE, RECURSIVE_DIVISION, RECURSIVE_QUADRANTS]


# Braid maze is a maze with no dead ends
# this implementation shuffles all wall positions into a list, then goes through the list and attempts to build a wall there
# if building a wall results in a dead end being created, undo that wall and move on
# repeat until queue is empty
# this strategy can result in inaccessible 'pockets', so afterwards we iterate through and paint all paths we can visit from (1,1)
# if there are no unvisited paths, we're good, otherwise, we look for a wall we can break down between a visited path and an univisted path
# repeat until there are no unvisited paths
def braid_maze(width, height):
    maze = zeroes(width, height)
    border(maze, width, height)
    pillars(maze, width, height)

    queue = []

    for x in range(width):
        for y in range(height):
            if maze[y][x] == 0:
                queue.append((x, y))

    random.shuffle(queue)

    while len(queue) > 0:
        x, y = queue.pop()

        # if this makes a dead end, we will undo this
        maze[y][x] = 1
        if has_dead_ends(maze, width, height):
            maze[y][x] = 0

    fill(maze, width, height, (1, 1), 2)
    # take down walls that can't be accessed
    while maze_contains(maze, width, height, 0):
        removed_wall = False
        for x in range(width):
            for y in range(height):
                if maze[y][x] == 1 and not removed_wall and not (y == 0 or y == height - 1 or x == 0 or x == width - 1):
                    if maze[y - 1][x] == 0 and maze[y + 1][x] == 2 or maze[y - 1][x] == 2 and maze[y + 1][x] == 0:
                        maze[y][x] = 0
                        removed_wall = True
                    elif maze[y][x - 1] == 0 and maze[y][x + 1] == 2 or maze[y][x - 1] == 2 and maze[y][x + 1] == 0:
                        maze[y][x] = 0
                        removed_wall = True

        replace_all(maze, width, height, 2, 0)
        fill(maze, width, height, (1, 1), 2)

    replace_all(maze, width, height, 2, 0)
    return maze


# A perfect maze is defined by the property: if any two outside walls are removed, there is exactly one path connecting those two points
# This algorithm randomly builds walls from the borders of the maze, and only builds a wall that won't connect with another branch
def perfect_maze(width, height):
    maze = zeroes(width, height)
    border(maze, width, height)
    pillars(maze, width, height)
    fill(maze, width, height, (0, 0), 2)
    queue = []

    for x in range(width):
        for y in range(height):
            if maze[y][x] == 0:
                queue.append((x, y))

    random.shuffle(queue)

    while len(queue) > 0:
        x, y = queue.pop(0)

        if maze[y][x + 1] == 2 and maze[y][x - 1] == 1:
            maze[y][x] = 2
            maze[y][x + 1] = 2
            maze[y][x - 1] = 2
        elif maze[y + 1][x] == 2 and maze[y - 1][x] == 1:
            maze[y][x] = 2
            maze[y + 1][x] = 2
            maze[y - 1][x] = 2
        elif maze[y + 1][x] == 1 and maze[y - 1][x] == 1:
            queue.append((x, y))
        elif maze[y][x + 1] == 1 and maze[y][x - 1] == 1:
            queue.append((x, y))

    replace_all(maze, width, height, 2, 1)
    return maze


def divide_vertical(maze, width, height, start, end):
    x1, y1 = start
    x2, y2 = end

    options = []
    for x in range(x1 + 1, x2):
        if x % 2 == 0:
            options.append(x)

    random.shuffle(options)
    x = options.pop()

    options = []
    for y in range(y1 + 1, y2):
        if y % 2 == 1:
            options.append(y)
        maze[y][x] = 1

    random.shuffle(options)
    maze[options.pop()][x] = 0
    divide(maze, width, height, start, (x, y2))
    divide(maze, width, height, (x, y1), end)


def divide_horizontal(maze, width, height, start, end):
    x1, y1 = start
    x2, y2 = end

    options = []
    for y in range(y1 + 1, y2):
        if y % 2 == 0:
            options.append(y)

    random.shuffle(options)
    y = options.pop()

    options = []
    for x in range(x1 + 1, x2):
        if x % 2 == 1:
            options.append(x)
        maze[y][x] = 1

    random.shuffle(options)
    maze[y][options.pop()] = 0

    divide(maze, width, height, start, (x2, y))
    divide(maze, width, height, (x1, y), end)


def divide(maze, width, height, start, end):
    x1, y1 = start
    x2, y2 = end

    if abs(x1 - x2) == 2 and abs(y2 - y1) == 2:
        return
    elif abs(x1 - x2) == 2:
        # must divide horizontally
        divide_horizontal(maze, width, height, start, end)
    elif abs(y1 - y2) == 2:
        # must divide vertically
        divide_vertical(maze, width, height, start, end)
    else:
        # can divide either way
        if random.random() >= 0.5:
            divide_horizontal(maze, width, height, start, end)
        else:
            divide_vertical(maze, width, height, start, end)


# this algorithm creates a perfect maze as well
# it works be recursively taking a region, slicing it horizontall or vertically, and leaving one space open to pass through
# then take the resulting two regions from the split, and repeat the same operation
# this algorithm results in very few 'diagonal' paths, and creates a somewhat 'blocky' maze
def recursive_division_maze(width, height):
    maze = zeroes(width, height)
    border(maze, width, height)

    divide(maze, width, height, (0, 0), (width - 1, height - 1))

    return maze


def divide_quadrants(maze, width, height, start, end):
    x1, y1 = start
    x2, y2 = end

    if abs(x1 - x2) == 2 and abs(y2 - y1) == 2:
        return
    elif abs(x1 - x2) == 2:
        # must divide horizontally
        divide_horizontal(maze, width, height, start, end)
    elif abs(y1 - y2) == 2:
        # must divide vertically
        divide_vertical(maze, width, height, start, end)
    else:
        # can divide either way
        options = []
        for x in range(x1 + 1, x2):
            for y in range(y1 + 1, y2):
                if y % 2 == 0 and x % 2 == 0:
                    options.append((x, y))

        random.shuffle(options)
        wall_x, wall_y = options.pop()

        for x in range(x1 + 1, x2):
            maze[wall_y][x] = 1
        for y in range(y1 + 1, y2):
            maze[y][wall_x] = 1

        # left
        options = []
        for x in range(x1 + 1, wall_x):
            if x % 2 == 1:
                options.append(x)

        random.shuffle(options)
        maze[wall_y][options.pop()] = 0

        # right
        options = []
        for x in range(wall_x, x2):
            if x % 2 == 1:
                options.append(x)

        random.shuffle(options)
        maze[wall_y][options.pop()] = 0

        # up
        options = []
        for y in range(y1 + 1, wall_y):
            if y % 2 == 1:
                options.append(y)

        random.shuffle(options)
        maze[options.pop()][wall_x] = 0

        # down
        options = []
        for y in range(wall_y, y2):
            if y % 2 == 1:
                options.append(y)

        random.shuffle(options)
        maze[options.pop()][wall_x] = 0

        divide_quadrants(maze, width, height, start, (wall_x, wall_y))
        divide_quadrants(maze, width, height, (wall_x, start[1]), (end[0], wall_y))
        divide_quadrants(maze, width, height, (start[0], wall_y), (wall_x, end[1]))
        divide_quadrants(maze, width, height, (wall_x, wall_y), end)


# this algorithm does not create a perfect maze. It promises there is at least one path between any two squares, and there can be dead ends
# it works be recursively taking a region, slicing it horizontally AND vertically, and leaving one space open to pass through each quadrants neighbors
# then take the resulting four regions from the split, and repeat the same operation
# this algorithm results in a very sparse maze
def recursive_quadrants_maze(width, height):
    maze = zeroes(width, height)
    border(maze, width, height)

    divide_quadrants(maze, width, height, (0, 0), (width - 1, height - 1))

    return maze


def print_maze(maze, width, height):
    for y in range(height):
        row = ''
        for x in range(width):
            row = row + MAZE_CHARS[maze[y][x]]
        print(row)


def get_maze(maze_type, width, height):
    if width % 2 == 0 or height % 2 == 0:
        print('Width and height must be even.')
        sys.exit(1)

    if maze_type == PERFECT_MAZE:
        return perfect_maze(width, height)
    elif maze_type == BRAID_MAZE:
        return braid_maze(width, height)
    elif maze_type == RECURSIVE_DIVISION:
        return recursive_division_maze(width, height)
    elif maze_type == RECURSIVE_QUADRANTS:
        return recursive_quadrants_maze(width, height)

    print('Invalid maze type')
    sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--maze', default='perfect')
    parser.add_argument('--width', type=int, default=21)
    parser.add_argument('--height', type=int, default=21)
    args = parser.parse_args()

    maze = get_maze(args.maze, args.width, args.height)
    print_maze(maze, args.width, args.height)