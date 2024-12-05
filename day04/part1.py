import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def check_xmas(row_index, col_index, grid):
    row_count = len(grid)
    col_count = len(grid[0])

    count = 0
    for row_diff in [-1, 0, 1]:
        for col_diff in [-1, -0, 1]:
            if row_diff == 0 and col_diff == 0:
                continue

            if (row_index + row_diff >= row_count) or (row_index + row_diff < 0) or \
                    (col_index + col_diff >= col_count) or (col_index + col_diff < 0):
                continue

            neighbour = grid[row_index + row_diff][col_index + col_diff]
            if neighbour != 'M':
                continue

            if (row_index + 3 * row_diff >= row_count) or (row_index + 3 * row_diff < 0) or \
                    (col_index + 3 * col_diff >= col_count) or (col_index + 3 * col_diff < 0):
                continue

            word = ''.join(
                grid[row_index + i * row_diff][col_index + i * col_diff] for i in range(0, 4)
            )

            if word == 'XMAS':
                count += 1

    return count


def compute(s: str) -> int:
    grid = []
    for line in s.splitlines():
        row = []
        for letter in line:
            row.append(letter)
        grid.append(row)

    xmas_count = 0
    for row_index in range(len(grid)):
        for col_index in range(len(grid[0])):
            letter = grid[row_index][col_index]
            if letter != 'X':
                continue

            xmas_count += check_xmas(row_index, col_index, grid)

    return xmas_count


INPUT_S = '''\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''
EXPECTED = 18


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
