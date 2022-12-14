def range_to_set(s):
    start, end = tuple(map(int, s.split("-")))
    return set(range(start, end + 1))


def parse():
    with open("04.txt") as f:
        for line in f:
            yield tuple(map(range_to_set, line.strip().split(",")))


def one_contains_other(set1, set2):
    return set1 <= set2 or set1 >= set2


if __name__ == "__main__":
    # pprint(list(parse()))

    print(sum(1 for pairing in parse() if one_contains_other(*pairing)))
    print(sum(1 for pairing in parse() if pairing[0] & pairing[1]))
