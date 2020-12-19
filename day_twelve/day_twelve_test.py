import unittest
import os
from files.reader import get_puzzle_input_path
import day_eleven.travel as travel


class FreeFloatingShip:
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
        self.heading: str = "east"

    def manhattan_distance_travelled(self) -> int:
        return abs(self.position.x) + abs(self.position.y)

    def navigate(self, instruction: str) -> None:
        action = instruction[0]
        value = int(instruction[1:])

        def move(direction: str, times: int) -> None:
            for _ in range(0, times):
                self.position = travel.move[direction](self.position)

        def rotate_right(times):
            for _ in range(0, times):
                self.heading = self.turn_right_from[self.heading]

        def rotate_left(times):
            for _ in range(0, times):
                self.heading = self.turn_left_from[self.heading]

        if action == "F":
            move(self.heading, value)
        elif action == "N":
            move("north", value)
        elif action == "E":
            move("east", value)
        elif action == "S":
            move("south", value)
        elif action == "W":
            move("west", value)
        elif action == "R":
            rotate_right(value // 90)
        elif action == "L":
            rotate_left(value // 90)
        else:
            raise Exception(f"unknown action {action}")


class DayTwelveTests(unittest.TestCase):

    def test_ship_starts_at_zero(self):
        ship = FreeFloatingShip()
        self.assertEqual(ship.position, travel.Coordinate(0, 0))
        self.assertEqual(ship.heading, "east")

    def test_ship_can_move_forward(self):
        ship = FreeFloatingShip()
        ship.navigate("F1")
        self.assertEqual(ship.position, travel.Coordinate(1, 0))
        self.assertEqual(ship.heading, "east")

    def test_ship_can_move_north(self):
        ship = FreeFloatingShip()
        ship.navigate("N1")
        self.assertEqual(ship.position, travel.Coordinate(0, -1))
        self.assertEqual(ship.heading, "east")

    def test_ship_can_move_east(self):
        ship = FreeFloatingShip()
        ship.navigate("E1")
        self.assertEqual(ship.position, travel.Coordinate(1, 0))
        self.assertEqual(ship.heading, "east")

    def test_ship_can_move_south(self):
        ship = FreeFloatingShip()
        ship.navigate("S1")
        self.assertEqual(ship.position, travel.Coordinate(0, 1))
        self.assertEqual(ship.heading, "east")

    def test_ship_can_move_west(self):
        ship = FreeFloatingShip()
        ship.navigate("W1")
        self.assertEqual(ship.position, travel.Coordinate(-1, 0))
        self.assertEqual(ship.heading, "east")

    def test_ship_can_move_west_more_than_one(self):
        ship = FreeFloatingShip()
        ship.navigate("W3")
        self.assertEqual(ship.position, travel.Coordinate(-3, 0))
        self.assertEqual(ship.heading, "east")

    def test_ship_can_rotate(self):
        ship = FreeFloatingShip()
        ship.navigate("R90")
        self.assertEqual(ship.heading, "south")

    def test_ship_can_rotate_twice(self):
        ship = FreeFloatingShip()
        ship.navigate("R180")
        self.assertEqual(ship.heading, "west")

    def test_ship_can_rotate_thrice(self):
        ship = FreeFloatingShip()
        ship.navigate("R270")
        self.assertEqual(ship.heading, "north")

    def test_ship_can_rotate_frice(self):
        ship = FreeFloatingShip()
        ship.navigate("R360")
        self.assertEqual(ship.heading, "east")

    def test_ship_can_rotate_left(self):
        ship = FreeFloatingShip()
        ship.navigate("L90")
        self.assertEqual(ship.heading, "north")

        ship.navigate("R90")
        ship.navigate("L180")
        self.assertEqual(ship.heading, "west")

        ship.navigate("L90")
        self.assertEqual(ship.heading, "south")

    def test_ship_can_rotate_and_move(self):
        ship = FreeFloatingShip()
        ship.navigate("R180")
        ship.navigate("F4")
        self.assertEqual(ship.heading, "west")
        self.assertEqual(ship.position, travel.Coordinate(-4, 0))

    def test_ship_following_example_instructions(self):
        example = [
            "F10",
            "N3",
            "F7",
            "R90",
            "F11"
        ]
        ship = FreeFloatingShip()

        for i in example:
            ship.navigate(i)

        self.assertEqual(ship.heading, "south")
        self.assertEqual(ship.position, travel.Coordinate(17, 8))
        self.assertEqual(ship.manhattan_distance_travelled(), 25)

    def test_ship_following_puzzle_input(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            puzzle_input = [
                s.strip() for s
                in content.read().splitlines()
                if len(s.strip()) > 0
            ]

        ship = FreeFloatingShip()

        for i in puzzle_input:
            ship.navigate(i)

        self.assertEqual(ship.manhattan_distance_travelled(), 1007)
