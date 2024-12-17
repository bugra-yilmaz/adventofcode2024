import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

W = 101
T = 103


def get_robots(s: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    robots = []
    for line in s.splitlines():
        position_x, position_y = list(map(int, line.split()[0].split('=')[1].split(',')))
        velocity_x, velocity_y = list(map(int, line.split()[1].split('=')[1].split(',')))
        robot = (position_x, position_y), (velocity_x, velocity_y)
        robots.append(robot)
    return robots


def get_robot_position(robot: tuple[tuple[int, int], tuple[int, int]], w: int, t: int, n: int) -> tuple[int, int]:
    (position_x, position_y), (velocity_x, velocity_y) = robot
    position_x = (position_x + n * velocity_x) % w
    position_y = (position_y + n * velocity_y) % t
    return position_x, position_y


def get_consecutive_count(robot_positions: list[tuple[int, int]], y: int, w: int) -> int:
    consecutive_max = 0
    consecutive = 0
    for x in range(w):
        if (x, y) in robot_positions:
            consecutive += 1
        else:
            consecutive_max = max(consecutive_max, consecutive)
            consecutive = 0
    return consecutive_max


def display(robot_positions: list[tuple[int, int]], w: int, t: int):
    s = ''
    for y in range(t):
        for x in range(w):
            c = robot_positions.count((x, y))
            if c == 0:
                s += '.'
            else:
                s += str(c)
        s += '\n'
    print(s)


def compute(s: str, w: int, t: int) -> int:
    robots = get_robots(s)
    c, index = 0, -1
    for i in range(10000):
        robot_positions = [get_robot_position(robot, w, t, i+1) for robot in robots]
        c_i = max(get_consecutive_count(robot_positions, y, w) for y in range(t))
        if c_i > c:
            c = c_i
            index = i
            display(robot_positions, w, t)

    return index + 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read(), W, T))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
