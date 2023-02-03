import re
import sys


def open_input(day):
    return open(f"{day}.txt" if len(sys.argv) < 2 else sys.argv[1])


def numbers(line):
    return [int(number) for number in re.findall(r"-?\d+", line)]


def manhattan_distance(n):
    return int(abs(n.real) + abs(n.imag))


def neighbors(n, *, diagonal):
    offset = [1j**i for i in range(4)]
    if diagonal:
        offset.extend((1 + 1j) * 1j**i for i in range(4))
    return [n + o for o in offset]
