# https://hachyderm.io/@KeyJ@mastodon.gamedev.place/109547823771648367

VALUES = [*map(int, open("20.txt"))]
LENGTH = len(VALUES)


def P(c):
    ORDER = [*range(LENGTH)]
    for r in ORDER * c:
        i = ORDER.index(r)
        ORDER.insert((i + VALUES[ORDER.pop(i)]) % (LENGTH - 1), r)
    print(
        sum(
            VALUES[ORDER[(ORDER.index(VALUES.index(0)) + i * 1000) % LENGTH]]
            for i in (1, 2, 3)
        )
    )


P(1)
VALUES = [n * 811589153 for n in VALUES]
P(10)
