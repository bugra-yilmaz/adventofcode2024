import argparse
import os.path
from itertools import product

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

N_MAX_TRIES = 100
COST_A = 3
COST_B = 1


def get_machines(s: str) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    machines = []
    (a_x, a_y), (b_x, b_y), (p_x, p_y) = (0, 0), (0, 0), (0, 0)
    count = 0
    for line in s.splitlines():
        if line == '':
            machine = ((a_x, a_y), (b_x, b_y), (p_x, p_y))
            machines.append(machine)
            count = 0
            continue
        if count == 0:
            a_x = int(line.split('X+')[1].split(',')[0])
            a_y = int(line.split('Y+')[1])
        elif count == 1:
            b_x = int(line.split('X+')[1].split(',')[0])
            b_y = int(line.split('Y+')[1])
        elif count == 2:
            p_x = int(line.split('X=')[1].split(',')[0])
            p_y = int(line.split('Y=')[1])
        count += 1
    machine = ((a_x, a_y), (b_x, b_y), (p_x, p_y))
    machines.append(machine)

    return machines


def get_min_cost_win(machine: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]) -> int:
    (a_x, a_y), (b_x, b_y), (p_x, p_y) = machine
    min_cost_win = None
    for n_a, n_b in product(range(N_MAX_TRIES + 1), range(N_MAX_TRIES + 1)):
        x = a_x * n_a + b_x * n_b
        y = a_y * n_a + b_y * n_b
        if x == p_x and y == p_y:
            cost = n_a * COST_A + n_b * COST_B
            if not min_cost_win:
                min_cost_win = cost
            else:
                min_cost_win = min(min_cost_win, cost)
    if not min_cost_win:
        min_cost_win = 0

    return min_cost_win


def compute(s: str) -> int:
    machines = get_machines(s)
    return sum(get_min_cost_win(machine) for machine in machines)


INPUT_S = '''\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''
EXPECTED = 480


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
