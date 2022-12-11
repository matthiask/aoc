from collections import Counter, defaultdict
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
    polymer, rules = read()

    counts = defaultdict(int)
    for pair in zip(polymer, polymer[1:]):
        counts[pair] += 1

    pprint(counts)

    pair_rules = {}
    for pair, middle in rules.items():
        pair_rules[tuple(list(pair))] = [(pair[0], middle), (middle, pair[1])]

    pprint(pair_rules)

    for _i in range(40):
        for pair, count in list(counts.items()):
            if count < 0:
                raise Exception
            if count == 0:
                continue
            counts[pair] -= count
            for new in pair_rules[pair]:
                counts[new] += count

    pprint(counts)

    element_counts = defaultdict(int)
    # First element
    element_counts["P"] += 1
    # Now, only ever count the second element of a pair to not double count
    # any elements
    for pair, count in counts.items():
        element_counts[pair[1]] += count

    frequencies = sorted(element_counts.items(), key=lambda r: r[1])
    pprint(frequencies[-1][1] - frequencies[0][1])


if __name__ == "__main__":
    # pprint(read())
    part1()
    part2()
