from __future__ import annotations
from typing import Literal
import unittest
import os
from files.reader import get_puzzle_input_path


class Console:
    accumulator: int = 0
    terminated: bool = False

    @staticmethod
    def boot_code_from(s: str) -> list:
        return [x.strip()
                for x in s.splitlines()
                if len(x.strip()) > 0]

    @ staticmethod
    def parse(s: str) -> Console:
        return Console(Console.boot_code_from(s))

    def __init__(self, boot_code: list) -> None:
        self.boot_code = boot_code

    def execute(self, instruction_line: int):
        if instruction_line >= len(self.boot_code):
            print('terminating')
            return -1

        try:
            instruction = self.boot_code[instruction_line].split(' ')[
                0].strip()
            argument = int(
                self.boot_code[instruction_line].split(' ')[1].strip())
        except IndexError:
            raise IndexError(
                f"""cannot get argument and instruction from
                  {self.boot_code}
                  at line {instruction_line}
                 """)

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
                if next in lines_visited:
                    keep_running = False
                elif next == -1:
                    self.terminated = True
                    keep_running = False
                else:
                    lines_visited.add(next)
                    next = self.execute(next)
        except BaseException:
            pass


class DayEightTests(unittest.TestCase):

    def test_a_single_acc_increments_by_amount(self):
        console = Console.parse("""
        acc +1
        """)
        console.execute(0)
        self.assertEqual(console.accumulator, 1)

    def test_a_single_acc_increments_by_a_different_amount(self):
        console = Console.parse("""
        acc +2
        """)
        console.execute(0)
        self.assertEqual(console.accumulator, 2)

    def test_a_single_acc_returns_next_instruction_line_to_run(self):
        console = Console.parse("""
        acc +2
        """)
        next = console.execute(0)
        self.assertEqual(next, 1)

    def test_a_jump_can_jump_forwards(self):
        console = Console.parse("""
        jmp +2
        nop
        nop
        """)
        next = console.execute(0)
        self.assertEqual(next, 2)

    def test_a_jump_can_jump_backwards(self):
        console = Console.parse("""
        nop
        nop
        jmp -2
        """)
        next = console.execute(2)
        self.assertEqual(next, 0)

    def test_nop_returns_next_line(self):
        console = Console.parse("""
        nop +0
        nop +0
        jmp -2
        """)
        next = console.execute(0)
        self.assertEqual(next, 1)

    def test_executing_immediately_after_last_instruction_terminates(self):
        console = Console.parse("""
        nop +0
        nop +0
        jmp -2
        """)
        next = console.execute(3)
        self.assertEqual(next, -1)

    def test_can_run_the_program(self):
        console = Console.parse("""
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

    def test_can_run_the_program_to_termination(self):
        console = Console.parse("""
        nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
nop -4
acc +6
        """)
        console.run()
        self.assertEqual(console.accumulator, 8)
        self.assertEqual(console.terminated, True)

    def test_part_one(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            ss = content.read()
            console = Console.parse(ss)
            console.run()
            self.assertEqual(console.accumulator, 1217)

    def patch_code(self, boot_code, patch_index, patch_in):
        patched_code = boot_code.copy()

        patched_code[patch_index] = patched_code[patch_index].replace(
            "jmp" if patch_in == "nop" else "nop",
            patch_in
        )

        console = Console(patched_code)
        console.run()
        if console.terminated:
            print(f"""
            program terminated at index {patch_index}
            by replacing {patch_in}
            accumulator is {console.accumulator}
            """)
            return console

    def test_part_two(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            content = content.read()
            boot_code = Console.boot_code_from(content)
            current = 0
            patch_index = -1
            patch_in: str = "not set"

            for current in range(0, len(boot_code)):
                if boot_code[current].startswith('jmp'):
                    if self.patch_code(boot_code, current, "nop"):
                        patch_index = current
                        patch_in = "nop"

                elif boot_code[current].startswith('nop'):
                    if self.patch_code(boot_code, current, "jmp"):
                        patch_index = current
                        patch_in = "jmp"

            console = self.patch_code(boot_code, patch_index, patch_in)
            self.assertEqual(console.terminated, True)
            self.assertEqual(console.accumulator, 501)
