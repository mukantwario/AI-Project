import argparse
from mazegen import get_maze
from agents import get_agent
from util import Problem

def run(maze, ai, trials, width, height):
  # TODO: all of this

  # setup some data structure for reporting results

  # for each trial
    # create a list of agents, will only be one if `all` is not selected
      # use get_agent
    # create a list of mazes, will only be one if `all` is not selected
      # use get_maze

    # for each maze
      # create a problem object for this maze
      # for each agent
        # get a plan from this agent
        # record results of this agent-maze pair into the reporting data structure

  # print report results
  print('done!')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--maze', default='perfect')
  parser.add_argument('--ai', default='astar')
  parser.add_argument('--trials', type=int, default=1)
  parser.add_argument('--width', type=int, default=20)
  parser.add_argument('--height', type=int, default=20)
  args = parser.parse_args()  

  run(args.maze, args.ai, args.trials, args.width, args.height)