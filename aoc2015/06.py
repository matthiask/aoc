import re
from collections import defaultdict

from tools import range_inclusive


IN = [*open("06.txt")]


def parse_pair(s):
    return [int(part) for part in s.split(",")]


def parse_line(s):
    numbers = [int(number) for number in re.findall(r"[0-9]+", s)]
    return [{"turn on": "ON", "turn of": "OFF", "toggle ": "TOGGLE"}[s[:7]], *numbers]


instructions = [parse_line(line) for line in IN]


on = set()
for instruction, *coordinates in instructions:
    rect = {
        complex(x, y)
        for y in range_inclusive(coordinates[1], coordinates[3])
        for x in range_inclusive(coordinates[0], coordinates[2])
    }

    if instruction == "ON":
        on |= rect
    elif instruction == "OFF":
        on -= rect
    elif instruction == "TOGGLE":
        on = (on - rect) | (rect - on)

print(len(on))


brightness = defaultdict(int)
for instruction, *coordinates in instructions:
    rect = [
        complex(x, y)
        for y in range_inclusive(coordinates[1], coordinates[3])
        for x in range_inclusive(coordinates[0], coordinates[2])
    ]

    if instruction == "ON":
        for c in rect:
            brightness[c] += 1
    elif instruction == "OFF":
        for c in rect:
            brightness[c] = max(brightness[c] - 1, 0)
    elif instruction == "TOGGLE":
        for c in rect:
            brightness[c] += 2

print(sum(brightness.values()))
