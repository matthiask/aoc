from dataclasses import dataclass
from itertools import count
from pprint import pp

from tools import numbers, open_input


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

    def vertical(self, dz):
        return Brick(
            self.x1,
            self.y1,
            self.z1 + dz,
            self.x2,
            self.y2,
            self.z2 + dz,
        )

    def intersects(self, other):
        return (
            overlaps(self.x1, self.x2, other.x1, other.x2)
            and overlaps(self.y1, self.y2, other.y1, other.y2)
            and overlaps(self.z1, self.z2, other.z1, other.z2)
        )


bricks = [Brick(*numbers(line)) for line in open_input("22")]
floor = Brick(0, 0, 0, 9999, 9999, 0)
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

    pp(settled)
    would_be_safe_to_disintegrate = 0
    for maybe_disintegrate in settled[1:]:
        up = maybe_disintegrate.vertical(1)
        # Find bricks which are supported by the brick we're looking at currently
        supported = [s for s in settled if s != maybe_disintegrate and s.intersects(up)]
        for b in supported:
            below = b.vertical(-1)
            if not any(
                s.intersects(below)
                for s in settled
                if s != maybe_disintegrate and s != b
            ):
                break
        else:
            would_be_safe_to_disintegrate += 1
    print(would_be_safe_to_disintegrate)


solve1()
