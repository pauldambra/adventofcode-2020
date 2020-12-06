import os
from files.reader import get_puzzle_input_path, split_grouped_input
import unittest

example_input = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""


def prepare_group(s: str):
    return list(s.replace(" ", ""))


def parse_groups(puzzle_input: str):
    return [prepare_group(s) for s
            in split_grouped_input(puzzle_input)]


def uniquify(groups):
    return [sorted(list(set(g))) for g in groups]


def sum_counts(groups):
    return sum([len(x) for x in groups])


class DaySixTests(unittest.TestCase):

    def test_can_read_groups(self):
        groups = parse_groups(example_input)
        self.assertEqual(groups, [
            ["a", "b", "c"],
            ["a", "b", "c"],
            ["a", "b", "a", "c"],
            ["a", "a", "a", "a"],
            ["b"]
        ])

    def test_can_uniquify_groups(self):
        groups = [
            ["a", "b", "c"],
            ["a", "b", "c"],
            ["a", "b", "a", "c"],
            ["a", "a", "a", "a"],
            ["b"]
        ]
        uniquified = uniquify(groups)
        self.assertEqual(uniquified, [
            ["a", "b", "c"],
            ["a", "b", "c"],
            ["a", "b", "c"],
            ["a"],
            ["b"]
        ])

    def test_can_count_and_sum_uniquified_groups(self):
        uniquified = [
            ["a", "b", "c"],
            ["a", "b", "c"],
            ["a", "b", "c"],
            ["a"],
            ["b"]
        ]
        sum_of_counts = sum_counts(uniquified)
        self.assertEqual(sum_of_counts, 11)

    def test_sum_counts_for_puzzle_input(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            ss = content.read()
        sum_of_counts = sum_counts(uniquify(parse_groups(ss)))
        self.assertEqual(sum_of_counts, 6686)
