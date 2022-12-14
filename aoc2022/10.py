import sys
from itertools import count
from pprint import pprint


NOOP = "NOOP"
ADDX = "ADDX"


def identity(value):
    """
    >>> identity(3)
    3
    >>> identity(-3)
    -3
    """
    return value


def adder(amount):
    """
    >>> adder(4)(5)
    9
    """
    return lambda value: value + amount


def parse(op):
    tokens = op.split()
    if tokens[0] == "noop":
        return [NOOP, 1, identity]
    elif tokens[0] == "addx":
        return [ADDX, 2, adder(int(tokens[1]))]
    raise Exception(f"Unknown op {op}")


def execute(ops):
    cycle = count(1)
    x = 1

    for op in ops:
        for _i in range(op[1]):
            yield next(cycle), x
        x = op[2](x)


def signal_strength(ops):
    for cycle, x in execute(ops):
        if (cycle + 20) % 40 == 0:
            yield cycle * x


def part1(ops):
    return sum(signal_strength(ops))


def part2(ops):
    cycle = count(1)
    x = 1

    for cycle, x in execute(ops):
        scanline_x = (cycle - 1) % 40
        if -1 <= scanline_x - x <= 1:
            sys.stdout.write("#")
        else:
            sys.stdout.write(".")
        if cycle % 40 == 0:
            sys.stdout.write("\n")


if __name__ == "__main__":
    with open("10.txt") as f:
        ops = list(map(parse, f))

    # pprint(list(execute(ops)))
    pprint(part1(ops))

    part2(ops)
