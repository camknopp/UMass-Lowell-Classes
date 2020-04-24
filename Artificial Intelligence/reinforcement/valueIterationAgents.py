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
        
        for i in range(self.iterations):
            curr_vals = self.values.copy()
            for state in self.mdp.getStates():
                value_list = list()
                if self.mdp.isTerminal(state):
                    self.values[state] = 0
                else:
                    for action in self.mdp.getPossibleActions(state):
                        curr = 0
                        for next_state in self.mdp.getTransitionStatesAndProbs(state, action):
                            curr += next_state[1]*(self.mdp.getReward(state, action, next_state[0]) + self.discount * curr_vals[next_state[0]])
                        value_list.append(curr)
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
        Q = 0
        for next_state in self.mdp.getTransitionStatesAndProbs(state, action):
             Q += next_state[1]*(self.mdp.getReward(state, action, next_state[0]) + self.discount * self.values[next_state[0]])
        return Q

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if not self.mdp.isTerminal(state):
            b_action = None
            b_val = -float('inf')
            
            for action in self.mdp.getPossibleActions(state):
                curr = 0
                for next_state in self.mdp.getTransitionStatesAndProbs(state, action):
                    curr += next_state[1]*(self.mdp.getReward(state, action, next_state[0]) + self.discount * self.values[next_state[0]])
                if curr > b_val:
                    b_val = curr
                    b_action = action
                    
            return b_action
        return None

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
        for i in range(0, self.iterations):
            curr = i %  len(self.mdp.getStates())
            state = self.mdp.getStates()[curr]
            action = self.computeActionFromValues(state)

            if action is None:
                self.values[state] = 0
            else:
                self.values[state] = self.computeQValueFromValues(state, action)

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
        predecessors = dict()
        pq = util.PriorityQueue()
        for state in self.mdp.getStates():
            predecessors[state]=set()
            
        for s in self.mdp.getStates():
            for a in self.mdp.getPossibleActions(s):
                for nextState in self.mdp.getTransitionStatesAndProbs(s, a):
                    if nextState[1]>0:
                        predecessors[nextState[0]].add(s)
        
        for s in self.mdp.getStates():
            stateQValues = util.Counter()

            for action in self.mdp.getPossibleActions(s):
                stateQValues[action] = self.computeQValueFromValues(s, action)

            if len(stateQValues) > 0:
                maxQValue = stateQValues[stateQValues.argMax()]
                diff = abs(self.values[s] - maxQValue)
                pq.push(s, -diff)

        
        for i in range(self.iterations):
            if pq.isEmpty():
                return
            s = pq.pop()
            stateQValues = util.Counter()

            for action in self.mdp.getPossibleActions(s):
                stateQValues[action] = self.computeQValueFromValues(s, action)

            max_Q = stateQValues[stateQValues.argMax()]
            self.values[s] = maxQValue

            for p in predecessors[s]:
                p_Q = util.Counter()
                for action in self.mdp.getPossibleActions(p):
                    p_Q[action] = self.computeQValueFromValues(p, action)
                
                max_Q = p_Q[p_Q.argMax()]
                diff = abs(self.values[p] - max_Q)

                if diff > self.theta:
                    pq.update(p, -diff)
            


