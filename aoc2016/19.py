from dataclasses import dataclass
from itertools import count
from pprint import pprint


@dataclass
class Elf:
    id: int
    next: "Elf"


def circle(count):
    elves = []
    elf = None
    for i in range(count, 0, -1):
        elf = Elf(i, elf)
        elves.append(elf)
    elves[0].next = elves[-1]
    return elves[-1]
    # return list(reversed(elves))


def party(elf):
    while elf != elf.next:
        # print(elf.id, elf.next.id)
        # Take all presents from next elf, they are out.
        elf.next = elf.next.next
        elf = elf.next
    return elf


# party([1,2,3,4,5])
# pprint(circle(5))
# pprint(circle(5))
# pprint(party(circle(5)))
# pprint(party(circle(3005290)))


def party2(elf):
    lst = [elf]
    e = elf
    while (e := e.next) != elf:
        lst.append(e)

    half = lst[len(lst) // 2 - 1]

    c = count()
    while elf != elf.next:
        # print("elf", elf.id, "half-prev", half.id, "half", half.next.id)
        # print(half.next.id, "is removed")
        half.next = half.next.next
        if next(c) % 2 == 0:
            half = half.next
        elf = elf.next

    return elf


print(party2(circle(5)))
print(party2(circle(3005290)))
"""
def elves(count):
    return list(range(1, count + 1))


def party1(elves):
    i = 0
    while len(elves) > 1:
        # print(elves)
        if i + 1 >= len(elves):
            elves.pop((i + 1) % len(elves))
            i = i % len(elves)
            print("debug", len(elves))
        else:
            elves.pop((i + 1) % len(elves))
            i += 1
    return elves[0]


print(party1(elves(5)))
print(party1(elves(3005290)))
"""
