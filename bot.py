from dataclasses import dataclass
from random import choice
import time
from typing import Self
from board import Board, Space, Coordinate 


class aibot:

    count = 0

    def __init__(self, artificial_delay: float = 0):
        self.name = f"rando_{aibot.count}"
        self.artificial_delay = artificial_delay
        aibot.count += 1

    def mine(self, board: Board, color: Space) -> Coordinate:
        mineable = board.mineable_by_player(color)
        time.sleep(self.artificial_delay)
        return choice(tuple(mineable))
    
    @dataclass
    class Node[T]:
        coordinate: tuple[Coordinate, Coordinate]
        value: T 
        children: list[int] | None = None
       
        def __init__(self):
            self.root = None


        def move(self, board: Board, color: Space) -> tuple[Coordinate, Coordinate] | None:
            #make a tree of all moves
            #call heuristic to find value of boards
            #pick move with minimax value

            pieces = board.find_all(color)
            moves = []
            for piece in pieces:
                moves.append(board.walkable_from_coord(piece))
            if len(moves) == 0:
                return None
            
            return None
        
        def heuristic(self, board: Board, color: Space) -> int:
            ...
        
