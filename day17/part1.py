import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def read_registers(s: str) -> dict[str, int]:
    registers_s = s.split('\n\n')[0]
    registers = {}
    for line in registers_s.splitlines():
        register = line.split('Register ')[1].split(': ')[0]
        value = int(line.split(': ')[1])
        registers[register] = value

    return registers


def read_program(s: str) -> list[int]:
    program_s = s.split('\n\n')[1]
    program = list(map(int, program_s.split(':')[1].split(',')))

    return program


def get_combo_operand(operand: int, registers: dict[str, int]) -> int:
    if operand <= 3:
        return operand
    elif operand == 4:
        return registers['A']
    elif operand == 5:
        return registers['B']
    elif operand == 6:
        return registers['C']
    else:
        raise ValueError(f"Unexpected combo operand: {operand}")


def adv(operand: int, registers: dict[str, int]) -> int:
    numerator = registers['A']
    denominator = 2 ** get_combo_operand(operand, registers)
    return numerator // denominator


def execute(opcode: int, operand: int, registers: dict[str, int]) -> tuple[int | None, int | None]:
    pointer = None
    output = None

    if opcode == 0:
        result = adv(operand, registers)
        registers['A'] = result
    elif opcode == 1:
        result = registers['B'] ^ operand
        registers['B'] = result
    elif opcode == 2:
        result = get_combo_operand(operand, registers) % 8
        registers['B'] = result
    elif opcode == 3:
        if registers['A'] != 0:
            pointer = operand
    elif opcode == 4:
        result = registers['B'] ^ registers['C']
        registers['B'] = result
    elif opcode == 5:
        result = get_combo_operand(operand, registers) % 8
        output = result
    elif opcode == 6:
        result = adv(operand, registers)
        registers['B'] = result
    elif opcode == 7:
        result = adv(operand, registers)
        registers['C'] = result
    else:
        raise ValueError(f"Unknown opcode: {opcode}")

    return pointer, output


def compute(s: str) -> str:
    registers = read_registers(s)
    program = read_program(s)

    pointer = 0
    outputs = []
    while pointer < len(program):
        opcode, operand = program[pointer: pointer+2]
        jump, output = execute(opcode, operand, registers)

        if output is not None:
            outputs.append(str(output))

        if jump is not None:
            pointer = jump
        else:
            pointer += 2

    return ','.join(outputs)


INPUT_S = '''\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
'''
EXPECTED = '4,6,3,5,6,3,5,2,1,0'


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
