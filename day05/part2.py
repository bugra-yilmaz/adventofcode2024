import argparse
import os.path
from collections import defaultdict

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    parse_rules = True
    rules = defaultdict(set)
    orderings = []
    for line in s.splitlines():
        if line == '':
            parse_rules = False
            continue

        if parse_rules:
            number_before, number_after = list(map(int, line.split('|')))
            rules[number_before].add(number_after)
        else:
            ordering = list(map(int, line.split(',')))
            orderings.append(ordering)

    sum_ = 0
    k = 0
    fail_k = -1
    while k < len(orderings):
        ordering = orderings[k]
        print(ordering)

        fail = False
        for i in range(len(ordering) - 1):
            number_first = ordering[i]

            for j in range(i+1, len(ordering)):
                number_after = ordering[j]

                if number_first in rules[number_after]:
                    fail = True
                    fail_k = k
                    ordering[i] = number_after
                    ordering[j] = number_first
                    break

            if fail:
                break

        if not fail and fail_k == k:
            n = ordering[len(ordering) // 2]
            sum_ += n

        if not fail:
            k += 1

    return sum_


INPUT_S = '''\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''
EXPECTED = 123


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
