from dataclasses import dataclass, field
from itertools import count, cycle
from pprint import pp
from string import ascii_uppercase

from tools import numbers, open_input


ascii_uppercase_iter = cycle(ascii_uppercase)


def overlaps(start1, end1, start2, end2):
    return end1 >= start2 and end2 >= start1


@dataclass(frozen=True, slots=True)
class Brick:
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int
    s: str = field(default_factory=lambda: next(ascii_uppercase_iter))

    def vertical(self, dz):
        return Brick(
            self.x1,
            self.y1,
            self.z1 + dz,
            self.x2,
            self.y2,
            self.z2 + dz,
            self.s,
        )

    def intersects(self, other):
        return (
            overlaps(self.x1, self.x2, other.x1, other.x2)
            and overlaps(self.y1, self.y2, other.y1, other.y2)
            and overlaps(self.z1, self.z2, other.z1, other.z2)
        )


bricks = [Brick(*numbers(line)) for line in open_input("22")]
floor = Brick(-99999, -99999, 0, 99999, 99999, 0)
pp(bricks)
# pp(floor)


def solve1():
    settled = [
        floor,
    ]
    print("Settling...")
    for brick in bricks:
        for dz in count(0, -1):
            # print(f"Trying to move {brick} down {dz - 1}")
            next = brick.vertical(dz - 1)
            if any(s.intersects(next) for s in settled):
                settled.append(brick.vertical(dz))
                break

    # pp(settled)

    print("Checking which bricks would be safe to disintegrate...")
    safe = set()
    for maybe_disintegrate in settled[1:]:
        up = maybe_disintegrate.vertical(1)
        # Find bricks which are supported by the brick we're looking at currently
        if supported := [
            s for s in settled if s != maybe_disintegrate and s.intersects(up)
        ]:
            for b in supported:
                below = b.vertical(-1)
                if len({s for s in settled if s != b and s.intersects(below)}) >= 2:
                    safe.add(maybe_disintegrate)
        else:
            safe.add(maybe_disintegrate)
    pp(sorted(brick.s for brick in safe))
    print(len(safe))


solve1()
