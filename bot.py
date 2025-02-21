from dataclasses import dataclass
from random import choice
import time
from typing import Optional
from board import Board, Space, Coordinate 

class aibot:
    count = 0  

    def __init__(self, artificial_delay: float = 0):
        self.name = f"aibot_{aibot.count}"
        aibot.count += 1
        self.artificial_delay = artificial_delay

    def mine(self, board: Board, color: Space) -> Coordinate:
        """Pick a random mineable space to dig out."""
        mineable = board.mineable_by_player(color)
        time.sleep(self.artificial_delay)
        return choice(tuple(mineable))
    
    def move(self, board: Board, color: Space) -> Optional[tuple[Coordinate, Coordinate]]:
        best_move = self.minimax(board, color, depth=3)[1]
        return best_move

    def minimax(self, board: Board, color: Space, depth: int, maximizing=True):
        if depth == 0:
            return self.heuristic(board, color), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in self.possible_moves(board, color):
                new_board = board.copy()
                new_board.apply_move(move, color)
                evaluation = self.minimax(new_board, color, depth - 1, False)[0]
                if evaluation > max_eval:
                    max_eval, best_move = evaluation, move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            opponent_color = Space.RED if color == Space.BLUE else Space.BLUE
            for move in self.possible_moves(board, opponent_color):
                new_board = board.copy()
                new_board.apply_move(move, opponent_color)
                evaluation = self.minimax(new_board, color, depth - 1, True)[0]
                if evaluation < min_eval:
                    min_eval = evaluation
            return min_eval, None

    def heuristic(self, board: Board, color: Space) -> int:
        return len(board.mineable_by_player(color))

    def possible_moves(self, board: Board, color: Space) -> list: 
        moves = []
        for piece in board.find_all(color):
            for move in board.walkable_from_coord(piece):
                moves.append((piece, move))
        return moves
