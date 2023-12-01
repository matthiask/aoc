import operator
import re
from collections import defaultdict
from functools import reduce
from itertools import combinations_with_replacement


IN = [*open("15.txt")]
ingredients = {}
for line in IN:
    name, properties = line.split(": ")
    ingredients[name] = [
        (prop, int(val)) for prop, val in re.findall(r"(\w+) ([-\d]+)", properties)
    ]


def score(combination):
    values = defaultdict(int)
    for name, properties in ingredients.items():
        for prop, value in properties:
            values[prop] += combination.count(name) * value

    # Part 2
    if values["calories"] != 500:
        return 0

    return reduce(
        operator.mul,
        (max(0, value) for prop, value in values.items() if prop != "calories"),
        1,
    )


# print(ingredients)
combinations = combinations_with_replacement(ingredients.keys(), 100)
print(max(map(score, combinations)))
