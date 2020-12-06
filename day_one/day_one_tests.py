from files.reader import get_puzzle_input_path
import unittest
from itertools import combinations
import os


def combination_that_sums_2020(ns, length):
    candidates = list(combinations(ns, length))
    xs = [combination for combination in candidates
          if sum(combination) == 2020]
    return xs[0]


def read_numbers_from_file(f):
    with open(f) as content:
        lines = [line.rstrip() for line in content]
    return [int(s) for s in lines]


class DayOneTests(unittest.TestCase):

    def test_list_combinations_part_one(self):
        expenses = [1721,
                    979,
                    366,
                    299,
                    675,
                    1456]

        candidate = combination_that_sums_2020(expenses, 2)

        self.assertEqual(candidate[0] * candidate[1], 514579)

    def test_puzzle_input_combinations_part_one(self):
        expenses = read_numbers_from_file(
            get_puzzle_input_path(os.path.dirname(__file__)))

        candidate = combination_that_sums_2020(expenses, 2)

        self.assertEqual(candidate[0] * candidate[1], 55776)

    def test_list_combinations_part_two(self):
        expenses = [1721,
                    979,
                    366,
                    299,
                    675,
                    1456]

        candidate = combination_that_sums_2020(expenses, 3)

        self.assertEqual(
            candidate[0] * candidate[1] * candidate[2],
            241861950)

    def test_puzzle_input_combinations_part_two(self):
        expenses = read_numbers_from_file(
            get_puzzle_input_path(os.path.dirname(__file__)))

        candidate = combination_that_sums_2020(expenses, 3)

        self.assertEqual(
            candidate[0] * candidate[1] * candidate[2], 223162626)


if __name__ == '__main__':
    unittest.main()
