from day_eleven.travel import Grid, LineOfSightAdjacentSeats
import os
import unittest
from files.reader import get_puzzle_input_path


example_input = """
        L.LL.LL.LL
        LLLLLLL.LL
        L.L.L..L..
        LLLL.LL.LL
        L.LL.LL.LL
        L.LLLLL.LL
        ..L.L.....
        LLLLLLLLLL
        L.LLLLLL.L
        L.LLLLL.LL"""


class DayElevenTests(unittest.TestCase):

    def test_can_init_grid_with_string_input(self):
        grid = Grid(example_input)

        self.assertEqual(grid.height, 10)
        self.assertEqual(grid.width, 10)

    def test_can_get_grid_cells_by_coordinate(self):
        grid = Grid(example_input)

        self.assertEqual(grid.get(0, 0), 'L')
        self.assertEqual(grid.get(1, 0), '.')
        self.assertEqual(grid.get(7, 1), '.')
        self.assertEqual(grid.get(7, 2), 'L')

    def test_can_get_adjacent_cells_by_coordinate_inside_grid(self):
        grid = Grid(example_input)

        self.assertEqual(grid.adjacent_to(3, 3), [
                         'L', 'L', '.', 'L', '.', '.', 'L', 'L'])
        self.assertEqual(grid.adjacent_to(6, 7), [
                         'L', '.', '.', '.', 'L', 'L', 'L', 'L'])

    def test_can_get_adjacent_cells_by_coordinate_at_edge_of_grid(self):
        grid = Grid(example_input)

        self.assertEqual(grid.adjacent_to(0, 3), ['L', '.', 'L', '.', 'L'])
        self.assertEqual(grid.adjacent_to(9, 1), ['L', 'L', 'L', '.', '.'])

    def test_grids_can_be_equal(self):
        self.assertEqual(Grid(example_input), Grid(example_input))

    def test_can_model_one_round(self):
        grid = Grid(example_input)
        next_grid = grid.tick()

# pep 8 putting spaces in the grid defined below
# cos it looked like a comment to the linter
# autopep8: off
        expected = Grid("""#.##.##.##
                        #######.##
                        #.#.#..#..
                        ####.##.##
                        #.##.##.##
                        #.#####.##
                        ..#.#.....
                        ##########
                        #.######.#
                        #.#####.##""")
        # autopep8: on

        actual = next_grid

        self.assertEqual(expected, actual)

    def test_can_model_a_second_round(self):
        grid = Grid(example_input)
        next_grid = grid.tick().tick()

# pep 8 putting spaces in the grid defined below
# cos it looked like a comment to the linter
# autopep8: off
        expected = Grid("""
                        #.LL.L#.##
                        #LLLLLL.L#
                        L.L.L..L..
                        #LLL.LL.L#
                        #.LL.LL.LL
                        #.LLLL#.##
                        ..L.L.....
                        #LLLLLLLL#
                        #.LLLLLL.L
                        #.#LLLL.##""")
# autopep8: on

        self.assertEqual(next_grid, expected)

    def test_can_stabilise_after_some_ticks(self):
        grid = Grid(example_input)
        x = grid.tick().tick().tick().tick().tick()
        y = x.tick()
        z = y.tick()
        self.assertEqual(x, y)
        self.assertEqual(y, z)

    def test_occupied_seats_when_map_stabilises(self):
        grid = Grid(example_input)
        next_grid = grid.tick()
        while grid != next_grid:
            grid = next_grid
            next_grid = next_grid.tick()

        self.assertEqual(next_grid.occupied_seats(), 37)

    def test_occupied_seats_after_puzzle_input_stabilizes(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            puzzle_input = content.read()

        grid = Grid(puzzle_input)
        next_grid = grid.tick()
        while grid != next_grid:
            grid = next_grid
            next_grid = next_grid.tick()

        self.assertEqual(next_grid.occupied_seats(), 2412)

    def test_can_find_adjacent_seats_by_ignoring_space(self):
        grid = Grid("""
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
# ........
...#.....
        """)

        self.assertEqual(grid.get(3, 4), 'L')
        adjacent_seats = LineOfSightAdjacentSeats.find(grid, 3, 4)
        self.assertEqual(adjacent_seats, [
                         '#', '#', '#', '#', '#', '#', '#', '#'])

    def test_can_find_adjacent_seats_second_example(self):
        grid = Grid("""
.............
.L.L.#.#.#.#.
.............
        """)

        self.assertEqual(grid.get(1, 1), 'L')
        adjacent_seats = LineOfSightAdjacentSeats.find(grid, 1, 1)
        self.assertEqual(adjacent_seats, ['L'])

    def test_occupied_seats_when_map_stabilises_part_two(self):
        grid = Grid(example_input, LineOfSightAdjacentSeats, 5)
        next_grid = grid.tick()
        while grid != next_grid:
            grid = next_grid
            next_grid = next_grid.tick()

        self.assertEqual(next_grid.occupied_seats(), 26)

    def test_occupied_seats_after_puzzle_input_stabilizes_part_two(self):
        with open(get_puzzle_input_path(os.path.dirname(__file__))) as content:
            puzzle_input = content.read()

        grid = Grid(puzzle_input, LineOfSightAdjacentSeats, 5)
        next_grid = grid.tick()
        while grid != next_grid:
            grid = next_grid
            next_grid = next_grid.tick()

        self.assertEqual(next_grid.occupied_seats(), 2176)
