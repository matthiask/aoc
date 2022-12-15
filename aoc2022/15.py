import re
from collections import namedtuple


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


Sensor = namedtuple("Sensor", "origin beacon")


def _sensor(line):
    """
    >>> _sensor("Sensor at x=2, y=18: closest beacon is at x=-2, y=15")
    Sensor(origin=(2, 18), beacon=(-2, 15))
    """
    coordinates = [int(part) for part in re.findall(r"([-\d]+)", line)]
    return Sensor(tuple(coordinates[0:2]), tuple(coordinates[2:4]))


def read(filename):
    with open(filename) as f:
        return [_sensor(line.strip()) for line in f]


def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def exclusions_at_y(filename, y_of_interest):
    exclusions_at_y = set()
    occupied_at_y = set()

    for sensor in read(filename):
        if sensor.origin[1] == y_of_interest:
            occupied_at_y.add(sensor.origin)
        if sensor.beacon[1] == y_of_interest:
            occupied_at_y.add(sensor.beacon)

        d = manhattan_distance(sensor.origin, sensor.beacon)
        y_diff = abs(sensor.origin[1] - y_of_interest)
        # print(sensor, d, y_diff)
        if d > y_diff:
            x_range = abs(d - y_diff)
            # print(sensor.origin[0] - x_range, sensor.origin[1] + x_range)
            for x in range_inclusive(
                sensor.origin[0] - x_range, sensor.origin[0] + x_range
            ):
                exclusions_at_y.add((x, y_of_interest))

    # print(sorted(exclusions_at_y))
    # print(sorted(occupied_at_y))
    return exclusions_at_y - occupied_at_y


def just_outside(sensor):
    """
    >>> sorted(just_outside(Sensor((0, 0), (1, 0))))
    [(-2, 0), (-1, -1), (-1, 1), (0, -2), (0, 2), (1, -1), (1, 1), (2, 0)]
    """
    outside = set()
    d = manhattan_distance(sensor.origin, sensor.beacon) + 1  # just outside
    x, y = sensor.origin
    for i in range(d + 1):  # range_inclusive
        # NE
        outside.add((x + i, y - d + i))
        # SE
        outside.add((x + i, y + d - i))
        # SW
        outside.add((x - d + i, y + i))
        # NW
        outside.add((x - d + i, y - i))
    return outside


def part2(filename):
    """

    Short research:

    https://doc.sagemath.org/html/en/reference/calculus/sage/symbolic/relation.html#sage.symbolic.relation.solve_ineq
    https://en.wikipedia.org/wiki/Fourier%E2%80%93Motzkin_elimination

    I think I give up 😂

    """

    sensors = read(filename)
    maybe = just_outside(sensors[0])
    for sensor in sensors[1:]:
        maybe &= just_outside(sensor)
    return maybe


if __name__ == "__main__":
    # part1()

    print("part1 test", len(exclusions_at_y("15-test.txt", 10)))
    print("part2 test", part2("15-test.txt"))
    print("part1", len(exclusions_at_y("15.txt", 2000000)))
