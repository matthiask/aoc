from dataclasses import dataclass
from collections import defaultdict
from itertools import chain
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

    @classmethod
    def read(cls):
        system = cls()
        with open("12.txt") as f:
            for line in f:
                start, end = line.strip().split("-")
                system.create_path(start, end)
        return system

    def get_cave(self, name):
        if name not in self._caves:
            self._caves[name] = Cave(name, name.isupper())
        return self._caves[name]

    def create_path(self, start, end):
        cave1 = self.get_cave(start)
        cave2 = self.get_cave(end)

        assert not (cave1.is_big and cave2.is_big), "The code does not handle loops."

        self._paths[cave1].append(cave2)
        self._paths[cave2].append(cave1)

    def adjacent_caves(self, cave):
        return self._paths[cave]


def is_visitable(cave, path):
    # Small caves can only be visited once
    if cave.is_big:
        return True
    return cave not in path


def _deepen_into_adjacent_caves(paths):
    for path in paths:
        yield {
            path + (cave,)
            for cave in system.adjacent_caves(path[-1])
            if is_visitable(cave, path)
        }


def _deepen(paths):
    return set(chain.from_iterable(_deepen_into_adjacent_caves(paths)))


def bfs(system):
    start = system.get_cave("start")
    end = system.get_cave("end")

    end_reached = set()
    paths = {(start,)}
    while True:
        paths = _deepen(paths)

        end_reached |= {path for path in paths if path[-1] == end}
        paths -= end_reached

        if not paths:
            break

    print(len(end_reached))


if __name__ == "__main__":
    system = System.read()
    pprint(system._caves)
    pprint(system._paths)

    pprint(bfs(system))
