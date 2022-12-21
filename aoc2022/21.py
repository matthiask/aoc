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
    from pprint import pprint

    pprint(parse(test))

    # pprint(evaluate(parse(test)))

    calculations = parse(test)
    print("part1 test", calculations["root"].value(calculations))
    calculations = parse(input)
    print("part1", calculations["root"].value(calculations))
