from itertools import count


p1_start = 6
p2_start = 2


def die(sum_of):
    """
    >>> d = die(3)
    >>> next(d)
    6
    >>> next(d)
    15
    >>> next(d)
    24
    """
    d = count(0)

    while True:
        yield sum(next(d) for _i in range(sum_of)) % 100 + sum_of


def modulo_one(num, mod):
    """
    >>> modulo_one(10, 10)
    10
    >>> modulo_one(11, 10)
    1
    >>> modulo_one(12, 10)
    2
    """
    return (num - 1) % mod + 1


def play():
    p1_position = 6
    p2_position = 2

    p1_score = 0
    p2_score = 0

    d = die(3)
    die_throws = 0

    while True:
        p1_position = modulo_one(p1_position + next(d), 10)
        p1_score += p1_position
        die_throws += 3

        if p1_score >= 1000:
            return p2_score * die_throws

        p2_position = modulo_one(p2_position + next(d), 10)
        p2_score += p2_position
        die_throws += 3

        if p2_score >= 1000:
            return p1_score * die_throws


if __name__ == "__main__":
    print(play())
