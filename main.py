import argparse
from mazegen import get_maze, ALL_MAZES, print_maze
from agents import get_agent, ALL_AGENTS
from util import Problem
import time

ALL = 'all'

def run(mazeType, ai, trials, width, height):
  # TODO: all of this

  # setup some data structure for reporting results

  # for each trial
  for trial in range(trials):
    # create a list of agents, will only be one if `all` is not selected
    agents = []
    t0 = time.time()
    if ai == ALL:
      for agent in ALL_AGENTS:
        agents.append(get_agent(agent))
    else:
      agents.append(get_agent(ai))
      
      
    # create a list of mazes, will only be one if `all` is not selected
    mazes = []
    if mazeType == ALL:
      for maze in ALL_MAZES:
        mazes.append(get_maze(maze, width, height))
    else:
      mazes.append(get_maze(mazeType, width, height))

    # for each maze
    for maze in mazes:
      # create a problem object for this maze, corner to corner
      problem = Problem((1,1), (width-2, height-2), maze, width, height)
      # for each agent
      for agent in agents:
        # get a plan from this agent
        plan = agent.getPlan(problem)
        # record results of this agent-maze pair into the reporting data structure
        print(plan)
        print_maze(problem.maze, width, height)
  # print report results
  print('done!')
  t1 = time.time()
  total_time = t1 - t0
  print("Time elapsed: ", total_time, "\n")

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  #parser.add_argument('--maze', default='perfect')
  parser.add_argument('--maze', default='perfect')
  #parser.add_argument('--ai', default='astar')
  #parser.add_argument('--ai', default='bfs')
  parser.add_argument('--ai', default='dfs')
  parser.add_argument('--trials', type=int, default=1)
  parser.add_argument('--width', type=int, default=21)
  parser.add_argument('--height', type=int, default=21)
  args = parser.parse_args()  

  run(args.maze, args.ai, args.trials, args.width, args.height)