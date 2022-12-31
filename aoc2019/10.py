import math
import sys
from collections import defaultdict
from itertools import cycle


grid = [*open(sys.argv[1] if len(sys.argv) > 1 else "10.txt")]
points = [
    (x, y)
    for y, line in enumerate(grid)
    for x, c in enumerate(line.strip())
    if c == "#"
]


def visibility_spec(from_point, to_point):
    """
    atan2 goes from -pi to +pi

    atan2(+0.00001, -1) ~= +pi
    atan2(-0.00001, -1) ~= -pi
    atan2(0, -1) == pi
    atan2(0, 1) == pi

    But, we want to order by angle for the vaporization order. Jumble and
    juggle x, y and the base angle to make the result of this func start at "0"
    for straight upwards and increasing to almost 2*pi when following the
    circle in the clockwise direction.

    >>> visibility_spec((0, 0), (0, -1))
    0.0
    >>> 1.5 < visibility_spec((0, 0), (1, 0)) < 1.6
    True
    >>> 3 <= visibility_spec((0, 0), (0, 1)) <= 3.2
    True
    >>> 4.7 < visibility_spec((0, 0), (-1, 0)) < 4.8
    True
    >>> 6.2 < visibility_spec((0, 0), (-0.0001, -1))
    True
    """
    vec = [
        to_point[0] - from_point[0],
        to_point[1] - from_point[1],
    ]
    return math.pi - math.atan2(*vec)


def visible_asteroids_from(p):
    return len({visibility_spec(p, point) for point in points if p != point})


# print(grid)
visibility_counts = sorted((visible_asteroids_from(point), point) for point in points)
print("part1", visibility_counts[-1][0])

station = visibility_counts[-1][1]
directions = defaultdict(list)
for point in points:
    spec = visibility_spec(station, point)
    directions[spec].append(point)
asteroids = cycle(
    [
        sorted(points, key=lambda point: math.dist(station, point))
        for angle, points in sorted(directions.items())
    ]
)
vaporized = 0
for direction in asteroids:
    if direction:
        vaporized += 1
        if vaporized == 200:
            print(direction.pop(0))
            break
        else:
            direction.pop()
