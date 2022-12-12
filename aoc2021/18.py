def add(n1, n2):
    return [n1, n2]


def explode(n):
    """
    >>> explode([[[[[9, 8], 1], 2], 3], 4])
    [[[[0, 9], 2], 3], 4]
    >>> explode([7, [6, [5, [4, [3, 2]]]]])
    [7, [6, [5, [7, 0]]]]
    >>> explode([[6, [5, [4, [3, 2]]]], 1])
    [[6, [5, [7, 0]]], 3]
    >>> explode([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    >>> explode([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
    [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    """

    def _apply(p, idx, to_explode):
        if idx > 0 and to_explode[0] and isinstance(p[idx - 1], int):
            p[idx - 1] += to_explode[0]
            to_explode[0] = 0
        if idx < len(p) - 1 and to_explode[1]:
            if isinstance(p[idx + 1], int):
                p[idx + 1] += to_explode[1]
            if isinstance(p[idx + 1], list):
                # FIXME should recurse here?
                p[idx + 1][0] += to_explode[1]
            to_explode[1] = 0

    def _helper(p, depth):
        for idx in range(len(p)):
            if isinstance(p[idx], list):
                if depth < 4:
                    if to_explode := _helper(p[idx], depth + 1):
                        _apply(p, idx, to_explode)
                        return to_explode
                else:
                    # Inner list has depth 4 and is to be exploded.
                    to_explode = p[idx]
                    p[idx] = 0
                    _apply(p, idx, to_explode)
                    return to_explode

    _helper(n, 1)
    return n
