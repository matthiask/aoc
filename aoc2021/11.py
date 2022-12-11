import operator
from functools import reduce


with open("11.txt") as f:
    INITIAL = {
        (x, y): int(h) for y, line in enumerate(f) for x, h in enumerate(line.strip())
    }


max_x = max(x for x, y in INITIAL.keys()) + 1
max_y = max(y for x, y in INITIAL.keys()) + 1

all_points = [(x, y) for x in range(max_x) for y in range(max_y)]


def pretty(energy):
    return "\n".join(
        " ".join(str(energy[(x, y)]) for x in range(max_x))
        for y in range(max_y)
    )


def surrounding(point):
    x, y = point
    deltas = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
    points = [(x + dx, y + dy) for dx, dy in deltas]
    return set((x, y) for (x, y) in points if 0 <= x < max_x and 0 <= y < max_y)


def enough_energy_to_flash(energy):
    return {point for point in all_points if energy[point] > 9}


def part1():
    energy = dict(INITIAL)
    flash_count = 0

    def _maybe_flash(flashed):
        if new := enough_energy_to_flash(energy) - flashed:
            for flashing in new:
                for point in surrounding(flashing):
                    energy[point] += 1

            return len(new) + _maybe_flash(flashed | new)
        for point in flashed:
            energy[point] = 0
        return 0

    for _i in range(100):
        for point in all_points:
            energy[point] += 1

        flash_count += _maybe_flash(set())

    print("part1", flash_count)


def part2():
    energy = dict(INITIAL)
    flash_count = 0

    def _maybe_flash(flashed):
        if new := enough_energy_to_flash(energy) - flashed:
            for flashing in new:
                for point in surrounding(flashing):
                    energy[point] += 1

            return len(new) + _maybe_flash(flashed | new)
        for point in flashed:
            energy[point] = 0
        return 0

    for step in range(1000):
        for point in all_points:
            energy[point] += 1

        if _maybe_flash(set()) == max_x * max_y:
            print("part2", step + 1)
            break


if __name__ == "__main__":
    part1()
    part2()
