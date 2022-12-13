import re
from collections import defaultdict
from itertools import repeat
from pprint import pprint


with open("05.txt") as f:
    coordinates = [
        [int(v) for v in re.findall(r"([0-9]+)", line.strip())] for line in f
    ]


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


def _register_hits(intersections, x_iterable, y_iterable):
    for x, y in zip(x_iterable, y_iterable):
        intersections[(x, y)] += 1


def part1(*, enable_diagonal):
    intersections = defaultdict(int)

    for x1, y1, x2, y2 in coordinates:
        if x1 == x2:
            _register_hits(intersections, repeat(x1), range_inclusive(y1, y2))
        elif y1 == y2:
            _register_hits(intersections, range_inclusive(x1, x2), repeat(y1))
        elif enable_diagonal:
            _register_hits(
                intersections,
                range_inclusive(x1, x2),
                range_inclusive(y1, y2),
            )

    # pprint(intersections)
    return sum(1 for pos, count in intersections.items() if count > 1)


print("part1:", part1(enable_diagonal=False))
print("part2:", part1(enable_diagonal=True))
