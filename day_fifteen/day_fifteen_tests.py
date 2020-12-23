import collections
import unittest
from typing import Generator


def start_game(initial: list[int], end_turn: int) -> Generator[int, None, None]:
    turn = 1
    faster_game_numbers: dict[int, collections.deque] = dict()

    def update_game_record(n: int):
        if n not in faster_game_numbers:
            faster_game_numbers[n] = collections.deque()

        faster_game_numbers[n].appendleft(turn)

    last_number = None
    game_numbers = collections.deque()
    for number in initial:
        game_numbers.appendleft(number)
        update_game_record(number)
        turn += 1
        last_number = number
        yield number

    while turn <= end_turn:
        seen_before = last_number in faster_game_numbers
        is_not_first_occurence = len(faster_game_numbers[last_number]) > 1

        if seen_before and is_not_first_occurence:
            last_seen = faster_game_numbers[last_number][0]
            last_turn = turn - 1
            if last_seen == last_turn:
                last_seen = faster_game_numbers[last_number][1]

            age = last_turn - last_seen
        else:
            age = 0

        update_game_record(age)
        last_number = age
        turn += 1
        yield age


class DayFifteenTests(unittest.TestCase):
    def test_can_have_list_to_count_from(self):
        game = start_game([0, 3, 6], 3)
        first = next(game)
        self.assertEqual(0, first)

    def test_can_get_second_from_initial_list(self):
        game = start_game([0, 3, 6], 3)
        next(game)
        second = next(game)
        self.assertEqual(3, second)

    def test_can_get_number_after_initial_list(self):
        game = start_game([0, 3, 6], 4)
        next(game)
        next(game)
        next(game)
        first_calculated = next(game)
        self.assertEqual(0, first_calculated)

    def test_can_get_first_number_from_age(self):
        game = start_game([0, 3, 6], 5)
        next(game)
        next(game)
        next(game)
        next(game)
        first_from_age = next(game)
        self.assertEqual(3, first_from_age)

    def test_can_get_second_number_with_age(self):
        game = start_game([0, 3, 6], 6)
        next(game)
        next(game)
        next(game)
        next(game)
        next(game)
        x = next(game)
        self.assertEqual(3, x)

    def test_can_get_ten_steps_in(self):
        game = start_game([0, 3, 6], 11)
        expected = [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]
        for i in range(0, 10):
            x = next(game)
            self.assertEqual(expected[i], x)

    def assert_number_at_turn_x(self, initial_list, limit, expected):
        game = start_game(initial_list, limit)
        for _ in range(0, limit):
            x = next(game)

        self.assertEqual(expected, x)

    def test_2020th_step_for_examples(self):
        self.assert_number_at_turn_x([0, 3, 6], 2020, 436)
        self.assert_number_at_turn_x([1, 3, 2], 2020, 1)

    def test_2020th_step_for_puzzle_input(self):
        self.assert_number_at_turn_x([0, 1, 5, 10, 3, 12, 19], 2020, 1373)

    def test_part_two_examples(self):
        limit = 30000000
        self.assert_number_at_turn_x([0, 1, 5, 10, 3, 12, 19], limit, 112458)
