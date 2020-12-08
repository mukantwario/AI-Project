import random
from util import Directions

MAZE_CHARS = ['  ','██','▒▒','░░']
PERFECT_MAZE = 'perfect'
BRAID_MAZE = 'braid'
RECURSIVE_DIVISION = 'recursive_division'
RECURSIVE_QUADRANTS = 'recursive_quadrants'


def zeroes(width, height):
  maze = []
  for i in range(height):
    row = []
    for j in range(width):
      row.append(0)
    maze.append(row)
  return maze

def border(maze, width, height):
  for i in range(height):
    for j in range(width):
      if i == 0 or i == height - 1 or j == 0 or j == width - 1:
        maze[i][j] = 1

def pillars(maze, width, height):
  for x in range(width):
    for y in range(height):
      if x % 2 == 0 and y % 2 == 0:
        maze[y][x] = 1

def has_dead_ends(maze, width, height):
  for x in range(width):
    for y in range(height):
      if not (y == 0 or y == height - 1 or x == 0 or x == width - 1):
        sum = 0
        sum += maze[y+1][x]
        sum += maze[y][x+1]
        sum += maze[y-1][x]
        sum += maze[y][x-1]

        if sum > 2:
          return True
  return False

def fill(maze, width, height, start, replace):
  queue = []
  visited = set()
  x_init, y_init = start
  old_color = maze[y_init][x_init]

  queue.append(start)
  while len(queue) > 0:
    x, y = queue.pop()
    maze[y][x] = replace
    visited.add((x, y))
    for direction in Directions.LIST:
      dx, dy = Directions.TO_VECTOR[direction]
      x2, y2 = int(x + dx), int(y + dy)
      if x2 >= 0 and x2 < width and y2 >= 0 and y2 < height:
        if (x2, y2) not in visited and maze[y2][x2] == old_color:
          queue.append((x2, y2))

def replace_all(maze, width, height, replace, new_color):
  for x in range(width):
    for y in range(height):
      if maze[y][x] == replace:
        maze[y][x] = new_color

def maze_contains(maze, width, height, item):
  for x in range(width):
    for y in range(height):
      if maze[y][x] == item:
        return (x, y)

  return False