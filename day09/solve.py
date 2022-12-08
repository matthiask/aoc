from pprint import pprint

from collections import namedtuple


"""
Coordinates:

initial: (0, 0)
"""

_moves = {
    "U": (0, 1),
    "R": (1, 0),
    "D": (0, -1),
    "L": (-1, 0),
}


Move = namedtuple("Move", "delta count")


def _parse_move(line):
    """
    >>> _parse_move("R 1")
    Move(delta=(1, 0), count=1)
    >>> _parse_move("D 15")
    Move(delta=(0, -1), count=15)
    """
    direction, count = line.strip().split(" ")
    return Move(_moves[direction], int(count))


def _delta(head, tail):
    """
    Return (dx, dy) where dx > 0 if head is to the right of the tail

    >>> _delta((5, 5), (8, 3))
    (-3, 2)
    """
    return (head[0] - tail[0], head[1] - tail[1])


def _tail_move(head, tail):
    """
    Determine tail moves

    >>> _tail_move((0, 0), (0, 0))
    (0, 0)
    >>> _tail_move((1, 1), (0, 0))
    (0, 0)
    >>> _tail_move((-1, -1), (0, 0))
    (0, 0)
    >>> _tail_move((2, 0), (0, 0))
    (1, 0)
    >>> _tail_move((0, 2), (0, 0))
    (0, 1)
    >>> _tail_move((2, 1), (0, 0))
    (1, 1)
    >>> _tail_move((1, 2), (0, 0))
    (1, 1)
    >>> _tail_move((-1, -2), (0, 0))
    (-1, -1)
    """
    d = _delta(head, tail)
    adx = abs(d[0])
    ady = abs(d[1])

    if adx <= 1 and ady <= 1:
        return (0, 0)
    elif adx == 0:
        # ady == 2
        return (0, d[1] // ady)
    elif ady == 0:
        # adx == 2
        return (d[0] // adx, 0)
    else:
        return (d[0] // adx, d[1] // ady)


def _apply_move(pos, delta):
    """
    >>> _apply_move((1, 1), (1, 3))
    (2, 4)
    """
    return (pos[0] + delta[0], pos[1] + delta[1])


def part1(head_moves):
    head = (0, 0)
    tail = (0, 0)
    tail_visited = {tail}
    for head_move in head_moves:
        for _i in range(head_move.count):
            head = _apply_move(head, head_move.delta)
            tail = _apply_move(tail, _tail_move(head, tail))
            tail_visited.add(tail)

    pprint(tail_visited)
    return len(tail_visited)


if __name__ == "__main__":
    with open("input.txt") as f:
        head_moves = list(map(_parse_move, f))
    # pprint(head_moves)

    pprint(part1(head_moves))
