import argparse
import os.path
from collections import defaultdict
from itertools import permutations

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_antinode(position1: tuple[int, int], position2: tuple[int, int]) -> tuple[int, int]:
    diff = position2[0] - position1[0], position2[1] - position1[1]
    antinode = position2[0] + diff[0], position2[1] + diff[1]

    return antinode


def compute(s: str) -> int:
    grid = s.splitlines()
    row_count = len(grid)
    col_count = len(grid[0])

    antennas = defaultdict(list)
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            if col != '.':
                antennas[col].append((row_index, col_index))

    antinodes = set()
    for antenna, positions in antennas.items():
        pairs = list(permutations(positions, 2))
        for pair in pairs:
            antinode = get_antinode(pair[0], pair[1])
            if -1 < antinode[0] < row_count and -1 < antinode[1] < col_count:
                antinodes.add(antinode)

    return len(antinodes)


INPUT_S = '''\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''
EXPECTED = 14


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
