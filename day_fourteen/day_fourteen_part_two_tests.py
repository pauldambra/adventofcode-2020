import itertools
import math
import os
import re
import unittest

from day_fourteen.chip import BitMask, ThirtySixBitNumber
from files.reader import get_puzzle_input_path


class VersionTwoBitMask:

    def __init__(self, mask: str) -> None:
        self.mask = mask
        self.number_of_xs_in_mask = sum([1 for c in self.mask if c == "X"])
        self.seen_applications = {}

    def apply_to(self, num: ThirtySixBitNumber) -> list[ThirtySixBitNumber]:
        if num in self.seen_applications:
            return self.seen_applications[num]

        number_of_copies = int(math.pow(2, self.number_of_xs_in_mask))
        copies = [num.copy()] + ([num.copy()] * (number_of_copies - 1))
        for i, m in enumerate(self.mask):
            if m == "1":
                for copy in copies:
                    copy.set_bit_in_place(i, 1)

        seen_xs = 0
        for index in range(0, 36):
            if self.mask[index] != "X":
                continue

            # now repeat by 2^seen_xs across the list
            # so 2^0 is 1 -> goes 01010101
            # 2^1 is 2    -> goes 001100110011
            # 2^2 is 4    -> goes 0000111100001111
            for _ in range(0, number_of_copies):
                pattern = [0] * pow(2, seen_xs) + [1] * pow(2, seen_xs)
                pattern_generator = itertools.cycle(pattern)
                for copy_index, copy in enumerate(copies):
                    copies[copy_index] = copy.set_bit(index, next(pattern_generator))

            seen_xs += 1

        self.seen_applications[num] = copies
        return copies

    def __eq__(self, o: object) -> bool:
        if isinstance(o, BitMask):
            return self.mask == o.mask
        else:
            return False

    def __repr__(self) -> str:
        return f"V2BitMask: {self.mask}"


class VersionTwoDecoderProgram:
    def __init__(self) -> None:
        self.bitmask: VersionTwoBitMask = None
        self.memory = {}

    def process_line(self, line: str):
        if line.startswith('mask'):
            self.bitmask = VersionTwoBitMask(line.split(" = ")[1].strip())
        elif line.startswith("mem"):
            match = re.match(r"mem\[(\d+)] = (\d+)", line)
            address = int(match.group(1))
            num = ThirtySixBitNumber(int(match.group(2)))
            decoded_addresses = self.bitmask.apply_to(ThirtySixBitNumber(address))

            for decoded_address in decoded_addresses:
                self.memory[decoded_address.value] = num.value


    def sum_memory(self):
        return sum(self.memory.values())


class DayFourteenPartTwoTests(unittest.TestCase):

    def test_can_read_version_two_bitmask(self):
        program = VersionTwoDecoderProgram()
        program_input = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
        """
        input_lines = [line.strip()
                       for line in program_input.splitlines()
                       if len(line.strip()) > 0]

        for line in input_lines:
            program.process_line(line)

        self.assertEqual(program.bitmask, BitMask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"))

    def test_v2_bitmask_zero_does_nothing(self):
        mask = VersionTwoBitMask("000000000000000000000000000000000000")
        bits = [0] * 36
        bits[35] = 1
        bits[34] = 0
        num = ThirtySixBitNumber(bits)

        actual = mask.apply_to(num)

        self.assertEqual(actual[0].bits[35], 1)
        self.assertEqual(actual[0].bits[34], 0)

    def test_v2_bitmask_one_writes_one(self):
        mask = VersionTwoBitMask("000000000000000000000000000001010101")
        bits = [0] * 36
        num = ThirtySixBitNumber(bits)

        actual = mask.apply_to(num)
        self.assertEqual(len(actual), 1)

        result = actual[0]
        self.assertEqual(result.bits[35], 1)
        self.assertEqual(result.bits[34], 0)
        self.assertEqual(result.bits[33], 1)
        self.assertEqual(result.bits[32], 0)
        self.assertEqual(result.bits[31], 1)
        self.assertEqual(result.bits[30], 0)
        self.assertEqual(result.bits[29], 1)

    def test_v2_bitmask_x_writes_all_possibilities(self):
        mask = VersionTwoBitMask("000000000000000000000000000000X1001X")
        num = ThirtySixBitNumber(42)
        results = mask.apply_to(num)

        self.assertEqual(len(results), 4)

        self.assertCountEqual(
            results,
            [
                ThirtySixBitNumber(26),
                ThirtySixBitNumber(27),
                ThirtySixBitNumber(58),
                ThirtySixBitNumber(59)
            ]
        )

    def test_set_bits_in_place(self):
        x = ThirtySixBitNumber(36)
        y = x.set_bit(31, 1)
        self.assertEqual(52, y.value)

        z = x.set_bit_in_place(31, 1)
        self.assertEqual(52, z.value)
        self.assertEqual(52, x.value)

    def test_program_with_example_input(self):
        program = VersionTwoDecoderProgram()
        example_input = """
    mask = 000000000000000000000000000000X1001X
    mem[42] = 100
    mask = 00000000000000000000000000000000X0XX
    mem[26] = 1"""

        input_lines = [line.strip()
                       for line in example_input.splitlines()
                       if len(line.strip()) > 0]

        for line in input_lines:
            program.process_line(line)

        self.assertEqual(program.sum_memory(), 208)

    # def test_program_with_puzzle_input(self):
    #     """
    #     Takes 9h 20m to return the correct result
    #     """
    #     program = VersionTwoDecoderProgram()
    #
    #     with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
    #         input_lines = [line.strip()
    #                        for line in content.read().splitlines()
    #                        if len(line.strip()) > 0]
    #
    #     for line in input_lines:
    #         program.process_line(line)
    #
    #     self.assertEqual(program.sum_memory(), 3219837697833)
