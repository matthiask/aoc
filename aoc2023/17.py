from itertools import chain, pairwise
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


def _deepen(path):
    for d in (1, 1j, -1, -1j):
        pos = path[0] + d
        if not (0 <= pos.real < W and 0 <= pos.imag < H):
            # Outside
            continue
        if len(path[2]) > 3 and all(b - a == d for a, b in pairwise(path[2][-4:])):
            # Same direction too long
            continue
        if pos in path[2]:
            # Already visited
            continue

        yield (pos, path[1] + GRID[pos], [*path[2], pos])


def solve1():
    paths = [
        # (position, heat_loss, visited)
        (start, 0, []),
    ]

    heat_loss = set()
    while paths:
        paths = list(chain.from_iterable(_deepen(path) for path in paths))

        end_reached = [path for path in paths if path[0] == end]
        heat_loss |= {path[1] for path in end_reached}
        paths = [path for path in paths if path[0] != end]

        # print("paths", paths)
        print("paths", len(paths))
        print("heat_loss", heat_loss)

    pp(("part1", min(heat_loss)))


solve1()
