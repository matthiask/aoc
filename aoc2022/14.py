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


class OutOfBounds(Exception):
    pass


def find_position(grid):
    x, y = START

    (min_x, max_x, min_y, max_y) = bounds(grid)

    def _straight_down():
        nonlocal x, y
        moved = False
        while not grid.get((x, y + 1)):
            moved = True
            y += 1

            if y > max_y:
                # Yay, exceptions for control flow.
                raise OutOfBounds()
        return moved

    def _diagonally(dx):
        nonlocal x, y
        moved = False
        while grid.get((x, y + 1)) and not grid.get((x + dx, y + 1)):
            moved = True
            x += dx
            y += 1
        return moved

    try:
        while True:
            _straight_down()
            if _diagonally(-1):
                continue
            if _diagonally(1):
                continue

            grid[(x, y)] = "O"
            return True

    except OutOfBounds:
        return False


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


def main():
    grid = read("14.txt")

    found = 0
    while find_position(grid):
        found += 1

    print(printify(grid, "."))
    print("part1", found)


if __name__ == "__main__":
    main()
