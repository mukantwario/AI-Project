import argparse


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--ai')
  parser.add_argument('--maze')
  args = parser.parse_args()

  mazeTypes = ['perfect', '']

  print(args.algorithm)