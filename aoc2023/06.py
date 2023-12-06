from pprint import pprint

from tools import numbers, open_input


input = open_input("06")
races = list(zip(numbers(next(input)), numbers(next(input))))


pprint(races)


def distance_mm(button_ms, race_ms):
    mm_ms = button_ms
    return mm_ms * (race_ms - button_ms)


part1 = 1
for race_ms, distance_to_beat in races:
    part1 *= sum(
        1 if distance_mm(button_ms, race_ms) > distance_to_beat else 0
        for button_ms in range(1, race_ms)
    )

pprint(("part1", part1))
