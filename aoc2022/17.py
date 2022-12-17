from dataclasses import dataclass, field, replace
from itertools import cycle
from time import monotonic
from typing import List


rocks = """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""


def parse_jets(filename):
    with open(filename) as f:
        return list(f.read().strip())


LEFT = 64
RIGHT = 1


@dataclass
class Rock:
    pattern: str
    bits: List[int]

    def shift(self, direction):
        if direction == "<":
            if all(b & LEFT == 0 for b in self.bits):
                return replace(self, bits=[b << 1 for b in self.bits])
        elif direction == ">":
            if all(b & RIGHT == 0 for b in self.bits):
                return replace(self, bits=[b >> 1 for b in self.bits])
        else:
            raise Exception()
        return self


@dataclass
class Chamber:
    bits: List[int] = field(default_factory=list)

    @property
    def rows(self):
        return len(self.bits)

    def fall_one(self, rock, jets):
        row = self.rows + 3
        while True:
            next_rock = rock.shift(next(jets))
            if all(b1 & b2 == 0 for b1, b2 in zip(next_rock.bits, self.bits[row:])):
                rock = next_rock

            next_row = row - 1
            if next_row < 0:
                break

            if any(b1 & b2 for b1, b2 in zip(rock.bits, self.bits[next_row:])):
                break

            row = next_row

        # Register hit
        chamber_rows = self.rows
        for index, bits in enumerate(rock.bits):
            bit_row = row + index
            if bit_row < chamber_rows:
                self.bits[bit_row] |= bits
            else:
                self.bits.append(bits)

    def prettify(self, rock_bits=None):
        return "\n".join(
            "".join("#" if bit & 1 << idx else "." for idx in range(6, -1, -1))
            for bit in reversed(self.bits + (rock_bits or []))
        )


def parse_rock(rock):
    """
    bits[0] is lowermost row
    bits[1] is row above it
    etc.
    """

    bits = [
        int(f"{row.strip():.<7}".replace("#", "1").replace(".", "0"), 2) >> 2
        for row in reversed(rock.split("\n"))
    ]
    return Rock(rock, bits)


def parse_rocks(rocks):
    return [parse_rock(rock.strip()) for rock in rocks.split("\n\n")]


if __name__ == "__main__":
    from pprint import pprint

    chamber = Chamber()
    rocks = parse_rocks(rocks)
    jets = parse_jets("17.txt")

    pprint(rocks)
    pprint(jets)

    rocks = cycle(rocks)
    jets = cycle(jets)

    for _i in range(2022):
        rock = next(rocks)
        print(f"\n\nInserting {rock}...")
        # print(chamber.prettify([0, 0, 0] + rock.bits))
        chamber.fall_one(rock, jets)

    print(chamber.prettify())
    print(chamber.rows)

    start = monotonic()
    count = 1000000000000
    for i in range(count):
        rock = next(rocks)
        chamber.fall_one(rock, jets)

        if i and i % 1000000 == 0:
            elapsed = monotonic() - start
            estimate = elapsed / i * count
            print(
                f"{i} / {count} ({i / count * 100:.2f}%), elapsed {elapsed:.2f}s, estimated {estimate:.2f}s"
            )
    print(chamber.rows)


# Gave up on the second part, see https://www.reddit.com/r/adventofcode/comments/znykq2/2022_day_17_solutions/
# The dumb solution would require almost a month if not running out of memory.
