IN = [line.strip().split() for line in open("12.txt")]
registers = {r: 0 for r in "abcd"}
ip = 0


# part 2
registers["c"] = 1


def read(r):
    if r in "abcd":
        return registers[r]
    return int(r)


while ip < len(IN):
    op = IN[ip]
    if op[0] == "cpy":
        registers[op[2]] = read(op[1])
    elif op[0] == "inc":
        registers[op[1]] += 1
    elif op[0] == "dec":
        registers[op[1]] -= 1
    elif op[0] == "jnz":
        if read(op[1]) != 0:
            ip += int(op[2])
            continue

    ip += 1

print(registers)
