from pprint import pp

from tools import neighbors, open_input


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
                pp(("start", xy))
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


def find_path():
    start, grid = parse()
    path = [start]
    while True:
        next_xy = [xy for xy in connects_to(grid, path[-1]) if xy not in path]
        if not next_xy:
            break
        path.append(next_xy[0])
    return path


def solve1():
    pp(("part1", len(find_path()) // 2))


class WrongSideError(Exception):
    pass


def solve2():
    def _solve(side):
        path = find_path()
        pp(path)
        inside = {
            path[i + 1] + (path[i + 1] - path[i]) * side for i in range(len(path) - 1)
        }
        inside |= {
            path[i] + (path[i + 1] - path[i]) * side for i in range(len(path) - 1)
        }
        path = set(path)
        inside -= path

        while True:
            flood = set(inside)
            for xy in inside:
                flood |= set(neighbors(xy, diagonal=True))
            flood -= path
            # pp((flood, inside))
            if flood == inside:
                break
            inside = flood

            if -1 in inside:
                raise WrongSideError

        pp(inside)
        pp(("part2", len(inside)))

    try:
        # If path is clockwise, use right hand side
        _solve(1j)
    except WrongSideError:
        # Else use left hand side
        _solve(-1j)


solve1()
solve2()
