
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        # if has reach winning condition
        if self.currentState.state == self.victoryCondition:
            return True

        # enumerate all children state from current state, if unscaned and unvisited state found, return
        movables = self.gm.getMovables()
        for movable_index, movable in enumerate(movables):
            # this children has already been scaned
            if movable_index < self.currentState.nextChildToVisit:
                continue
            # this children is first scaned, but equal state may have been visited
            self.gm.makeMove(movable)
            childState = GameState(self.gm.getGameState(), self.currentState.depth + 1, movable)
            childState.parent = self.currentState
            self.currentState.children.append(childState)
            self.currentState.nextChildToVisit = movable_index + 1
            if childState in self.visited and self.visited[childState] == True:
                self.gm.reverseMove(movable)
                continue
            else:
                self.currentState = childState
                self.visited[childState] = True
                if childState.state == self.victoryCondition:
                    return True
                else:
                    return False
        # no new state found, thus back to parent State and solveOneStep
        if self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.solveOneStep()
        else:
            # TODO if DFS is finished and winning state is not reached
            # TODO return False will cause Dead Loop in self.solve()
            # TODO return True for now (Which should False)
            return True


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True