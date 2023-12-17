import heapq
from itertools import pairwise
from pprint import pp

from tools import open_input


IN = open_input("17").read().strip().split("\n")
W = len(IN[0])
H = len(IN)
GRID = {x + y * 1j: int(IN[y][x]) for y in range(H) for x in range(W)}
start = 0
end = (W - 1) + (H - 1) * 1j
pp({"start": start, "end": end})
# pp(GRID)


def _deepen(heat_loss, point, visited):
    for d in (1, 1j, -1, -1j):
        pos = point + d
        if not (0 <= pos.real < W and 0 <= pos.imag < H):
            # Outside
            continue
        if len(visited) > 3 and all(b - a == d for a, b in pairwise(visited[-4:])):
            # Same direction too long
            continue
        if pos in visited:
            # Already visited
            continue

        yield (heat_loss + GRID[pos], pos, [*visited, pos])


def solve1():
    seen = set()
    heap = [(0, 0, start, [])]

    while heap:
        # print("heap", heap)
        heat_loss, _, point, visited = heapq.heappop(heap)
        if point == end:
            pp(("part1", heat_loss))
            return

        for next in _deepen(heat_loss, point, visited):
            # print(next, seen)
            if next[:2] in seen:
                continue
            seen.add(next[:2])
            heapq.heappush(
                heap,
                (
                    next[0],
                    next[0] * 100000 + next[1].real * 100 + next[1].imag,
                    next[1],
                    next[2],
                ),
            )

        # print(heap)
        print("heap length", len(heap))

    print("Oops")
    # pp(("part1", min(heat_loss)))


solve1()
