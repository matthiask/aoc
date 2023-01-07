IN = [*open("12.txt")]


registers = {r: 0 for r in "abcd"}
ip = 0


# part 2
registers["c"] = 1


def read(r):
    if r in "abcd":
        return registers[r]
    return int(r)


while ip < len(IN):
    match IN[ip].strip().split():
        case ("cpy", what, register):
            registers[register] = read(what)
        case ("inc", register):
            registers[register] += 1
        case ("dec", register):
            registers[register] -= 1  # XXX max(0, ...) ?
        case ("jnz", register, offset):
            if read(register) != 0:
                ip += int(offset)
                continue

    ip += 1

print(registers)
