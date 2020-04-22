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


import mdp, util

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
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        vcurr = util.Counter()
        for i in range(self.iterations):
            vcurr = self.values.copy()
            for state in self.mdp.getStates():
                all_actions = self.mdp.getPossibleActions(state)
                transitions = []
                value_list = []
                if self.mdp.isTerminal(state):
                    self.values[state] = 0
                else:
                    for action in all_actions:
                        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
                        value = 0
                        for transition in transitions:
                            value += transition[1]*(self.mdp.getReward(state, action, transition[0]) + self.discount * vcurr[transition[0]])
                        value_list.append(value)
                    self.values[state] = max(value_list)


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
        value = 0
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        for transition in transitions:
             value += transition[1]*(self.mdp.getReward(state, action, transition[0]) + self.discount * self.values[transition[0]])
        return value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        else:
            bestval = -99999999999
            bestaction = 0
            all_actions = self.mdp.getPossibleActions(state)
            for action in all_actions:
                transitions = self.mdp.getTransitionStatesAndProbs(state, action)
                value = 0
                for transition in transitions:
                    value += transition[1]*(self.mdp.getReward(state, action, transition[0]) + self.discount * self.values[transition[0]])
                if value > bestval:
                    bestaction = action
                    bestval = value
            return bestaction

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
        for k in range(self.iterations):

            state = self.mdp.getStates()[k %  len(self.mdp.getStates())]
            best = self.computeActionFromValues(state)
            if best is None:
                V = 0
            else:
                V = self.computeQValueFromValues(state, best)
            self.values[state] = V

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

    def computeQValues(self, state):
        # Returns a counter containing all qValues from a given state

        actions = self.mdp.getPossibleActions(state)  # All possible actions from a state
        qValues = util.Counter()  # A counter holding (action, qValue) pairs

        for action in actions:
            # Putting the calculated Q value for the given action into my counter
            qValues[action] = self.computeQValueFromValues(state, action)

        return qValues

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        allStates = self.mdp.getStates()
        predecessors = dict()
        for state in allStates:
            predecessors[state]=set()
        for state in allStates:
            allactions=self.mdp.getPossibleActions(state)
            for a in allactions:
                possibleNextStates = self.mdp.getTransitionStatesAndProbs(state, a)
                for nextState,pred in possibleNextStates:
                    if pred>0:
                        predecessors[nextState].add(state)
        pq = util.PriorityQueue()
        for state in allStates:

            stateQValues = self.computeQValues(state)

            if len(stateQValues) > 0:
                maxQValue = stateQValues[stateQValues.argMax()]
                diff = abs(self.values[state] - maxQValue)
                pq.push(state, -diff)
        for i in range(self.iterations):
            if pq.isEmpty():
                return
            state = pq.pop()
            stateQValues = self.computeQValues(state)
            maxQValue = stateQValues[stateQValues.argMax()]
            self.values[state] = maxQValue
            for p in predecessors[state]:

                pQValues = self.computeQValues(p)
                maxQValue = pQValues[pQValues.argMax()]
                diff = abs(self.values[p] - maxQValue)

                if diff > self.theta:
                    pq.update(p, -diff)

