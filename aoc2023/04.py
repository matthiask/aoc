from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint

from tools import numbers, open_input


IN = [line.strip() for line in open_input("04")]


@dataclass
class Card:
    id: int
    winning: set[int]
    have: set[int]

    def same(self):
        return len(self.winning & self.have)

    def point_value(self):
        same = len(self.winning & self.have)
        if same:
            return 2 ** (same - 1)
        return 0


def parse():
    for line in IN:
        card, n = line.split(": ")
        winning, have = n.split(" | ")
        yield Card(
            id=int(card.split()[1]),
            winning=set(numbers(winning)),
            have=set(numbers(have)),
        )


def solve1():
    # pprint(list(parse()))
    pprint(sum(card.point_value() for card in parse()))


def solve2():
    cards = list(parse())
    factor = defaultdict(lambda: 1, ((card.id, 1) for card in cards))
    for card in cards:
        factor.setdefault(card.id, 1)
        for i in range(card.same()):
            factor[card.id + 1 + i] += factor[card.id]
    pprint(factor)
    pprint(sum(factor.values()))


solve1()
solve2()
