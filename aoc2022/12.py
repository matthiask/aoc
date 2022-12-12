import heapq


with open("12.txt") as f:
    heightmap = {
        (x, y): h for y, line in enumerate(f) for x, h in enumerate(line.strip())
    }


start = next(point for point, height in heightmap.items() if height == "S")
end = next(point for point, height in heightmap.items() if height == "E")


max_x = max(x for x, y in heightmap)
max_y = max(y for x, y in heightmap)


def surrounding(point):
    x, y = point
    return set(
        filter(
            None,
            (
                # West
                (x + 1, y) if x + 1 < max_x else None,
                # South
                (x, y + 1) if y + 1 < max_y else None,
                # East
                (x - 1, y) if x > 0 else None,
                # North
                (x, y - 1) if y > 0 else None,
            ),
        )
    )


def _height(height):
    if height == "S":
        return ord("a")
    elif height == "E":
        return ord("z")
    return ord(height)


def only_visitable(height, points):
    """
    >>> only_visitable("a", {(1, 0), (2, 0), (3, 0)})
    {(1, 0), (2, 0)}
    """
    h = _height(height)
    return {point for point in points if _height(heightmap[point]) - h <= 1}


def solve(start):
    seen = {start}
    heap = [(0, start)]

    while heap:
        cost, point = heapq.heappop(heap)

        if point == end:
            return cost

        for next in only_visitable(heightmap[point], surrounding(point)):
            if next in seen:
                continue
            seen.add(next)
            heapq.heappush(heap, (cost + 1, next))

        # print(len(heap))


def part2():
    steps = set()
    for point, height in heightmap.items():
        if height in {"a", "S"}:
            steps.add(solve(point) or 99999)
    return min(steps)


if __name__ == "__main__":
    print("part1", solve(start))
    print("part2", part2())
