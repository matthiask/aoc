"""
https://github.com/tginsberg/advent-2021-kotlin/blob/master/src/main/kotlin/com/ginsberg/advent2021/Day22.kt

Nice alternative solution

add(c1, c2) =>

    if intersects(c1, c2)
        return [c1, c2, -(intersection(c1, c2))]
    return [c1, c2]

That is, add a negative volume for intersections. Flip flop.
"""

import re
import time
from dataclasses import dataclass
from itertools import chain, product
from typing import Tuple


# All ranges are [from, to)


@dataclass
class Cube:
    x: Tuple[int, int]
    y: Tuple[int, int]
    z: Tuple[int, int]

    @property
    def volume(self):
        """
        >>> Cube((0, 2), (0, 2), (0, 2)).volume
        8
        >>> Cube((0, -2), (0, -2), (0, 2)).volume
        0
        >>> Cube((0, 0), (0, 2), (0, 2)).volume
        0
        """
        dims = [
            self.x[1] - self.x[0],
            self.y[1] - self.y[0],
            self.z[1] - self.z[0],
        ]
        if any(d <= 0 for d in dims):
            return 0
        return dims[0] * dims[1] * dims[2]


def parse_line(line):
    """
    We add +1 to all endings so that we can work with half-closed [from, to)
    ranges which are much easier to handle than fully closed [from, to] ranges.
    """
    return line.split()[0], Cube(
        *[
            tuple(int(part) + idx for idx, part in enumerate(group))
            for group in re.findall(r"([-\d]+)\.\.([-\d]+)", line)
        ]
    )


def read(filename):
    with open(filename) as f:
        return [parse_line(line) for line in f]


def overlaps(c1, c2):
    return (
        c1.x[1] >= c2.x[0]
        and c2.x[1] >= c1.x[0]
        and c1.y[1] >= c2.y[0]
        and c2.y[1] >= c1.y[0]
        and c1.z[1] >= c2.z[0]
        and c2.z[1] >= c1.z[0]
    )


def contains(c1, c2):
    return (
        c1.x[0] <= c2.x[0] <= c2.x[1] <= c1.x[1]
        and c1.y[0] <= c2.y[0] <= c2.y[1] <= c1.y[1]
        and c1.z[0] <= c2.z[0] <= c2.z[1] <= c1.z[1]
    )


def _clamp(minimum, value, maximum):
    return min(max(value, minimum), maximum)


def _truncate_range(range, truncator):
    return [
        _clamp(truncator[0], range[0], truncator[1]),
        _clamp(truncator[0], range[1], truncator[1]),
    ]


def subtract(c1, c2):
    """
    >>> c1, c2 = Cube((0, 2), (0, 2), (0, 2)), Cube((0, 1), (0, 1), (0, 2))
    >>> subtract(c1, c2)
    [Cube(x=(0, 1), y=(1, 2), z=(0, 2)), Cube(x=(1, 2), y=(0, 1), z=(0, 2)), Cube(x=(1, 2), y=(1, 2), z=(0, 2))]
    >>> (c1.volume, sum(c.volume for c in subtract(c1, c2)))
    (8, 6)
    >>> c1, c2 = Cube((0, 10), (0, 10), (0, 10)), Cube((4, 5), (4, 5), (4, 5))
    >>> len(subtract(c1, c2))
    26
    >>> (c1.volume, sum(c.volume for c in subtract(c1, c2)))
    (1000, 999)
    >>> len(subtract(c2, c1))
    0
    >>> c1, c2 = Cube((0, 10), (0, 10), (0, 10)), Cube((5, 15), (5, 15), (5, 15))
    >>> len(subtract(c1, c2))
    7
    >>> (c1.volume, sum(c.volume for c in subtract(c1, c2)))
    (1000, 875)
    >>> c1, c2 = Cube((0, 10), (0, 10), (0, 10)), Cube((20, 25), (20, 25), (20, 25))
    >>> len(subtract(c1, c2))
    1
    """
    u = [
        c1.x[0],
        *_truncate_range(c2.x, c1.x),
        c1.x[1],
    ]
    v = [
        c1.y[0],
        *_truncate_range(c2.y, c1.y),
        c1.y[1],
    ]
    w = [
        c1.z[0],
        *_truncate_range(c2.z, c1.z),
        c1.z[1],
    ]

    cubes = []
    for dims in product(
        zip(u, u[1:]),
        zip(v, v[1:]),
        zip(w, w[1:]),
    ):
        c = Cube(*dims)
        if c.volume and not contains(c2, c):
            cubes.append(c)
    return cubes


def add(c1, c2):
    """
    >>> c1, c2 = Cube((0, 2), (0, 2), (0, 2)), Cube((0, 1), (0, 1), (0, 2))
    >>> add(c1, c2)
    [Cube(x=(0, 2), y=(0, 2), z=(0, 2))]
    >>> c1, c2 = Cube((0, 10), (0, 10), (0, 10)), Cube((5, 15), (5, 15), (5, 15))
    >>> len(add(c1, c2))
    8
    >>> (c1.volume, sum(c.volume for c in add(c1, c2)))
    (1000, 1875)
    >>> c1, c2 = Cube((0, 10), (0, 10), (0, 10)), Cube((20, 25), (20, 25), (20, 25))
    >>> len(add(c1, c2))
    2
    >>> (c1.volume, sum(c.volume for c in add(c1, c2)))
    (1000, 1125)
    """
    if contains(c1, c2):
        return [c1]
    if overlaps(c1, c2):
        return subtract(c1, c2) + [c2]
    return [c1, c2]


def remove_overlaps(cubes, cube):
    ret = []
    overlapping = []
    for c in cubes:
        if overlaps(c, cube):
            overlapping.append(c)
        else:
            ret.append(c)

    if overlapping:
        ret.extend(add(cube, overlapping[0]))
        for c in overlapping[1:]:
            ret.extend(subtract(c, cube))
    else:
        ret.append(cube)
    return ret


def part1():
    cube_of_interest = Cube((-50, 51), (-50, 51), (-50, 51))
    instructions_and_cubes = read("22.txt")

    on = [Cube((0, 0), (0, 0), (0, 0))]

    for instruction, cube in instructions_and_cubes:
        if not contains(cube_of_interest, cube):
            continue

        if instruction == "on":
            on = remove_overlaps(on, cube)

        elif instruction == "off":
            on = list(chain.from_iterable(subtract(c, cube) for c in on))

        else:
            raise Exception()

    print("part1", sum(c.volume for c in on))


def part2():
    instructions_and_cubes = read("22.txt")

    on = [Cube((0, 0), (0, 0), (0, 0))]

    step = 0
    for instruction, cube in instructions_and_cubes:
        if instruction == "on":
            on = remove_overlaps(on, cube)

        elif instruction == "off":
            on = list(chain.from_iterable(subtract(c, cube) for c in on))

        else:
            raise Exception()

        step += 1
        print(step, len(on), time.process_time())

        on = sorted(on, key=lambda cube: cube.volume, reverse=True)

    print("part2", sum(c.volume for c in on))


if __name__ == "__main__":
    # pprint(read("22-test.txt"))
    part1()
    part2()
