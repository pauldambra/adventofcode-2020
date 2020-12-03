import unittest
from dataclasses import dataclass


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
        return CoordinateLookup(True, x, y, map_rows[y][wrapped_index])


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


if __name__ == '__main__':
    unittest.main()
