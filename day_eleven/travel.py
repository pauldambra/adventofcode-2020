from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Callable


@dataclass
class Coordinate:
    x: int
    y: int


move: dict[str, Coordinate] = {
    'west': lambda coord: Coordinate(coord.x - 1, coord.y),
    'north west': lambda coord: Coordinate(coord.x - 1, coord.y - 1),
    'north': lambda coord: Coordinate(coord.x, coord.y - 1),
    'north east': lambda coord: Coordinate(coord.x + 1, coord.y - 1),
    'east': lambda coord: Coordinate(coord.x + 1, coord.y),
    'south east': lambda coord: Coordinate(coord.x + 1, coord.y + 1),
    'south': lambda coord: Coordinate(coord.x, coord.y + 1),
    'south west': lambda coord: Coordinate(coord.x - 1, coord.y + 1),
}


class Travel(ABC):

    @abstractmethod
    def get_seeker(grid: Grid, x: int, y: int) -> Callable[[str], str]:
        pass

    @classmethod
    def get_adjacent_seats_using(class_, seek):
        return [c for c in [
            seek("west"),
            seek("north west"),
            seek("north"),
            seek("north east"),
            seek("east"),
            seek("south east"),
            seek("south"),
            seek("south west")
        ] if c]


class LineOfSightAdjacentSeats(Travel):
    def get_seeker(grid: Grid, x: int, y: int):
        def seeker(direction: str) -> str:
            next_coords: Coordinate = move[direction](Coordinate(x, y))

            while (next_result := grid.get_by_coordinate(next_coords)) == '.':
                next_coords = move[direction](next_coords)

            return next_result

        return seeker

    @classmethod
    def find(class_, grid: Grid, x: int, y: int) -> list[int]:
        seek = class_.get_seeker(grid, x, y)
        return class_.get_adjacent_seats_using(seek)


class DirectlyAdjacentSeats(Travel):
    def get_seeker(grid: Grid, x: int, y: int):
        def seeker(direction: str) -> str:
            next_coords: Coordinate = move[direction](Coordinate(x, y))
            return grid.get_by_coordinate(next_coords)

        return seeker

    @classmethod
    def find(class_, grid: Grid, x: int, y: int) -> list[int]:
        seek = class_.get_seeker(grid, x, y)
        return class_.get_adjacent_seats_using(seek)


class Grid:

    def __init__(self,
                 grid_description: str,
                 adjacent_seat_finder=DirectlyAdjacentSeats,
                 tolerance=4) -> None:
        self.adjacent_seat_finder = adjacent_seat_finder
        self.tolerance = tolerance
        try:
            self.grid_description = grid_description.strip().replace(" ", "")
        except AttributeError as ae:
            print(f"could not strip description: {grid_description}")
            raise ae

        self.rows = [line.strip().replace(" ", "") for line
                     in grid_description.splitlines()
                     if line and len(line.strip()) > 0]
        self.height = len(self.rows)
        self.width = len(self.rows[0])

    def get_by_coordinate(self, coord: Coordinate) -> str:
        return self.get(coord.x, coord.y)

    def get(self, x: int, y: int) -> str:
        if x < 0 or y < 0:
            return None

        if x >= self.width or y >= self.height:
            return None

        row = self.rows[y]
        return row[x]

    def adjacent_to(self, x: int, y: int) -> list[str]:
        return self.adjacent_seat_finder.find(self, x, y)

    def tick(self):
        copied = list(map(list, self.rows))

        for x in range(0, self.width):
            for y in range(0, self.height):
                seat = self.get(x, y)
                adjacents = self.adjacent_to(x, y)
                if seat == 'L':
                    if not any(x == '#' for x in adjacents):
                        copied[y][x] = '#'
                elif seat == '#':
                    if adjacents.count('#') >= self.tolerance:
                        copied[y][x] = 'L'

        described_rows = [''.join(x) for x in copied]
        description = '\n'.join(described_rows)
        return Grid(description, self.adjacent_seat_finder, self.tolerance)

    def occupied_seats(self) -> int:
        return self.grid_description.count('#')

    def __hash__(self):
        return self.grid_description.__hash__()

    def __eq__(self, o: object) -> bool:
        return self.grid_description == o.grid_description

    def __repr__(self) -> str:
        return self.grid_description
