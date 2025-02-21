from dataclasses import dataclass
from random import choice
import time
from typing import Self
from board import Board, Space, Coordinate 


class aibot:

    def __init__(self, artificial_delay: float = 0):
        self.name = f"rando_{aibot.count}"
        self.artificial_delay = artificial_delay

    def mine(self, board: Board, color: Space) -> Coordinate:
        mineable = board.mineable_by_player(color)
        time.sleep(self.artificial_delay)
        return choice(tuple(mineable))
    
    @dataclass
    class Node[T]:
        board: Board
        value: T 
        children: list[int] | None = None
       
        def __init__(self):
            self.root = None

        def __init__(self):
            self.root = None


        def move(self, board: Board, color: Space) -> tuple[Coordinate, Coordinate] | None:
            #make a tree of all moves
            #call heuristic to find value of boards
            #pick move with minimax value

            self.root.board = board
            pieces = board.find_all(color)
            moves = []
            for piece in pieces:
                moves.append(board.mineable_by_player(piece))
                for move in moves:
                    ...
            if len(moves) == 0:
                return None
            for move in moves: 
                heuristic()
            if 
            return
        
        def heuristic(self, board: Board, color: Space) -> int:
            ...
        
