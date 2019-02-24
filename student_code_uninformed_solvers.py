
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStepDFS(self):
        movables = self.gm.getMovables()
        # if current state has another child state
        if len(movables) > self.currentState.nextChildToVisit:
            movable = movables[self.currentState.nextChildToVisit]
            self.gm.makeMove(movable)
            childState = GameState(self.gm.getGameState(), self.currentState.depth + 1, movable)
            childState.parent = self.currentState
            # self.currentState.children.append(childState)
            self.currentState.nextChildToVisit += 1
            # if such child state is not visited, this step is done
            if childState not in self.visited:
                self.currentState = childState
                self.visited[childState] = True
                # terminated, return Ture/False
                return True
            # child state is visited before, back-track
            else:
                self.gm.reverseMove(movable)
                return self.solveOneStepDFS()
        # no more child state, try to back-track
        else:
            # if current state has parent state, can back-track
            if self.currentState.parent:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStepDFS()
            # (root state) has no parent state, cannot back-track
            else:
                # terminated, return Ture/False
                return True

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
        # solveOneStepDFS without depth_limit
        self.solveOneStepDFS()
        # Finally, return True if the solution state is reached, False otherwise
        if self.currentState.state == self.victoryCondition:
            return True
        else:
            return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.depth_limit = 0
        self.visitedBFS = dict()
        self.visitedBFS[self.currentState] = 0

    def solveOneStepDLS(self):
        # if currentState is reach depth_limit, no going deeper
        if self.currentState.depth >= self.depth_limit:
            # if current state has parent state, can back-track
            if self.currentState.parent:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStepDLS()
            # (root state) has no parent state, cannot back-track
            else:
                # terminated, return False because new state not found
                return False
        # almost same to DFS
        movables = self.gm.getMovables()
        # if current state has another child state
        if len(movables) > self.currentState.nextChildToVisit:
            movable = movables[self.currentState.nextChildToVisit]
            self.gm.makeMove(movable)
            childState = GameState(self.gm.getGameState(), self.currentState.depth + 1, movable)
            childState.parent = self.currentState
            # self.currentState.children.append(childState)
            self.currentState.nextChildToVisit += 1
            # if such child state is not visited in BFS, return
            if childState not in self.visitedBFS:
                self.currentState = childState
                self.visitedBFS[childState] = childState.depth
                # terminated, return True because new state found
                return True
            # if such child state is visited in current DLS or depth_limit or deeper, back-track
            elif childState in self.visited or childState.depth == self.depth_limit or childState.depth > self.visitedBFS[childState]:
                self.gm.reverseMove(movable)
                return self.solveOneStepDLS()
            # if such child state is not visited in current DLS and not depth_limit, go deeper
            else:
                self.currentState = childState
                self.visited[childState] = True
                return self.solveOneStepDLS()
        # no more child state, try to back-track
        else:
            # if current state has parent state, can back-track
            if self.currentState.parent:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStepDLS()
            # (root state) has no parent state, cannot back-track
            else:
                # terminated, return False because new state not found
                return False

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

        # if has reach winning condition
        if self.currentState.state == self.victoryCondition:
            return True
        # solveOneStepDLS iteratively with current depth_limit
        while not self.solveOneStepDLS():
            self.depth_limit += 1
            self.visited = dict()
            self.currentState = GameState(self.gm.getGameState(), 0, None)
            self.visited[self.currentState] = True
        # Finally, return True if the solution state is reached, False otherwise
        if self.currentState.state == self.victoryCondition:
            return True
        else:
            return False


"""
        NOTE - Using myFlag to iteratively deepening search
        # if has reach winning condition
        if self.currentState.state == self.victoryCondition:
            return True

        def solveOneStepHelper(one_more_chance):
            movables = self.gm.getMovables()
            # if current state has another child state
            if len(movables) > self.currentState.nextChildToVisit:
                # the layer of current state has been explored before, go deeper
                if len(movables) == len(self.currentState.children):
                    movable = movables[self.currentState.nextChildToVisit]
                    self.gm.makeMove(movable)
                    childState = self.currentState.children[self.currentState.nextChildToVisit]
                    self.currentState.nextChildToVisit += 1
                    self.currentState = childState
                    return solveOneStepHelper(one_more_chance)
                # current state has not been fully explored, explore child states
                else:
                    movable = movables[self.currentState.nextChildToVisit]
                    self.gm.makeMove(movable)
                    childState = GameState(self.gm.getGameState(), self.currentState.depth + 1, movable)
                    childState.parent = self.currentState
                    self.currentState.children.append(childState)
                    self.currentState.nextChildToVisit += 1
                    # if such child state is not visited, this step is done
                    if childState not in self.visited:
                        self.currentState = childState
                        self.visited[childState] = True
                        if childState.state == self.victoryCondition:
                            return True
                        else:
                            return False
                    # child state is visited before, back-track
                    else:
                        # Set myFlag(visited-state): full nextChildToVisit and empty children[].
                        childState.nextChildToVisit = len(movables)
                        self.gm.reverseMove(movable)
                        return solveOneStepHelper(one_more_chance)
            # no more child state, try to back-track
            else:
                # if not myFlag(visited-state), reset nextChildToVisit and back-track
                if len(movables) == len(self.currentState.children):
                    if self.currentState.parent:
                        self.currentState.nextChildToVisit = 0
                        self.gm.reverseMove(self.currentState.requiredMovable)
                        self.currentState = self.currentState.parent
                    else:
                        if one_more_chance:
                            self.currentState.nextChildToVisit = 0
                            one_more_chance = False
                        else:
                            return True
                    return solveOneStepHelper(one_more_chance)
                # if myFlag(visited-state), back-track
                else:
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    self.currentState = self.currentState.parent
                    return solveOneStepHelper(one_more_chance)

        if self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
        return solveOneStepHelper(True)
"""