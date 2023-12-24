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

    @property
    def xy2d(self):
        return Vec2d(self.x, self.y)


@dataclass
class Mat2d:
    values: list[list[int]]

    @property
    def det(self):
        v = self.values
        return v[0][0] * v[1][1] - v[0][1] * v[1][0]

    @property
    def inv(self):
        f = 1 / self.det
        v = self.values
        return Mat2d(
            [
                [f * v[1][1], -f * v[0][1]],
                [-f * v[1][0], f * v[0][0]],
            ]
        )

    def __mul__(self, other):
        if isinstance(other, Vec2d):
            v = self.values
            return Vec2d(
                v[0][0] * other.x + v[0][1] * other.y,
                v[1][0] * other.x + v[1][1] * other.y,
            )
        return NotImplemented


@dataclass
class Vec2d:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2d(self.x * other, self.y * other)
        return NotImplemented


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

        # Av = b
        A = Mat2d(
            [
                [h1.v.x, -h2.v.x],
                [h1.v.y, -h2.v.y],
            ]
        )
        b = h2.p.xy2d - h1.p.xy2d

        try:
            v = A.inv * b
        except ZeroDivisionError:
            continue
        else:
            p = h1.p.xy2d + h1.v.xy2d * v.x
            # print(h1)
            # print(h2)
            # print(A)
            # print(A.inv)
            # print(b)
            # print(v, p)
            # print()

            if v.x > 0 and v.y > 0:
                if min <= p.x <= max and min <= p.y <= max:
                    intersections += 1
                    # print("Intersects!")

        """
                print(x, p)
        continue

        try:
            t = (h1.p.x - h2.p.x) / (h2.v.x - h1.v.x)
        except ZeroDivisionError:
            continue
        if t > 0:
            at = h1.at(t)
            if min <= at.x <= max and min <= at.y <= max:
                # print(t, at)
                intersections += 1
        """

    print(intersections)


solve1("24-test.txt", 7, 27)
solve1("24.txt", 200000000000000, 400000000000000)
