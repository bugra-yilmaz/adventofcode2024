import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_new_direction(direction):
    if direction == (-1, 0):
        return 0, 1
    elif direction == (0, 1):
        return 1, 0
    elif direction == (1, 0):
        return 0, -1
    elif direction == (0, -1):
        return -1, 0
    else:
        raise ValueError(f"Invalid direction: {direction}")


def compute(s: str) -> int:
    grid = s.splitlines()

    obstacles = set()
    row_count = len(grid)
    col_count = len(grid[0])
    start = 0, 0
    direction = (0, 0)
    for row, line in enumerate(grid):
        for col, c in enumerate(line):
            if c == '#':
                obstacles.add((row, col))
            elif c == '^':
                start = row, col
                direction = (-1, 0)

    visits = set()
    position_row, position_col = start
    while -1 < position_row < row_count and -1 < position_col < col_count:
        visits.add((position_row, position_col))

        new_position = position_row + direction[0], position_col + direction[1]
        if new_position in obstacles:
            direction = get_new_direction(direction)
            continue

        position_row, position_col = new_position

    return len(visits)


INPUT_S = '''\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''
EXPECTED = 41


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
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
