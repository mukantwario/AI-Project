import argparse
import random
import sys
from util import Directions


MAZE_CHARS = ['  ','██','▒▒','░░']
PERFECT_MAZE = 'perfect'
BRAID_MAZE = 'braid'
RECURSIVE_DIVISION = 'recursive_division'

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
          if maze[y-1][x] == 0 and maze[y+1][x] == 2 or  maze[y-1][x] == 2 and maze[y+1][x] == 0:
            maze[y][x] = 0
            removed_wall = True
          elif maze[y][x-1] == 0 and maze[y][x+1] == 2 or  maze[y][x-1] == 2 and maze[y][x+1] == 0:
            maze[y][x] = 0
            removed_wall = True
            
    replace_all(maze, width, height, 2, 0)
    fill(maze, width, height, (1, 1), 2)

  replace_all(maze, width, height, 2, 0)
  return maze

def perfect_maze(width, height):
  maze = zeroes(width, height)
  border(maze, width, height)
  pillars(maze, width, height)
  fill(maze, width, height, (0,0), 2)
  queue = []
  
  for x in range(width):
    for y in range(height):
      if maze[y][x] == 0:
        queue.append((x, y))

  random.shuffle(queue)

  while len(queue) > 0:    
    x, y = queue.pop(0)

    if maze[y][x+1] == 2 and maze[y][x-1] == 1:
      maze[y][x] = 2
      maze[y][x+1] = 2
      maze[y][x-1] = 2
    elif maze[y+1][x] == 2 and maze[y-1][x] == 1:
      maze[y][x] = 2
      maze[y+1][x] = 2
      maze[y-1][x] = 2
    elif maze[y+1][x] == 1 and maze[y-1][x] == 1:
      queue.append((x,y))
    elif maze[y][x+1] == 1 and maze[y][x-1] == 1:
      queue.append((x,y))
    
  replace_all(maze, width, height, 2, 1)
  return maze

def divide_vertical(maze, width, height, start, end):
  x1, y1 = start
  x2, y2 = end

def divide_horizontal(maze, width, height, start, end):
  x1, y1 = start
  x2, y2 = end

def divide(maze, width, height, start, end):
  x1, y1 = start
  x2, y2 = end

  if abs(x1-x2) == 2 and abs(y2-y1) == 2:
    return
  elif abs(x1-x2) == 2:
    # must divide horizontally
    divide_horizontal(maze, width, height, start, end)
  elif abs(y1-y2) == 2:
    # must divide vertically
    divide_vertical(maze, width, height, start, end)
  else:
    # can divide either way
    if random.random() >= 0.5:
      divide_horizontal(maze, width, height, start, end)
    else:
      divide_vertical(maze, width, height, start, end)

def recursive_division_maze(width, height):
  maze = zeroes(width, height)
  border(maze, width, height)

  divide(maze, width, height, (0,0), (width-1, height-1))

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

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--maze', default='perfect')
  parser.add_argument('--width', type=int, default=21)
  parser.add_argument('--height', type=int, default=21)
  args = parser.parse_args()

  maze = get_maze(args.maze, args.width, args.height)
  print_maze(maze,args.width, args.height)