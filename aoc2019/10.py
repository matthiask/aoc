import sys
from math import gcd


grid = [*open(sys.argv[1] if len(sys.argv) > 1 else "10.txt")]
points = [
    (x, y)
    for y, line in enumerate(grid)
    for x, c in enumerate(line.strip())
    if c == "#"
]


def sign(v):
    if v > 0:
        return 1
    elif v < 0:
        return -1
    return 0


def visibility_spec(from_point, to_point):
    vec = [
        to_point[0] - from_point[0],
        to_point[1] - from_point[1],
    ]
    d = gcd(*vec)
    return (sign(vec[0]), sign(vec[1]), vec[0] // d, vec[1] // d)


def visible_asteroids_from(p):
    return len({visibility_spec(p, point) for point in points if p != point})


# print(grid)
print("part1", max(visible_asteroids_from(point) for point in points))
