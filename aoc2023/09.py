from pprint import pp

from tools import numbers, open_input


def parse():
    return [numbers(line) for line in open_input("09")]


def differences(line):
    return [line[i + 1] - line[i] for i in range(len(line) - 1)]


def solve1():
    lines = parse()
    total = 0
    for line in lines:
        line_total = 0
        while any(line):
            # pp(line)
            line_total += line[-1]
            line = differences(line)
        total += line_total
        pp(("line_total", line, line_total))
    pp(("part1", total))

    # pp(n)


# pp(parse())
solve1()
