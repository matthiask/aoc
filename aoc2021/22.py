import re
from dataclasses import dataclass
from itertools import product
from pprint import pprint


# All ranges are [from, to)


@dataclass
class Cube:
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

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
    return Cube(
        *[
            tuple(int(part) + idx for idx, part in enumerate(group))
            for group in re.findall(r"([-\d]+)\.\.([-\d]+)", line)
        ]
    )


def read(filename):
    with open(filename) as f:
        cubes = [parse_line(line) for line in f]
    return cubes


def overlaps(c1, c2):
    return (
        c1.x[1] >= c2.x[0]
        and c2.x[1] >= c1.x[0]
        and c1.y[1] >= c2.y[0]
        and c2.y[1] >= c1.y[0]
        and c1.z[1] >= c2.z[0]
        and c2.z[1] >= c1.z[0]
    )


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
    >>> len(subtract(c2, c1))
    0
    >>> c1, c2 = Cube((0, 10), (0, 10), (0, 10)), Cube((5, 15), (5, 15), (5, 15))
    >>> len(subtract(c1, c2))
    7
    """
    if not overlaps(c1, c2):
        return c1

    u = [c1.x[0], c2.x[0], c2.x[1], c1.x[1]]
    v = [c1.y[0], c2.y[0], c2.y[1], c1.y[1]]
    w = [c1.z[0], c2.z[0], c2.z[1], c1.z[1]]

    cubes = []
    for dims in product(
        zip(u, u[1:]),
        zip(v, v[1:]),
        zip(w, w[1:]),
    ):
        c = Cube(*dims)
        if c.volume and c != c2:
            cubes.append(c)
    return cubes


def test():
    c = Cube((0, 2), (0, 2), (0, 2))

    assert c.volume == 27

    assert overlaps(c, Cube((1, 3), (0, 2), (0, 2)))
    assert overlaps(c, Cube((2, 4), (0, 2), (0, 2)))
    assert not overlaps(c, Cube((3, 4), (0, 2), (0, 2)))


if __name__ == "__main__":
    test()

    # pprint(read("22-test.txt"))
