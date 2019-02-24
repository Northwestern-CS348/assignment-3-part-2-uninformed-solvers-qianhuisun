from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg_list = []
        for peg_id in range(1, 4):
            ask_id = parse_input("fact: (on ?disk peg" + str(peg_id) + ")")
            listOfBindings = self.kb.kb_ask(ask_id)
            if listOfBindings:
                peg_list.append( [int(bindings.bindings_dict["?disk"].replace("disk", "")) for bindings in listOfBindings] )
            else:
                peg_list.append( [] )
        peg_tup = []
        for disk_list in peg_list:
            disk_list.sort()
            disk_tup = tuple(disk_list)
            peg_tup.append(disk_tup)
        peg_tup = tuple(peg_tup)
        return peg_tup

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        disk_1 = str(movable_statement.terms[0])
        peg_1 = str(movable_statement.terms[1])
        peg_2 = str(movable_statement.terms[2])
        self.kb.kb_retract( parse_input("fact: (thetop " + disk_1 + " " + peg_1 + ")") )
        self.kb.kb_retract( parse_input("fact: (on " + disk_1 + " " + peg_1 + ")") )
        answer = self.kb.kb_ask( parse_input("fact: (top " + disk_1 + " ?disk2)") )
        if answer:
            disk_2 = answer[0].bindings_dict["?disk2"]
            self.kb.kb_retract( parse_input("fact: (top " + disk_1 + " " + disk_2 + ")") )
            self.kb.kb_assert( parse_input("fact: (thetop " + disk_2 + " " + peg_1 + ")") )
        else:
            self.kb.kb_assert( parse_input("fact: (empty " + peg_1 + ")") )
        answer = self.kb.kb_ask( parse_input("fact: (thetop ?disk3 " + peg_2 + ")") )
        if answer:
            disk_3 = answer[0].bindings_dict["?disk3"]
            self.kb.kb_retract( parse_input("fact: (thetop " + disk_3 + " " + peg_2 + ")") )
            self.kb.kb_assert( parse_input("fact: (top " + disk_1 + " " + disk_3 + ")") )
        else:
            self.kb.kb_retract( parse_input("fact: (empty " + peg_2 + ")") )
        self.kb.kb_assert( parse_input("fact: (thetop " + disk_1 + " " + peg_2 + ")") )
        self.kb.kb_assert( parse_input("fact: (on " + disk_1 + " " + peg_2 + ")") )

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        board_matrix = []
        for row_id in range(1, 4):
            row_list = []
            for col_id in range(1, 4):
                ask_id = parse_input("fact: (at ?piece pos" + str(col_id) + " pos" + str(row_id) + ")")
                listOfBindings = self.kb.kb_ask(ask_id)
                if listOfBindings:
                    row_list.append(int(listOfBindings[0].bindings_dict["?piece"].replace("tile", "")))
                else:
                    row_list.append(-1)
            board_matrix.append(row_list)
        board_tup = []
        for row_list in board_matrix:
            row_tup = tuple(row_list)
            board_tup.append(row_tup)
        board_tup = tuple(board_tup)
        return board_tup

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        piece = str(movable_statement.terms[0])
        initialX = str(movable_statement.terms[1])
        initialY = str(movable_statement.terms[2])
        targetX = str(movable_statement.terms[3])
        targetY = str(movable_statement.terms[4])
        self.kb.kb_retract( parse_input("fact: (empty " + targetX + " " + targetY + ")") )
        self.kb.kb_retract( parse_input("fact: (at " + piece + " " + initialX + " " + initialY + ")") )
        self.kb.kb_assert( parse_input("fact: (empty  " + initialX + " " + initialY + ")") )
        self.kb.kb_assert( parse_input("fact: (at " + piece + " " + targetX + " " + targetY + ")") )

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
