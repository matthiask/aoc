import sys
from collections import defaultdict


filename = sys.argv[1] if len(sys.argv) > 1 else "06.txt"


centers = defaultdict(list)
for center, satellite in (
    line.split(")") for line in open(filename).read().strip().split("\n")
):
    centers[center].append(satellite)


def count_orbits(center):
    orbits = [count_orbits(satellite) for satellite in centers[center]]

    planets = sum((orbit[0] for orbit in orbits), 0)
    orbits = planets + sum((orbit[1] for orbit in orbits), 0)
    print(locals())
    return planets + 1, orbits


print("part1", count_orbits("COM"))


orbiting = {}
for center, satellites in centers.items():
    for satellite in satellites:
        orbiting[satellite] = center


def path(satellite):
    while satellite := orbiting.get(satellite):
        yield satellite


print(orbiting)
you = list(path("YOU"))
san = list(path("SAN"))

for index, center in enumerate(you):
    try:
        index2 = san.index(center)
    except ValueError:
        continue

    print(index + index2)
    break
