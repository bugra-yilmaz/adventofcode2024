import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_report_safe(report: list[int]) -> bool:
    if report[1] > report[0]:
        for i in range(1, len(report)):
            if report[i] - report[i - 1] < 1 or report[i] - report[i - 1] > 3:
                return False
    else:
        for i in range(1, len(report)):
            if report[i] - report[i - 1] > -1 or report[i] - report[i - 1] < -3:
                return False

    return True


def compute(s: str) -> int:
    reports = []
    for line in s.splitlines():
        report = list(map(int, line.split()))
        reports.append(report)

    count = 0
    for report in reports:
        count += is_report_safe(report)

    return count


INPUT_S = '''\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''
EXPECTED = 2


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
