import operator
from functools import reduce


with open("09.txt") as f:
    heightmap = [[int(h) for h in line.strip()] for line in f]

max_x = len(heightmap[0])
max_y = len(heightmap)


def is_low_point(x, y):
    h = heightmap[y][x]
    return all(
        (
            # North
            heightmap[y - 1][x] > h if y > 0 else True,
            # West
            heightmap[y][x + 1] > h if x + 1 < max_x else True,
            # South
            heightmap[y + 1][x] > h if y + 1 < max_y else True,
            # East
            heightmap[y][x - 1] > h if x > 0 else True,
        )
    )


def find_low_points():
    return [
        (x, y) for x in range(0, max_x) for y in range(0, max_y) if is_low_point(x, y)
    ]


def part1():
    return sum(1 + heightmap[y][x] for x, y in find_low_points())


def surrounding(point):
    x, y = point
    return set(
        filter(
            None,
            (
                (x, y - 1) if y > 0 else None,
                (x + 1, y) if x + 1 < max_x else None,
                (x, y + 1) if y + 1 < max_y else None,
                (x - 1, y) if x > 0 else None,
            ),
        )
    )


def find_basin(point):
    basin = {point}
    while True:
        candidates = reduce(
            operator.or_, (surrounding(point) for point in basin), basin
        )
        new = {point for point in candidates if heightmap[point[1]][point[0]] < 9}
        if new == basin:
            return basin
        # print(basin, new)
        basin = new


def part2():
    low_points = find_low_points()
    basins = {point: len(find_basin(point)) for point in low_points}
    largest = sorted(basins.values(), reverse=True)
    return largest[0] * largest[1] * largest[2]


if __name__ == "__main__":
    print("part1", part1())
    print("part2", part2())
