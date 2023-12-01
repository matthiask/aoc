import heapq


with open("15.txt") as f:
    riskmap = {
        (x, y): int(h) for y, line in enumerate(f) for x, h in enumerate(line.strip())
    }
    # We do not *enter* the starting point, let's just set the risk
    # to zero to make summing the total risk easier.
    # riskmap[(0, 0)] = 0


def surrounding(point, *, factor):
    x, y = point
    return set(
        filter(
            None,
            (
                # West
                (x + 1, y) if x + 1 < 100 * factor else None,
                # South
                (x, y + 1) if y + 1 < 100 * factor else None,
                # East
                (x - 1, y) if x > 0 else None,
                # North
                (x, y - 1) if y > 0 else None,
            ),
        )
    )


def risk_part1(point):
    return riskmap[point]


def risk_part2(point):
    x_q, x_r = divmod(point[0], 100)
    y_q, y_r = divmod(point[1], 100)
    risk = x_q + y_q + riskmap[(x_r, y_r)]

    return 1 + (risk - 1) % 9


def solve(*, calculate_risk, factor):
    seen = {(0, 0)}
    heap = [(0, (0, 0))]

    ending = (100 * factor - 1, 100 * factor - 1)

    while heap:
        risk, point = heapq.heappop(heap)

        if point == ending:
            return risk

        for next in surrounding(point, factor=factor):
            if next in seen:
                continue
            seen.add(next)
            heapq.heappush(heap, (risk + calculate_risk(next), next))

        # print(heap)


if __name__ == "__main__":
    print("part1", solve(calculate_risk=risk_part1, factor=1))
    print("part2", solve(calculate_risk=risk_part2, factor=5))
