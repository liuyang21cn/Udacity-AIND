# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def getStartState(self):
     """
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"

  # initial state
  state = problem.getStartState()
  explored = dict()
  solutions = []
  dfs_helper(problem, state, solutions, explored)

  return solutions

# set a helper function
def dfs_helper(problem, state, solutions, explored):
    # check if goal state
    if problem.isGoalState(state):
        return True
    # loop over successors
    for leaf, action, _ in problem.getSuccessors(state):
        # if leaf not in explored
        if leaf not in explored:
            # add leaf to explored and add action
            explored[leaf] = True
            solutions.append(action)
            # return True if the following steps come to goal state
            if dfs_helper(problem, leaf, solutions, explored):
                return True
            # if not true, remove the current action
            solutions.pop()
    return False

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  # initial state
  state = problem.getStartState()
  # keep track action path for every leaf
  action_map = dict()
  action_map[state] = []
  # check if node visited
  explored = set()
  # frontier
  frontier = util.Queue()
  # create dict to store info at every node, idea is similar to linked list
  node = {}
  node['parent'] = None
  node['action'] = None
  node['state'] = state
  frontier.push(node)

  if problem.isGoalState(state):
      return []
  while not frontier.isEmpty():
      # pop the node at the smallest level
      node = frontier.pop()
      state = node['state']
      # check if node is goal, return actions associated with it
      if problem.isGoalState(state):
          break
      # if node in explored, check next poped node
      if state in explored:
          continue
      explored.add(state)
      # for leaf in current node's successors
      for leaf, action, _ in problem.getSuccessors(state):
          if leaf not in explored:
              # create new node and add to frontier
              new_node = {}
              new_node['parent'] = node
              new_node['action'] = action
              new_node['state'] = leaf
              frontier.push(new_node)
  solutions = []
  while node['action'] != None:
      solutions.insert(0, node['action'])
      node = node['parent']
  return solutions

  # if problem.isGoalState(state):
  #     return []
  # # if frontier not empty
  # while not frontier.isEmpty():
  #     # pop the node at the smallest level
  #     node = frontier.pop()
  #     # check if node is goal, return actions associated with it
  #     if problem.isGoalState(node):
  #         return action_map[node]
  #     # if node in explored, check next poped node
  #     if node in explored:
  #         continue
  #     explored.add(node)
  #     # for leaf in current node's successors
  #     for leaf, action, _ in problem.getSuccessors(node):
  #         if leaf not in explored:
  #             # if leaf not in explored, copy the actions of parent node
  #             action_map[leaf] = action_map[node]
  #             # append current action
  #             action_map[leaf].append(action)
  #             # add leaf to frontier for bfs search purposes
  #             frontier.push(leaf)
  # return nonthing if frontier is empty
  # return []


def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  # initial state
  state = problem.getStartState()
  # check if node visited
  explored = set()
  # create node to store information, consider as a linked list
  node = {}
  node['parent'] = None
  node['action'] = None
  node['cost'] = 0
  node["state"] = state
  # frontier as PriorityQueue
  frontier = util.PriorityQueue()
  frontier.push(node, node['cost'])

  if problem.isGoalState(state):
      return []
  while not frontier.isEmpty():
      # pop the node at the smallest level
      node = frontier.pop()
      state = node["state"]
      # check if node is goal, return actions associated with it
      if problem.isGoalState(state):
          break
      # if node in explored, check next poped node
      if state in explored:
          continue
      explored.add(state)
      # for leaf in current node's successors
      for leaf, action, cost in problem.getSuccessors(state):
          if leaf not in explored:
              new_node = {}
              new_node['parent'] = node
              new_node['action'] = action
              new_node['state'] = leaf
              new_node['cost'] = node['cost'] + cost
              frontier.push(new_node, cost)

  solutions = []
  while node['action'] != None:
      solutions.insert(0, node['action'])
      node = node['parent']
  return solutions


def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  # initial state
  state = problem.getStartState()
  # check if node visited
  explored = set()
  # create node to store information, consider as a linked list
  node = {}
  node['parent'] = None
  node['action'] = None
  node['cost'] = heuristic(state, problem)
  node["state"] = state
  # frontier as PriorityQueue
  frontier = util.PriorityQueue()
  frontier.push(node, node['cost'])

  if problem.isGoalState(state):
      return []
  while not frontier.isEmpty():
      # pop the node at the smallest level
      node = frontier.pop()
      state = node["state"]
      # check if node is goal, return actions associated with it
      if problem.isGoalState(state):
          break
      # if node in explored, check next poped node
      if state in explored:
          continue
      explored.add(state)
      # for leaf in current node's successors
      for leaf, action, cost in problem.getSuccessors(state):
          if leaf not in explored:
              new_node = {}
              new_node['parent'] = node
              new_node['action'] = action
              new_node['state'] = leaf
              # cost = previous cost + cost + heuristic distance
              new_node['cost'] = node['cost'] + cost + heuristic(leaf, problem)
              frontier.push(new_node, cost)

  solutions = []
  while node['action'] != None:
      solutions.insert(0, node['action'])
      node = node['parent']
  return solutions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
