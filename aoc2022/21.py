import operator
from dataclasses import dataclass


input = open("21.txt").read()


test = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""


_operations = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
    "=": operator.eq,
}


@dataclass
class Calculation:
    name: str
    dependencies: list[str]
    _value: int | None = None
    operation: str | None = None

    def value(self, calculations):
        if self._value is not None:
            return self._value
        return _operations[self.operation](
            *[calculations[name].value(calculations) for name in self.dependencies]
        )


class Human:
    name = "humn"

    def __init__(self):
        self.calculations = []

    def value(self, calculations):
        return self

    def __add__(self, value):
        self.calculations.append(lambda v: v - value)
        return self

    __radd__ = __add__

    def __sub__(self, value):
        self.calculations.append(lambda v: v + value)
        return self

    def __rsub__(self, value):
        # will_be_known = intermediate - humn
        # ==> humn = intermediate - will_be_known
        self.calculations.append(lambda v: value - v)
        return self

    def __mul__(self, value):
        # will_be_known = intermediate * humn
        # ==> humn = will_be_known // intermediate
        self.calculations.append(lambda v: v // value)
        return self

    __rmul__ = __mul__

    def __floordiv__(self, value):
        self.calculations.append(lambda v: v * value)
        return self

    def __eq__(self, value):
        # print("__eq__", value)
        # return self

        for calc in reversed(self.calculations):
            value = calc(value)
        return value


def parse_calculation(line):
    name, calculation = line.split(": ")
    try:
        _value = int(calculation)
    except ValueError:
        parts = calculation.split()
        return name, Calculation(
            name=name, dependencies=[parts[0], parts[2]], operation=parts[1]
        )
    else:
        return name, Calculation(name=name, dependencies=[], _value=_value)


def parse(input):
    return dict(parse_calculation(line) for line in input.strip().splitlines())


if __name__ == "__main__":
    # from pprint import pprint
    # pprint(parse(test))
    # pprint(evaluate(parse(test)))

    calculations = parse(test)
    print("part1 test", calculations["root"].value(calculations))
    calculations = parse(input)
    print("part1", calculations["root"].value(calculations))

    calculations = parse(test)
    calculations["humn"] = Human()
    calculations["root"].operation = "="
    print("part2 test", calculations["root"].value(calculations))

    calculations = parse(input)
    calculations["humn"] = Human()
    calculations["root"].operation = "="
    print("part2", calculations["root"].value(calculations))
