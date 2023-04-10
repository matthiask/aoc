import re

from tools import open_input


instructions = [re.split(r"[\s,]+", line.strip()) for line in open_input("23")]


def run(reg):
    ip = 0
    while 0 <= ip < len(instructions):
        op, *args = instructions[ip]
        if op == "hlf":
            reg[args[0]] //= 2
        elif op == "tpl":
            reg[args[0]] *= 3
        elif op == "inc":
            reg[args[0]] += 1
        elif op == "jmp":
            ip += int(args[0])
            continue
        elif op == "jie":
            if reg[args[0]] % 2 == 0:
                ip += int(args[1])
                continue
        elif op == "jio":
            if reg[args[0]] == 1:
                ip += int(args[1])
                continue

        ip += 1

    return reg


print(run({"a": 0, "b": 0}))
print(run({"a": 1, "b": 0}))
