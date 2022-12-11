from collections import Counter
from itertools import chain


with open("06.txt") as f:
    INITIAL = [int(days) for days in f.read().strip().split(",")]


# def cycle_one(fish):
#     if fish == 0:
#         return [6, 8]
#     else:
#         return [fish - 1]
#
#
# def cycle_all(fishes):
#     return list(chain.from_iterable(cycle_one(fish) for fish in fishes))
#
#
# def part1():
#     fishes = INITIAL
#     for _i in range(80):
#         fishes = cycle_all(fishes)
#     print("part1:", len(fishes))
#
#
# part1()


counter = Counter()
counter.update(INITIAL)

generation = [counter.get(days, 0) for days in range(0, 9)]


def cycle(generation):
    head, *tail = generation
    tail[6] += head
    tail.append(head)
    return tail


p1 = generation[:]
for _i in range(80):
    p1 = cycle(p1)

print(sum(p1))

p2 = generation[:]
for _i in range(256):
    p2 = cycle(p2)

print(sum(p2))
