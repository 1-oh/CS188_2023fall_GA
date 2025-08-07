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
from game import Directions
from typing import List

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # # Note : the DFS may not find the solution with the smallest cost
    class StateWithFather:
        """
        A class that contains state and its father state, which is convenient to
        find its path backward, we use it to fill the statelist
        """
        def __init__(self, currentState, fatherStateWithFather, action):
            self.currentState = currentState
            self.fatherStateWithFather = fatherStateWithFather
            self.actionFromFather = action
    
    def SolutionFinder(GoalWithFW : StateWithFather) -> List[Directions]:
        ret = []
        currentStateWF = GoalWithFW

        while currentStateWF.fatherStateWithFather is not None:
            ret.append(currentStateWF.actionFromFather)
            currentStateWF = currentStateWF.fatherStateWithFather
        ret.reverse()
        return ret 
    
    # In the DFS, we use the stack to store the fringe
    # Each time pop an element, we put its successors into the fringe
    # There should not be an "isVisited" judgement
    """"
    KeyPoint : when to check and revise the "isVisited"? : When pop the fringe(stack) rather
    than put in the fringe, because this is "search", not the "traversal", so we need to
    consider all possible ways
    """
    fringe = util.Stack()
    startStateWF = StateWithFather(problem.getStartState(), None, None)
    fringe.push(item = startStateWF)
    isVisit = set()
    
    while(not fringe.isEmpty()):
        stateWFPop = fringe.pop()
        statePop = stateWFPop.currentState
        if problem.isGoalState(statePop):
            return SolutionFinder(stateWFPop)
        if statePop not in isVisit:
            isVisit.add(statePop)
            for eachState in problem.getSuccessors(statePop):
                fringe.push(StateWithFather(eachState[0], stateWFPop, eachState[1]))
               
    return None

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Note : the BFS must find the solution with the lowest level
    class StateWithFather:
        """
        A class that contains state and its father state, which is convenient to
        find its path backward, we use it to fill the statelist
        """
        def __init__(self, currentState, fatherStateWithFather, action):
            self.currentState = currentState
            self.fatherStateWithFather = fatherStateWithFather
            self.actionFromFather = action
    
    def SolutionFinder(GoalWithFW : StateWithFather) -> List[Directions]:
        ret = []
        currentStateWF = GoalWithFW

        while currentStateWF.fatherStateWithFather is not None:
            ret.append(currentStateWF.actionFromFather)
            currentStateWF = currentStateWF.fatherStateWithFather
        ret.reverse()
        return ret 
    
    # In the BFS, we use the stack to Queue the fringe
    # Each time pop an element, we put its successors into the fringe

    # There should  be an "isVisited" judgement, since we span all ways from the
    # start(center) to the edge, and not want to go back(this will not influence
    # the integeity of all ways in BFS)
    """"
    KeyPoint : when to check and revise the "isVisited"? : When put into fringe rather(queue)
    than pop the fringe, because we want to have the best solution, so we don't need to consider
    all ways
    """
    fringe = util.Queue()
    startStateWF = StateWithFather(problem.getStartState(), None, None)
    fringe.push(item = startStateWF)
    # TO-DO:Implement the isVisit
    isVisit = set()
    isVisit.add(problem.getStartState())

    while(not fringe.isEmpty()):
        stateWFPop = fringe.pop()
        statePop = stateWFPop.currentState
        if problem.isGoalState(statePop):
            return SolutionFinder(stateWFPop)
        for eachState in problem.getSuccessors(statePop):
            #To avoid revisiting the nodes that have been visited 
            if eachState[0] not in isVisit: 
               fringe.push(StateWithFather(eachState[0], stateWFPop, eachState[1]))
               isVisit.add(eachState[0])
    return None
    

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    class StateWithFather:
        """
        A class that contains state and its father state, which is convenient to
        find its path backward, we use it to fill the statelist
        """
        def __init__(self, currentState, fatherStateWithFather, action):
            self.currentState = currentState
            self.fatherStateWithFather = fatherStateWithFather
            self.actionFromFather = action
    
    def SolutionFinder(GoalWithFW : StateWithFather) -> List[Directions]:
        ret = []
        currentStateWF = GoalWithFW

        while currentStateWF.fatherStateWithFather is not None:
            ret.append(currentStateWF.actionFromFather)
            currentStateWF = currentStateWF.fatherStateWithFather
        ret.reverse()
        return ret 
    
    # To find the total cost from the start to the currentNode
    def FindTotalCostAlready(CurrentWithFW : StateWithFather):
        return problem.getCostOfActions(SolutionFinder(CurrentWithFW))
    
    # In the uniformCostSearch, we use the PriorityQueue with function "g(n)" as the fringe
    # Each time pop an element, we put its successors into the fringe

    # There should  be an "isFather" judgement, to avoid being stuck in
    # infinite loop
    
    fringe = util.PriorityQueueWithFunction(FindTotalCostAlready)
    startStateWF = StateWithFather(problem.getStartState(), None, None)
    fringe.push(item = startStateWF)
    """
    Helpful improvement:
    We can keep an "alreadyVisit" dictionary to map nodes that have been visited to
    their shorstest value right now.Only when the new node's solution is better than 
    previous one on the same position(if there exists) we update it, otherwise we just 
    skip it to increase efficiency.
    """
    alreadyVisit = {}
    alreadyVisit.update({startStateWF.currentState : 0})

    while(not fringe.isEmpty()):
        stateWFPop = fringe.pop()
        statePop = stateWFPop.currentState
        fatherWF = stateWFPop.fatherStateWithFather

        if problem.isGoalState(statePop):
            return SolutionFinder(stateWFPop)
        for eachState in problem.getSuccessors(statePop):
            #To avoid revisiting the node that is current node's father
            if (fatherWF is None) or (fatherWF.currentState is not eachState[0]) :
               possibleWF = StateWithFather(eachState[0], stateWFPop, eachState[1])
               if (eachState[0] not in alreadyVisit.keys()) or alreadyVisit[eachState[0]] > FindTotalCostAlready(possibleWF):
                  fringe.push(possibleWF)
                  alreadyVisit.update({eachState[0] : FindTotalCostAlready(possibleWF)})
    
    return None

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    class StateWithFather:
        """
        A class that contains state and its father state, which is convenient to
        find its path backward, we use it to fill the statelist
        """
        def __init__(self, currentState, fatherStateWithFather, action):
            self.currentState = currentState
            self.fatherStateWithFather = fatherStateWithFather
            self.actionFromFather = action
    
    def SolutionFinder(GoalWithFW : StateWithFather) -> List[Directions]:
        ret = []
        currentStateWF = GoalWithFW

        while currentStateWF.fatherStateWithFather is not None:
            ret.append(currentStateWF.actionFromFather)
            currentStateWF = currentStateWF.fatherStateWithFather
        ret.reverse()
        return ret 
    
    # To find the total cost from the start to the currentNode
    def CalculateF(CurrentWithFW : StateWithFather):
        return problem.getCostOfActions(SolutionFinder(CurrentWithFW)) + heuristic(CurrentWithFW.currentState, problem)
    
    # In the A* Search, we use the PriorityQueue with function "h(n)+g(n)" as fringe
    # Each time pop an element, we put its successors into the fringe

    # There should  be an "isFather" judgement, to avoid being stuck in
    # infinite loop
    
    fringe = util.PriorityQueueWithFunction(CalculateF)
    startStateWF = StateWithFather(problem.getStartState(), None, None)
    fringe.push(item = startStateWF)
    """
    Helpful improvement:
    We can keep an "alreadyVisit" dictionary to map nodes that have been visited to
    their shorstest value right now.Only when the new node's solution is better than 
    previous one on the same position(if there exists) we update it, otherwise we just 
    skip it to increase efficiency.
    """
    alreadyVisit = {}
    alreadyVisit.update({startStateWF.currentState : heuristic(startStateWF.currentState, problem)})

    while(not fringe.isEmpty()):
        stateWFPop = fringe.pop()
        statePop = stateWFPop.currentState
        fatherWF = stateWFPop.fatherStateWithFather

        if problem.isGoalState(statePop):
            return SolutionFinder(stateWFPop)
        for eachState in problem.getSuccessors(statePop):
            #To avoid revisiting the node that is current node's father
            if (fatherWF is None) or (fatherWF.currentState is not eachState[0]) :
               possibleWF = StateWithFather(eachState[0], stateWFPop, eachState[1])
               if (eachState[0] not in alreadyVisit.keys()) or alreadyVisit[eachState[0]] > CalculateF(possibleWF):
                  fringe.push(possibleWF)
                  alreadyVisit.update({eachState[0] : CalculateF(possibleWF)})
    
    return None

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
