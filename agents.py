from util import Agent
from queue import PriorityQueue
import util
import sys
from util import Directions
import copy

DFS = 'dfs'
BFS = 'bfs'
ASTAR = 'astar'
MDP = 'mdp'

ALL_AGENTS = [DFS, BFS, ASTAR, MDP]
ITERATIONS = 10000
WALL_REWARD = -150.0
GOAL_REWARD = 100.0
DISCOUNT_FACTOR = 0.5


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
        if problem.isGoalState(state):
            return state[1]
        if state[0] not in visited:
            visited.add(state[0])
            for child in problem.getSuccessors(state):
                if child[0] not in visited:
                    q.push(child, state[2] + child[2])

    return []

class Policy:
    def __init__(self, problem):  # problem is a Problem
        # Signal 'no policy' by just displaying the maze there
        self.best_actions = copy.deepcopy(problem.maze)

    def __str__(self):

        def f(dir):
            if dir =='North':
                return '^'
            if dir =='South':
                return 'v'
            if dir =='East':
                return '>'
            if dir =='West':
                return '<'
            if dir == 0:
                return ' '
            if dir == 1:
                return '█'
            return dir

        return '\n'.join([' '.join(
            [str(f(element)) for element in row]
        ) for row in self.best_actions])

    def __len__(self):
        max = 100000
        x, y = (1, 1)
        steps = 0
        while not (y == len(self.best_actions) - 2 and x == len(self.best_actions[0]) - 2):
            steps += 1
            if steps > max:
                return max
            dx, dy = Directions.TO_VECTOR[self.best_actions[y][x]]
            x, y = int(x + dx), int(y + dy)

        return steps

# Generates the maximum utility value of a state from all the possible
# utility values allowed based on possible legal moves
# returns value and the direction
def Q_max(moves, R, V_copy, i, j, problem):
    A = {a: 0 for a in moves}
    for m in moves:
        dx, dy = Directions.TO_VECTOR[m]
        nextx, nexty = int(j + dx), int(i + dy)

        A[m] += (R[nexty][nextx] + (DISCOUNT_FACTOR * V_copy[nexty][nextx]))
    max_key = max(A, key=A.get)
    return max_key, A[max_key]


class MdpAgent(Agent):

    def getPlan(self, problem, iterations=100):
        # make a copy of the maze
        grid = copy.deepcopy(problem.maze)

        # get the start state
        start = problem.getStartState()

        # Initial Utility Matrix
        V = [[0 for j in range(len(problem.maze[0]))] for i in range(len(problem.maze))]

        # Reward Matrix
        R = [[GOAL_REWARD if problem.isGoalState(((j, i),)) else
            0 if problem.maze[i][j] == 0 else
            WALL_REWARD for j in range(len(problem.maze[0]))] for i in range(len(problem.maze))]

        while iterations > 0:
            # Creates a copy of utility matrix for every new iteration
            V_copy = copy.deepcopy(V)
            for i in range(1, len(problem.maze) - 1):
                for j in range(1, len(problem.maze[i]) - 1):
                    # if the goal is met, or we're on a wall, skip the state and go onto the next state
                    if problem.isGoalState(((j, i),)) or problem.maze[i][j] == 1:
                        continue

                    # compute the maximum possible utility value for that state along with the direction
                    key, value = Q_max(problem.legalMoves(i, j, grid), R, V_copy, i, j, problem)
                    # remove legal moves
                    # update the utility matrix
                    V[i][j] = value

                    # update the maze with direction
                    problem.maze[i][j] = key
            iterations -= 1

        # Generate the Policy based on above computation
        policy = Policy(problem)

        # reset the maze to original value
        problem.maze = grid
        return policy



def get_agent(agent_type):
  if agent_type == DFS:
    return DfsAgent()
  elif agent_type == BFS:
    return BfsAgent()
  elif agent_type == ASTAR:
    return AstarAgent()
  elif agent_type == MDP:
    return MdpAgent()

  print('Invalid agent type.')
  sys.exit(1)
