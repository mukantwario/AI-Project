import sys

class Directions:
  NORTH = 'North'
  SOUTH = 'South'
  EAST = 'East'
  WEST = 'West'

  LIST = [NORTH, SOUTH, EAST, WEST]

  LEFT = {
    NORTH: WEST,
    SOUTH: EAST,
    EAST:  NORTH,
    WEST:  SOUTH
  }

  RIGHT = dict([(y,x) for x, y in LEFT.items()])

  REVERSE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
  }

  TO_VECTOR = {
    NORTH: (0, 1),
    SOUTH: (0, -1),
    EAST: (1, 0),
    WEST: (-1, 0),
  }
               

class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:

  def registerInitialState(self, state): # inspects the starting state
  """
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    """
    The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
    must return an action from Directions.{North, South, East, West, Stop}
    """
    print('not defined')    
    sys.exit(1)

class Problem:
    def __init__(self, startState):
        self.start = startState.start
        self.maze = startState.maze

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        for direction in Directions.LIST:
            x,y = state[0]
            dx, dy = Directions.TO_VECTOR[direction]
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.maze[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for direction in Directions.LIST:
            # figure out the next state and see whether it's legal
            dx, dy = Directions.TO_VECTOR[direction]
            x, y = int(x + dx), int(y + dy)
            if self.maze[x][y]:
                return 999999
            cost += 1
        return cost