
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

        def solveOneStepHelper():
            movables = self.gm.getMovables()
            # if current state has another child state
            if len(movables) > self.currentState.nextChildToVisit:
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
                    self.gm.reverseMove(movable)
                    return solveOneStepHelper()
            # no more child state, try to back-track
            else:
                # if current state has parent state, can back-track
                if self.currentState.parent:
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    self.currentState = self.currentState.parent
                    return solveOneStepHelper()
                # (root state) has no parent state, cannot back-track
                else:
                    # TODO --avoid deadloop--
                    # If there is at least one solution, solverDFS.solve() must find it, due to no circular state and finite states.
                    # otherwise, solverDFS.solve() return False, 
                    # when back to root state in solveOneStep() and return True(for terminating while in solve()). 
                    return True
        
        return solveOneStepHelper()


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

        # TODO --avoid deadloop--
        # If there is at least one solution, solverBFS.solve() must find it,
        # otherwise, solverBFS.solve() return False, 
        # when no univisited state can be found in solveOneStep() and return True(for terminating while in solve()). 
        if self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
        return solveOneStepHelper(True)