import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

N = 100
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


def get_robot_position(robot: tuple[tuple[int, int], tuple[int, int]], w: int, t: int) -> tuple[int, int]:
    (position_x, position_y), (velocity_x, velocity_y) = robot
    position_x = (position_x + N * velocity_x) % w
    position_y = (position_y + N * velocity_y) % t
    return position_x, position_y


def compute(s: str, w: int, t: int) -> int:
    robots = get_robots(s)
    robots_after = [get_robot_position(robot, w, t) for robot in robots]

    mid_w = w // 2
    mid_t = t // 2

    q1 = sum(1 for robot_x, robot_y in robots_after if robot_x < mid_w and robot_y < mid_t)
    q2 = sum(1 for robot_x, robot_y in robots_after if robot_x > mid_w and robot_y < mid_t)
    q3 = sum(1 for robot_x, robot_y in robots_after if robot_x < mid_w and robot_y > mid_t)
    q4 = sum(1 for robot_x, robot_y in robots_after if robot_x > mid_w and robot_y > mid_t)

    return q1 * q2 * q3 * q4


INPUT_S = '''\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''
INPUT_W = 11
INPUT_T = 7
EXPECTED = 12


@pytest.mark.parametrize(
    ('input_s', 'input_w', 'input_t', 'expected'),
    (
        (INPUT_S, INPUT_W, INPUT_T, EXPECTED),
    ),
)
def test(input_s: str, input_w: int, input_t: int,  expected: int) -> None:
    assert compute(input_s, input_w, input_t) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read(), W, T))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
