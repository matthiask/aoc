import operator
from collections import defaultdict, namedtuple

from utils import open_input


registers = defaultdict(int)
operators = {
    ">=": operator.ge,
    ">": operator.gt,
    "<=": operator.le,
    "<": operator.lt,
    "==": operator.eq,
    "!=": operator.ne,
}
ip = 0
Op = namedtuple("Op", "register op cond")


def _parse_line(line):
    tokens = line.strip().split(" ")
    delta = int(tokens[2])
    return Op(
        tokens[0],
        (lambda value: value + delta)
        if tokens[1] == "inc"
        else (lambda value: value - delta),
        (lambda: operators[tokens[5]](registers[tokens[4]], int(tokens[6]))),
    )


max_transitory = 0
IN = [_parse_line(line) for line in open_input("08")]
while 0 <= ip < len(IN):
    op = IN[ip]
    if op.cond():
        registers[op.register] = op.op(registers[op.register])
    ip += 1

    max_transitory = max(max_transitory, max(registers.values()))

print("part1", max(registers.values()))
print("part2", max_transitory)
