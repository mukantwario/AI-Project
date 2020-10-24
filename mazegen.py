import argparse
import random
import sys


MAZE_CHARS = ['  ','██']
PERFECT_MAZE = 'perfect'
BRAID_MAZE = 'braid'

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


def braid_maze(width, height):
  maze = zeroes(width, height)
  border(maze, width, height)

  for x in range(width):
    for y in range(height):
      if x % 2 == 0 and y % 2 == 0:
        maze[y][x] = 1


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

  return maze

def perfect_maze(width, height):
  maze = zeroes(width, height)
  border(maze, width, height)

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

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--maze', default='perfect')
  parser.add_argument('--width', type=int, default=21)
  parser.add_argument('--height', type=int, default=21)
  args = parser.parse_args()

  maze = get_maze(args.maze, args.width, args.height)
  print_maze(maze,args.width, args.height)