from dataclasses import dataclass
from random import choice
import time
from typing import Optional
from board import Board, Space, Coordinate
from copy import copy

class aibot_1:
    count = 0
    def __init__(self):
        
        self.name = f"aibot_{aibot_1.count}"
        aibot_1.count += 1
        self.max_depth = 2 # 2 is like the max for the aibot to not run out of time
        
        self.transposition_table = {}

    def mine(self, board: Board, color: Space) -> Coordinate:
        
        mineable = board.mineable_by_player(color)
        return choice(tuple(mineable))
    
    def apply_move(self, board: Board, move: tuple[Coordinate, Coordinate], color: Space):
        start, end = move
        board[start] = Space.EMPTY
        board[end] = color

    def move(self, board: Board, color: Space) -> Optional[tuple[Coordinate, Coordinate]]:
        best_move = None
        
        for depth in range(1, self.max_depth + 1):
            score, move_found = self.minimax_ab(board, color, depth, alpha=-float('inf'), beta=float('inf'), maximizing=True) #Start from here
            if move_found is not None:
                best_move = move_found

        return best_move

    def minimax_ab(self, board: Board, color: Space, depth: int, alpha: float, beta: float, maximizing: bool, move: bool):
        
        state_key = (board, color, depth, alpha, beta, maximizing)
        if state_key in self.transposition_table:
            return self.transposition_table[state_key]

        if depth == 0: #Base Case
            val = self.heuristic(board, color)
            self.transposition_table[state_key] = (val, None)
            return val, None

        current_color = color if maximizing else self.opponent(color)
        moves = self.possible_moves(board, current_color)
        mines = self.possible_mines(board, current_color)

        if move:
            if not moves:
                val = self.heuristic(board, color)
                self.transposition_table[state_key] = (val, None)
                return val, None
        else: 
            if not mines:
                val = self.heuristic(board, color)
                self.transposition_table[state_key] = (val, None)
                return val, None

        best_move = None

        if maximizing: #Max
            value = float('-inf')
            for move in moves:
                new_board = copy(board)
                self.apply_move(new_board, move, current_color)
                evaluation, _ = self.minimax_ab(new_board, color, depth - 1, alpha, beta, maximizing=False) 
                
                if evaluation > value: #Comparing Scores from heuristic
                    value, best_move = evaluation, move
                    
                alpha = max(alpha, value)
                if beta <= alpha: #Cut time
                    break 
        else: #Min
            value = float('inf')
            for move in moves:
                new_board = copy(board)
                self.apply_move(new_board, move, current_color)
                evaluation, _ = self.minimax_ab(new_board, color, depth - 1, alpha, beta, maximizing=True)
                
                if evaluation < value: #Comparing Scores from heuristic
                    value, best_move = evaluation, move
                    
                beta = min(beta, value)
                if beta <= alpha: #Cut time
                    break 

        self.transposition_table[state_key] = (value, best_move)
        return value, best_move

    def opponent(self, color: Space) -> Space:
        return Space.RED if color == Space.BLUE else Space.BLUE

    def heuristic(self, board: Board, color: Space) -> float:
        
        opp = self.opponent(color)

        my_mineable = len(board.mineable_by_player(color))
        opp_mineable = len(board.mineable_by_player(opp))
        my_walkable = len(board.walkable_by_player(color))
        opp_walkable = len(board.walkable_by_player(opp))
    
        return 4*(my_mineable - opp_mineable)+1*(my_walkable - opp_walkable) #Heuristic 3:1 ratio between mineable and walkable

    def possible_moves(self, board: Board, color: Space) -> list[tuple[Coordinate, Coordinate]]:
        moves = []
        for piece in board.find_all(color):
            for destination in board.walkable_from_coord(piece):
                moves.append((piece, destination))
        return moves
    
    def possible_mines(self, board: Board, color: Space) -> list[tuple[Coordinate, Coordinate]]:
        mines = []
        for piece in board.find_all(color):
            for destination in board.mineable_by_player(piece):
                mines.append((piece, destination))
        return mines