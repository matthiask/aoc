import re
from collections.abc import Callable
from dataclasses import dataclass
from pprint import pprint
from typing import Any


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


def parse_monkey(lines, *, relief):
    idx = _int_from_line(lines.pop(0))
    items = _ints_from_line(lines.pop(0))

    op = re.search(r"new = old (.) ([0-9]+|old)", lines.pop(0)).groups()
    match op:
        case ("*", "old"):
            operation = lambda worry: relief(worry * worry)
        case ("*", v):
            v = int(v)
            operation = lambda worry: relief(worry * v)
        case ("+", v):
            v = int(v)
            operation = lambda worry: relief(worry + v)
        case _:
            raise Exception

    divisible_by = _int_from_line(lines.pop(0))
    if_true = _int_from_line(lines.pop(0))
    if_false = _int_from_line(lines.pop(0))

    if lines:
        lines.pop(0)

    return Monkey(idx, items, operation, divisible_by, if_true, if_false)


def parse(*, relief):
    with open("11.txt") as f:
        lines = [line.strip() for line in f]
    while lines:
        yield parse_monkey(lines, relief=relief)


def simulate(*, relief, rounds):
    monkeys = {monkey.idx: monkey for monkey in parse(relief=relief)}

    for _i in range(rounds):
        for monkey in monkeys.values():
            monkey.throw_all(monkeys)

    # pprint(monkeys)
    inspection_counts = sorted(monkey.inspection_count for monkey in monkeys.values())
    # pprint(inspection_counts)
    pprint(inspection_counts[-1] * inspection_counts[-2])


if __name__ == "__main__":
    simulate(rounds=20, relief=lambda v: v // 3)
    simulate(rounds=10000, relief=lambda v: v % (11 * 2 * 5 * 17 * 19 * 7 * 3 * 13))
