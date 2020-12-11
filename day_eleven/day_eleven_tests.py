import os
import unittest
from files.reader import get_puzzle_input_path


class Grid:

    def __init__(self, grid_description: str) -> None:
        try:
            self.grid_description = grid_description.strip()
        except AttributeError as ae:
            print(f"could not strip description: {grid_description}")
            raise ae

        self.rows = [line.strip() for line
                     in grid_description.splitlines()
                     if line and len(line.strip()) > 0]
        self.height = len(self.rows)
        self.width = len(self.rows[0])

    def get(self, x: int, y: int) -> str:
        if x < 0 or y < 0:
            return None

        if x >= self.width or y >= self.height:
            return None

        row = self.rows[y]
        return row[x]

    def adjacent_to(self, x: int, y: int) -> list[str]:
        return [c for c in [
            self.get(x - 1, y),
            self.get(x - 1, y - 1),
            self.get(x, y - 1),
            self.get(x + 1, y - 1),
            self.get(x + 1, y),
            self.get(x + 1, y + 1),
            self.get(x, y + 1),
            self.get(x - 1, y + 1)
        ] if c]

    def tick(self):
        copied = list(map(list, self.rows))

        for x in range(0, self.width):
            for y in range(0, self.height):
                seat = self.get(x, y)
                adjacents = self.adjacent_to(x, y)
                if seat == 'L':
                    if not any(x == '#' for x in adjacents):
                        copied[y][x] = '#'
                    #     print(f"""
                    # adjacents: {adjacents}
                    # seat: {seat}
                    # now: {copied[y][x]}
                    # """)
                elif seat == '#':
                    if adjacents.count('#') >= 4:
                        copied[y][x] = 'L'

        described_rows = [''.join(x) for x in copied]
        description = '\n'.join(described_rows)
        return Grid(description)

    def occupied_seats(self) -> int:
        return self.grid_description.count('#')

    def __hash__(self):
        return self.grid_description.__hash__()

    def __eq__(self, o: object) -> bool:
        return self.grid_description == o.grid_description

    def __repr__(self) -> str:
        return self.grid_description


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

        expected = Grid("""#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##""").grid_description

        actual = next_grid.grid_description

        self.assertMultiLineEqual(expected, actual)

    def test_can_model_a_second_round(self):
        grid = Grid(example_input)
        next_grid = grid.tick().tick()
        self.assertMultiLineEqual(next_grid.grid_description, Grid("""
        #.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##""").grid_description)

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
