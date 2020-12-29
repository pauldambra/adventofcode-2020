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

    neighbour_calculations = [
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
        raise NotImplementedError("Must implemented in a subclass")


@dataclass(frozen=True)
class FourDimensionalCoordinate(Coordinate):
    x: int
    y: int
    z: int
    w: int

    def neighbours(self) -> list[ThreeDimensionalCoordinate]:
        this_plane = [x(self) for x in self.neighbour_calculations]
        this_plane_w1 = [replace(coord, w=coord.w - 1) for coord in this_plane]
        this_plane_w2 = [replace(coord, w=coord.w + 1) for coord in this_plane]
        second_plane = [replace(coord, z=coord.z - 1) for coord in this_plane]
        second_plane_w1 = [replace(coord, w=coord.w - 1) for coord in second_plane]
        second_plane_w2 = [replace(coord, w=coord.w + 1) for coord in second_plane]
        third_plane = [replace(coord, z=coord.z + 1) for coord in this_plane]
        third_plane_w1 = [replace(coord, w=coord.w - 1) for coord in third_plane]
        third_plane_w2 = [replace(coord, w=coord.w + 1) for coord in third_plane]

        results = []
        results.extend(this_plane)
        results.extend(this_plane_w1)
        results.extend(this_plane_w2)
        results.extend(second_plane)
        results.extend(second_plane_w1)
        results.extend(second_plane_w2)
        results.extend(third_plane)
        results.extend(third_plane_w1)
        results.extend(third_plane_w2)
        results.append(replace(self, w=self.w - 1))
        results.append(replace(self, w=self.w + 1))
        results.append(replace(self, z=self.z - 1))
        results.append(replace(self, z=self.z - 1, w=self.w - 1))
        results.append(replace(self, z=self.z - 1, w=self.w + 1))
        results.append(replace(self, z=self.z + 1))
        results.append(replace(self, z=self.z + 1, w=self.w - 1))
        results.append(replace(self, z=self.z + 1, w=self.w + 1))
        return results


@dataclass(frozen=True)
class ThreeDimensionalCoordinate(Coordinate):
    x: int
    y: int
    z: int

    def neighbours(self) -> list[ThreeDimensionalCoordinate]:
        this_plane = [x(self) for x in self.neighbour_calculations]
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
    coordinates: dict[ThreeDimensionalCoordinate, Literal['.', '#']]

    def get(self, coord: ThreeDimensionalCoordinate) -> Literal['.', '#']:
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
        results: dict[ThreeDimensionalCoordinate, Literal['.', '#']] = {}
        for y, row in enumerate(rows):
            for x, col in enumerate(row):
                results[ThreeDimensionalCoordinate(x, y, 0)] = col

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
                drawing += self.__get(self.coordinates, ThreeDimensionalCoordinate(x, y, z))
            drawing += "\n"
        return drawing

    def count_active(self):
        return sum(1 for x in self.coordinates.values() if x == '#')

    @classmethod
    def parse_4d(cls, starting_state: str) -> PocketDimension:
        rows = [
            x.strip() for x
            in starting_state.splitlines()
            if len(x.strip()) > 0
        ]
        results: dict[FourDimensionalCoordinate, Literal['.', '#']] = {}
        for y, row in enumerate(rows):
            for x, col in enumerate(row):
                results[FourDimensionalCoordinate(x, y, 0, 0)] = col

        return PocketDimension(results)


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
        a = ThreeDimensionalCoordinate(0, 1, 2)
        b = ThreeDimensionalCoordinate(-1, 1, 2)
        c = ThreeDimensionalCoordinate(-1, 0, 2)
        d = ThreeDimensionalCoordinate(0, 0, 2)
        e = ThreeDimensionalCoordinate(1, 0, 2)
        f = ThreeDimensionalCoordinate(1, 1, 2)
        g = ThreeDimensionalCoordinate(1, 2, 2)
        h = ThreeDimensionalCoordinate(0, 2, 2)
        i = ThreeDimensionalCoordinate(-1, 2, 2)
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
            pd.get(ThreeDimensionalCoordinate(x, y, z))
        )

    def test_pocket_dimension_can_start_with_non_dot_coords(self):
        x = randint(0, 999999999)
        y = randint(0, 999999999)
        z = randint(0, 999999999)

        pd = PocketDimension({
            ThreeDimensionalCoordinate(x, y, z): '#'
        })

        self.assertEqual(
            '#',
            pd.get(ThreeDimensionalCoordinate(x, y, z))
        )

    def test_can_parse_string_input_to_starting_coordinates(self):
        pd = PocketDimension.parse(example_input)
        self.assertEqual(
            '#',
            pd.get(ThreeDimensionalCoordinate(1, 0, 0))
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
        self.assertEqual('#', pd.get(ThreeDimensionalCoordinate(0, 1, -1)))
        self.assertEqual(11, pd.count_active())

    def test_can_tick_thrice_from_example(self):
        pd = PocketDimension.parse(example_input)
        for _ in range(0, 3):
            pd.tick()

        self.assertEqual(38, pd.count_active())

    def test_can_tick_six_from_example(self):
        pd = PocketDimension.parse(example_input)
        for _ in range(0, 6):
            pd.tick()

        self.assertEqual(112, pd.count_active())

    def test_can_tick_six_for_part_one(self):
        pd = PocketDimension.parse(puzzle_input)
        for _ in range(0, 6):
            pd.tick()

        self.assertEqual(388, pd.count_active())

    def test_can_get_neighbours_in_4d(self):
        c = FourDimensionalCoordinate(0, 0, 0, 0)
        self.assertEqual(
            80,
            len(c.neighbours())
        )

    def test_can_parse_in_4d(self):
        pd = PocketDimension.parse_4d(example_input)
        self.assertEqual(
            '#',
            pd.get(FourDimensionalCoordinate(1, 0, 0, 0))
        )

    def test_six_ticks_for_part_two_example(self):
        pd = PocketDimension.parse_4d(example_input)
        for _ in range(0, 6):
            pd.tick()

        self.assertEqual(
            848,
            pd.count_active()
        )

    def test_six_ticks_for_part_two(self):
        pd = PocketDimension.parse_4d(puzzle_input)
        for _ in range(0, 6):
            pd.tick()

        self.assertEqual(
            2280,
            pd.count_active()
        )
