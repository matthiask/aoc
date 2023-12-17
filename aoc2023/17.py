from collections import defaultdict
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
max_same = 3


def _deepen(path):
    for d in (1, 1j, -1, -1j):
        pos = path[0] + d
        if not (0 <= pos.real < W and 0 <= pos.imag < H):
            # Outside
            continue
        if len(path[2]) > max_same and all(
            b - a == d for a, b in pairwise(path[2][-1 - max_same :])
        ):
            # Same direction too long
            continue
        if pos in path[2]:
            # Already visited
            continue

        yield (pos, path[1] + GRID[pos], [*path[2], pos])


def solve1():
    paths = [
        # (position, heat_loss, visited)
        (start, 0, [0]),
    ]

    heat_loss = 99999999999
    while paths:
        paths = list(chain.from_iterable(_deepen(path) for path in paths))

        # Prune search space. Find the cheapest path for each current position
        positions = defaultdict(list)
        for path in sorted(paths, key=lambda path: path[1]):
            positions[path[0]].append(path)

        # Keep a few of the cheapest paths per position
        paths = list(chain.from_iterable(p[:2] for p in positions.values()))

        end_reached = [path for path in paths if path[0] == end]
        if end_reached:
            min_path = sorted(end_reached, key=lambda path: path[1])[0]
            if min_path[1] < heat_loss:
                print("min_path", min_path)
                heat_loss = min_path[1]
        paths = [path for path in paths if path[0] != end]

        # print("paths", paths)
        print("paths", len(paths))
        # pp(paths)
        # print("heat_loss", heat_loss)

    pp(("part1", heat_loss))


solve1()
