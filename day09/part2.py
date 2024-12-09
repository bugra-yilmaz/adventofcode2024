import argparse
import os.path
from copy import deepcopy

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_checksum(files: list[tuple[int, int, str]]) -> int:
    sum_ = 0
    for index, count, file_id in files:
        for i in range(index, index+count):
            sum_ += i * int(file_id)

    return sum_


def compute(s: str) -> int:
    s = s.splitlines()[0]

    files = []
    free = []
    index = 0
    file_id = 0
    is_free = False
    for n in s:
        if not is_free:
            files.append((index, int(n), str(file_id)))
            file_id += 1
        else:
            free.append((index, int(n)))
        index += int(n)
        is_free = not is_free

    files_copy = deepcopy(files)
    for i, (index_file, count_file, file_id) in enumerate(files_copy[::-1]):
        for j, (index_free, count_free) in enumerate(free):
            if index_free > index_file:
                continue

            if count_free < count_file:
                continue

            free[j] = index_free + count_file, count_free - count_file
            files[-i-1] = index_free, count_file, file_id
            break

    return get_checksum(files)


INPUT_S = '''\
2333133121414131402
'''
EXPECTED = 2858


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
