import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_checksum(files: list[str]) -> int:
    sum_ = 0
    for i, f in enumerate(files):
        if f == '.':
            break
        id_ = int(f)
        sum_ += i * id_

    return sum_


def compute(s: str) -> int:
    s = s.splitlines()[0]

    disk = []
    file_id = 0
    is_free = False
    for n in s:
        if not is_free:
            disk += [str(file_id)] * int(n)
            file_id += 1
        else:
            disk += ['.'] * int(n)
        is_free = not is_free

    index = len(disk) - 1
    for file_id in disk[::-1]:
        if file_id == '.':
            index -= 1
            continue

        first_free_index = disk.index('.')
        if first_free_index > index:
            break
        disk[first_free_index], disk[index] = disk[index], disk[first_free_index]
        index -= 1

    return get_checksum(disk)


INPUT_S = '''\
2333133121414131402
'''
EXPECTED = 1928


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
