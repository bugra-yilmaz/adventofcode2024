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
    paths = [(start, direction, cost)]
    costs = {(start, direction): cost}

    while paths:
        path = paths.pop(0)
        position, direction, cost = path

        position_row, position_col = position
        direction_row, direction_col = direction
        next_position_row, next_position_col = position_row + direction_row, position_col + direction_col

        # forward
        if grid[next_position_row][next_position_col] == '.':
            next_position = next_position_row, next_position_col
            next_cost = cost + 1
            if (next_position, direction) not in costs or next_cost < costs[(next_position, direction)]:
                costs[(next_position, direction)] = next_cost
                next_path = (next_position, direction, next_cost)
                paths.append(next_path)

        # rotate c
        next_direction_rc = get_direction_r_c(direction)
        next_cost = cost + 1000
        if (position, next_direction_rc) not in costs or next_cost < costs[(position, next_direction_rc)]:
            costs[(position, next_direction_rc)] = next_cost
            next_path = (position, next_direction_rc, next_cost)
            paths.append(next_path)

        # rotate cc
        next_direction_rcc = get_direction_r_cc(direction)
        next_cost = cost + 1000
        if (position, next_direction_rcc) not in costs or next_cost < costs[(position, next_direction_rcc)]:
            costs[(position, next_direction_rcc)] = next_cost
            next_path = (position, next_direction_rcc, next_cost)
            paths.append(next_path)

    return min(cost for (position, _), cost in costs.items() if position == end)


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
EXPECTED1 = 7036

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
EXPECTED2 = 11048


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
