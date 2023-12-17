from heapq import heappop, heappush

from tools import open_input, range_inclusive


# Not my solution :-(
G = {
    x + y * 1j: int(c)
    for y, r in enumerate(open_input("17"))
    for x, c in enumerate(r.strip())
}


def f(min, max, end=[*G][-1], x=0):
    # Tuples:
    # - heat_loss
    # - arbitrary counter value
    # - next position
    # - direction (1 or 1j)
    # Two starts, once S, once E
    todo = [(0, 0, 0, 1), (0, 0, 0, 1j)]
    seen = set()

    while todo:
        val, _, pos, dir = heappop(todo)

        if pos == end:
            # print(val)
            # continue
            return val
        if (pos, dir) in seen:
            continue
        seen.add((pos, dir))

        # for d in 1j / dir, -1j / dir:
        for d in dir * 1j, dir * -1j:
            for i in range_inclusive(min, max):
                if (new_pos := pos + d * i) in G:
                    new_val = val + sum(G[pos + d * j] for j in range_inclusive(1, i))
                    heappush(todo, (new_val, (x := x + 1), new_pos, d))


# print(f(1, 3), f(4, 10))
print(f(1, 3), f(4, 10))
