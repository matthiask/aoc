import operator
import re
from collections import namedtuple
from pprint import pp

from tools import numbers, open_input


part = namedtuple("part", "x m a s")


def parse():
    workflowlines, partlines = open_input("19").read().strip().split("\n\n")

    workflows = {}
    for line in workflowlines.split("\n"):
        name, steps = line[:-1].split("{")
        steps = steps.split(",")
        fn = None
        for step in steps[::-1]:
            if ":" in step:
                condition, target = step.split(":")
                var, op, val = re.split(r"([<>])", condition)
                op = {">": operator.gt, "<": operator.lt}[op]
                val = int(val)
                fn = (  # noqa: E731
                    lambda part, fn=fn, var=var, op=op, val=val, target=target: target
                    if op(getattr(part, var), val)
                    else fn(part)
                )
            else:
                fn = lambda part, target=step: target  # noqa: E731
        workflows[name] = fn

    parts = [part(*numbers(line)) for line in partlines.split("\n")]
    return workflows, parts


def rating(part):
    return sum(part._asdict().values())


def solve1():
    workflows, parts = parse()
    # pp(rules)
    # pp(parts)

    r = 0
    for part in parts:
        state = "in"
        while (state := workflows[state](part)) not in {"A", "R"}:
            pass

        if state == "A":
            r += rating(part)

        # print(part, state)
    pp(("part1", r))


solve1()
