from dataclasses import dataclass, field, replace
from itertools import cycle


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
        return cycle(list(f.read().strip()))


LEFT = 64
RIGHT = 1


@dataclass
class Rock:
    pattern: str
    bits: list[int]

    def shift(self, direction):
        if direction == "<":
            print("Left... ", end="")
            if all(b & LEFT == 0 for b in self.bits):
                print("yes! ", end="")
                return replace(self, bits=[b << 1 for b in self.bits])
        elif direction == ">":
            print("Right... ", end="")
            if all(b & RIGHT == 0 for b in self.bits):
                print("yes! ", end="")
                return replace(self, bits=[b >> 1 for b in self.bits])
        else:
            raise Exception()
        return self


@dataclass
class Chamber:
    bits: list[int] = field(default_factory=list)

    @property
    def uppermost_row(self):
        return len(self.bits)

    def insert_rock(self, rock):
        row = len(self.bits) + 4
        return [rock, row]

    def fall_one(self, falling_rock, jets):
        rock, row = falling_rock
        while True:
            rock = rock.shift(next(jets))
            print("Rock is", rock)
            next_row = row - 1

            if next_row > 0 and all(
                b1 & b2 == 0 for b1, b2 in zip(rock.bits, self.bits[next_row - 1 :])
            ):
                # No hit
                row = next_row
                continue

            break

        # Register hit
        chamber_rows = self.uppermost_row
        for index, bits in enumerate(rock.bits):
            bit_row = row + index
            if bit_row < chamber_rows:
                self.bits[bit_row] |= bits
            else:
                self.bits.append(bits)

    def prettify(self):
        return "\n".join(
            "".join("#" if bit & 1 << idx else "." for idx in range(6, -1, -1))
            for bit in reversed(self.bits)
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

    # pprint(jets("17-test.txt"))
    pprint(parse_rocks(rocks))

    chamber = Chamber()
    rocks = cycle(parse_rocks(rocks))
    jets = parse_jets("17-test.txt")

    for _i in range(10):
        rock = next(rocks)
        print(f"Inserting {rock}...")
        fr = chamber.insert_rock(rock)
        chamber.fall_one(fr, jets)

        print()
        print(chamber.prettify())

    print(chamber.uppermost_row)
