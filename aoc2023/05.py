from dataclasses import dataclass
from pprint import pprint

from tools import numbers, open_input


parts = open_input("05").read().strip().split("\n\n")


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

    @property
    def src_min(self):
        return self.src

    @property
    def src_max(self):
        return self.src + self.len - 1

    def overlaps(self, range2):
        return range2.max > self.src_min and range2.min < self.src_max

    def map2(self, range2):
        if range2.max < self.src_min or range2.min > self.src_max:
            yield range2
        else:
            # Part of range2 below self
            below = self.src_min - range2.min
            if below > 0:
                yield Range2(range2.min, below)

            # Part of range2 above self
            above = range2.max - self.src_max
            if above > 0:
                yield Range2(self.src_max + 1, above)

            if (len := range2.len - max(below, 0) - max(above, 0)) > 0:
                yield Range2(
                    self.dst + self.src_min - range2.min,
                    len,
                )


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


def parse_maps():
    maps = {}
    for map in parts[1:]:
        lines = map.split("\n")
        src, dst = lines[0].split(" ")[0].split("-to-")
        maps[src] = Map(
            src=src,
            dst=dst,
            ranges=[Range(*numbers(line)) for line in lines[1:]],
        )

    return maps


def solve1():
    seeds = numbers(parts[0])
    maps = parse_maps()

    # pprint(seeds)
    # pprint(maps)

    # for number in (0, 50, 96, 98, 100):
    #     pprint((number, maps["seed"].map(number)))

    final = []

    for number in seeds:
        type = "seed"
        while type in maps:
            number = maps[type].map(number)
            type = maps[type].dst
        final.append(number)
        # pprint(number)

    pprint(("part1", min(final)))


@dataclass
class Range2:
    min: int
    len: int

    @property
    def max(self):
        return self.min + self.len - 1


def solve2():
    n = numbers(parts[0])
    ranges = []
    for i in range(0, len(n), 2):
        ranges.append(Range2(*n[i : i + 2]))
    pprint(ranges)
    maps = parse_maps()

    type = "seed"
    while type in maps:
        new_ranges = []
        for range2 in ranges:
            for r in maps[type].ranges:
                if r.overlaps(range2):
                    new_ranges.extend(r.map2(range2))
        ranges = new_ranges
        pprint((type, ranges))
        type = maps[type].dst

    pprint(ranges)


solve1()
solve2()
