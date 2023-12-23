from pprint import pp

from tools import open_input


IN = [*open_input("23")]
G = {x + y * 1j: c for y, line in enumerate(IN) for x, c in enumerate(line.strip())}
start = next(xy for xy, c in G.items() if xy.imag == 0 and c == ".")
end = next(xy for xy, c in G.items() if xy.imag == len(IN) - 1 and c == ".")
# pp(G)
# pp((start, end))

neighbors_with_slopes = [(1, ">"), (1j, "v"), (-1, "<"), (-1j, "^")]

paths = [[start]]
final = []
while paths:
    next_paths = []
    for path in paths:
        for dxy, slope in neighbors_with_slopes:
            if (
                (next_xy := path[-1] + dxy)
                and (c := G.get(next_xy))
                and next_xy not in path
            ):
                if next_xy == end:
                    final.append([*path, next_xy])
                # elif c == slope or c == ".":
                elif c != "#":
                    next_paths.append([*path, next_xy])
    paths = next_paths

pp([len(path) - 1 for path in final])
