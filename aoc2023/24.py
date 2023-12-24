from dataclasses import dataclass
from itertools import combinations

from tools import numbers


def almost_equal(f1, f2):
    return abs(f1 - f2) < 0.0001


@dataclass
class Vec:
    x: int
    y: int
    z: int


@dataclass
class Hailstone:
    p: Vec
    v: Vec

    @classmethod
    def from_line(cls, line):
        n = numbers(line)
        return cls(Vec(*n[:3]), Vec(*n[3:]))

    def at(self, t):
        return Vec(
            self.p.x + t * self.v.x,
            self.p.y + t * self.v.y,
            self.p.z + t * self.v.z,
        )


def solve1(inp, min, max):
    with open(inp) as f:
        stones = [Hailstone.from_line(line) for line in f]
    intersections = 0
    for h1, h2 in combinations(stones, 2):
        # p1 + t * v1 = p2 + t * v2
        # p1 - p2 = t * (v2 - v1)
        # (p1 - p2) / (v2 - v1) = t
        # pprint((h1, h2))

        try:
            t = (h1.p.x - h2.p.x) / (h2.v.x - h1.v.x)
        except ZeroDivisionError:
            continue
        if t > 0:
            at = h1.at(t)
            if min <= at.x <= max and min <= at.y <= max:
                print(t, at)
                intersections += 1
    print(intersections)


solve1("24-test.txt", 7, 27)
solve1("24.txt", 200000000000000, 400000000000000)
