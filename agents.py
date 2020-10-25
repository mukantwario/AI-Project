from util import Agent
import sys

DFS = 'dfs'
BFS = 'bfs'
ASTAR = 'astar'

class DfsAgent(Agent):
  def getPlan(self, problem):
    # TODO: implement DFS w/ this problem
    print('not defined') 
    sys.exit(1)

class BfsAgent(Agent):
  def getPlan(self, problem):
    # TODO: implement BFS w/ this problem
    print('not defined') 
    sys.exit(1)

class AstarAgent(Agent):
  def getPlan(self, problem):
    # TODO: implement ASTAR w/ this problem
    print('not defined') 
    sys.exit(1)

def get_agent(agent_type):
  if agent_type == DFS:
    return DfsAgent()
  elif agent_type == BFS:
    return BfsAgent()
  elif agent_type == ASTAR:
    return AstarAgent()
    
  print('Invalid agent type.')
  sys.exit(1)