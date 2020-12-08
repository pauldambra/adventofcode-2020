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
        self.contained_bags = set()
        self.can_be_contained_by_bags = set()

    def contains(self, bag: Bag):
        self.contained_bags.add(bag)
        bag.can_be_contained_by(self)

    def can_be_contained_by(self, bag):
        self.can_be_contained_by_bags.add(bag)

    def can_be_in(self):
        bs = set()
        bs.update(self.can_be_contained_by_bags)
        for bag in self.can_be_contained_by_bags:
            bs.update(bag.can_be_in())

        return frozenset(bs)

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
                print(f"'{s}'")
                parent = s.split("bags contain")[0].strip()
                if parent not in bags:
                    bags[parent] = Bag(parent)

                children = [
                    pattern.sub("", x.strip().strip('.')
                                .strip('bag').strip('bags').strip())
                    for x
                    in s.split("bags contain")[1].split(",")
                ]
                for child in children:
                    if child != "no other":
                        if child not in bags:
                            bags[child] = Bag(child)

                        bags[parent].contains(bags[child])

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
        self.assertEqual(light_red.contained_bags, set([muted_yellow]))

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
        self.assertEqual(bags['light red'].contained_bags,
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
        self.assertEqual(bags['light red'].contained_bags,
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
