import operator
import re


IN = [*open("16.txt")]

search = """\
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""


def parse_facts(s):
    return {key: int(value) for key, value in re.findall(r"(\w+): (\d+)", s)}


sf = parse_facts(search)

for sue in IN:
    facts = parse_facts(sue)
    if all(sf[attribute] == value for attribute, value in facts.items()):
        print(sue)
        break


comparators = {
    "cats": operator.gt,
    "trees": operator.gt,
    "pomeranians": operator.lt,
    "goldfish": operator.lt,
}

for sue in IN:
    facts = parse_facts(sue)
    if all(
        comparators.get(attribute, operator.eq)(value, sf[attribute])
        for attribute, value in facts.items()
    ):
        print(sue)
        break
