import unittest
import data.sliding
import os
from files.reader import get_puzzle_input_path


def organise_plugs(adapters):
    adapter_joltage = sorted([int(j.strip())
                              for j in adapters
                              if j and len(j.strip()) > 0])
    device_joltage = max(adapter_joltage) + 3

    still_has_valid_possible_adapter = True
    next_possible = 0
    adapter_order = [0]
    while still_has_valid_possible_adapter and next_possible <= device_joltage:
        next_three = range(next_possible + 1, next_possible + 4)
        for candidate in next_three:
            if candidate in adapter_joltage:

                adapter_order.append(candidate)

            next_possible = candidate

    adapter_order.append(device_joltage)

    steps = data.sliding.window(adapter_order, 2)
    counted_steps = [y - x for (x, y) in steps]

    seen_steps = {}
    for counted_step in counted_steps:
        if counted_step not in seen_steps:
            seen_steps[counted_step] = 0

        seen_steps[counted_step] = seen_steps[counted_step] + 1

    return seen_steps


class DayTenTests(unittest.TestCase):

    def test_wat(self):
        adapters = """
        16
10
15
5
1
11
7
19
6
12
4
        """.splitlines()
        seen_joltage_steps = organise_plugs(adapters)

        self.assertEqual(seen_joltage_steps, {1: 7, 3: 5})

    def test_puzzle_input_part_one(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            puzzle_input = content.read().splitlines()

        seen_joltage_steps = organise_plugs(puzzle_input)

        self.assertEqual(seen_joltage_steps, {1: 73, 3: 31})
        self.assertEqual(seen_joltage_steps[1] * seen_joltage_steps[3], 2263)
