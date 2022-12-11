from dataclasses import dataclass
from collections import defaultdict
from pprint import pprint


@dataclass
class Cave:
    name: str
    is_big: bool

    def __hash__(self):
        return hash(self.name)


class System:
    def __init__(self):
        self._caves = {}
        self._paths = defaultdict(list)

    def get_cave(self, name):
        if name not in self._caves:
            self._caves[name] = Cave(name, name.isupper())
        return self._caves[name]

    def create_path(self, start, end):
        cave1 = self.get_cave(start)
        cave2 = self.get_cave(end)

        self._paths[cave1].append(cave2)
        self._paths[cave2].append(cave1)

    def adjacent_caves(self, cave):
        return self._paths[cave]


def read():
    system = System()
    with open("12.txt") as f:
        for line in f:
            start, end = line.strip().split("-")
            system.create_path(start, end)
    return system


if __name__ == "__main__":
    system = read()
    pprint(system._caves)
    pprint(system._paths)
