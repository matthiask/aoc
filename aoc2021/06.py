from collections import Counter
from itertools import chain


with open("06.txt") as f:
    INITIAL = [int(days) for days in f.read().strip().split(",")]


def cycle_one(fish):
    if fish == 0:
        return [6, 8]
    else:
        return [fish - 1]


def cycle_all(fishes):
    return list(chain.from_iterable(cycle_one(fish) for fish in fishes))


def part1():
    fishes = INITIAL
    for _i in range(80):
        fishes = cycle_all(fishes)
    print("part1:", len(fishes))


part1()
