import os
import unittest
import itertools
from files.reader import get_puzzle_input_path


def window(seq, n=2):
    """from https://stackoverflow.com/a/6822773/222163
    Returns a sliding window (of width n) over data from the iterable
       s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
       """
    it = iter(seq)
    result = tuple(itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def get_valid_numbers_from_preamble(preamble):
    result = set([
        x + y for (x, y)
        in itertools.permutations(preamble, 2)
    ])
    return result


def seek_first_invalid_number(s: str, preamble_length: int):
    input = [int(line.strip())
             for line in s.splitlines()
             if line and len(line.strip()) > 0]
    windows = window(input, preamble_length+1)

    for w in windows:
        preamble = w[:preamble_length]
        value = w[preamble_length]
        valid_numbers = get_valid_numbers_from_preamble(preamble)
        if value not in valid_numbers:
            return value

    # x = [(w[:preamble_length-1], w[preamble_length-1]) for w in windows]
    # y = [(get_valid_numbers_from_preamble(preamble), value)
    #      for (preamble, value)
    #      in x]
    # return [value for (valid_numbers, value)
    #         in y if value not in valid_numbers]


def find_encryption_weakness(i: str, invalid_number: int):
    ns = [int(s.strip())
          for s in i.splitlines() if s and len(s.strip()) > 0]

    match = ()
    for i in range(2, len(ns)):
        for x in window(ns, i):
            if sum(x) == invalid_number:
                match = x

    smallest = min(match)
    largest = max(match)
    return smallest + largest


class DayNineTests(unittest.TestCase):

    def test_can_window(self):
        ss = [1, 2, 3, 4, 5, 6, 7, 8]
        windows = list(window(ss, 3))
        self.assertEqual(
            windows,
            [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7), (6, 7, 8)])

    def test_can_get_sum_of_permutations(self):
        ss = (1, 2, 3, 4, 5)
        valid_numbers = get_valid_numbers_from_preamble(ss)
        self.assertEqual(valid_numbers, {3, 4, 5, 6, 7, 8, 9})

    def test_one_through_25(self):
        numbers = list(range(1, 26))
        valid_numbers = get_valid_numbers_from_preamble(numbers)
        self.assertIn(26, valid_numbers)
        self.assertIn(49, valid_numbers)
        self.assertNotIn(100, valid_numbers)
        self.assertNotIn(50, valid_numbers)

    def test_example_input_part_one(self):
        z = seek_first_invalid_number("""
        35
        20
        15
        25
        47
        40
        62
        55
        65
        95
        102
        117
        150
        182
        127
        219
        299
        277
        309
        576
        """, 6)

        self.assertEqual(z, 127)

    def test_part_one(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            content = content.read()

        z = seek_first_invalid_number(content, 25)
        print(z)
        self.assertEqual(z, 375054920)

    def test_find_encryption_weakness_in_example_input(self):
        i = """35
            20
            15
            25
            47
            40
            62
            55
            65
            95
            102
            117
            150
            182
            127
            219
            299
            277
            309
            576"""

        weakness = find_encryption_weakness(i, 127)

        self.assertEqual(weakness, 62)

    def test_encryption_weakness_with_puzzle_input(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            puzzle_input = content.read()
        weakness = find_encryption_weakness(puzzle_input, 375054920)

        self.assertEqual(weakness, 54142584)
