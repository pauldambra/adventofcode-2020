from __future__ import annotations
from files.reader import get_puzzle_input_path
import unittest
from dataclasses import dataclass
from parameterized import parameterized
from random import randint
import re
import os

example_input = """
        class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""


class Predicate:
    pass


@dataclass
class RangePredicate(Predicate):
    low: int
    high: int

    def matches(self, candidate: int) -> bool:
        return self.low <= candidate <= self.high


@dataclass
class Specification:
    def matches(self, _: int) -> bool:
        raise NotImplementedError("subclasses must implement this")


@dataclass
class TwoRangesSpecification(Specification):
    name: str
    first_range: RangePredicate
    second_range: RangePredicate

    def matches(self, candidate: int) -> bool:
        return (
            self.first_range.matches(candidate) or
            self.second_range.matches(candidate)
        )

    @classmethod
    def parse(class_, input: str) -> TwoRangesSpecification:
        """
        input looks like this class: 1-3 or 5-7
        """
        matches = re.search("(.*): (\d+)-(\d+) or (\d+)-(\d+)", input)

        return TwoRangesSpecification(
            matches.group(1),
            RangePredicate(int(matches.group(2)), int(matches.group(3))),
            RangePredicate(int(matches.group(4)), int(matches.group(5)))
        )


@dataclass
class All(Specification):
    specs: list[Specification]

    def matches(self, candidate: int) -> bool:
        return all(spec.matches(candidate) for spec in self.specs)


@dataclass
class Any(Specification):
    specs: list[Specification]

    def matches(self, candidate: int) -> bool:
        return any(spec.matches(candidate) for spec in self.specs)


@dataclass
class DefaultSpecification(Specification):
    def matches(self, _: int) -> bool:
        return False


def parse_input(i: str):
    specs = []
    nearby = []
    reading_rules = True
    reading_nearby = False
    for line in [cs.strip() for cs in i.splitlines() if len(cs.strip()) > 0]:
        if (line == "your ticket:"):
            reading_rules = False

        if reading_rules:
            specs.append(TwoRangesSpecification.parse(line))

        if reading_nearby:
            nearby.append([int(x) for x in line.split(',')])

        if (line == "nearby tickets:"):
            reading_nearby = True

    return {
        'rules': specs,
        'nearby_tickets': nearby
    }


def check_ticket(values):
    invalid_ticket_fields = []
    spec_chain = Any(values['rules'])
    for ticket in values['nearby_tickets']:
        invalid_ticket_fields.append([
            field for field
            in ticket
            if not spec_chain.matches(field)
        ])

    return invalid_ticket_fields


def flatten(t): return [item for sublist in t for item in sublist]


class DaySixteenTests(unittest.TestCase):

    @parameterized.expand([
        [0, False], [1, True], [4, True], [6, False], [8, True], [11, False]
    ])
    def test_specification_pattern(self, candidate, expected):
        specification = TwoRangesSpecification(
            "name",
            RangePredicate(1, 5),
            RangePredicate(7, 9)
        )
        self.assertEqual(
            expected, specification.matches(candidate)
        )

    def test_default_specification(self):
        specification = DefaultSpecification()
        self.assertFalse(specification.matches(randint(0, 999999999)))

    @parameterized.expand([
        [0, False], [1, False], [2, True], [6, False], [8, True], [11, False]
    ])
    def test_chaining_specifications(self, candidate, expected):
        first = TwoRangesSpecification("first",
                                       RangePredicate(1, 5),
                                       RangePredicate(6, 10))
        second = TwoRangesSpecification("second",
                                        RangePredicate(2, 3),
                                        RangePredicate(7, 9))
        final = DefaultSpecification()
        chain = All([first, second, final])
        self.assertEqual(False, chain.matches(candidate))

    @parameterized.expand([
        [0, False],
        [1, True],
        [2, True],
        [6, False],
        [8, True],
        [10, True],
        [11, False]
    ])
    def test_chaining_specifications_for_any_match(self, candidate, expected):
        first = TwoRangesSpecification("first",
                                       RangePredicate(1, 5),
                                       RangePredicate(6, 10))
        second = TwoRangesSpecification("second",
                                        RangePredicate(2, 3),
                                        RangePredicate(7, 9))
        final = DefaultSpecification()
        chain = All([first, second, final])
        self.assertEqual(False, chain.matches(candidate))

    def test_parse_two_range_spec_from_input(self):
        input = "class: 1-3 or 5-7"
        spec = TwoRangesSpecification.parse(input)
        expected = TwoRangesSpecification(
            "class", RangePredicate(1, 3), RangePredicate(5, 7))
        self.assertEqual(expected, spec)

    def test_can_get_rules_from_input(self):
        parts = parse_input(example_input)
        self.assertEqual(
            [
                TwoRangesSpecification(
                    "class", RangePredicate(1, 3), RangePredicate(5, 7)),
                TwoRangesSpecification(
                    "row", RangePredicate(6, 11), RangePredicate(33, 44)),
                TwoRangesSpecification(
                    "seat", RangePredicate(13, 40), RangePredicate(45, 50))
            ],
            parts['rules']
        )

    def test_can_get_nearby_tickets(self):
        parts = parse_input(example_input)
        self.assertEqual(
            [
                [7, 3, 47],
                [40, 4, 50],
                [55, 2, 20],
                [38, 6, 12]
            ],
            parts['nearby_tickets']
        )

    def test_can_get_check_for_invalid_tickets(self):
        parts = parse_input(example_input)
        actual = check_ticket(parts)
        self.assertEqual(
            [[], [4], [55], [12]],
            actual
        )
        invalids = flatten(actual)
        self.assertEqual(
            71,
            sum(invalids)
        )

    def test_part_one_puzzle_input(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            puzzle_input = content.read()

        parts = parse_input(puzzle_input)
        actual = check_ticket(parts)
        invalids = flatten(actual)
        self.assertEqual(
            29019,
            sum(invalids)
        )
