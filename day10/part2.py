import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def get_trail_count(start: tuple[int, int], grid: list[list[int]], row_count: int, col_count: int) -> int:
    trails = []

    paths = [[start]]
    while len(paths) > 0:
        path = paths.pop(0)

        end = path[-1]
        end_row, end_col = end
        value_end = grid[end_row][end_col]

        for direction in DIRECTIONS:
            direction_row, direction_col = direction
            position = end_row + direction_row, end_col + direction_col
            position_row, position_col = position

            if not (-1 < position_row < row_count and -1 < position_col < col_count):
                continue

            value_position = grid[position_row][position_col]

            if value_position == value_end + 1:
                if value_position == 9:
                    trails.append(path + [position])
                    continue

                paths.append(path + [position])

    return len(trails)


def compute(s: str) -> int:
    grid = s.splitlines()
    grid = [[int(n) for n in row] for row in grid]
    row_count = len(grid)
    col_count = len(grid[0])
    starts = [(row_index, col_index) for row_index, row in enumerate(grid) for col_index, n in enumerate(row) if n == 0]

    sum_ = 0
    for start in starts:
        sum_ += get_trail_count(start, grid, row_count, col_count)

    return sum_


INPUT_S = '''\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''
EXPECTED = 81


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
