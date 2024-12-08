import argparse
import os.path
from collections import defaultdict
from itertools import combinations
from math import gcd

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_antinodes(
    position1: tuple[int, int],
    position2: tuple[int, int],
    row_count: int,
    col_count: int,
) -> set[tuple[int, int]]:

    diff = position2[0] - position1[0], position2[1] - position1[1]
    diff_gcd = gcd(diff[0], diff[1])
    diff = int(diff[0] / diff_gcd), int(diff[1] / diff_gcd)

    antinodes = set()

    out = False
    i = 1
    while not out:
        antinode_row = position2[0] - i * diff[0]
        antinode_col = position2[1] - i * diff[1]
        if -1 < antinode_row < row_count and -1 < antinode_col < col_count:
            antinodes.add((antinode_row, antinode_col))
            i += 1
        else:
            out = True

    out = False
    i = 1
    while not out:
        antinode_row = position2[0] + i * diff[0]
        antinode_col = position2[1] + i * diff[1]
        if -1 < antinode_row < row_count and -1 < antinode_col < col_count:
            antinodes.add((antinode_row, antinode_col))
            i += 1
        else:
            out = True

    antinodes.add(position1)
    antinodes.add(position2)

    return antinodes


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
        pairs = list(combinations(positions, 2))
        for pair in pairs:
            pair_antinodes = get_antinodes(pair[0], pair[1], row_count, col_count)
            antinodes = antinodes.union(pair_antinodes)

    return len(antinodes)


INPUT_S1 = '''\
T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........
'''
EXPECTED1 = 9

INPUT_S2 = '''\
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
EXPECTED2 = 34


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
