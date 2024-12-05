import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def check_xmas(row_index, col_index, grid):
    row_count = len(grid)
    col_count = len(grid[0])

    if (row_index + 1 >= row_count) or (row_index - 1 < 0) or \
            (col_index + 1 >= col_count) or (col_index - 1 < 0):
        return False

    word1 = ''.join([
        grid[row_index - 1][col_index - 1],
        grid[row_index][col_index],
        grid[row_index + 1][col_index + 1],
    ])
    word2 = ''.join([
        grid[row_index + 1][col_index + 1],
        grid[row_index][col_index],
        grid[row_index - 1][col_index - 1],
    ])
    if word1 != 'MAS' and word2 != 'MAS':
        return False

    word3 = ''.join([
        grid[row_index + 1][col_index - 1],
        grid[row_index][col_index],
        grid[row_index - 1][col_index + 1],
    ])
    word4 = ''.join([
        grid[row_index - 1][col_index + 1],
        grid[row_index][col_index],
        grid[row_index + 1][col_index - 1],
    ])
    if word3 != 'MAS' and word4 != 'MAS':
        return False

    return True


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
            if letter != 'A':
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
EXPECTED = 9


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
