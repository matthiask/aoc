from collections import defaultdict
from functools import reduce
from pprint import pprint

from tools import neighbors, open_input


IN = [line.strip() for line in open_input("03")]
W = len(IN[0])
H = len(IN)


def parse():
    symbols = {}
    numbers = defaultdict(str)
    for y in range(H):
        number_xy = None
        for x in range(W):
            c = IN[y][x]
            if c in "0123456789":
                if number_xy is None:
                    number_xy = x + y * 1j
                numbers[number_xy] += c
                continue
            number_xy = None
            if c != ".":
                symbols[x + y * 1j] = c

    neighbors_of_symbols = reduce(
        lambda a, b: a | b,
        (set(neighbors(xy, diagonal=True)) for xy in symbols),
    )
    numbers = dict(numbers)

    """
    pprint(
        {
            "symbols": symbols,
            "numbers": numbers,
            "neighbors_of_symbols": neighbors_of_symbols,
        }
    )
    """

    return symbols, numbers, neighbors_of_symbols


def number_locations(xy, number):
    return {xy + i for i in range(len(number))}


def solve1():
    symbols, numbers, neighbors_of_symbols = parse()

    pprint(
        sum(
            int(number)
            for xy, number in numbers.items()
            if number_locations(xy, number) & neighbors_of_symbols
        )
    )


def solve2():
    symbols, numbers, neighbors_of_symbols = parse()

    numbers_with_locations = [
        [number, number_locations(xy, number)] for xy, number in numbers.items()
    ]
    # pprint(numbers_with_locations)

    gears = []
    for xy, symbol in symbols.items():
        if symbol != "*":
            continue

        adjacent_numbers = [
            number
            for number, locations in numbers_with_locations
            if set(neighbors(xy, diagonal=True)) & locations
        ]
        if len(adjacent_numbers) == 2:
            gears.append(int(adjacent_numbers[0]) * int(adjacent_numbers[1]))

    pprint(sum(gears))


solve1()
solve2()
