def manhattan_distance(n):
    return int(abs(n.real) + abs(n.imag))


def neighbors(n, *, diagonal):
    offset = [1j**i for i in range(4)]
    if diagonal:
        offset.extend((1 + 1j) * 1j**i for i in range(4))
    return [n + o for o in offset]
