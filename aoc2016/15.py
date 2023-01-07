import re
from dataclasses import dataclass
from sys import argv


@dataclass
class Disc:
    number: int
    positions: int
    zero: int

    def at(self, seconds: int) -> int:
        return (self.zero + seconds) % self.positions


def parse_disc(line):
    numbers = [int(n) for n in re.findall(r"\d+", line)]
    return Disc(numbers[0], numbers[1], numbers[3])


discs = [parse_disc(line) for line in open("15.txt" if len(argv) < 2 else argv[1])]


def all_zero():
    seconds = 0
    while True:
        seconds += 1
        if all(disc.at(seconds + offset + 1) == 0 for offset, disc in enumerate(discs)):
            return seconds


# print(discs)
print(all_zero())
discs.append(Disc(99, 11, 0))
print(all_zero())
