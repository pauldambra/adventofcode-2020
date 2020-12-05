import unittest
import math
import os
from dataclasses import dataclass


@dataclass
class Searcher:
    level: int
    start: int
    end: int
    a_key: str
    b_key: str

    def search(self, search_string):
        if self.end == self.start:
            return self.start
        else:
            try:
                search_key = search_string[self.level]
            except IndexError:
                raise IndexError(
                    f"""cannot get index {self.evel} from {search_string}.
                     currently start: {self.start} and end: {self.end}""")

            next_level = self.level + 1

            diff = math.floor((self.end - self.start)/2)
            if search_key == self.a_key:
                end = self.start + diff
                next_searcher = Searcher(
                    next_level, self.start, end, self.a_key, self.b_key)

            elif search_key == self.b_key:
                start = self.start + diff + 1
                next_searcher = Searcher(
                    next_level, start, self.end, self.a_key, self.b_key)

            else:
                raise ValueError(
                    f"at level {self.level} cannot use {search_key}")

            return next_searcher.search(search_string)


def get_puzzle_input_path():
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, 'puzzle_input.txt')


column_searcher = Searcher(7, 0, 7, "L", "R")
row_searcher = Searcher(0, 0, 127, "F", "B")


def generate_id(search_string):
    row = row_searcher.search(search_string)
    column = column_searcher.search(search_string)
    id = (row*8)+column
    return id


class DayThreeTests(unittest.TestCase):

    def test_column_tree_can_search_row_F(self):
        column_result = row_searcher.search("FFFFFFF")
        self.assertEqual(column_result, 0)

    def test_column_tree_can_search_row_one_B(self):
        column_result = row_searcher.search("FFFFFFB")
        self.assertEqual(column_result, 1)

    def test_example_input_for_rows(self):
        self.assertEqual(row_searcher.search("BFFFBBFRRR"), 70)
        self.assertEqual(row_searcher.search("FFFBBBFRRR"), 14)
        self.assertEqual(row_searcher.search("BBFFBBFRLL"), 102)

    def test_example_input_for_columns(self):
        self.assertEqual(column_searcher.search("BFFFBBFRRR"), 7)
        self.assertEqual(column_searcher.search("FFFBBBFRRR"), 7)
        self.assertEqual(column_searcher.search("BBFFBBFRLL"), 4)

    def test_example_input_for_unique_id(self):
        self.assertEqual(generate_id("BFFFBBFRRR"), 567)
        self.assertEqual(generate_id("FFFBBBFRRR"), 119)
        self.assertEqual(generate_id("BBFFBBFRLL"), 820)

    def test_puzzle_input_part_one(self):
        with open(get_puzzle_input_path()) as content:
            ss = content.read().split("\n")
        seat_ids = [generate_id(s) for s in ss]
        max_seat_id = max(seat_ids)
        self.assertEqual(max_seat_id, 878)

    def test_puzzle_input_part_two(self):
        with open(get_puzzle_input_path()) as content:
            ss = content.read().split("\n")
        seat_ids = [generate_id(s) for s in ss]
        sorted_seat_ids = sorted(seat_ids)

        candidates = []
        for index in range(1, len(sorted_seat_ids)):
            current = sorted_seat_ids[index]
            previous = sorted_seat_ids[index-1]
            if current - previous != 1:
                candidates.append(current-1)

        my_seat = candidates[0]
        self.assertEqual(my_seat, 504)


if __name__ == '__main__':
    unittest.main()
