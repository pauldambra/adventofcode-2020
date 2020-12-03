import unittest
from dataclasses import dataclass
from functools import reduce
import operator


@dataclass
class CoordinateLookup:
    within_map: bool
    x: int
    y: int
    encountered: str


def read(x, y, map_rows):
    if y >= len(map_rows):
        return CoordinateLookup(False, x, y, None)
    else:
        wrapped_index = x % len(map_rows[0])
        map_row = map_rows[y]
        return CoordinateLookup(True, x, y, map_row[wrapped_index])


def walk_the_map(map, x_step=3, y_step=1):
    encountered = []
    still_within_map = True
    x = 0
    y = 0
    while still_within_map:
        x += x_step
        y += y_step
        next = read(x, y, map)
        if (next.within_map):
            encountered.append(next)
        still_within_map = next.within_map

    return encountered


def count_trees_encountered(map, x_step, y_step):
    map_encounters = walk_the_map(map, x_step, y_step)
    return sum(1 for x in map_encounters if x.encountered == "#")


class DayThreeTests(unittest.TestCase):

    def test_get_coordinates_within_map_row(self):
        map = "#.#.#...........#.....#.#....##".split("\n")
        one = read(0, 0, map)
        two = read(1, 0, map)

        self.assertEqual(one.encountered, '#')
        self.assertEqual(two.encountered, '.')

    def test_get_coordinates_after_map_row_wrapped(self):
        map = "#.#.#...........#.....#.#....##".split("\n")
        one = read(len(map[0]), 0, map)

        self.assertEqual(one.encountered, '#')

    def test_get_coordinates_from_row_one(self):
        map = "#.#.#.\n.#.#.#".split("\n")
        one = read(0, 1, map)

        self.assertEqual(one.encountered, '.')

    def test_get_wrapped_coordinates_from_row_one(self):
        map = "#.#.#.\n.#.#.#".split("\n")
        one = read(7, 1, map)

        self.assertEqual(one.encountered, '#')

    def test_never_outside_of_map_for_x_row(self):
        map = "#.#.#.\n.#.#.#".split("\n")
        results = [read(i, 0, map) for i in range(0, 100)]
        for x in results:
            self.assertTrue(x.within_map)

    def test_can_be_outside_of_map_for_y_row(self):
        map = "#.#.#.\n.#.#.#".split("\n")
        result = read(0, len(map), map)
        self.assertFalse(result.within_map)

    def test_can_walk_the_map(self):
        map = ".......\n...x...\n......x\n..x...\n".strip().split("\n")
        map_encounters = walk_the_map(map)

        [self.assertEqual(s.encountered, 'x') for s in map_encounters]

    def test_example_input(self):
        map = ["..##.......",
               "#...#...#..",
               ".#....#..#.",
               "..#.#...#.#",
               ".#...##..#.",
               "..#.##.....",
               ".#.#.#....#",
               ".#........#",
               "#.##...#...",
               "#...##....#",
               ".#..#...#.#"]
        map_encounters = walk_the_map(map)
        self.assertEqual(
            sum(1 for x in map_encounters if x.encountered == "#"),
            7)

    def test_puzzle_input(self):
        with open('puzzle_input.txt') as content:
            map = [line.rstrip() for line in content]
        map_encounters = walk_the_map(map)
        trees_encountered = sum(
            1 for x in map_encounters if x.encountered == "#")
        self.assertEqual(
            trees_encountered,
            292)

    def test_example_part_two(self):
        map = ["..##.......",
               "#...#...#..",
               ".#....#..#.",
               "..#.#...#.#",
               ".#...##..#.",
               "..#.##.....",
               ".#.#.#....#",
               ".#........#",
               "#.##...#...",
               "#...##....#",
               ".#..#...#.#"]
        different_slopes = [
            count_trees_encountered(map, 1, 1),
            count_trees_encountered(map, 3, 1),
            count_trees_encountered(map, 5, 1),
            count_trees_encountered(map, 7, 1),
            count_trees_encountered(map, 1, 2),
        ]
        self.assertEqual(
            different_slopes,
            [2, 7, 3, 4, 2])
        self.assertEqual(reduce(operator.mul, different_slopes), 336)

    def test_puzzle_input_part_two(self):
        with open('puzzle_input.txt') as content:
            map = [line.rstrip() for line in content]
        different_slopes = [
            count_trees_encountered(map, 1, 1),
            count_trees_encountered(map, 3, 1),
            count_trees_encountered(map, 5, 1),
            count_trees_encountered(map, 7, 1),
            count_trees_encountered(map, 1, 2),
        ]

        self.assertEqual(reduce(operator.mul, different_slopes), 9354744432)


if __name__ == '__main__':
    unittest.main()
