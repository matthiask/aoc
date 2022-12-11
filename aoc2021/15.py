import heapq
import operator
from functools import reduce


with open("15.txt") as f:
    riskmap = {
        (x, y): int(h) for y, line in enumerate(f) for x, h in enumerate(line.strip())
    }
    # We do not *enter* the starting point, let's just set the risk
    # to zero to make summing the total risk easier.
    # riskmap[(0, 0)] = 0


ending = (99, 99)
max_x = 100
max_y = 100


risk = [(0, 0, 0)]


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


def solve():
    seen = {(0, 0)}
    heap = [(0, (0, 0))]

    while heap:
        risk, point = heapq.heappop(heap)

        if point == ending:
            return risk

        for next in surrounding(point):
            if next in seen:
                continue
            seen.add(next)
            heapq.heappush(heap, (risk + riskmap[next], next))

        print(heap)


if __name__ == "__main__":
    print("part1", solve())
    # print("part2", part2())
