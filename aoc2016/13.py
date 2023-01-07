import heapq


IN = 1352


def is_wall(x, y):
    v = bin(x * x + 3 * x + 2 * x * y + y + y * y + IN)[2:]
    return v.count("1") % 2


def surrounding(x, y):
    yield (x + 1, y)
    yield (x, y + 1)
    if x > 0:
        yield (x - 1, y)
    if y > 0:
        yield (x, y - 1)


def visitable(x, y):
    return [p for p in surrounding(x, y) if not is_wall(*p)]


def path_length(start, end):
    seen = {start}
    heap = [(0, start)]
    while heap:
        cost, p = heapq.heappop(heap)
        if p == end:
            return cost
        for to in visitable(*p):
            if to not in seen:
                seen.add(to)
                heapq.heappush(heap, (cost + 1, to))


print(path_length((1, 1), (31, 39)))
