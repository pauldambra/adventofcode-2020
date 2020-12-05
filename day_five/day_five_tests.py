import unittest
import math


def search_column(search_string, level=0, start=0, end=127):
    print([search_string, level, start, end])
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
        print(f"for {start} and {end} half way step is {diff}")
        if search_key == "F":
            return search_column(search_string, level + 1, start, start + diff)
        elif search_key == "B":
            return search_column(search_string, level + 1, start + diff + 1, end)
        else:
            raise ValueError(f"at level {level} cannot use {search_key}")


class DayThreeTests(unittest.TestCase):

    def test_column_tree_can_search_F(self):
        column_result = search_column("FFFFFFF")
        self.assertEqual(column_result, 0)

    def test_column_tree_can_search_one_B(self):
        column_result = search_column("FFFFFFB")
        self.assertEqual(column_result, 1)

    def test_example_input(self):
        self.assertEqual(search_column("BFFFBBFRRR"), 70)
        self.assertEqual(search_column("FFFBBBFRRR"), 14)
        self.assertEqual(search_column("BBFFBBFRLL"), 102)


if __name__ == '__main__':
    unittest.main()
