import re

from dataclasses import dataclass
from typing import Any, Callable
from pprint import pprint


@dataclass
class Monkey:
    idx: int
    items: list[int]
    operation: Callable[Any, Any]
    divisible_by: int
    if_true: int
    if_false: int

    inspection_count: int = 0

    def throw_all(self, monkeys):
        while self.items:
            item = self.operation(self.items.pop(0))

            self.inspection_count += 1

            if item % self.divisible_by == 0:
                monkeys[self.if_true].catch(item)
            else:
                monkeys[self.if_false].catch(item)

    def catch(self, item):
        self.items.append(item)


def _int_from_line(line):
    return _ints_from_line(line)[0]


def _ints_from_line(line):
    return [int(s) for s in re.findall(r"([0-9]+)", line)]


OP = {
    "+": lambda v: lambda worry: (worry + v) // 3,
    "*": lambda v: lambda worry: (worry * v) // 3,
}


def parse_monkey(lines):
    idx = _int_from_line(lines.pop(0))
    items = _ints_from_line(lines.pop(0))

    op = re.search(r"new = old (.) ([0-9]+|old)", lines.pop(0)).groups()
    if op == ("*", "old"):
        operation = lambda worry: (worry * worry) // 3
    else:
        operation = OP[op[0]](int(op[1]))

    divisible_by = _int_from_line(lines.pop(0))
    if_true = _int_from_line(lines.pop(0))
    if_false = _int_from_line(lines.pop(0))

    if lines:
        lines.pop(0)

    return Monkey(idx, items, operation, divisible_by, if_true, if_false)


def parse():
    with open("input.txt") as f:
        lines = [line.strip() for line in f]
    while lines:
        yield parse_monkey(lines)


if __name__ == "__main__":
    monkeys = {monkey.idx: monkey for monkey in parse()}

    for _i in range(20):
        for monkey in monkeys.values():
            monkey.throw_all(monkeys)

    pprint(monkeys)

    inspection_counts = sorted(monkey.inspection_count for monkey in monkeys.values())
    pprint(inspection_counts)

    print(inspection_counts[-1] * inspection_counts[-2])
