import unittest
import math
import os


def get_puzzle_input_path():
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, 'puzzle_input.txt')


def search_column(search_string, level=7, start=0, end=7):
    try:
        search_key = search_string[level]
    except IndexError:
        raise IndexError(f"cannot get index {level} from {search_string}")

    if end - start == 1:
        if search_key == "L":
            return start
        elif search_key == "R":
            return end
        else:
            raise ValueError(f"at level {level} cannot use {search_key}")
    else:
        diff = math.floor((end - start)/2)
        if search_key == "L":
            return search_column(search_string, level + 1, start, start + diff)
        elif search_key == "R":
            return search_column(search_string, level + 1, start + diff + 1, end)
        else:
            raise ValueError(f"at level {level} cannot use {search_key}")


def search_row(search_string, level=0, start=0, end=127):
    try:
        search_key = search_string[level]
    except IndexError:
        raise IndexError(f"cannot get index {level} from {search_string}")

    if end - start == 1:
        if search_key == "F":
            return start
        elif search_key == "B":
            return end
        else:
            raise ValueError(f"at level {level} cannot use {search_key}")
    else:
        diff = math.floor((end - start)/2)
        if search_key == "F":
            return search_row(search_string, level + 1, start, start + diff)
        elif search_key == "B":
            return search_row(search_string, level + 1, start + diff + 1, end)
        else:
            raise ValueError(f"at level {level} cannot use {search_key}")


def generate_id(search_string):
    row = search_row(search_string)
    column = search_column(search_string)
    id = (row*8)+column
    return id


class DayThreeTests(unittest.TestCase):

    def test_column_tree_can_search_row_F(self):
        column_result = search_row("FFFFFFF")
        self.assertEqual(column_result, 0)

    def test_column_tree_can_search_row_one_B(self):
        column_result = search_row("FFFFFFB")
        self.assertEqual(column_result, 1)

    def test_example_input_for_rows(self):
        self.assertEqual(search_row("BFFFBBFRRR"), 70)
        self.assertEqual(search_row("FFFBBBFRRR"), 14)
        self.assertEqual(search_row("BBFFBBFRLL"), 102)

    def test_example_input_for_columns(self):
        self.assertEqual(search_column("BFFFBBFRRR"), 7)
        self.assertEqual(search_column("FFFBBBFRRR"), 7)
        self.assertEqual(search_column("BBFFBBFRLL"), 4)

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


if __name__ == '__main__':
    unittest.main()
