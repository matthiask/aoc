from collections import Counter
from pprint import pprint


def read():
    with open("14.txt") as f:
        template, rules = f.read().split("\n\n")
    rules = rules.strip().split("\n")
    rules = dict(rule.split(" -> ") for rule in rules)
    return template, rules


def step(template, rules):
    """
    >>> step("ABC", {"AB": "D", "BC": "E"})
    'ADBEC'
    """
    result = [template[0]]
    for i in range(len(template) - 1):
        result.append(rules[template[i:i+2]])
        result.append(template[i+1])
    return "".join(result)


def eval(polymer):
    counter = Counter()
    counter.update(polymer)
    frequencies = sorted(counter.items(), key=lambda r: r[1])
    return frequencies[-1][1] - frequencies[0][1]


def part1():
    p, rules = read()
    for _i in range(10):
        p = step(p, rules)
    print(len(p))
    print(eval(p))


def part2():
    p, rules = read()
    for _i in range(40):
        p = step(p, rules)
        print(_i + 1, len(p), eval(p))


if __name__ == "__main__":
    # pprint(read())
    part1()
    part2()
