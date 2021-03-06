import os
from files.reader import get_puzzle_input_path, split_groups
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


def prepare_groups_for_part_one(groups):
    flattened_answers = [" ".join(x).strip() for x in groups]
    return [prepare_group(s) for s in flattened_answers]


def any_yes(groups):
    prepared_answers = prepare_groups_for_part_one(groups)
    return [sorted(list(set(g))) for g in prepared_answers]


def keep_shared(peoples_answers):
    num_of_people = len(peoples_answers)
    seen_answers = {}
    for answers in peoples_answers:
        for answer in answers:
            if answer not in seen_answers:
                seen_answers[answer] = 0

            seen_answers[answer] = seen_answers[answer] + 1

    everyone_answered = [
        k for (k, _) in seen_answers.items()
        if seen_answers[k] == num_of_people
    ]

    return everyone_answered


def everyone_yes(groups):
    unique_per_person = [[sorted(list(set(x))) for x in groups_answers]
                         for groups_answers in groups]
    everyone_said_yes = [keep_shared(answers) for answers in unique_per_person]
    return everyone_said_yes


def sum_counts(groups):
    return sum([len(x) for x in groups])


class DaySixTests(unittest.TestCase):

    def test_can_read_groups(self):
        groups = split_groups(example_input)
        self.assertEqual(groups, [
            ["abc"],
            ["a", "b", "c"],
            ["ab", "ac"],
            ["a", "a", "a", "a"],
            ["b"]
        ])

    def test_can_any_yes_groups(self):
        groups = [
            ["abc"],
            ["a", "b", "c"],
            ["ab", "ac"],
            ["a", "a", "a", "a"],
            ["b"]
        ]
        uniquified = any_yes(groups)
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
        sum_of_counts = sum_counts(any_yes(split_groups(ss)))
        self.assertEqual(sum_of_counts, 6686)

    def test_sum_part_two_counts_for_example_input(self):
        sum_of_counts = sum_counts(everyone_yes(split_groups(example_input)))
        self.assertEqual(sum_of_counts, 6)

    def test_sum_counts_for_puzzle_input_part_two(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            ss = content.read()
        sum_of_counts = sum_counts(everyone_yes(split_groups(ss)))
        self.assertEqual(sum_of_counts, 3476)
