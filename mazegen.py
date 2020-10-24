import argparse

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

def braid_maze(width, height):
  maze = zeroes(width, height)
  border(maze, width, height)

  return maze

def perfect_maze(width, height):
  maze = zeroes(width, height)
  border(maze, width, height)

  return maze

def print_maze(maze, width, height):
  for x in range(width):
    row = ''
    for y in range(height):
      row = row + MAZE_CHARS[maze[y][x]]
    print(row)

def get_maze(maze_type, width, height):
  if maze_type == PERFECT_MAZE:
    return perfect_maze(width, height)
  elif maze_type == BRAID_MAZE:
    return braid_maze(width, height)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--maze', default='perfect')
  parser.add_argument('--width', type=int, default=20)
  parser.add_argument('--height', type=int, default=20)
  args = parser.parse_args()

  maze = get_maze(args.maze, args.width, args.height)
  print_maze(maze,args.width, args.height)