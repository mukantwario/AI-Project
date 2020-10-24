import argparse


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--maze', default='perfect')
  parser.add_argument('--ai', default='astar')
  parser.add_argument('--trials', type=int, default=1)
  parser.add_argument('--width', type=int, default=20)
  parser.add_argument('--height', type=int, default=20)
  args = parser.parse_args()

  mazeTypes = ['perfect', '']

  print(args.algorithm)