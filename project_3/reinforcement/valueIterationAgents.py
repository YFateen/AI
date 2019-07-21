# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util, sys, copy, pdb, time

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):

        # Write value iteration code here. 
        for i in range(self.iterations):

          tempValues = util.Counter()
          # Compute value for each state
          for tempState in self.mdp.getStates():

            # The value of a terminal state is always 0 by default
            if not self.mdp.isTerminal(tempState):
              tempValue = -sys.maxint
              # State Value = max(QValues)
              for tempAction in self.mdp.getPossibleActions(tempState):
                tempQ = self.computeQValueFromValues(tempState, tempAction)
                if (tempQ > tempValue):
                  tempValue = tempQ

              tempValues[tempState] = tempValue
          self.values = tempValues

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        toReturn = 0

        # List of tuples: (nextState, prob)
        transitionStates = self.mdp.getTransitionStatesAndProbs(state, action)

        # Q Value. Take possible states. Sum of: probablity * (reward function + discountFactor * previousValue)
        #          If an action has multiple outcomes, the QValue for the action is the sum of the QValues of the possible outcomes.
        for tempState in transitionStates:
          toReturn += tempState[1] * (self.mdp.getReward(state, action, tempState[0]) + self.discount * self.values[tempState[0]])

        return toReturn

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        toReturnValue = -sys.maxint
        toReturnAction = None
        listOfActions = self.mdp.getPossibleActions(state)

        if (self.mdp.isTerminal(state) or len(listOfActions) == 0):
          return None

        for tempAction in listOfActions:
          tempQ = self.computeQValueFromValues(state, tempAction)
          # Naturally resolves corner cases, if two actions have the same QValue the first action discovered is prioritized
          if tempQ > toReturnValue:
            toReturnValue = tempQ
            toReturnAction = tempAction

        return toReturnAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        allStates = self.mdp.getStates()
        for i in range(self.iterations):
            currState = allStates[i%len(allStates)]
            if not self.mdp.isTerminal(currState):
                act = self.computeActionFromValues(currState)
                qval = self.computeQValueFromValues(currState, act)
                self.values[currState] = qval

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors = {}
        for state in self.mdp.getStates():
            predecessors[state] = self.getPredecessors(state)

        queue = util.PriorityQueue()
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                diff = abs(self.values[state] - self.highestQVal(state))
                queue.update(state, -diff)

        for i in range(self.iterations):
            if queue.isEmpty():
                return
            s = queue.pop()
            self.values[s] = self.highestQVal(s)
            for p in list(predecessors[s]):
                diff = abs(self.values[p] - self.highestQVal(p))
                if diff > self.theta:
                    queue.update(p, -diff)

    # Returns a set of predecessor states
    def getPredecessors(self, state):
        statePredecessors = set()
        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                for act in self.mdp.getPossibleActions(s):
                    for nextState in self.mdp.getTransitionStatesAndProbs(s, act):
                        if nextState[0] == state and nextState[1] > 0:
                            statePredecessors.add(s)
        return statePredecessors
                        
    def highestQVal(self, state):
        ret = -99999
        for action in self.mdp.getPossibleActions(state):
            Q = sum([nextState[1] * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState[0])) for nextState in self.mdp.getTransitionStatesAndProbs(state, action)])
            ret = self.computeQValueFromValues(state, action) if (Q > ret) else ret
        return ret
