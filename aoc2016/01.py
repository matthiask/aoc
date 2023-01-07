IN = open("01.txt").read().strip().split(", ")
directions = [1j, 1, -1j, -1]


def mh(where):
    return int(abs(where.real) + abs(where.imag))


def p1():
    where = 0
    direction = 0
    for walk in IN:
        assert walk[0] in ("L", "R")
        direction = (direction + (1 if walk[0] == "R" else -1)) % 4
        where += directions[direction] * int(walk[1:])
    print(mh(where))


def p2():
    where = 0
    direction = 0
    seen = set()
    for walk in IN:
        assert walk[0] in ("L", "R")
        direction = (direction + (1 if walk[0] == "R" else -1)) % 4
        for _ in range(int(walk[1:])):
            where += directions[direction]
            if where in seen:
                print(mh(where))
                return
            seen.add(where)


p1()
p2()
