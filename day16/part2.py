import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def get_direction_r_c(direction: tuple[int, int]):
    index = DIRECTIONS.index(direction)
    next_index = (index + 1) % len(DIRECTIONS)
    return DIRECTIONS[next_index]


def get_direction_r_cc(direction: tuple[int, int]):
    index = DIRECTIONS.index(direction)
    next_index = (index - 1) % len(DIRECTIONS)
    return DIRECTIONS[next_index]


def compute(s: str) -> int:
    grid = [[cell for cell in line] for line in s.splitlines()]
    row_count = len(grid)
    col_count = len(grid[0])
    start_row, start_col = row_count - 2, 1
    grid[start_row][start_col] = '.'
    end_row, end_col = 1, col_count - 2
    grid[end_row][end_col] = '.'
    start = start_row, start_col
    end = end_row, end_col
    direction = (0, 1)
    cost = 0
    paths = [([start], direction, cost)]
    costs = {(start, direction): cost}
    end_paths = []

    while paths:
        path = paths.pop(0)
        positions, direction, cost = path
        position = positions[-1]

        position_row, position_col = position
        direction_row, direction_col = direction
        next_position_row, next_position_col = position_row + direction_row, position_col + direction_col

        # forward
        if grid[next_position_row][next_position_col] == '.':
            next_position = next_position_row, next_position_col
            next_cost = cost + 1
            if (next_position, direction) not in costs or next_cost <= costs[(next_position, direction)]:
                costs[(next_position, direction)] = next_cost
                next_path = (positions + [next_position], direction, next_cost)
                paths.append(next_path)
                if next_position == end:
                    end_paths.append(next_path)

        # rotate c
        next_direction_rc = get_direction_r_c(direction)
        next_cost = cost + 1000
        if (position, next_direction_rc) not in costs or next_cost <= costs[(position, next_direction_rc)]:
            costs[(position, next_direction_rc)] = next_cost
            next_path = (positions, next_direction_rc, next_cost)
            paths.append(next_path)

        # rotate cc
        next_direction_rcc = get_direction_r_cc(direction)
        next_cost = cost + 1000
        if (position, next_direction_rcc) not in costs or next_cost <= costs[(position, next_direction_rcc)]:
            costs[(position, next_direction_rcc)] = next_cost
            next_path = (positions, next_direction_rcc, next_cost)
            paths.append(next_path)

    min_cost = min(cost for (position, _), cost in costs.items() if position == end)
    best_paths = [path for (path, _, cost) in end_paths if cost == min_cost]
    best_path_tiles = set()
    for best_path in best_paths:
        best_path_tiles |= set(best_path)

    return len(best_path_tiles)


INPUT_S1 = '''\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''
EXPECTED1 = 45

INPUT_S2 = '''\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
'''
EXPECTED2 = 64


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
