from util import Agent
from queue import PriorityQueue
import util
import sys

DFS = 'dfs'
BFS = 'bfs'
ASTAR = 'astar'

ALL_AGENTS = [DFS, BFS, ASTAR]

class DfsAgent(Agent):
  def getPlan(self, problem):
      # TODO: implement DFS w/ this problem
      start = problem.getStartState()
      stack = util.Stack()
      stack.push(start)
      visited = set()
      while not stack.isEmpty():
          state = stack.pop()
          visited.add(state[0])
          if problem.isGoalState(state):
             return state[1]
          successors = problem.getSuccessors(state)
          for item in successors:
              if item[0] in visited:
                  continue
              stack.push(item)
      return []
    #print('not defined')
    #sys.exit(1)

class BfsAgent(Agent):
  def getPlan(self, problem):

    start = problem.getStartState()
    
    visited = {start[0]}
    q = []

    def push(item):
        if item[0] not in visited:
            visited.add(item[0])
            q.append(item)


    for state in problem.getSuccessors(start): 
        push(state)

    while len(q) > 0:
        state = q.pop(0)

        if problem.isGoalState(state):
            return state[1]

        for child in problem.getSuccessors(state):
            push(child)

    return []

class PriorityItem:
    def __init__(self, priority, item):
        self.priority = priority
        self.item = item
    
    def __lt__(self, other):
        return self.priority < other.priority

def nullHeuristic(state, problem=None):
    return 0

class AstarAgent(Agent):
  def getPlan(self, problem, heuristic=nullHeuristic):
    # the shape of our queue items is: {position, weight, path, pathCost}

    start = problem.getStartState()
    
    # visited is a dict with the key being the position, and the value being cost to potentially get there
    visited = set()
    q = util.PriorityQueue()
    q.push(start, 0)
    while not q.isEmpty():
        state = q.pop()
        if problem.isGoalState(state[0]):
            return state[1]
        if state[0] not in visited:
            visited.add(state[0])
            for child in problem.getSuccessors(state):
                if child[0] not in visited:
                    q.push(child, state)

    return []

def get_agent(agent_type):
  if agent_type == DFS:
    return DfsAgent()
  elif agent_type == BFS:
    return BfsAgent()
  elif agent_type == ASTAR:
    return AstarAgent()
    
  print('Invalid agent type.')
  sys.exit(1)
