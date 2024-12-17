import argparse
import os.path

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OFFSET = 10000000000000
COST_A = 3
COST_B = 1


def get_machines(s: str) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    machines = []
    (a_x, a_y), (b_x, b_y), (p_x, p_y) = (0, 0), (0, 0), (0, 0)
    count = 0
    for line in s.splitlines():
        if line == '':
            machine = ((a_x, a_y), (b_x, b_y), (p_x, p_y))
            machines.append(machine)
            count = 0
            continue
        if count == 0:
            a_x = int(line.split('X+')[1].split(',')[0])
            a_y = int(line.split('Y+')[1])
        elif count == 1:
            b_x = int(line.split('X+')[1].split(',')[0])
            b_y = int(line.split('Y+')[1])
        elif count == 2:
            p_x = int(line.split('X=')[1].split(',')[0]) + OFFSET
            p_y = int(line.split('Y=')[1]) + OFFSET
        count += 1
    machine = ((a_x, a_y), (b_x, b_y), (p_x, p_y))
    machines.append(machine)

    return machines


def get_min_cost_win(machine: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]) -> int:
    (a_x, a_y), (b_x, b_y), (p_x, p_y) = machine

    det_denom = a_x * b_y - b_x * a_y
    if det_denom == 0:
        n_a = p_x // a_x
        n_b = p_x // b_x
        if (n_a * a_x, n_a * a_y) == (p_x, p_y) and n_a * COST_A < n_b * COST_B:
            return n_a * COST_A
        elif (n_b * b_x, n_b * b_y) == (p_x, p_y):
            return n_b * COST_B
    else:
        n_a, n_b = int((p_x * b_y - b_x * p_y) / det_denom), int((a_x * p_y - p_x * a_y) / det_denom)
        if n_a * a_x + n_b * b_x == p_x and n_a * a_y + n_b * b_y == p_y:
            return n_a * COST_A + n_b * COST_B

    return 0


def compute(s: str) -> int:
    machines = get_machines(s)
    return sum(get_min_cost_win(machine) for machine in machines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
