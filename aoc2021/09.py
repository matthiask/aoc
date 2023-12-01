import operator
from functools import reduce


with open("09.txt") as f:
    heightmap = {
        (x, y): int(h) for y, line in enumerate(f) for x, h in enumerate(line.strip())
    }


max_x = 100
max_y = 100


def is_low_point(point):
    h = heightmap[point]
    return all(heightmap[ps] > h for ps in surrounding(point))


def find_low_points():
    all_points = ((x, y) for x in range(max_x) for y in range(max_y))
    return [point for point in all_points if is_low_point(point)]


def part1():
    return sum(1 + heightmap[point] for point in find_low_points())


def surrounding(point):
    x, y = point
    return set(
        filter(
            None,
            (
                # North
                (x, y - 1) if y > 0 else None,
                # West
                (x + 1, y) if x + 1 < max_x else None,
                # South
                (x, y + 1) if y + 1 < max_y else None,
                # East
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
        new = {point for point in candidates if heightmap[point] < 9}
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
