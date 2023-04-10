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


def range_inclusive(start, end):
    """
    >>> range_inclusive(2, 5)
    [2, 3, 4, 5]
    >>> range_inclusive(5, 2)
    [5, 4, 3, 2]
    """
    if start > end:
        return list(range(start, end - 1, -1))
    else:
        return list(range(start, end + 1))
