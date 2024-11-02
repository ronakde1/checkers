from copy import deepcopy
import math
from dataclasses import dataclass


@dataclass
class Piece:
    is_king: bool
    is_ai: bool

    def __repr__(self):
        return f"{"c" if self.is_ai else "b"}"


class Square:
    def __init__(self, piece: None | Piece = None):
        self.piece = piece

    def is_king(self):
        return (self.piece is not None) and self.piece.is_king

    def is_ai(self):
        return (self.piece is not None) and self.piece.is_ai

    def is_actual_piece(self):
        return self.piece is not None

    def __repr__(self):
        if self.is_actual_piece():
            return f"{"c" if self.is_ai else "b"}"
        else:
            return "-"


class CheckersSolver:
    def __init__(self, board: list[list[Square]]):
        self.board = board

    def calculate_move(self):
        current_state = _Node(deepcopy(self.board))

        first_moves = current_state.get_children()
        print(first_moves)
        if len(first_moves) == 0:
            print("No more moves")
            exit()

        dict = {}
        for i in range(len(first_moves)):
            child = first_moves[i]
            value = _Node.minimax(child.get_board(), 4, -math.inf, math.inf)
            dict[value] = child

        if len(dict.keys()) == 0:
            print("Computer has cornered itself")
            exit()

        move = dict[max(dict)].move

        print(f"move: {move}")

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
        board[new_i][new_j] = Square(Piece(is_king=new_i == queen_row, is_ai=old.is_ai))


class _Node:
    def __init__(self, board, move=None):
        self.board = board
        self.value = None
        self.move = move
        self.parent = None

    def __repr__(self):
        return f"Node {{ board: {self.board}, value: {self.value}, move: {self.move}, parent: {self.parent}}}"

    def get_children(self):
        current_state = deepcopy(self.board)
        available_moves = self.find_available_moves(current_state)
        children_states = []
        queen_row = 7

        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            CheckersSolver._make_a_move(state, old_i, old_j, new_i, new_j, queen_row)
            children_states.append(_Node(state, [old_i, old_j, new_i, new_j]))
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
    def find_available_moves(board: list[list[None | Piece]]):
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if board[m][n] is None:
                    continue

                if board[m][n].is_ai and not board[m][n].is_king:
                    if _Node.check_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if _Node.check_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if _Node.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if _Node.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
                elif board[m][n].is_ai and board[m][n].is_king:
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
        if board[via_i][via_j].is_actual_piece():
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
    def calculate_heuristics(board: list[list[Square]]):
        result = 0
        mine = 0
        opp = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] is None:
                    continue

                if board[i][j].is_ai:
                    mine += 1

                    if not board[i][j].is_king:
                        result += 5
                    if board[i][j].is_king:
                        result += 10

                    if i == 0 or j == 0 or i == 7 or j == 7:
                        result += 7
                    if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
                        continue
                    if (not board[i + 1][j - 1].is_ai()) and not board[i - 1][j + 1].is_actual_piece():
                        result -= 3
                    if (not board[i + 1][j + 1].is_ai()) and not board[i - 1][j - 1].is_actual_piece():
                        result -= 3
                    if (not board[i - 1][j - 1].is_ai()) and board[i - 1][j - 1].is_king() and not board[i + 1][j + 1].is_actual_piece():
                        result -= 3

                    if (not board[i - 1][j + 1].is_ai()) and board[i - 1][j + 1].is_king() and not board[i + 1][j - 1].is_actual_piece():
                        result -= 3
                    if i + 2 > 7 or i - 2 < 0:
                        continue
                    if (not board[i + 1][j - 1].is_ai()) and not board[i + 2][j - 2].is_actual_piece():
                        result += 6
                    if i + 2 > 7 or j + 2 > 7:
                        continue
                    if (not board[i + 1][j + 1].is_ai()) and (not board[i + 1][j + 1].is_king()) and not board[i + 2][j + 2].is_actual_piece():
                        result += 6

                elif not board[i][j].is_ai():
                    opp += 1

        return result + (mine - opp) * 1000

    @staticmethod
    def minimax(board, depth, alpha, beta):
        if depth == 0:
            return _Node.calculate_heuristics(board)
        current_state = _Node(deepcopy(board))

        min_eval = math.inf
        for child in current_state.get_children():
            ev = _Node.minimax(child.get_board(), depth - 1, alpha, beta)
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
                current_board[i][j] = Square(Piece(is_king=False, is_ai=True))
    for i in range(5, 8, 1):
        for j in range(8):
            if (i + j) % 2 == 1:
                current_board[i][j] = Square(Piece(is_king=False, is_ai=False))

    _print_board(current_board)
    move = CheckersSolver(current_board)
    move.calculate_move()
