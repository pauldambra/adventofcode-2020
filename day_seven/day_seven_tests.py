from __future__ import annotations
import os
import typing
import unittest
import re
from files.reader import get_puzzle_input_path

example_input = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""


class Bag:
    """bags can contain one or more bags
     and can be contained by one or more bags.
     there should only be one instance for any given colour"""

    def __init__(self, colour):
        self.colour = colour
        self.can_contain_bags: typing.Dict[Bag, int] = {}
        self.can_be_contained_by_bags = set()

    def contains(self, bag: Bag, number_contained: int = 1):
        if bag in self.can_contain_bags:
            new_count = self.can_contain_bags[bag] + number_contained
        else:
            new_count = number_contained
        self.can_contain_bags[bag] = new_count
        bag.can_be_contained_by(self)

    def contained_bags(self) -> set:
        return frozenset(self.can_contain_bags)

    def can_be_contained_by(self, bag):
        self.can_be_contained_by_bags.add(bag)

    def can_be_in(self):
        bs = set()
        bs.update(self.can_be_contained_by_bags)
        for bag in self.can_be_contained_by_bags:
            bs.update(bag.can_be_in())

        return frozenset(bs)

    def count_children(self):
        count = 0
        for child_bag, child_count in self.can_contain_bags.items():
            count += child_count
            count += child_count * child_bag.count_children()

        return count

    def __repr__(self) -> str:
        return f"Bag: {self.colour}"

    def __eq__(self, other):
        if isinstance(other, Bag):
            return self.colour == other.colour
        return False

    def __hash__(self):
        return self.colour.__hash__()

    @staticmethod
    def parse(ss) -> typing.Dict[str, Bag]:
        bags: typing.Dict[str, Bag] = {}
        pattern = re.compile(r"^\d+ ")

        for x in ss.splitlines():
            s = x.strip()
            if s:
                parent = s.split("bags contain")[0].strip()
                if parent not in bags:
                    bags[parent] = Bag(parent)

                uncounted_children = [
                    x.strip().strip('.')
                    .strip('bag').strip('bags').strip()
                    for x
                    in s.split("bags contain")[1].split(",")
                ]
                counted_children = []
                for uncounted in uncounted_children:
                    if uncounted != "no other":
                        parts = uncounted.split(" ", 1)
                        count = int(parts[0].strip())
                        child = parts[1].strip()
                        counted_children.append([count, child])

                for count, child in counted_children:
                    if child not in bags:
                        bags[child] = Bag(child)

                    bags[parent].contains(bags[child], count)

        return bags


class DaySevenTests(unittest.TestCase):

    # def test_example_input_has_four_bags_that_could_contain_shiny_gold(self):
    #     count_of_bags = how_many_bags_can_contain(
    #         "shiny gold",
    #         parse_regulations_from(example_input))

    #     self.assertEqual(count_of_bags, 4)

    def test_one_bag_can_contain_one_other(self):
        """
            light red:
                muted yellow
        """
        muted_yellow = Bag("muted yellow")
        light_red = Bag("light red")
        light_red.contains(muted_yellow)
        self.assertEqual(muted_yellow.can_be_in(), frozenset([light_red]))

    def test_one_bag_can_contain_more_than_other(self):
        """
            light red:
                muted yellow
                yucky green
        """
        muted_yellow = Bag("muted yellow")
        yucky_green = Bag("yucky_green")
        light_red = Bag("light red")
        light_red.contains(muted_yellow)
        light_red.contains(yucky_green)
        self.assertEqual(muted_yellow.can_be_in(), frozenset([light_red]))
        self.assertEqual(yucky_green.can_be_in(), frozenset([light_red]))

    def test_one_bag_can_contain_nested_bags(self):
        """
            light red:
                muted yellow:
                    yucky green
        """
        muted_yellow = Bag("muted yellow")
        yucky_green = Bag("yucky_green")
        light_red = Bag("light red")
        light_red.contains(muted_yellow)
        muted_yellow.contains(yucky_green)
        self.assertEqual(muted_yellow.can_be_in(), frozenset([light_red]))
        self.assertEqual(yucky_green.can_be_in(),
                         frozenset([muted_yellow, light_red]))

    def test_one_bag_can_contain_one_other_but_not_twice(self):
        """
            light red:
                muted yellow
        """
        muted_yellow = Bag("muted yellow")
        light_red = Bag("light red")
        light_red.contains(muted_yellow)
        light_red.contains(muted_yellow)
        self.assertEqual(muted_yellow.can_be_in(), frozenset([light_red]))
        self.assertEqual(light_red.contained_bags(), set([muted_yellow]))

    def test_one_bag_can_contain_nested_bags_several_levels(self):
        """
            light red:
                muted yellow:
                    yucky green:
                        lovely pink
        """
        muted_yellow = Bag("muted yellow")
        yucky_green = Bag("yucky green")
        lovely_pink = Bag("lovely pink")
        light_red = Bag("light red")
        light_red.contains(muted_yellow)
        muted_yellow.contains(yucky_green)
        yucky_green.contains(lovely_pink)
        self.assertEqual(muted_yellow.can_be_in(), frozenset([light_red]))
        self.assertEqual(lovely_pink.can_be_in(),
                         frozenset([muted_yellow, light_red, yucky_green]))

    def test_can_parse_bags_out_of_input_strings(self):

        s = "light red bags contain 1 bright white bag, 2 muted yellow bags."
        bags = Bag.parse(s)

        self.assertEqual(bags, {
            'light red': Bag('light red'),
            'bright white': Bag('bright white'),
            'muted yellow': Bag('muted yellow')
        })

    def test_can_parse_bags_out_of_input_strings_with_more_than_one_line(self):
        s = """
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        light red bags contain 1 blue bag.
        """
        bags = Bag.parse(s)

        self.assertEqual(bags, {
            'light red': Bag('light red'),
            'bright white': Bag('bright white'),
            'muted yellow': Bag('muted yellow'),
            'blue': Bag('blue')
        })

    def test_can_parse_bags_and_relations(self):
        s = """
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        light red bags contain 1 blue bag.
        """
        bags = Bag.parse(s)

        self.assertEqual(bags, {
            'light red': Bag('light red'),
            'bright white': Bag('bright white'),
            'muted yellow': Bag('muted yellow'),
            'blue': Bag('blue')
        })
        self.assertEqual(bags['light red'].contained_bags(),
                         set([
                             Bag('bright white'),
                             Bag('muted yellow'),
                             Bag('blue')
                         ]))

    def test_can_parse_bags_ignoring_bags_that_cannot_have_children(self):
        s = """
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        bright white bags contain no other bags.
        """
        bags = Bag.parse(s)

        self.assertEqual(bags, {
            'light red': Bag('light red'),
            'bright white': Bag('bright white'),
            'muted yellow': Bag('muted yellow')
        })
        self.assertEqual(bags['light red'].contained_bags(),
                         set([
                             Bag('bright white'),
                             Bag('muted yellow')
                         ]))

    def test_example_input(self):
        bags = Bag.parse(example_input)

        self.assertEqual(len(bags), 9)

        can_hold_gold = bags['shiny gold'].can_be_in()

        self.assertEqual(len(can_hold_gold), 4)

    def test_puzzle_input_part_one(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            ss = content.read()
        bags = Bag.parse(ss)

        can_hold_gold = bags['shiny gold'].can_be_in()

        self.assertEqual(len(can_hold_gold), 246)

    def test_can_count_children_bags(self):
        """
            light red:
                muted yellow
        """
        muted_yellow = Bag("muted yellow")
        light_red = Bag("light red")
        light_red.contains(muted_yellow)

        self.assertEqual(light_red.count_children(), 1)

    def test_can_count_nested_children_bags(self):
        """
            light red:
                muted yellow:
                    green
        """
        muted_yellow = Bag("muted yellow")
        light_red = Bag("light red")
        green = Bag("green")
        light_red.contains(muted_yellow)
        muted_yellow.contains(green)
        self.assertEqual(light_red.count_children(), 2)

    def test_can_count_varying_numbers_of_children_bags(self):
        """
            light red:
                2 x muted yellow:
                    4 X green

            so light red contains 2 muted yellow
            and each of those contain 4 other bags
            for a total of 10
        """
        muted_yellow = Bag("muted yellow")
        light_red = Bag("light red")
        green = Bag("green")
        light_red.contains(muted_yellow, 2)
        muted_yellow.contains(green, 4)
        self.assertEqual(light_red.count_children(), 10)

    def test_part_two_example_one(self):
        example_one_part_two = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""
        bags = Bag.parse(example_one_part_two)

        gold_contains = bags['shiny gold'].count_children()

        self.assertEqual(gold_contains, 126)

    def test_puzzle_input_part_two(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            ss = content.read()
        bags = Bag.parse(ss)

        gold_contains = bags['shiny gold'].count_children()

        self.assertEqual(gold_contains, 2976)
