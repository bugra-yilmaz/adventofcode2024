import argparse
import os.path
import re

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    do_pattern = re.compile(r'do\(\)')
    dont_pattern = re.compile(r"don't\(\)")
    dos = [match.start() for match in re.finditer(do_pattern, s)]
    donts = [match.start() for match in re.finditer(dont_pattern, s)]

    invalid_parts = []
    previous_next_do = 0
    for dont in donts:
        dos = [do for do in dos if do > dont]
        next_do = min(dos) if dos else None
        if next_do:
            if next_do == previous_next_do:
                continue
            invalid_parts.append((dont, next_do))
            previous_next_do = next_do
        else:
            if previous_next_do == len(s):
                continue
            invalid_parts.append((dont, len(s)))
            previous_next_do = len(s)

    re_s = ''
    for i, c in enumerate(s):
        invalid = False
        for start, end in invalid_parts:
            if start <= i <= end:
                invalid = True
                break
        if not invalid:
            re_s += c

    pattern = re.compile(r'mul\(\d{,3},\d{,3}\)')
    matches = re.findall(pattern, re_s)

    sum_ = 0
    for match in matches:
        n1 = int(match.split('mul(')[1].split(',')[0])
        n2 = int(match.split(',')[1].split(')')[0])
        sum_ += n1 * n2

    return sum_


INPUT_S = '''\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
'''
EXPECTED = 48


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
