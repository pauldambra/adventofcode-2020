import unittest
import re
import os
from files.reader import get_puzzle_input_path


class ThirtySixBitNumber:

    def __init__(self, *args) -> None:
        if isinstance(args[0], int):
            self.value = args[0]
            self.bits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            remaining = args[0]
            for power in range(35, -1, -1):
                position_value = pow(2, power)
                if remaining > 0 and remaining >= position_value:
                    self.bits[power] = 1
                    remaining -= position_value

        else:
            self.bits = args[0]
            self.bits.reverse()

            self.value = 0
            for power in range(0, 36):
                position_value = pow(2, power)
                if args[0][power] == 1:
                    self.value += position_value

        self.bits.reverse()

    def __eq__(self, o: object) -> bool:
        return self.bits == o.bits

    def __repr__(self) -> str:
        return f"value: {self.value} for bits {self.bits}"

    def copy(self):
        return ThirtySixBitNumber(self.value)

    def set_bit(self, index: int, value: int):
        bits = self.bits.copy()
        bits[index] = value
        return ThirtySixBitNumber(bits)


class Program:
    def __init__(self) -> None:
        self.bitmask: BitMask = None
        self.memory = {}

    def process_line(self, line: str):
        if (line.startswith('mask')):
            self.bitmask = BitMask(line.split(" = ")[1].strip())
        elif (line.startswith("mem")):
            match = re.match(r"mem\[(\d+)\] = (\d+)", line)
            address = int(match.group(1))
            num = ThirtySixBitNumber(int(match.group(2)))
            self.memory[address] = self.bitmask.apply_to(num).value

    def sum_memory(self):
        return sum(self.memory.values())


def parse(program: str):
    program_lines = [line.strip()
                     for line in program.splitlines()
                     if len(line.strip()) > 0]

    instructions = []
    for line in program_lines[1:]:
        match = re.match(r"mem\[(\d+)\] = (\d+)", line)
        instructions.append((
            int(match.group(1)),
            ThirtySixBitNumber(int(match.group(2)))
        ))

    return {
        'mask': BitMask(program_lines[0].split(" = ")[1].strip()),
        'values': instructions
    }


def apply_bitmask(parsed_program: str):
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


class BitMask:

    def __init__(self, mask: str) -> None:
        self.mask = mask

    def apply_to(self, num: ThirtySixBitNumber) -> ThirtySixBitNumber:
        copy = num.copy()
        for i, m in enumerate(self.mask):
            if m != "X":
                copy = copy.set_bit(i, int(m))

        return copy

    def __eq__(self, o: object) -> bool:
        return self.mask == o.mask

    def __repr__(self) -> str:
        return f"BitMask: {self.mask}"


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
        self.assertEqual(n.value, 3)

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

    def test_initialise_memory_with_puzzle_input(self):
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
        program = Program()
        input = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
        """
        input_lines = [line.strip()
                       for line in input.splitlines()
                       if len(line.strip()) > 0]

        for line in input_lines:
            program.process_line(line)

        print(program.memory)

        self.assertEqual(program.memory,
                         {
                             7: 101,
                             8: 64
                         }
                         )

        self.assertEqual(program.sum_memory(), 165)

    def test_program_with_puzzle_input(self):
        program = Program()

        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            input_lines = [line.strip()
                           for line in content.read().splitlines()
                           if len(line.strip()) > 0]

        for line in input_lines:
            program.process_line(line)

        self.assertEqual(program.sum_memory(), 16003257187056)
