from itertools import islice

from utils import manhattan_distance, neighbors


def locations():
    current = 0
    visited = {current}
    direction = -1j
    while True:
        yield current
        left = direction * 1j
        if current + left in visited:
            current += direction
        else:
            current += left
            direction *= 1j
        visited.add(current)


IN = 289326
print(manhattan_distance(next(islice(locations(), IN - 1, IN))))


grid = {0: 1}
for loc in islice(locations(), 1, 9999999):
    grid[loc] = v = sum(grid.get(n, 0) for n in neighbors(loc, diagonal=True))
    if v > IN:
        print(v)
        break
