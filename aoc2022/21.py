import operator
from dataclasses import dataclass
from functools import reduce


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


# django/utils/topological_sort.py
class CyclicDependencyError(ValueError):
    pass


def topological_sort_as_sets(dependency_graph):
    """
    Variation of Kahn's algorithm (1962) that returns sets.

    Take a dependency graph as a dictionary of node => dependencies.

    Yield sets of items in topological order, where the first set contains
    all nodes without dependencies, and each following set contains all
    nodes that may depend on the nodes only in the previously yielded sets.
    """
    todo = dependency_graph.copy()
    while todo:
        current = {node for node, deps in todo.items() if not deps}

        if not current:
            raise CyclicDependencyError(
                "Cyclic dependency in graph: {}".format(
                    ", ".join(repr(x) for x in todo.items())
                )
            )

        yield current

        # remove current from todo's nodes & dependencies
        todo = {
            node: (dependencies - current)
            for node, dependencies in todo.items()
            if node not in current
        }


def stable_topological_sort(nodes, dependency_graph):
    result = []
    for layer in topological_sort_as_sets(dependency_graph):
        for node in nodes:
            if node in layer:
                result.append(node)
    return result


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
        return reduce(
            _operations[self.operation],
            (calculations[name].value(calculations) for name in self.dependencies),
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


def evaluate(calculations):
    evaluation_ordering = stable_topological_sort(
        calculations.keys(),
        {key: calculation.dependency_list for key, calculation in calculations.items()},
    )

    values = {}
    for name in evaluation_ordering:
        values[name] = 0


if __name__ == "__main__":
    from pprint import pprint

    pprint(parse(test))

    # pprint(evaluate(parse(test)))

    calculations = parse(test)
    print("part1 test", calculations["root"].value(calculations))
    calculations = parse(input)
    print("part1", calculations["root"].value(calculations))
