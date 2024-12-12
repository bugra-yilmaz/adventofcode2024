import argparse
import os.path
from collections import defaultdict

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

N_BLINKS = 75


def compute(s: str) -> int:
    s = s.splitlines()[0]
    numbers = list(map(int, s.split()))

    start = defaultdict(int)
    for number in numbers:
        start[number] += 1

    for i in range(N_BLINKS):
        updates = defaultdict(int)

        for number, count in start.items():
            updates[number] -= count
            number_s = str(number)
            length = len(number_s)

            if number == 0:
                updates[1] += count
            elif length % 2 == 0:
                mid = length // 2
                left, right = number_s[:mid], number_s[mid:]
                updates[int(left)] += count
                updates[int(right)] += count
            else:
                updates[number * 2024] += count

        for number, count in updates.items():
            start[number] += count
            if start[number] == 0:
                start.pop(number)

    return sum(start.values())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
