import argparse
import os.path
from collections import defaultdict

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_neighbours(
    row_index: int,
    col_index: int,
    row_count: int,
    col_count: int,
    grid: list[list[str]],
) -> list[tuple[int, int]]:
    neighbours = []
    for row_diff, col_diff in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        neighbour_row_index, neighbour_col_index = row_index + row_diff, col_index + col_diff
        if (-1 < neighbour_row_index < row_count) and (-1 < neighbour_col_index < col_count):
            if grid[row_index][col_index] == grid[neighbour_row_index][neighbour_col_index]:
                neighbours.append((neighbour_row_index, neighbour_col_index))

    return neighbours


def update_neighbours(
    position: tuple[int, int],
    region_id: int,
    regions: dict[int: list[tuple[int, int]]],
    row_count: int,
    col_count: int,
    grid: list[list[str]],
):
    row_index, col_index = position
    neighbours = get_neighbours(row_index, col_index, row_count, col_count, grid)
    for neighbour in neighbours:
        if neighbour not in regions:
            regions[neighbour] = region_id
            update_neighbours(neighbour, region_id, regions, row_count, col_count, grid)
    return


def get_corners(position: tuple[int, int]) -> list[tuple[int, int]]:
    diffs = [(1, 0), (0, 1), (1, 1)]
    corners = [position]
    for diff_row, diff_col in diffs:
        corner = position[0] + diff_row, position[1] + diff_col
        corners.append(corner)

    return corners


def get_number_of_sides(region: list[tuple[int, int]]) -> int:
    corner_counts = defaultdict(int)
    for position in region:
        corners = get_corners(position)
        for corner in corners:
            corner_counts[corner] += 1

    region_corners = [corner for corner, count in corner_counts.items() if count % 2 == 1]
    additional_region_corners = [
        corner for corner, count in corner_counts.items()
        if count == 2 and (corner in region and (corner[0] - 1, corner[1] - 1) in region)
    ]
    region_corners += 2 * additional_region_corners
    n_sides = len(region_corners)

    return n_sides


def compute(s: str) -> int:
    grid = [list(row) for row in s.splitlines()]
    row_count = len(grid)
    col_count = len(grid[0])

    regions = defaultdict(int)
    region_id = 1
    for row_index, row in enumerate(grid):
        for col_index, letter in enumerate(row):
            position = row_index, col_index
            if position in regions:
                continue

            neighbours = get_neighbours(row_index, col_index, row_count, col_count, grid)
            neighbour_regions = {regions[neighbour] for neighbour in neighbours if neighbour in regions}
            if len(neighbour_regions) > 1:
                raise ValueError(
                    f"More than one region for same letter neighbours: {neighbours}, "
                    f"regions: {neighbour_regions}",
                )
            elif len(neighbour_regions) == 1:
                region_id_existing = neighbour_regions.pop()
                regions[position] = region_id_existing
                for neighbour in neighbours:
                    if neighbour not in regions:
                        regions[neighbour] = region_id_existing
                        update_neighbours(neighbour, region_id_existing, regions, row_count, col_count, grid)
            else:
                regions[position] = region_id
                for neighbour in neighbours:
                    if neighbour not in regions:
                        regions[neighbour] = region_id
                        update_neighbours(neighbour, region_id, regions, row_count, col_count, grid)
                region_id += 1

    regions_r = {}
    for position, region_id in regions.items():
        if region_id in regions_r:
            regions_r[region_id].append(position)
        else:
            regions_r[region_id] = [position]
    regions = regions_r

    result = sum(get_number_of_sides(region) * len(region) for region in regions.values())

    return result


INPUT_S1 = '''\
AAAA
BBCD
BBCC
EEEC
'''
EXPECTED1 = 80

INPUT_S2 = '''\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
'''
EXPECTED2 = 236

INPUT_S3 = '''\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
'''
EXPECTED3 = 368

INPUT_S4 = '''\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''
EXPECTED4 = 1206


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S1, EXPECTED1),
        (INPUT_S2, EXPECTED2),
        (INPUT_S3, EXPECTED3),
        (INPUT_S4, EXPECTED4),
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
