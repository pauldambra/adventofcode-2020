from __future__ import annotations

import unittest
from dataclasses import dataclass, replace
from typing import Literal
from random import randint

example_input = """
.#.
..#
###
"""

puzzle_input = """
.###.#.#
####.#.#
#.....#.
####....
#...##.#
########
..#####.
######.#
"""


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int
    z: int

    __neighbour_calculations = [
        lambda coord: replace(coord, x=coord.x - 1),
        lambda coord: replace(coord, x=coord.x - 1, y=coord.y - 1),
        lambda coord: replace(coord, y=coord.y - 1),
        lambda coord: replace(coord, x=coord.x + 1, y=coord.y - 1),
        lambda coord: replace(coord, x=coord.x + 1),
        lambda coord: replace(coord, x=coord.x + 1, y=coord.y + 1),
        lambda coord: replace(coord, y=coord.y + 1),
        lambda coord: replace(coord, x=coord.x - 1, y=coord.y + 1),
    ]

    def neighbours(self) -> list[Coordinate]:
        this_plane = [x(self) for x in self.__neighbour_calculations]
        second_plane = [replace(coord, z=coord.z - 1) for coord in this_plane]
        third_plane = [replace(coord, z=coord.z + 1) for coord in this_plane]

        results = []
        results.extend(this_plane)
        results.extend(second_plane)
        results.extend(third_plane)
        results.append(replace(self, z=self.z - 1))
        results.append(replace(self, z=self.z + 1))
        return results


@dataclass
class PocketDimension:
    coordinates: dict[Coordinate, Literal['.', '#']]

    def get(self, coord: Coordinate) -> Literal['.', '#']:
        return self.__get(self.coordinates, coord)

    @staticmethod
    def __get(universe, coord):
        try:
            return universe[coord]
        except KeyError:
            return '.'

    def tick(self):
        pre_tick = self.coordinates.copy()
        candidates = set()

        for c in self.coordinates.keys():
            candidates.add(c)
            for n in c.neighbours():
                candidates.add(n)

        for c in candidates:
            active_neighbours = [
                x for x
                in [self.__get(pre_tick, n) for n in c.neighbours()]
                if x == '#'
            ]
            current_state = self.__get(pre_tick, c)
            if current_state == '#':
                if not 2 <= len(active_neighbours) <= 3:
                    self.coordinates[c] = '.'
            else:
                if len(active_neighbours) == 3:
                    self.coordinates[c] = '#'


    @classmethod
    def parse(cls, starting_state):
        rows = [
            x.strip() for x
            in starting_state.splitlines()
            if len(x.strip()) > 0
        ]
        results: dict[Coordinate, Literal['.', '#']] = {}
        for y, row in enumerate(rows):
            for x, col in enumerate(row):
                results[Coordinate(x, y, 0)] = col

        return PocketDimension(results)

    def draw_plane(self, z: int) -> str:
        plane = [c for c in self.coordinates.keys() if c.z == z]
        min_y = min([c.y for c in plane])
        max_y = max([c.y for c in plane])
        min_x = min([c.x for c in plane])
        max_x = max([c.x for c in plane])
        drawing = ""
        plane_extent = {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y
        }
        print(plane_extent)
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                drawing += self.__get(self.coordinates, Coordinate(x, y, z))
            drawing += "\n"
        return drawing

    def count_active(self):
        return sum(1 for x in self.coordinates.values() if x == '#')


class DaySeventeenTests(unittest.TestCase):

    def test_coord_can_give_neighbours(self):
        """
           left = -1
           up = -1
           right = +1
           down = +1

          -1 0 1
         0 c d e
         1 b a f
         2 i h g
        """
        a = Coordinate(0, 1, 2)
        b = Coordinate(-1, 1, 2)
        c = Coordinate(-1, 0, 2)
        d = Coordinate(0, 0, 2)
        e = Coordinate(1, 0, 2)
        f = Coordinate(1, 1, 2)
        g = Coordinate(1, 2, 2)
        h = Coordinate(0, 2, 2)
        i = Coordinate(-1, 2, 2)
        first_plane = [a, b, c, d, e, f, g, h, i]
        second_plane = [replace(coord, z=1) for coord in first_plane]
        third_plane = [replace(coord, z=3) for coord in first_plane]

        neighbours = a.neighbours()
        expected = [
            b, c, d, e, f, g, h, i
        ]
        expected.extend(second_plane)
        expected.extend(third_plane)
        self.assertCountEqual(
            expected,
            neighbours
        )

    def test_pocket_dimension_starts_with_all_unspecified_coords_as_dot(self):
        pd = PocketDimension({})
        x = randint(0, 999999999)
        y = randint(0, 999999999)
        z = randint(0, 999999999)
        self.assertEqual(
            '.',
            pd.get(Coordinate(x, y, z))
        )

    def test_pocket_dimension_can_start_with_non_dot_coords(self):
        x = randint(0, 999999999)
        y = randint(0, 999999999)
        z = randint(0, 999999999)

        pd = PocketDimension({
            Coordinate(x, y, z): '#'
        })

        self.assertEqual(
            '#',
            pd.get(Coordinate(x, y, z))
        )

    def test_can_parse_string_input_to_starting_coordinates(self):
        pd = PocketDimension.parse(example_input)
        self.assertEqual(
            '#',
            pd.get(Coordinate(1, 0, 0))
        )

    def test_can_tick(self):
        """
        after one tick from example input
        z=-1
        #..
        ..#
        .#.

        z=0
        #.#
        .##
        .#.

        z=1
        #..
        ..#
        .#.
        """
        pd = PocketDimension.parse(example_input)
        pd.tick()
        self.assertEqual('#', pd.get(Coordinate(0, 1, -1)))
        self.assertEqual(11, pd.count_active())

    def test_can_tick_thrice_from_example(self):
        pd = PocketDimension.parse(example_input)
        pd.tick()
        pd.tick()
        pd.tick()
        self.assertEqual(38, pd.count_active())

    def test_can_tick_six_from_example(self):
        pd = PocketDimension.parse(example_input)
        pd.tick()
        pd.tick()
        pd.tick()
        pd.tick()
        pd.tick()
        pd.tick()
        self.assertEqual(112, pd.count_active())

    def test_can_tick_six_for_part_one(self):
        pd = PocketDimension.parse(puzzle_input)
        pd.tick()
        pd.tick()
        pd.tick()
        pd.tick()
        pd.tick()
        pd.tick()
        self.assertEqual(388, pd.count_active())