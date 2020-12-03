import unittest


def read(x, y, map_rows):
    wrapped_index = x % len(map_rows[0])
    return map_rows[y][wrapped_index]


class DayThreeTests(unittest.TestCase):

    def test_get_coordinates_within_map_row(self):
        map = "#.#.#...........#.....#.#....##".split("\n")
        one = read(0, 0, map)
        two = read(1, 0, map)

        self.assertEqual(one, '#')
        self.assertEqual(two, '.')

    def test_get_coordinates_after_map_row_wrapped(self):
        map = "#.#.#...........#.....#.#....##".split("\n")
        one = read(len(map[0]), 0, map)

        self.assertEqual(one, '#')

    def test_get_coordinates_from_row_one(self):
        map = "#.#.#.\n.#.#.#".split("\n")
        one = read(0, 1, map)

        self.assertEqual(one, '.')

    def test_get_wrapped_coordinates_from_row_one(self):
        map = "#.#.#.\n.#.#.#".split("\n")
        one = read(7, 1, map)

        self.assertEqual(one, '#')


if __name__ == '__main__':
    unittest.main()
