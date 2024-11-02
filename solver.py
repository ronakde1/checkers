from copy import deepcopy
import math
from dataclasses import dataclass


@dataclass
class Piece:
    _is_king: bool
    _is_ai: bool

    def __repr__(self):
        val = "c" if self._is_ai else "p"
        return f"{val}"

    def __copy__(self):
        copy_object = Piece(_is_king=self._is_king, _is_ai=self._is_ai)
        return copy_object

    def __deepcopy__(self, memodict={}):
        copy_object = Piece(_is_king=self._is_king, _is_ai=self._is_ai)
        return copy_object


class Square:
    def __init__(self, piece: None | Piece = None):
        self.piece = piece

    def is_king(self):
        return (self.piece is not None) and self.piece._is_king

    def is_not_king(self):
        return (self.piece is not None) and not self.piece._is_king

    def is_ai(self):
        return (self.piece is not None) and self.piece._is_ai

    def is_not_ai(self):
        return (self.piece is not None) and (not self.piece._is_ai)

    def is_actual_piece(self):
        return self.piece is not None

    def __repr__(self):
        if self.is_actual_piece():
            val = "c" if self.is_ai() else "p"
            return f"{val}"
        else:
            return "-"

    def __copy__(self):
        copy_object = Square(self.piece)
        return copy_object

    def __deepcopy__(self, memodict={}):
        copy_object = Square(self.piece)
        return copy_object


class CheckersSolver:
    def __init__(self, board: list[list[Square]]):
        self.board = board

    def calculate_move(self) -> None | tuple[tuple[int, int],tuple[int, int]]:
        current_state = _Node(deepcopy(self.board))

        first_moves = current_state.get_children(True)
        print(first_moves)
        if len(first_moves) == 0:
            print("No more moves")
            return None

        dict = {}
        for i in range(len(first_moves)):
            child = first_moves[i]
            value = _Node.minimax(child.get_board(), 4, -math.inf, math.inf, False)
            dict[value] = child

        if len(dict.keys()) == 0:
            print("Computer has cornered itself")
            return None

        print(dict)

        move = dict[max(dict)].move

        print(f"move: {move}")

        return (move[0], move[1]), (move[2], move[3])

    @staticmethod
    def _make_a_move(board, old_i, old_j, new_i, new_j, queen_row):
        old = board[old_i][old_j]
        i_difference = old_i - new_i
        j_difference = old_j - new_j
        if i_difference == -2 and j_difference == 2:
            board[old_i + 1][old_j - 1] = Square()

        elif i_difference == 2 and j_difference == 2:
            board[old_i - 1][old_j - 1] = Square()

        elif i_difference == 2 and j_difference == -2:
            board[old_i - 1][old_j + 1] = Square()

        elif i_difference == -2 and j_difference == -2:
            board[old_i + 1][old_j + 1] = Square()

        board[old_i][old_j] = Square()
        board[new_i][new_j] = Square(Piece(_is_king=old.is_king() or (new_i == queen_row), _is_ai=old.is_ai()))


class _Node:
    def __init__(self, board, move=None):
        self.board = board
        self.value = None
        self.move = move
        self.parent = None

    def __repr__(self):
        return f"Node {{ value: {self.value}, move: {self.move}, parent: {self.parent}}}"

    def get_children(self, maximizing_player):
        current_state = deepcopy(self.board)
        available_moves = []

        #print(current_state)

        if maximizing_player:
            available_moves = self.find_available_moves(current_state)
            queen_row = 7
        else:
            available_moves = self.find_available_moves_player(current_state)
            queen_row = 0

        #print(available_moves)

        children_states = []

        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            CheckersSolver._make_a_move(state, old_i, old_j, new_i, new_j, queen_row)
            children_states.append(_Node(state, [old_i, old_j, new_i, new_j]))
        #print(children_states)
        return children_states

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def get_board(self):
        return self.board

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    @staticmethod
    def find_available_moves(board: list[list[Square]]):
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if board[m][n].is_ai() and (not board[m][n].is_king()):
                    if _Node.check_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if _Node.check_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if _Node.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if _Node.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
                elif board[m][n].is_ai() and board[m][n].is_king():
                    if _Node.check_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if _Node.check_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if _Node.check_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if _Node.check_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if _Node.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if _Node.check_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if _Node.check_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if _Node.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        #print("CPU", available_moves, available_jumps)

        if len(available_jumps) == 0:
            return available_moves
        else:
            return available_jumps


    @staticmethod
    def find_available_moves_player(board: list[list[Square]]):
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if (not board[m][n].is_ai()) and (not board[m][n].is_king()):
                    if _Node.check_player_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if _Node.check_player_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if _Node.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if _Node.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                elif (not board[m][n].is_ai()) and (board[m][n].is_king()):
                    if _Node.check_player_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if _Node.check_player_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if _Node.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if _Node.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if _Node.check_player_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if _Node.check_player_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if _Node.check_player_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if _Node.check_player_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])

        #print("player", available_moves, available_jumps)

        if len(available_jumps) == 0:
            return available_moves
        else:
            return available_jumps

    @staticmethod
    def check_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if not board[via_i][via_j].is_actual_piece():
            return False
        if board[via_i][via_j].is_ai():
            return False
        if board[new_i][new_j].is_actual_piece():
            return False
        if not board[old_i][old_j].is_actual_piece():
            return False
        if not board[old_i][old_j].is_ai():
            return False
        return True

    @staticmethod
    def check_moves(board, old_i, old_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if not board[old_i][old_j].is_actual_piece():
            return False
        if board[new_i][new_j].is_actual_piece():
            return False
        if not board[old_i][old_j].is_ai():
            return False
        if not board[new_i][new_j].is_actual_piece():
            return True

    @staticmethod
    def check_player_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if not board[via_i][via_j].is_actual_piece():
            return False
        if not board[via_i][via_j].is_ai():
            return False
        if board[new_i][new_j].is_actual_piece():
            return False
        if not board[old_i][old_j].is_actual_piece():
            return False
        if board[old_i][old_j].is_ai():
            return False
        return True

    @staticmethod
    def check_player_moves(board, old_i, old_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if not board[old_i][old_j].is_actual_piece():
            return False
        if board[new_i][new_j].is_actual_piece():
            return False
        if board[old_i][old_j].is_ai():
            return False
        if not board[new_i][new_j].is_actual_piece():
            return True

    @staticmethod
    def calculate_heuristics(board: list[list[Square]]):
        result = 0
        mine = 0
        opp = 0
        for i in range(8):
            for j in range(8):
                if board[i][j].is_ai():
                    mine += 1

                    if board[i][j].is_king():
                        result += 10
                    elif board[i][j].is_not_king():
                        result += 5

                    if i == 0 or j == 0 or i == 7 or j == 7:
                        result += 7
                    if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
                        continue
                    if board[i + 1][j - 1].is_not_ai() and not board[i - 1][j + 1].is_actual_piece():
                        result -= 3
                    if board[i + 1][j + 1].is_not_ai() and not board[i - 1][j - 1].is_actual_piece():
                        result -= 3
                    if board[i - 1][j - 1].is_not_ai() and board[i - 1][j - 1].is_king() and not board[i + 1][j + 1].is_actual_piece():
                        result -= 3

                    if board[i - 1][j + 1].is_not_ai() and board[i - 1][j + 1].is_king() and not board[i + 1][j - 1].is_actual_piece():
                        result -= 3
                    if i + 2 > 7 or i - 2 < 0:
                        continue
                    if board[i + 1][j - 1].is_not_ai() and not board[i + 2][j - 2].is_actual_piece():
                        result += 6
                    if i + 2 > 7 or j + 2 > 7:
                        continue
                    if board[i + 1][j + 1].is_not_ai() and not board[i + 2][j + 2].is_actual_piece():
                        result += 6

                elif board[i][j].is_not_ai():
                    opp += 1

        res = result + (mine - opp) * 1000
        return res

    @staticmethod
    def minimax(board, depth, alpha, beta, maximizing_player):
        #print("b", depth, depth - 1)
        if depth == 0:
            #print("a")
            return _Node.calculate_heuristics(board)
        current_state = _Node(deepcopy(board))

        if maximizing_player:
            max_eval = -math.inf
            for child in current_state.get_children(True):
                #print("c")
                ev = _Node.minimax(child.get_board(), depth - 1, alpha, beta, False)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            current_state.set_value(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in current_state.get_children(False):
                #print("d")
                ev = _Node.minimax(child.get_board(), depth - 1, alpha, beta, True)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            current_state.set_value(min_eval)
            return min_eval


def _print_board(board):
    i = 0
    print()
    for row in board:
        print(i, end="  |")
        i += 1
        for elem in row:
            print(elem, end=" ")
        print()
    print()
    for j in range(8):
        if j == 0:
            j = "     0"
        print(j, end="   ")
    print("\n")


if __name__ == '__main__':
    current_board = [[Square() for _ in range(8)] for _ in range(8)]
    for i in range(3):
        for j in range(8):
            if (i + j) % 2 == 1:
                current_board[i][j] = Square(Piece(_is_king=False, _is_ai=True))
    for i in range(5, 8, 1):
        for j in range(8):
            if (i + j) % 2 == 1:
                current_board[i][j] = Square(Piece(_is_king=False, _is_ai=False))

    _print_board(current_board)
    move = CheckersSolver(current_board)
    move.calculate_move()
