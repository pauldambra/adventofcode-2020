import os
import re
import unittest

from day_fourteen.chip import ThirtySixBitNumber, BitMask, VersionOneDecoderProgram
from files.reader import get_puzzle_input_path


def parse(program: str):
    program_lines = [line.strip()
                     for line in program.splitlines()
                     if len(line.strip()) > 0]

    instructions = []
    for line in program_lines[1:]:
        match = re.match(r"mem\[(\d+)] = (\d+)", line)
        instructions.append((
            int(match.group(1)),
            ThirtySixBitNumber(int(match.group(2)))
        ))

    return {
        'mask': BitMask(program_lines[0].split(" = ")[1].strip()),
        'values': instructions
    }


def apply_bitmask(parsed_program: dict):
    mask: BitMask = parsed_program['mask']
    masked_values = []
    for (k, v) in parsed_program['values']:
        masked_values.append((k, mask.apply_to(v)))

    return {
        'mask': mask,
        'values': masked_values
    }


def initialise_memory(masked_program) -> dict[int, int]:
    result = {}
    for (k, v) in masked_program['values']:
        result[k] = v.value

    return result


class DayFourteenTests(unittest.TestCase):

    def test_zero(self):
        zero = ThirtySixBitNumber(0)
        self.assertEqual(
            zero.bits,
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

    def test_one(self):
        n = ThirtySixBitNumber(1)
        self.assertEqual(
            n.bits,
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        )

    def test_two(self):
        n = ThirtySixBitNumber(2)
        self.assertEqual(
            n.bits,
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        )

    def test_three(self):
        n = ThirtySixBitNumber(3)
        self.assertEqual(
            n.bits,
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
        )

    def test_can_create_number_from_bits(self):
        n = ThirtySixBitNumber([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
        self.assertEqual(n.bits, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
        self.assertEqual(3, n.value)

    def test_example_values(self):
        self.assertEqual(ThirtySixBitNumber(73).bits,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1])

        self.assertEqual(ThirtySixBitNumber(101).bits,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1])

        self.assertEqual(ThirtySixBitNumber(64).bits,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])

    def test_bitmask_can_have_no_impact(self):
        mask = BitMask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        x = mask.apply_to(ThirtySixBitNumber(2))
        self.assertEqual(x, ThirtySixBitNumber(2))

    def test_bitmask_can_have_impact(self):
        mask = BitMask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX0X")
        x = mask.apply_to(ThirtySixBitNumber(2))
        self.assertEqual(x, ThirtySixBitNumber(0))

    def test_parse_program(self):
        program = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
        """
        parsed_program = parse(program)
        print(parsed_program['values'])
        self.assertEqual(
            parsed_program,
            {
                'mask': BitMask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"),
                'values': [
                    (8, ThirtySixBitNumber(11)),
                    (7, ThirtySixBitNumber(101)),
                    (8, ThirtySixBitNumber(0))
                ]
            }
        )

    def test_apply_bitmask(self):
        program = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
        """
        parsed_program = parse(program)
        masked_program = apply_bitmask(parsed_program)
        self.assertEqual(
            masked_program,
            {
                'mask': BitMask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"),
                'values': [
                    (8, ThirtySixBitNumber(73)),
                    (7, ThirtySixBitNumber(101)),
                    (8, ThirtySixBitNumber(64))
                ]
            }
        )

    def test_initialise_memory(self):
        program = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
        """
        parsed_program = parse(program)
        masked_program = apply_bitmask(parsed_program)
        initialised_memory = initialise_memory(masked_program)
        self.assertEqual(
            initialised_memory,
            {
                7: 101,
                8: 64
            }
        )

    def test_program_with_example_input(self):
        program = VersionOneDecoderProgram()
        example_input = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
        """
        input_lines = [line.strip()
                       for line in example_input.splitlines()
                       if len(line.strip()) > 0]

        for line in input_lines:
            program.process_line(line)

        print(program.memory)

        self.assertEqual(
            program.memory,
            {
                7: 101,
                8: 64
            }
        )

        self.assertEqual(program.sum_memory(), 165)

    def test_program_with_puzzle_input(self):
        program = VersionOneDecoderProgram()

        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            input_lines = [line.strip()
                           for line in content.read().splitlines()
                           if len(line.strip()) > 0]

        for line in input_lines:
            program.process_line(line)

        self.assertEqual(program.sum_memory(), 16003257187056)
