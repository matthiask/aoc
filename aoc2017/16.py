from tools import open_input


IN = open_input("16").read().strip().split(",")
programs = {v: k for k, v in enumerate("abcdefghijklmnop")}
count = len(programs)
# print(programs)

for move in IN:
    instr, arg = move[0], move[1:]
    if instr == "s":
        arg = int(arg)
        programs = {k: (v + arg) % count for k, v in programs.items()}
    elif instr == "x":
        one, two = map(int, arg.split("/"))
        programs = {
            k: one if v == two else two if v == one else v for k, v in programs.items()
        }
    elif instr == "p":
        one, two = arg.split("/")
        programs[one], programs[two] = programs[two], programs[one]
    else:
        raise Exception

print(programs)
print("".join(k for k, v in sorted(programs.items(), key=lambda row: row[1])))
