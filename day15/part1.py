import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRECTIONS = {'<': (0, -1), '>': (0, 1), 'v': (1, 0), '^': (-1, 0)}


def parse_grid(grid_rows: list[list[str]]) -> tuple[dict[tuple[int, int], str], tuple[int, int]]:
    grid = {}
    robot_row, robot_col = 0, 0
    for row_index, row in enumerate(grid_rows):
        for col_index, cell in enumerate(row):
            if cell == '#':
                grid[(row_index, col_index)] = 'wall'
            elif cell == 'O':
                grid[(row_index, col_index)] = 'box'
            elif cell == '@':
                grid[(row_index, col_index)] = 'robot'
                robot_row, robot_col = row_index, col_index
            else:
                grid[(row_index, col_index)] = 'free'

    return grid, (robot_row, robot_col)


def execute_move(
    robot: tuple[int, int],
    move: tuple[int, int],
    grid: dict[tuple[int, int], str],
) -> tuple[int, int]:
    robot_row, robot_col = robot
    move_row, move_col = move
    boxes_to_move = []
    can_move = False
    while True:
        robot_row, robot_col = robot_row + move_row, robot_col + move_col

        if grid[(robot_row, robot_col)] == 'free':
            can_move = True
            break

        if grid[(robot_row, robot_col)] == 'box':
            boxes_to_move.append((robot_row, robot_col))

        if grid[(robot_row, robot_col)] == 'wall':
            break

    if can_move:
        grid[robot] = 'free'
        for box in boxes_to_move:
            grid[box] = 'free'

        robot_row, robot_col = robot
        grid[(robot_row + move_row, robot_col + move_col)] = 'robot'

        for box_row, box_col in boxes_to_move:
            grid[(box_row + move_row, box_col + move_col)] = 'box'

        return robot_row + move_row, robot_col + move_col

    else:
        return robot


def get_box_coordinate(box: tuple[int, int]) -> int:
    row, col = box
    return 100 * row + col


def compute(s: str) -> int:
    grid_s = s.split('\n\n')[0].splitlines()
    grid_rows = [list(line) for line in grid_s]
    grid, robot = parse_grid(grid_rows)

    moves_s = s.split('\n\n')[1].splitlines()
    moves = [DIRECTIONS[move] for line in moves_s for move in line]

    for move in moves:
        robot = execute_move(robot, move, grid)

    boxes = [(row, col) for (row, col), value in grid.items() if value == 'box']
    return sum(get_box_coordinate(box) for box in boxes)


INPUT_S1 = '''\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
'''
EXPECTED1 = 2028

INPUT_S2 = '''\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''
EXPECTED2 = 10092


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S1, EXPECTED1),
        (INPUT_S2, EXPECTED2),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
