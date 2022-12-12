import functools
import json
from pprint import pprint


def add(n1, n2):
    return [n1, n2]


class Stop(Exception):
    pass


def split(n):
    """
    >>> split(10)
    [5, 5]
    >>> split(11)
    [5, 6]
    >>> split(12)
    [6, 6]
    """
    left = n // 2
    return [left, n - left]


def reduce(n):
    """
    >>> reduce([[[[[9, 8], 1], 2], 3], 4])[0]
    [[[[0, 9], 2], 3], 4]
    >>> reduce([7, [6, [5, [4, [3, 2]]]]])[0]
    [7, [6, [5, [7, 0]]]]
    >>> reduce([[6, [5, [4, [3, 2]]]], 1])[0]
    [[6, [5, [7, 0]]], 3]
    >>> reduce([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])[0]
    [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    >>> reduce([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])[0]
    [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    """

    def _apply(p, idx, to_explode):
        if idx > 0 and to_explode[0] and isinstance(p[idx - 1], int):
            p[idx - 1] += to_explode[0]
            to_explode[0] = 0
        if idx < len(p) - 1 and to_explode[1]:
            if isinstance(p[idx + 1], int):
                p[idx + 1] += to_explode[1]
            # FIXME That's bad.
            elif isinstance(p[idx + 1][0], int):
                p[idx + 1][0] += to_explode[1]
            elif isinstance(p[idx + 1][0][0], int):
                p[idx + 1][0][0] += to_explode[1]
            elif isinstance(p[idx + 1][0][0][0], int):
                p[idx + 1][0][0][0] += to_explode[1]
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
            elif p[idx] >= 10:
                p[idx] = split(p[idx])
                raise Stop()

    try:
        _changed = bool(_helper(n, 1))
    except Stop:
        return n, True
    return n, _changed


def add(n1, n2):
    """
    >>> add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1])
    [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    """
    n = [n1, n2]
    while True:
        n, changed = reduce(n)
        if not changed:
            return n


def magnitude(n):
    """
    >>> magnitude([[1,2],[[3,4],5]])
    143
    """

    def _magnitude(v):
        if isinstance(v, list) and len(v) == 2:
            return _magnitude(v[0]) * 3 + _magnitude(v[1]) * 2
        elif isinstance(v, int):
            return v
        else:
            raise Exception(f"What is {v}")

    return _magnitude(n)


def read():
    with open("18.txt") as f:
        numbers = [json.loads(line.strip()) for line in f]
    return numbers


if __name__ == "__main__":
    n = functools.reduce(add, read())
    pprint(magnitude(n))
