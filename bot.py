from random import choice
import time
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

    def move(self, board: Board, color: Space) -> tuple[Coordinate, Coordinate] | None:
        pieces = board.find_all(color)
        start = choice(tuple(pieces))
        ends = board.walkable_from_coord(start)
        if len(ends) == 0:
            return None
        return start, choice(tuple(ends))
    
    def heuristic(self, board: Board, color: Space) -> int:
        ...
    
