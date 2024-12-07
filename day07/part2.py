import argparse
import os.path
from copy import deepcopy

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def add(n1: int, n2: int) -> int:
    return n1 + n2


def mul(n1: int, n2: int) -> int:
    return n1 * n2


def com(n1: int, n2: int) -> int:
    return int(f"{n1}{n2}")


OPERATORS = add, mul, com


def solve(start: int, values: list[int], possible: set[int], target):
    if start > target or target in possible:
        return

    values_c = deepcopy(values)
    if not values_c:
        possible.add(start)
        return

    second = values_c.pop(0)
    for operator in OPERATORS:
        solve(operator(start, second), values_c, possible, target)


def check(target: int, values: list[int]) -> bool:
    possible = set()
    solve(values[0], values[1:], possible, target)

    return target in possible


def compute(s: str) -> int:
    sum_ = 0
    for line in s.splitlines():
        target_s, values_s = line.split(': ')
        target = int(target_s)
        values = list(map(int, values_s.split(' ')))
        if check(target, values):
            sum_ += target

    return sum_


INPUT_S = '''\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''
EXPECTED = 11387


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
