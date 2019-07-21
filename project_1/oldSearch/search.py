# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import time
import pdb


class Node:

    def __init__(self, state, myDirection = None, cost = None, parentList = None, distance = None):
        
        self.state = state
        self.list = []

        if myDirection is None:
            self.myDirection = None
        else:
            self.myDirection = myDirection

        if cost is None:
            self.cost = None
        else:
            self.cost = cost

        if parentList is None:
            if self.myDirection is not None:
                self.list.append(myDirection)
        else:
            if self.myDirection is not None:
                self.list = list(parentList)
                self.list.append(self.myDirection)
            else:
                self.list = list(parentList)

        if distance is None:
            self.distance = 0
        else:
            self.distance = distance

    def getState(self):
        return self.state 

    def getDirection(self):
        return self.myDirection

    def getCost(self):
        return self.cost

    def getList(self):
        return self.list

    def getDistance(self):
        return self.distance

    def getInfo(self):
        print "The current state is: ", self.state
        print "My direction is: ", self.myDirection
        print "The total cost is: ", self.cost
        print "The current list is: ", self.list

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    visitedOrNot = set()
    theStack = util.Stack()

    theRoot = Node(problem.getStartState())
    theStack.push(theRoot)
    goalNotAcheived = True

    while (goalNotAcheived):
        tempNode = theStack.pop()
        if (problem.isGoalState(tempNode.getState())):
            goalNotAcheived = False
            return tempNode.getList()

        if tempNode.getState() not in visitedOrNot:
            visitedOrNot.add(tempNode.getState())
            for child in problem.getSuccessors(tempNode.getState()):
                childNode = Node(child[0], child[1], child[2], tempNode.getList())
                theStack.push(childNode)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # pdb.set_trace() # This sets a breakpoint here

    visitedOrNot = set()
    theQueue = util.Queue()

    theRoot = Node(problem.getStartState())
    theQueue.push(theRoot)
    goalNotAcheived = True

    while (goalNotAcheived and theQueue.isEmpty() == False):
        tempNode = theQueue.pop()
        if (problem.isGoalState(tempNode.getState())):
            goalNotAcheived = False
            return tempNode.getList()

        if tempNode.getState() not in visitedOrNot:
            visitedOrNot.add(tempNode.getState())
            for child in problem.getSuccessors(tempNode.getState()):
                childNode = Node(child[0], child[1], child[2], tempNode.getList())
                theQueue.push(childNode)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    visitedOrNot = set()
    theQueue = util.PriorityQueue()

    theRoot = Node(problem.getStartState())
    theQueue.push(theRoot, 1000)
    goalNotAcheived = True

    while (goalNotAcheived):
        tempNode = theQueue.pop()
        if (problem.isGoalState(tempNode.getState())):
            goalNotAcheived = False
            return tempNode.getList()

        if tempNode.getState() not in visitedOrNot:
            visitedOrNot.add(tempNode.getState())
            for child in problem.getSuccessors(tempNode.getState()):
                childNode = Node(child[0], child[1], child[2], tempNode.getList())
                theQueue.push(childNode, problem.getCostOfActions(childNode.getList()))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# def aStarHeuristic(state1, state2, distance):
#     return (util.manhattanDistance(state1, state2) + distance)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visitedOrNot = set()
    theQueue = util.PriorityQueue()

    theRoot = Node(problem.getStartState())
    theQueue.push(theRoot, 1000000)
    goalNotAcheived = True

    while (goalNotAcheived):
        tempNode = theQueue.pop()
        if (problem.isGoalState(tempNode.getState())):
            goalNotAcheived = False
            return tempNode.getList()

        if tempNode.getState() not in visitedOrNot:
            visitedOrNot.add(tempNode.getState())
            for child in problem.getSuccessors(tempNode.getState()):
                childNode = Node(child[0], child[1], child[2], tempNode.getList())
                theQueue.push(childNode,  problem.getCostOfActions(childNode.getList()) + heuristic(childNode.getState(), problem))
                # theQueue.push(childNode, heuristic(tempNode.getState(), childNode.getState()) + childNode.getCost())



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
