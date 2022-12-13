import operator
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
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

    def small_intermediary_caves(self):
        return {
            cave
            for cave in self._caves.values()
            if not cave.is_big and cave.name not in {"start", "end"}
        }


def is_visitable_small_caves_only_once(cave, path):
    # Small caves can only be visited once
    if cave.is_big:
        return True
    return cave not in path


def is_visitable_one_small_cave_twice(small_cave):
    def _is_visitable(cave, path):
        if cave.is_big:
            return True
        if cave == small_cave:
            return sum(1 for cave in path if cave == small_cave) < 2
        return cave not in path

    return _is_visitable


def _deepen(paths, *, is_visitable):
    return reduce(
        operator.or_,
        (
            {
                path + (cave,)
                for cave in system.adjacent_caves(path[-1])
                if is_visitable(cave, path)
            }
            for path in paths
        ),
    )


def bfs(system, *, is_visitable):
    start = system.get_cave("start")
    end = system.get_cave("end")

    end_reached = set()
    paths = {(start,)}
    while True:
        paths = _deepen(paths, is_visitable=is_visitable)

        end_reached |= {path for path in paths if path[-1] == end}
        paths -= end_reached

        if not paths:
            break

    return end_reached


def part1(system):
    pprint(len(bfs(system, is_visitable=is_visitable_small_caves_only_once)))


def part2(system):
    paths = set()
    for cave in system.small_intermediary_caves():
        print(f"Allow visiting {cave} twice...")
        paths |= bfs(system, is_visitable=is_visitable_one_small_cave_twice(cave))
    pprint(len(paths))


if __name__ == "__main__":
    system = System.read()
    # pprint(system._caves)
    pprint(system._paths)

    part1(system)
    part2(system)
