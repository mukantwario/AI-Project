from util import Agent
from queue import PriorityQueue
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
    # the shape of our queue items is: {position, action, weight, path,}

    start = problem.getStartState()
    
    visited = {start[0]}
    q = []

    def push(item, parent):
        if item[0] not in visited:
            item = item + (parent[3] + [item[1]],)
            visited.add(item[0])
            q.append(item)


    for state in problem.getSuccessors(start): 
        push(state, (0,0,0,[]))

    while len(q) > 0:
        state = q.pop(0)

        if problem.isGoalState(state[0]):
            return state[3]

        for child in problem.getSuccessors(state[0]):
            push(child, state)

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
    # the shape of our queue items is: {position, action, weight, path, pathCost}

    start = problem.getStartState()
    
    # visited is a dict with the key being the position, and the value being cost to potentially get there
    visited = {start[0]:0}
    q = PriorityQueue()

    def push(item, parent):
        if item[0] not in visited or visited[item[0]] > parent[4]+item[2]:
            item = item + (parent[3] + [item[1]],parent[4]+item[2])
            h = heuristic(item[0],problem)+item[4]
            visited[item[0]] = parent[4] + item[2]
            q.put(PriorityItem(h, item))


    for state in problem.getSuccessors(start): 
        push(state, (0,0,0,[], 0))

    while not q.empty():
        state = q.get().item

        if problem.isGoalState(state[0]):
            return state[3]

        for child in problem.getSuccessors(state[0]):
            push(child, state)

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