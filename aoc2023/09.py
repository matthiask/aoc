from pprint import pp

from tools import numbers, open_input


def parse():
    return [numbers(line) for line in open_input("09")]


def differences(line):
    return [line[i + 1] - line[i] for i in range(len(line) - 1)]


def solve1():
    lines = parse()
    total_1 = 0
    total_2 = 0
    for line in lines:
        line_total_1 = 0
        line_total_2 = 0
        sign = 1
        while any(line):
            # pp(line)
            line_total_1 += line[-1]
            line_total_2 += line[0] * sign
            sign *= -1
            line = differences(line)
            # pp(locals())
        total_1 += line_total_1
        total_2 += line_total_2
        pp(("line_total_1", line, line_total_1))
        pp(("line_total_2", line, line_total_2))
    pp(("part1", total_1))
    pp(("part2", total_2))

    # pp(n)


# pp(parse())
solve1()
