from pprint import pprint

from tools import numbers, open_input


def distance_mm(button_ms, race_ms):
    mm_ms = button_ms
    return mm_ms * (race_ms - button_ms)


def solve1():
    input = open_input("06")
    races = list(zip(numbers(next(input)), numbers(next(input))))

    pprint(races)

    part1 = 1
    for race_ms, distance_to_beat in races:
        part1 *= sum(
            1 if distance_mm(button_ms, race_ms) > distance_to_beat else 0
            for button_ms in range(1, race_ms)
        )

    pprint(("part1", part1))


def solve2():
    input = open_input("06")
    races = list(
        zip(
            numbers(next(input).replace(" ", "")), numbers(next(input).replace(" ", ""))
        )
    )

    pprint(races)

    part2 = 1
    for race_ms, distance_to_beat in races:
        part2 *= sum(
            1 if distance_mm(button_ms, race_ms) > distance_to_beat else 0
            for button_ms in range(1, race_ms)
        )

    pprint(("part2", part2))


solve1()
solve2()
