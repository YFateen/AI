# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util, sys, time, pdb
from copy import deepcopy


from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
#         ghostdist = sum([util.manhattanDistance(newPos, ghostState.getPosition) for ghostState in newGhostStates])
#         foodDist = sum([util.manhattanDistance(newPos, foodPos) for foodPos in newFood])
#         return successorGameState.getScore() + ghostDist - foodDist

        "*** YOUR CODE HERE ***"
        toReturn = 0
        foodList = newFood.asList()
        numOfPelletes = 1
        for m in range(newFood.width):
          for n in range(newFood.height):
            if (newFood.data[m][n] == True):
              toReturn -= util.manhattanDistance(newPos, (m, n)) * 2
              numOfPelletes += 1

        toReturn = toReturn / numOfPelletes

        for ghost in newGhostStates:
          toReturn += (util.manhattanDistance(newPos, ghost.getPosition())) 
          if (ghost.getPosition() == newPos):
              return -sys.maxint
     
        toReturn += successorGameState.getScore()
        if (currentGameState.getPacmanPosition() == newPos):
          return -sys.maxint
        else:
          return toReturn

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def value(gameState, agent, depth):
          if (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)

          if (agent == gameState.getNumAgents() -1  and self.depth == depth):
            return self.evaluationFunction(gameState)

          if (agent == 0):
            return maxValue(gameState, agent, depth)
          else:
            return minValue(gameState, agent, depth)

        def maxValue(gameState, agent, depth):
          v = -sys.maxint
          for action in gameState.getLegalActions(agent):
            if (agent == gameState.getNumAgents() - 1):
              v = max(v, value(gameState.generateSuccessor(agent, action), agent, depth+1))
            else:
              v = max(v, value(gameState.generateSuccessor(agent, action), agent+1, depth))

        def minValue(gameState, agent, depth):
          v = sys.maxint
          for action in gameState.getLegalActions(agent):
            if (agent == gameState.getNumAgents() - 1):
              v = min(v, value(gameState.generateSuccessor(agent, action), agent, depth+1))
            else:
              v = min(v, value(gameState.generateSuccessor(agent, action), agent+1, depth))



        # Returns the minmax action and score of the agent with depth at the current gameState
        # def helper(gameState, agent, depth):
        #     if gameState.isWin() or gameState.isLose():
        #         return self.evaluationFunction(gameState)
        #     #Base case
        #     if self.depth == depth and agent == gameState.getNumAgents() - 1:
        #         actions = gameState.getLegalActions(agent)
        #         if agent == 0:
        #           return max([self.evaluationFunction(gameState.generateSuccessor(agent, act)) for act in actions])
        #         else:
        #           return min([self.evaluationFunction(gameState.generateSuccessor(agent, act)) for act in actions])

        #     else:
        #         actions = gameState.getLegalActions(agent)
        #         possibleActions = []
        #         for action in actions: # For each possible action, see what the best option the next level chooses
        #             if agent < gameState.getNumAgents() - 1:
        #                 possibleAction = helper(gameState.generateSuccessor(agent, action), agent + 1, depth)
        #             else:
        #                 possibleAction = helper(gameState.generateSuccessor(agent, action), 0, depth + 1)
        #             possibleActions.append(possibleAction)
        #         # Minmaxes the current level's actions
        #         if agent == 0:
        #           return max(possibleActions)
        #         else:
        #           return min(possibleActions)
        ret = ""
        currmax = -99999
        for action in gameState.getLegalActions(0):    
            move = value(gameState.generateSuccessor(0, action), 1, 0)
            if move > currmax:
                currmax = move
                ret = action
        return ret


class Node:

    def __init__(self, state, agentNum, depth, alpha, beta, paction, value):
        self.state = state
        self.myList = []
        
        if agentNum is None:
            self.agentNum = None
        else:
            self.agentNum = agentNum

        if depth is None:
            self.depth = None
        else:
            self.depth = depth

        if alpha is None:
            self.alpha = None
        else:
            self.alpha = alpha

        if beta is None:
            self.beta = None
        else:
            self.beta = beta

        if paction is None:
            self.paction = None
        else:
            self.paction = paction

        if value is None:
            self.value = None
        else:
            self.value = value

    def setParent(self, parent):
      self.myList.append(parent)

class AlphaBetaAgent(MultiAgentSearchAgent):

    """
      Your minimax agent with alpha-beta pruning (question 3)
    
          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def valueHelper(node):
          tempState = node.state
          if (tempState.isWin() or tempState.isLose()):
            node.value = self.evaluationFunction(tempState)
            return node

          # else:
          #   if (node.agentNum == 0 and node.depth < self.depth):
          #     node.value = maxValue(node)
          #     return node

          #   elif (node.agentNum == tempState.getNumAgents() - 1 and node.depth < self.depth):
          #     newNode = Node(tempState, 0, node.depth + 1, node.alpha, node.beta, node.paction, None)
          #     newNode.value = maxValue(newNode)
          #     return node

          #   elif (node.agentNum < tempState.getNumAgents() and node.depth < self.depth): 
          #     node.value = minValue(node)
          #     return node
          #   else:
          #     if (node.agentNum > 1  and node.depth < self.depth):
          #       node.value = minValue(node)
          #       return node
          #     if (node.agentNum == tempState.getNumAgents()):
          #       node.value = minValue(node)
          #       return node

          if (self.depth == node.depth) and (node.agentNum == gameState.getNumAgents()):
            node.value = self.evaluationFunction(tempState)
            return node

          else:
            if (node.agentNum == tempState.getNumAgents() - 1):
              node.depth += 1
              node.agentNum = 0
            else:
              node.agentNum += 1
            if node.agentNum == 0:
              node.value = maxValue(node)
              return node
            else:
              node.value = minValue(node)
              return node

        def maxValue(node):
          v = -sys.maxint
          state = node.state
          agentIndex = node.agentNum

          legalActions = state.getLegalActions(agentIndex)

          tempAlpha = node.alpha
          for tempAction in legalActions:
            tempState = state.generateSuccessor(agentIndex, tempAction)
            inputNode = Node(tempState, agentIndex, node.depth, tempAlpha, node.beta, tempAction, None)

            v = max(v, valueHelper(inputNode))
            if (v >= node.beta):
              return v
            tempAlpha = max(tempAlpha, v)
          return v

        def minValue(node):
          v = sys.maxint
          state = node.state
          agentIndex = node.agentNum

          legalActions = state.getLegalActions(agentIndex)

          tempBeta = node.beta
          for tempAction in legalActions:

            tempState = state.generateSuccessor(agentIndex, tempAction)
            inputNode = Node(tempState, agentIndex, node.depth, node.alpha, tempBeta, tempAction, None)

            v = min(v, valueHelper(inputNode))
            if (v <= node.alpha):
              return v
            tempBeta = min(tempBeta, v)
          return v

        theRoot = Node(gameState, 0, 0, 0, 0, None, 0)
        emptyList = []
        returnNode = valueHelper(theRoot)
        return returnNode.paction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

