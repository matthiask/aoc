import sys


IN = [
    line.strip().split()
    for line in open("23.txt" if len(sys.argv) < 2 else sys.argv[1])
]
registers = {r: 0 for r in "abcd"}
ip = 0

# part 1
registers["a"] = 7

# part 2
registers["a"] = 12


def read(r):
    if r in "abcd":
        return registers[r]
    return int(r)


while ip < len(IN):
    op = IN[ip]
    if op[0] == "cpy" and op[2] in registers:
        registers[op[2]] = read(op[1])
    elif op[0] == "inc" and op[1] in registers:
        registers[op[1]] += 1
    elif op[0] == "dec" and op[1] in registers:
        registers[op[1]] -= 1
    elif op[0] == "jnz":
        if read(op[1]) != 0:
            ip += read(op[2])
            continue
    elif op[0] == "tgl":
        offset = read(op[1])
        # Only executed next time if offset == 0
        if 0 <= (tgl := ip + offset) < len(IN):
            instr = IN[tgl]
            if len(instr) == 2:
                if instr[0] == "inc":
                    IN[tgl][0] = "dec"
                else:
                    IN[tgl][0] = "inc"
            elif len(instr) == 3:
                if instr[0] == "jnz":
                    IN[tgl][0] = "cpy"
                else:
                    IN[tgl][0] = "jnz"

    # print(ip, registers, IN)
    ip += 1

print(registers)
