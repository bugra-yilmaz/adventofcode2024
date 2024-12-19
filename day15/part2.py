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
            elif cell == '[':
                grid[(row_index, col_index)] = 'box_left'
                grid[(row_index, col_index + 1)] = 'box_right'
            elif cell == '@':
                grid[(row_index, col_index)] = 'robot'
                robot_row, robot_col = row_index, col_index
            elif cell == '.':
                grid[(row_index, col_index)] = 'free'

    return grid, (robot_row, robot_col)


def can_box_move(
    box_left: tuple[int, int],
    move_row: int,
    grid: dict[tuple[int, int], str],
) -> tuple[bool, set[tuple[int, int]]]:
    box_left_row, box_left_col = box_left
    box_right_row, box_right_col = box_left_row, box_left_col + 1
    box_left_next = box_left_row + move_row, box_left_col
    box_right_next = box_right_row + move_row, box_right_col

    boxes_to_move = set()
    if grid[box_left_next] == 'free' and grid[box_right_next] == 'free':
        return True, boxes_to_move
    elif grid[box_left_next] == 'wall' or grid[box_right_next] == 'wall':
        return False, boxes_to_move

    can_moves = []
    if grid[box_left_next] == 'box_left':
        can_move, boxes = can_box_move(box_left_next, move_row, grid)
        boxes_to_move |= boxes
        can_moves.append(can_move)
    elif grid[box_left_next] == 'box_right':
        box_left_next_row, box_left_next_col = box_left_next
        next_box = box_left_next_row, box_left_next_col - 1
        can_move, boxes = can_box_move(next_box, move_row, grid)
        boxes_to_move |= boxes
        can_moves.append(can_move)
    if grid[box_right_next] == 'box_left':
        can_move, boxes = can_box_move(box_right_next, move_row, grid)
        boxes_to_move |= boxes
        can_moves.append(can_move)

    return all(can_moves), boxes_to_move


def execute_move(
    robot: tuple[int, int],
    move: tuple[int, int],
    grid: dict[tuple[int, int], str],
) -> tuple[int, int]:
    robot_row, robot_col = robot
    move_row, move_col = move
    boxes_to_move = set()
    can_move = False
    while True:
        robot_row, robot_col = robot_row + move_row, robot_col + move_col

        if grid[(robot_row, robot_col)] == 'free':
            can_move = True
            break

        if grid[(robot_row, robot_col)].startswith('box'):
            if move == (1, 0) or move == (-1, 0):  # moving vertically
                if grid[(robot_row, robot_col)] == 'box_left':
                    box_left = (robot_row, robot_col)
                else:
                    box_left = (robot_row, robot_col - 1)
                box_right = box_left[0], box_left[1] + 1
                affected_boxes = [(box_left, 'box_left'), (box_right, 'box_right')]
                affected_cells = [box_left, box_right]
                can_move_vertical = True
                while affected_cells:
                    row, col = affected_cells.pop(0)
                    row = row + move[0]

                    if grid[(row, col)] == 'wall':
                        can_move_vertical = False
                        break

                    if grid[(row, col)] == 'free':
                        continue

                    if grid[(row, col)].startswith('box'):
                        if grid[(row, col)] == 'box_left':
                            box_left = (row, col)
                        else:
                            box_left = (row, col - 1)
                        box_right = box_left[0], box_left[1] + 1
                        affected_boxes.append((box_left, 'box_left'))
                        affected_boxes.append((box_right, 'box_right'))
                        affected_cells.append(box_left)
                        affected_cells.append(box_right)

                if can_move_vertical:
                    boxes_to_move = affected_boxes
                    can_move = True
                break

            else:  # moving horizontally, add the box's other half
                if move == (0, 1):
                    boxes_to_move.add(((robot_row, robot_col), 'box_left'))
                    boxes_to_move.add(((robot_row, robot_col + 1), 'box_right'))
                else:
                    boxes_to_move.add(((robot_row, robot_col), 'box_right'))
                    boxes_to_move.add(((robot_row, robot_col - 1), 'box_left'))
                robot_row, robot_col = robot_row + move_row, robot_col + move_col

        if grid[(robot_row, robot_col)] == 'wall':
            break

    if can_move:
        grid[robot] = 'free'
        for box, _ in boxes_to_move:
            grid[box] = 'free'

        robot_row, robot_col = robot
        grid[(robot_row + move_row, robot_col + move_col)] = 'robot'

        for (box_row, box_col), box_s in boxes_to_move:
            grid[(box_row + move_row, box_col + move_col)] = box_s

        return robot_row + move_row, robot_col + move_col

    else:
        return robot


def get_box_coordinate(box: tuple[int, int]) -> int:
    row, col = box
    return 100 * row + col


def display(grid: dict[tuple[int, int], str], row_count: int, col_count: int):
    s = ''
    for row_index in range(row_count):
        for col_index in range(col_count):
            if grid[(row_index, col_index)] == 'free':
                s += '.'
            elif grid[(row_index, col_index)] == 'wall':
                s += '#'
            elif grid[(row_index, col_index)] == 'box_left':
                s += '['
            elif grid[(row_index, col_index)] == 'box_right':
                s += ']'
            elif grid[(row_index, col_index)] == 'robot':
                s += '@'
        s += '\n'
    print(s)


def compute(s: str) -> int:
    s = s.replace('#', '##')
    s = s.replace('O', '[]')
    s = s.replace('.', '..')
    s = s.replace('@', '@.')

    grid_s = s.split('\n\n')[0].splitlines()
    grid_rows = [list(line) for line in grid_s]
    row_count, col_count = len(grid_rows), len(grid_rows[0])
    grid, robot = parse_grid(grid_rows)

    moves_s = s.split('\n\n')[1].splitlines()
    moves = [DIRECTIONS[move] for line in moves_s for move in line]

    for move in moves:
        robot = execute_move(robot, move, grid)

    boxes_left = [(row, col) for (row, col), value in grid.items() if value == 'box_left']
    return sum(get_box_coordinate(box) for box in boxes_left)


INPUT_TEST = '''\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
'''

INPUT_S1 = '''\
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
EXPECTED1 = 9021


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S1, EXPECTED1),
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
