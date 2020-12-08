import unittest
import os
from files.reader import get_puzzle_input_path


class Console:
    accumulator: int = 0

    def __init__(self, boot_code: str) -> None:
        self.boot_code = [s.strip()
                          for s in boot_code.splitlines()
                          if len(s) > 0]

    def execute(self, instruction_line: int):
        try:
            instruction = self.boot_code[instruction_line].split(' ')[
                0].strip()
            argument = int(
                self.boot_code[instruction_line].split(' ')[1].strip())
        except IndexError:
            raise IndexError(
                f"""cannot get argument and instruction from
                 {self.boot_code[instruction_line].split(' ')}""")

        if instruction == "acc":
            self.accumulator += argument
            return instruction_line + 1
        elif instruction == "jmp":
            return instruction_line + argument
        elif instruction == "nop":
            return instruction_line + 1

    def run(self):
        lines_visited = set()
        keep_running = True
        try:
            next = 0
            while keep_running:
                if (next in lines_visited):
                    print("already visited line " + next)
                    keep_running = False
                else:
                    lines_visited.add(next)
                    next = self.execute(next)
        except BaseException:
            pass


class DayEightTests(unittest.TestCase):

    def test_a_single_acc_increments_by_amount(self):
        console = Console("""
        acc +1
        """)
        console.execute(0)
        self.assertEqual(console.accumulator, 1)

    def test_a_single_acc_increments_by_a_different_amount(self):
        console = Console("""
        acc +2
        """)
        console.execute(0)
        self.assertEqual(console.accumulator, 2)

    def test_a_single_acc_returns_next_instruction_line_to_run(self):
        console = Console("""
        acc +2
        """)
        next = console.execute(0)
        self.assertEqual(next, 1)

    def test_a_jump_can_jump_forwards(self):
        console = Console("""
        jmp +2
        nop
        nop
        """)
        next = console.execute(0)
        self.assertEqual(next, 2)

    def test_a_jump_can_jump_backwards(self):
        console = Console("""
        nop
        nop
        jmp -2
        """)
        next = console.execute(2)
        self.assertEqual(next, 0)

    def test_nop_returns_next_line(self):
        console = Console("""
        nop +0
        nop +0
        jmp -2
        """)
        next = console.execute(0)
        self.assertEqual(next, 1)

    def test_can_run_the_program(self):
        console = Console("""
        nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
        """)
        console.run()
        self.assertEqual(console.accumulator, 5)

    def test_part_one(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            ss = content.read()
            console = Console(ss)
            console.run()
            self.assertEqual(console.accumulator, 1217)
