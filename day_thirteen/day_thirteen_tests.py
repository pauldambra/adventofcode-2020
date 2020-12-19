import unittest
import sys

puzzle_input = """
1002618
19,x,x,x,x,x,x,x,x,41,x,x,x,37,x,x,x,x,x,367,x,x,x,x,x,x,x,x,x,x,x,x,13,x,x,x,17,x,x,x,x,x,x,x,x,x,x,x,29,x,373,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,23
"""

example_input = """
939
7,13,x,x,59,x,31,19
"""


def parse_schedule(ss):
    lines = [s.strip() for s in ss.splitlines() if len(s.strip()) > 0]
    return {
        'time': int(lines[0]),
        'busses': sorted([int(x) for x in lines[1].split(',') if x != 'x'])
    }


def parse_schedule_with_gaps(ss: str) -> list[int]:
    lines = [s.strip() for s in ss.splitlines() if len(s.strip()) > 0]

    result = []
    for c in lines[-1].split(','):
        if c == 'x':
            result.append(0)
        else:
            result.append(int(c))

    return result


def find_first_multiple_below(target: int, multiple: int) -> int:
    return multiple * (target // multiple)


def find_spread(target: int, multiple: int) -> int:
    start = find_first_multiple_below(target, multiple)
    return {
        multiple: [
            start - multiple,
            start,
            start + multiple,
            start + (multiple * 2)
        ]
    }


def get_schedules(input):
    schedule = parse_schedule(input)
    ss = [find_spread(schedule['time'], s)
          for s
          in schedule['busses']]
    wat = {}
    for s in ss:
        wat.update(s)
    return {'time': schedule['time'], 'schedules': wat}


def get_earliest_bus_wait(input):
    wat = get_schedules(input)

    x = (-1, sys.maxsize)
    for key in wat['schedules']:
        schedule = wat['schedules'][key]
        candidates = [
            (k, v)
            for (k, v)
            in [(key, x - wat['time']) for x in schedule]
            if v > 0
        ]
        next_bus = min(candidates, key=lambda t: t[1])
        if next_bus[1] < x[1]:
            x = next_bus

    return x


def times_table(multiple: int) -> tuple[int, int]:
    num = 1
    while True:
        next = num * multiple
        yield (num, next)
        num += 1


class DayThirteenPartTwo(unittest.TestCase):

    def test_something(self):
        schedule: list[int] = parse_schedule_with_gaps("17,x,13,19")
        needed_matches = len(schedule) - 1

        matched = -1
        for num in times_table(schedule[0]):
            print(f"next {num}")
            matches = 0
            for index, possible in enumerate(schedule[1:]):
                time = num[1]+index+1
                if possible == 0:
                    print(f"at {time} - zero always matches")
                    matches += 1
                    continue

                if time % possible != 0:
                    break
                else:
                    print(
                        f"at {time} - modulo result {time % possible == 0}")
                    matches += 1

            if matches == needed_matches:
                print(f"matched at {num[1]}")
                matched = num[1]

            if matched > 0:
                break

        self.assertEqual(1, 2)

    def test_something_else(self):
        schedule: list[int] = parse_schedule_with_gaps(example_input)
        needed_matches = len(schedule) - 1

        matched = -1
        for num in times_table(schedule[0]):
            print(f"next {num}")
            matches = 0
            for index, possible in enumerate(schedule[1:]):
                time = num[1]+index+1
                if possible == 0:
                    print(f"at {time} - zero always matches")
                    matches += 1
                    continue

                if time % possible != 0:
                    break
                else:
                    print(
                        f"at {time} - modulo result {time % possible == 0}")
                    matches += 1

            if matches == needed_matches:
                print(f"matched at {num[1]}")
                matched = num[1]

            if matched > 0:
                break

        self.assertEqual(1, 2)

    def test_puzzle_input(self):
        schedule: list[int] = parse_schedule_with_gaps(puzzle_input)
        needed_matches = len(schedule) - 1

        matched = -1
        for num in times_table(schedule[0]):
            if num[0] < 100000000000000:
                continue

            # print(f"next {num}")
            matches = 0
            for index, possible in enumerate(schedule[1:]):
                time = num[1]+index+1
                if possible == 0:
                    # print(f"at {time} - zero always matches")
                    matches += 1
                    continue

                if time % possible != 0:
                    break
                else:
                    # print(
                    #     f"at {time} - modulo result {time % possible == 0}")
                    matches += 1

            if matches == needed_matches:
                print(f"matched at {num[1]}")
                matched = num[1]

            if matched > 0:
                break

        self.assertEqual(1, 2)


class DayThirteenTests(unittest.TestCase):

    def test_can_parse_busses(self):
        schedule = parse_schedule(example_input)
        self.assertEqual(schedule['time'], 939)
        self.assertEqual(schedule['busses'], [7, 13, 19, 31, 59])

    def test_get_first_multiple_below_number(self):
        x = find_first_multiple_below(26, 5)
        self.assertEqual(25, x)

        y = find_first_multiple_below(50, 7)
        self.assertEqual(49, y)

    def test_get_spread(self):
        x = find_spread(26, 5)
        self.assertEqual(x, {5: [20, 25, 30, 35]})

        y = find_spread(111, 11)
        self.assertEqual(y, {11: [99, 110, 121, 132]})

    def test_get_spread_for_example_input(self):
        wat = get_schedules(example_input)
        print(wat)
        schedules = wat['schedules']
        self.assertEqual(len(schedules), 5)
        self.assertEqual(schedules[7], [931, 938, 945, 952])
        self.assertEqual(schedules[13], [923, 936, 949, 962])
        self.assertEqual(schedules[19], [912, 931, 950, 969])
        self.assertEqual(schedules[31], [899, 930, 961, 992])
        self.assertEqual(schedules[59], [826, 885, 944, 1003])

    def test_get_earliest_bus_for_example_input(self):
        x = get_earliest_bus_wait(example_input)

        self.assertEqual(x[0] * x[1], 295)

    def test_get_earliest_bus_for_puzzle_input(self):
        x = get_earliest_bus_wait(puzzle_input)

        self.assertEqual(x[0] * x[1], 2238)
