import sys
import heapq

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
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0),
  }
               

class Agent:
  def getPlan(self, problem):
    print('not defined') 
    sys.exit(1)

class Problem:
    def __init__(self, startState, goalState, maze, width, height, transition_probs=None):
        self.start = startState
        self.maze = maze
        self.width = width
        self.height = height
        self.goal = goalState
        self.nodes_explored = 0
        
        if transition_probs is None:
          self.move_probs = [.25]*4
        else:
          self.move_probs = transition_probs
        
    def getStartState(self):
        return (self.start, [], 0)

    def isGoalState(self, state):
        return state[0] == self.goal

    def getSuccessors(self, state):
        self.nodes_explored += 1
        
        successors = []
        for direction in Directions.LIST:
            x,y = state[0]
            dx, dy = Directions.TO_VECTOR[direction]
            nextx, nexty = int(x + dx), int(y + dy)
            if nextx >= 0 and nextx < self.width and nexty >= 0 and nexty < self.height and self.maze[nexty][nextx] == 0:
                successors.append(((nextx, nexty), state[1]  + [direction], state[2] + 1))

        return successors
      
      # Generates legal moves available for the agent to move from a state
    def legalMoves(self, row, column, grid):
        self.nodes_explored += 1
        moves = []

        for direction in Directions.LIST:
            dx, dy = Directions.TO_VECTOR[direction]
            nextx, nexty = int(column + dx), int(row + dy)
            if nextx >= 0 and nextx < self.width and nexty >= 0 and nexty < self.height and grid[nexty][nextx] == 0:
                moves.append(direction)

        return moves

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
