import heapq
import random
from pprint import pprint


grid = {
    complex(x, y): c
    for y, line in enumerate(open("24.txt"))
    for x, c in enumerate(line.strip())
    if c != "."
}
walls = {p for p, c in grid.items() if c == "#"}
places = {c: p for p, c in grid.items() if c != "#"}
W = int(max(p.real for p in grid))
H = int(max(p.imag for p in grid))
place_names = sorted(places)

# print(grid)
# print(walls)
# print(W, H)
# print(places)


def surrounding(p):
    x = int(p.real)
    y = int(p.imag)
    if x > 0:
        yield complex(x - 1, y)
    if y > 0:
        yield complex(x, y - 1)
    if x < W:
        yield complex(x + 1, y)
    if y < H:
        yield complex(x, y + 1)


def visitable(p):
    return [_ for _ in surrounding(p) if _ not in walls]


def shortest_path(start, end):
    seen = set()
    heap = [(0, 0, start)]
    while heap:
        cost, _, p = heapq.heappop(heap)
        if p == end:
            return cost
        for to in visitable(p):
            if to not in seen:
                seen.add(to)
                heapq.heappush(heap, (cost + 1, random.random(), to))


def get_distances():
    distances = {}
    for i in range(len(place_names)):
        for j in range(i + 1, len(place_names)):
            distance = shortest_path(places[place_names[i]], places[place_names[j]])
            distances.setdefault(place_names[i], {})[place_names[j]] = distance
            distances.setdefault(place_names[j], {})[place_names[i]] = distance
    return distances


def solve():
    distances = get_distances()

    todo = [(0, "0")]
    while True:
        next_todo = []
        for distance, visited in todo:
            next_todo.extend(
                (distance + distances[visited[-1]][next], visited + next)
                for next in place_names
                if next not in visited
                # part2:
                or (len(visited) == 8 and next == "0")
            )
        # print(next_todo)
        if not next_todo:
            break
        todo = next_todo

    # pprint(todo)
    # pprint(distances)

    pprint(min(t[0] for t in todo))


solve()
