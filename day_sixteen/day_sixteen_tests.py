from __future__ import annotations

import math

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

part_two_example_input = """
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
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
    reading_own = False
    reading_nearby = False
    for line in [cs.strip() for cs in i.splitlines() if len(cs.strip()) > 0]:
        if line == "your ticket:":
            reading_rules = False
            reading_own = True

        if line == "nearby tickets:":
            reading_nearby = True
            reading_own = False

        if reading_own and line != "your ticket:":
            own = [int(x) for x in line.split(',')]

        if reading_rules:
            specs.append(TwoRangesSpecification.parse(line))

        if reading_nearby and line != "nearby tickets:":
            nearby.append([int(x) for x in line.split(',')])

    return {
        'rules': specs,
        'nearby_tickets': nearby,
        'own_ticket': own
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


def get_valid_tickets(values):
    spec_chain = Any(values['rules'])
    valid_tickets = []
    for ticket in values['nearby_tickets']:
        has_invalid = len([
            field for field
            in ticket
            if not spec_chain.matches(field)
        ]) > 0
        if not has_invalid:
            valid_tickets.append(ticket)

    return valid_tickets


def flatten(t): return [item for sublist in t for item in sublist]


def map_fields(valids, rules):
    candidates = []
    number_of_fields = len(rules)
    matched_positions = []
    matched_specs = []

    while len(candidates) < number_of_fields:
        # print(f"running because candidates length is {len(candidates)}")
        # print(candidates)

        for position in range(0, number_of_fields):
            if position in matched_positions:
                # print(f"skipping position {position}")
                continue

            column = [ticket[position] for ticket in valids]
            position_candidates = []

            for spec in rules:
                if spec.name in matched_specs:
                    # print(f"skipping matched spec {spec.name}")
                    continue

                could_be = [spec.matches(x) for x in column]
                # print(f"for field {spec.name} and position {position} spec results were")
                # print(could_be)
                if all(could_be):
                    position_candidates.append({
                        'spec': spec.name,
                        'position': position
                    })

            if len(position_candidates) == 1:
                # print("matched a candidate")
                # print(position_candidates)
                candidates.append(position_candidates[0])
                matched_specs.append(position_candidates[0]['spec'])
                matched_positions.append(position_candidates[0]['position'])

    return candidates


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

    def test_something_part_two(self):
        parts = parse_input(part_two_example_input)
        valids = get_valid_tickets(parts)
        print(valids)

        candidates = map_fields(valids, parts['rules'])

        print(candidates)
        self.assertEqual(1, 2)

    def test_something_part_two_puzzle_input(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            puzzle_input = content.read()

        parts = parse_input(puzzle_input)
        valids = get_valid_tickets(parts)

        candidates = map_fields(valids, parts['rules'])

        departure_fields = [f['position'] for f in candidates if f['spec'].startswith('departure')]

        my_departure_fields = []
        for departure_field in departure_fields:
            my_departure_fields.append(parts['own_ticket'][departure_field])

        departure_fields_product = math.prod(my_departure_fields)
        self.assertEqual(517827547723, departure_fields_product)
