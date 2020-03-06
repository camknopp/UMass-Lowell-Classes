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
import random
import util
import math

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

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
        newGhostPositions = successorGameState.getGhostPositions()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        """
        add together euclidean distances from newpos to all new food dots
        from this sum subtract the euclidean distance from newpos to all ghost states
        """
        score = successorGameState.getScore()

        for foodPos in newFood.asList():
            foodDistance = util.manhattanDistance(newPos, foodPos)
            score += float(1.0/foodDistance)

        for ghostPos in newGhostPositions:
            ghostDistance = util.manhattanDistance(newPos, ghostPos)
            if ghostDistance > 1:
                score += float(1.0/ghostDistance)

        return score


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        def minimax(agent, depth, gameState):
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agent > 0:  # minimize for ghosts
                next = agent + 1
                if gameState.getNumAgents() == next:
                    next = 0
                if next == 0:
                    depth += 1
                nodes = []
                for nextState in gameState.getLegalActions(agent):
                    nodes.append(
                        minimax(next, depth, gameState.generateSuccessor(agent, nextState)))
                return min(nodes)

            else:  # maximize for pacman
                nodes = []
                for nextState in gameState.getLegalActions(agent):
                    nodes.append(
                        minimax(1, depth, gameState.generateSuccessor(agent, nextState)))
                return max(nodes)

        action = None
        maximum = float("-inf")

        for state in gameState.getLegalActions(0):
            returnVal = minimax(1, 0, gameState.generateSuccessor(0, state))
            if returnVal > maximum or maximum == float("-inf"):
                action = state
                maximum = returnVal

        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        
        def maximize(agent, depth, game_state, alpha, beta):  # maximize function
            v = float("-inf")
            for newState in game_state.getLegalActions(agent):
                v = max(v, alphabetaprune(1, depth, game_state.generateSuccessor(agent, newState), alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def minimize(agent, depth, game_state, alpha, beta):  # minimize function
            v = float("inf")

            next_agent = agent + 1  # calculate the next agent and increase depth accordingly.
            if game_state.getNumAgents() == next_agent:
                next_agent = 0
            if next_agent == 0:
                depth += 1

            for newState in game_state.getLegalActions(agent):
                v = min(v, alphabetaprune(next_agent, depth, game_state.generateSuccessor(agent, newState), alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        def alphabetaprune(agent, depth, game_state, alpha, beta):
            if game_state.isLose() or game_state.isWin() or depth == self.depth:  # return the utility in case the defined depth is reached or the game is won/lost.
                return self.evaluationFunction(game_state)

            if agent == 0:  # maximize for pacman
                return maximize(agent, depth, game_state, alpha, beta)
            else:  # minimize for ghosts
                return minimize(agent, depth, game_state, alpha, beta)

        """Performing maximize function to the root node i.e. pacman using alpha-beta pruning."""
        utility = float("-inf")
        action = Directions.WEST
        alpha = float("-inf")
        beta = float("inf")
        for agentState in gameState.getLegalActions(0):
            ghostValue = alphabetaprune(1, 0, gameState.generateSuccessor(0, agentState), alpha, beta)
            if ghostValue > utility:
                utility = ghostValue
                action = agentState
            if utility > beta:
                return utility
            alpha = max(alpha, utility)

        return action


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
        def expectimax(agent, depth, gameState):
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            if agent > 0:  # minimize for ghosts
                next = agent + 1
                if gameState.getNumAgents() == next:
                    next = 0
                if next == 0:
                    depth += 1
                nodes = []
                for newState in gameState.getLegalActions(agent):
                    nodes.append(expectimax(
                        next, depth, gameState.generateSuccessor(agent, newState)))
                total = sum(nodes)
                return total / float(len(gameState.getLegalActions(agent)))
            else:  # maximize for pacman
                nodes = []
                for newState in gameState.getLegalActions(agent):
                    nodes.append(expectimax(
                        1, depth, gameState.generateSuccessor(agent, newState)))
                return max(nodes)

        action = None
        maximum = float("-inf")

        for agentState in gameState.getLegalActions(0):
            returnVal = expectimax(
                1, 0, gameState.generateSuccessor(0, agentState))
            if maximum == float("-inf") or returnVal > maximum:
                action = agentState
                maximum = returnVal

        return action


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: 
    - add 100k if win state, and subtract 100k if lose state
    - sum manhattan distances to all food dots
    - sum manhattan distances to all ghosts with a manhattan distance from pacman <= 5
    - 
      Finally, these terms are summed together and the result is returned as the
        utility score for that state.

    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()

    winLose = 0
    foodDistance = 0
    foodPenalty = 0
    ghosts = 0

    if currentGameState.isLose():
        winLose -= 100000
    elif currentGameState.isWin():
        winLose += 100000

    foodPenalty = -20*len(food)

    for dot in food:
        foodDistance += manhattanDistance(position, dot)

    for ghost in currentGameState.getGhostPositions():
        distance = manhattanDistance(position, ghost)
        if distance <= 5:
            ghosts += distance

    return currentGameState.getScore() + winLose + foodPenalty - foodDistance - ghosts


# Abbreviation
better = betterEvaluationFunction
