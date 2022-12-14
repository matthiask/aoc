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


def segment(start, end):
    if start[0] == end[0]:
        return [(start[0], y) for y in range_inclusive(start[1], end[1])]
    elif start[1] == end[1]:
        return [(x, start[1]) for x in range_inclusive(start[0], end[0])]
    raise Exception(f"Unable to create segment from {start} to {end}")


def bounds(image):
    min_x = min(x for x, y in image.keys())
    max_x = max(x for x, y in image.keys())
    min_y = min(y for x, y in image.keys())
    max_y = max(y for x, y in image.keys())
    return (min_x, max_x, min_y, max_y)


def printify(image, default):
    (min_x, max_x, min_y, max_y) = bounds(image)
    return "\n".join(
        "".join(image.get((x, y), default) for x in range_inclusive(min_x, max_x))
        for y in range_inclusive(min_y, max_y)
    )


def find_position(grid):
    x, y = START

    (min_x, max_x, min_y, max_y) = bounds(grid)

    while True:
        for dx in (0, -1, 1):
            if not grid.get((x + dx, y + 1)):
                x += dx
                y += 1

                if y > max_y:
                    return False

                break
        else:
            grid[(x, y)] = "O"
            return True


START = (500, 0)


def read(filename):
    grid = {START: "S"}

    with open(filename) as f:
        for line in (line.strip() for line in f):
            points = [tuple(map(int, point.split(","))) for point in line.split(" -> ")]

            for start, end in zip(points, points[1:]):
                for point in segment(start, end):
                    grid[point] = "#"
    return grid


def test():
    grid = read("14-test.txt")

    found = 0
    while find_position(grid):
        found += 1

    print(printify(grid, "."))
    print("part1", found)


def main():
    grid = read("14.txt")

    found = 0
    while find_position(grid):
        found += 1

    print(printify(grid, "."))
    print("part1", found)


def main_with_extended_floor():
    grid = read("14.txt")
    grid.pop(START)

    (min_x, max_x, min_y, max_y) = bounds(grid)

    height = max_y - min_y
    # The floor isn't infinite, extending it with (height+50) is enough.
    for x in range_inclusive(min_x - height - 50, max_x + height + 50):
        grid[(x, max_y + 2)] = "#"

    print(printify(grid, "."))

    found = 0
    while find_position(grid):
        found += 1
        if grid.get(START):
            break

        if found % 1000 == 0:
            print("Found", found)

    print(printify(grid, "."))
    print("part2", found)


if __name__ == "__main__":
    test()
    main()
    main_with_extended_floor()
