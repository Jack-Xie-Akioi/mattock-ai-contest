from dataclasses import dataclass
from random import choice
import time
from typing import Optional
from board import Board, Space, Coordinate
from copy import copy

class aibot:
    count = 0
    def __init__(self, artificial_delay: float = 0, max_depth: int = 1):
        """
        Args:
            artificial_delay: how long to sleep during 'mine'
            max_depth: the maximum depth for iterative deepening
        """
        self.name = f"aibot_{aibot.count}"
        aibot.count += 1
        self.artificial_delay = artificial_delay
        self.max_depth = max_depth  # e.g., search up to depth 4
        self.transposition_table = {}

    def mine(self, board: Board, color: Space) -> Coordinate:
        """Pick a random mineable space to dig out."""
        mineable = board.mineable_by_player(color)
        time.sleep(self.artificial_delay)
        return choice(tuple(mineable))

    def move(self, board: Board, color: Space) -> Optional[tuple[Coordinate, Coordinate]]:
        """
        Perform iterative deepening alpha-beta.
        We search from depth=1 up to self.max_depth, 
        and keep track of the best move found so far.
        """
        best_move = None
        best_score = float('-inf')  # track best score from the AI's perspective

        # Simple iterative deepening from 1 to max_depth
        for depth in range(1, self.max_depth + 1):
            score, move_found = self.minimax_ab(board, color, depth, alpha=-float('inf'), beta=float('inf'), maximizing=True)
            if move_found is not None:
                best_move = move_found
            best_score = score

        return best_move

    def minimax_ab(self, board: Board, color: Space, depth: int,
                   alpha: float, beta: float, maximizing: bool):
        """
        Alpha-Beta with transposition. Storing (board_hash, color, depth, alpha, beta, maximizing)
        as the key in the transposition table. 
        """
        state_key = (hash(board), color, depth, alpha, beta, maximizing)
        if state_key in self.transposition_table:
            return self.transposition_table[state_key]

        # Base case
        if depth == 0:
            val = self.heuristic(board, color)
            self.transposition_table[state_key] = (val, None)
            return val, None

        current_color = color if maximizing else self.opponent(color)
        moves = self.possible_moves(board, current_color)

        # If no moves, treat as leaf node
        if not moves:
            val = self.heuristic(board, color)
            self.transposition_table[state_key] = (val, None)
            return val, None

        best_move = None

        if maximizing:
            value = float('-inf')
            for move in moves:
                new_board = copy(board)
                new_board.apply_move(move, current_color)
                evaluation, _ = self.minimax_ab(new_board, color, depth - 1, alpha, beta, maximizing=False)
                if evaluation > value:
                    value, best_move = evaluation, move
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cutoff
        else:
            value = float('inf')
            for move in moves:
                new_board = copy(board)
                new_board.apply_move(move, current_color)
                evaluation, _ = self.minimax_ab(new_board, color, depth - 1, alpha, beta, maximizing=True)
                if evaluation < value:
                    value, best_move = evaluation, move
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cutoff

        self.transposition_table[state_key] = (value, best_move)
        return value, best_move

    def opponent(self, color: Space) -> Space:
        return Space.RED if color == Space.BLUE else Space.BLUE

    def heuristic(self, board: Board, color: Space) -> float:
        
        opp = self.opponent(color)

        my_mineable = len(board.mineable_by_player(color))
        opp_mineable = len(board.mineable_by_player(opp))
        return (
            (my_mineable - opp_mineable)   # mineable advantage
        )

    def possible_moves(self, board: Board, color: Space) -> list[tuple[Coordinate, Coordinate]]:
        moves = []
        for piece in board.find_all(color):
            for destination in board.walkable_from_coord(piece):
                moves.append((piece, destination))
        return moves
