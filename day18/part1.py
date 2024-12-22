import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

LENGTH = 71
COUNT = 1024

MOVES = ((0, 1), (0, -1), (1, 0), (-1, 0))


def compute(s: str, length: int, count: int) -> int:
    bytes_ = [tuple(map(int, line.split(','))) for line in s.splitlines()]
    blocks = set(bytes_[:count])

    paths = [((0, 0), 0)]
    shortest = {}
    end = (length-1, length-1)
    while paths:
        position, steps = paths.pop(0)
        x, y = position
        for move in MOVES:
            new_x, new_y = x + move[0], y + move[1]
            if -1 < new_x < length and -1 < new_y < length and (new_x, new_y) not in blocks:
                new_steps = steps + 1
                if (new_x, new_y) not in shortest or new_steps < shortest[(new_x, new_y)]:
                    shortest[(new_x, new_y)] = new_steps
                    paths.append(((new_x, new_y), new_steps))

    return shortest[end]


INPUT_S = '''\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''
LENGTH_ = 7
COUNT_ = 12
EXPECTED = 22


@pytest.mark.parametrize(
    ('input_s', 'length', 'count', 'expected'),
    (
        (INPUT_S, LENGTH_, COUNT_, EXPECTED),
    ),
)
def test(input_s: str, length: int, count: int, expected: int) -> None:
    assert compute(input_s, length, count) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read(), LENGTH, COUNT))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
