from dataclasses import dataclass
from pprint import pprint

from tools import numbers, open_input


IN = [line.strip() for line in open_input("05")]


@dataclass
class Range:
    dst: int
    src: int
    len: int

    def in_range(self, number):
        return self.src <= number < self.src + self.len

    def map(self, number):
        delta = number - self.src
        if 0 <= delta < self.len:
            return self.dst + delta
        return number


@dataclass
class Map:
    src: str
    dst: str
    ranges: list[Range]

    def map(self, number):
        for range in self.ranges:
            if range.in_range(number):
                number = range.map(number)
                break
        return number


def parse():
    parts = open_input("05").read().strip().split("\n\n")

    seeds = numbers(parts[0])
    maps = {}
    for map in parts[1:]:
        lines = map.split("\n")
        src, dst = lines[0].split(" ")[0].split("-to-")
        maps[src] = Map(
            src=src,
            dst=dst,
            ranges=[Range(*numbers(line)) for line in lines[1:]],
        )

    return seeds, maps


def solve1():
    seeds, maps = parse()
    pprint(seeds)
    pprint(maps)

    for number in (0, 50, 96, 98, 100):
        pprint((number, maps["seed"].map(number)))

    final = []

    for number in seeds:
        type = "seed"
        while type in maps:
            number = maps[type].map(number)
            type = maps[type].dst
        final.append(number)
        pprint(number)

    pprint(min(final))


def solve2():
    pass


solve1()
solve2()
