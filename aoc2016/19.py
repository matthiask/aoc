from dataclasses import dataclass
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
pprint(circle(5))
pprint(party(circle(5)))
pprint(party(circle(3005290)))
