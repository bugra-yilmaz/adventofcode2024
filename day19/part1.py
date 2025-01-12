import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    towels_s, designs_s = s.split('\n\n')
    towels = towels_s.split(', ')
    designs = designs_s.splitlines()
    max_towel_size = max(map(len, towels))

    count = 0
    for design in designs:
        possible = ['']
        while possible:
            current = possible.pop()
            if current == design:
                count += 1
                break

            index = len(current)
            for i in range(1, max_towel_size + 1):
                if index + i > len(design):
                    continue

                stripe = design[index: index+i]
                if stripe in towels:
                    possible.append(current + stripe)

    return count


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
EXPECTED = 6


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
