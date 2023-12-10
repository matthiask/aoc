from pprint import pp

from tools import open_input


N = -1j
E = 1
S = 1j
W = -1

pipes = {
    "|": [N, S],
    "-": [W, E],
    "L": [N, E],
    "J": [N, W],
    "7": [S, W],
    "F": [S, E],
    "S": [N, E, S, W],
}


def parse():
    start = None
    grid = {}
    for y, line in enumerate(open_input("10")):
        for x, c in enumerate(line.strip()):
            xy = x + y * 1j
            if c == ".":
                continue
            if c == "S":
                start = xy
            grid[xy] = pipes[c]

    return start, grid


def connects_to(grid, xy):
    # This cell connects to the following cells
    this_connects_to = [xy + offset for offset in grid.get(xy, ())]
    # Now we have to determine if the other cell also connects to this one
    connected = []
    for adjacent in this_connects_to:
        if any(adjacent + offset == xy for offset in grid.get(adjacent, ())):
            connected.append(adjacent)
    return connected


def solve1():
    start, grid = parse()
    path = [start]
    while True:
        next_xy = [xy for xy in connects_to(grid, path[-1]) if xy not in path]
        if not next_xy:
            break
        path.append(next_xy[0])
    # pp(path)
    pp(("part1", len(path) // 2))


solve1()
