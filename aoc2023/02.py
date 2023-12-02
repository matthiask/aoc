from dataclasses import dataclass
from functools import reduce
from pprint import pprint

from tools import open_input


@dataclass
class Sample:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __lt__(self, other):
        return (
            self.red <= other.red
            and self.green <= other.green
            and self.blue <= other.blue
        )

    def minimum_possible(self, other):
        return Sample(
            red=max(self.red, other.red),
            green=max(self.green, other.green),
            blue=max(self.blue, other.blue),
        )

    def power(self):
        return self.red * self.green * self.blue


@dataclass
class Game:
    id: int
    samples: list[Sample]


IN = [*open_input("02")]


def sample(sample):
    cubes = sample.split(", ")
    return Sample(**{cube.split()[1]: int(cube.split()[0]) for cube in cubes})


def games(lines):
    for line in lines:
        game, samples = line.split(": ")
        yield Game(
            id=int(game.split()[1]), samples=[sample(s) for s in samples.split("; ")]
        )


def solve1():
    counts = Sample(red=12, green=13, blue=14)
    # pprint(list(games(IN)))

    possible_id_sum = 0
    for game in games(IN):
        if all(sample < counts for sample in game.samples):
            possible_id_sum += game.id

    pprint(possible_id_sum)


def solve2():
    powers = 0
    for game in games(IN):
        sample = reduce(lambda a, b: a.minimum_possible(b), game.samples)
        powers += sample.power()

    pprint(powers)


solve1()
solve2()
