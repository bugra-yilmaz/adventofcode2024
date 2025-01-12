import argparse
import os.path
from functools import cache

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    towels_s, designs_s = s.split('\n\n')
    towels = set(towels_s.split(', '))
    designs = designs_s.splitlines()

    @cache
    def count_possibilities(design: str) -> int:
        if not design:
            return 1

        count = 0
        for towel in towels:
            if design.startswith(towel):
                count += count_possibilities(design[len(towel):])
        return count

    return sum(count_possibilities(design) for design in designs)


INPUT_S = '''\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''
EXPECTED = 16


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
