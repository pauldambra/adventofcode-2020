import os
from files.reader import get_puzzle_input_path
import unittest
import day_eleven.travel as travel


class WaypointShip:
    turn_right_from = {
        'east': 'south',
        'south': 'west',
        'west': 'north',
        'north': 'east'
    }
    turn_left_from = {
        'east': 'north',
        'north': 'west',
        'west': 'south',
        'south': 'east'
    }

    def __init__(self):
        self.position: travel.Coordinate = travel.Coordinate(0, 0)
        self.waypoint_position: travel.Coordinate = {'east': 10, 'north': 1}

    def manhattan_distance_travelled(self) -> int:
        return abs(self.position.x) + abs(self.position.y)

    def navigate(self, instruction: str) -> None:
        action = instruction[0]
        value = int(instruction[1:])

        def move_waypoint(direction: str, times: int) -> None:
            """
            moving north is negative, south is positive
            moving west is negative, south is positive
            """
            for _ in range(0, times):
                if direction == 'north':
                    if 'north' in self.waypoint_position:
                        self.waypoint_position['north'] += 1

                    elif 'south' in self.waypoint_position:
                        self.waypoint_position['south'] -= 1

                        if self.waypoint_position['south'] < 0:
                            self.waypoint_position['north'] = - \
                                self.waypoint_position['south']
                            del self.waypoint_position['south']

                if direction == 'south':
                    if 'south' in self.waypoint_position:
                        self.waypoint_position['south'] += 1

                    elif 'north' in self.waypoint_position:
                        self.waypoint_position['north'] -= 1
                        if self.waypoint_position['north'] < 0:
                            self.waypoint_position['south'] = - \
                                self.waypoint_position['north']
                            del self.waypoint_position['north']

                if direction == 'east':
                    if 'east' in self.waypoint_position:
                        self.waypoint_position['east'] += 1

                    elif 'west' in self.waypoint_position:
                        self.waypoint_position['west'] -= 1
                        if self.waypoint_position['west'] < 0:
                            self.waypoint_position['east'] = - \
                                self.waypoint_position['west']
                            del self.waypoint_position['west']

                if direction == 'west':
                    if 'west' in self.waypoint_position:
                        self.waypoint_position['west'] += 1

                    elif 'east' in self.waypoint_position:
                        self.waypoint_position['east'] -= 1
                        if self.waypoint_position['east'] < 0:
                            self.waypoint_position['west'] = - \
                                self.waypoint_position['east']
                            del self.waypoint_position['east']

        def move_ship(times: int) -> None:

            for _ in range(0, times):
                print(f"starting: {self.position}")
                print(f"waypoint: {self.waypoint_position}")
                self.position = travel.Coordinate(
                    self.position.x +
                    self.waypoint_position.get(
                        'east', 0) - self.waypoint_position.get('west', 0),
                    self.position.y +
                    self.waypoint_position.get(
                        'north', 0) - self.waypoint_position.get('south', 0),
                )
                print(f"finished: {self.position}")

        def rotate_left(times: int) -> None:
            new_position = {}
            if 'east' in self.waypoint_position:
                new_position['north'] = self.waypoint_position['east']
            if 'north' in self.waypoint_position:
                new_position['west'] = self.waypoint_position['north']
            if 'west' in self.waypoint_position:
                new_position['south'] = self.waypoint_position['west']
            if 'south' in self.waypoint_position:
                new_position['east'] = self.waypoint_position['south']

            self.waypoint_position = new_position

        def rotate_right(times: int) -> None:
            new_position = {}
            if 'east' in self.waypoint_position:
                new_position['south'] = self.waypoint_position['east']
            if 'south' in self.waypoint_position:
                new_position['west'] = self.waypoint_position['south']
            if 'west' in self.waypoint_position:
                new_position['north'] = self.waypoint_position['west']
            if 'north' in self.waypoint_position:
                new_position['east'] = self.waypoint_position['north']

            self.waypoint_position = new_position

        if action == "F":
            move_ship(value)
        elif action == "N":
            move_waypoint("north", value)
        elif action == "E":
            move_waypoint("east", value)
        elif action == "S":
            move_waypoint("south", value)
        elif action == "W":
            move_waypoint("west", value)
        elif action == "R":
            rotate_right(value // 90)
        elif action == "L":
            rotate_left(value // 90)
        else:
            raise Exception(f"unknown action {action}")


class DayTwelvePartTwoTests(unittest.TestCase):

    def test_ship_can_have_waypoint(self):
        ship = WaypointShip()
        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"east": 10, "north": 1})

    def test_N_moves_waypoint_north(self):
        ship = WaypointShip()

        ship.navigate("N4")

        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"east": 10, "north": 5})

    def test_N_moves_waypoint_east(self):
        ship = WaypointShip()

        ship.navigate("E2")

        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"east": 12, "north": 1})

    def test_N_moves_waypoint_west(self):
        ship = WaypointShip()

        ship.navigate("W10")

        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"east": 0, "north": 1})

    def test_N_moves_waypoint_west_to_west_of_ship(self):
        ship = WaypointShip()

        ship.navigate("W11")

        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"west": 1, "north": 1})

    def test_N_moves_waypoint_west_when_west_of_ship(self):
        ship = WaypointShip()

        ship.navigate("W11")
        ship.navigate("W1")

        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"west": 2, "north": 1})

    def test_N_moves_waypoint_east_when_west_of_ship(self):
        ship = WaypointShip()

        ship.navigate("W11")
        ship.navigate("E1")

        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"west": 0, "north": 1})

    def test_N_moves_waypoint_to_east_when_west_of_ship(self):
        ship = WaypointShip()

        ship.navigate("W11")
        ship.navigate("E3")

        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"east": 2, "north": 1})

    def test_N_moves_waypoint_to_zero_north(self):
        ship = WaypointShip()

        ship.navigate("S1")

        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"east": 10, "north": 0})

    def test_N_moves_waypoint_from_north_to_south(self):
        ship = WaypointShip()

        ship.navigate("S2")

        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"east": 10, "south": 1})

    def test_moves_waypoint_from_south_to_north(self):
        ship = WaypointShip()

        ship.navigate("S4")
        ship.navigate("N5")

        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.waypoint_position, {"east": 10, "north": 2})

    def test_F_moves_to_waypoint_and_waypoint_offset_does_not_change(self):
        ship = WaypointShip()

        ship.navigate("F1")
        self.assertEqual(ship.position, travel.Coordinate(10, 1))
        self.assertEqual(ship.waypoint_position, {"east": 10, "north": 1})

    def test_F10_moves_to_waypoint_and_waypoint_offset_does_not_change(self):
        ship = WaypointShip()

        ship.navigate("F10")
        self.assertEqual(ship.position, travel.Coordinate(100, 10))
        self.assertEqual(ship.waypoint_position, {"east": 10, "north": 1})

    def test_two_steps_of_example(self):
        ship = WaypointShip()

        ship.navigate("F10")
        ship.navigate("N3")

        self.assertEqual(ship.position, travel.Coordinate(100, 10))
        self.assertEqual(ship.waypoint_position, {"east": 10, "north": 4})

    def test_three_steps_of_example(self):
        ship = WaypointShip()

        ship.navigate("F10")
        ship.navigate("N3")
        ship.navigate("F7")

        self.assertEqual(ship.position, travel.Coordinate(170, 38))
        self.assertEqual(ship.waypoint_position, {"east": 10, "north": 4})

    def test_four_steps_of_example(self):
        ship = WaypointShip()

        ship.navigate("F10")
        ship.navigate("N3")
        ship.navigate("F7")
        ship.navigate("R90")

        self.assertEqual(ship.position, travel.Coordinate(170, 38))
        self.assertEqual(ship.waypoint_position, {"south": 10, "east": 4})

    def test_whole_example(self):
        ship = WaypointShip()

        ship.navigate("F10")
        ship.navigate("N3")
        ship.navigate("F7")
        ship.navigate("R90")
        ship.navigate("F11")

        self.assertEqual(ship.position, travel.Coordinate(214, -72))
        self.assertEqual(ship.manhattan_distance_travelled(), 286)

    def test_ship_following_puzzle_input(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            puzzle_input = [
                s.strip() for s
                in content.read().splitlines()
                if len(s.strip()) > 0
            ]

        ship = WaypointShip()

        for i in puzzle_input:
            ship.navigate(i)

        self.assertLess(ship.manhattan_distance_travelled(), 49854)
        self.assertEqual(ship.manhattan_distance_travelled(), 1007)
