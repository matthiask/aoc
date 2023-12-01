IN = [line.strip().split() for line in open("24.txt")]


def is_valid(model_number):
    variables = {v: 0 for v in "wxyz"}
    IP = 0
    input = iter(model_number)

    def value(v):
        return variables[v] if v in variables else int(v)

    while len(IN) > IP:
        op = IN[IP]
        if op[0] == "inp":
            variables[op[1]] = int(next(input))
        elif op[0] == "add":
            variables[op[1]] += value(op[2])
        elif op[0] == "mul":
            variables[op[1]] *= value(op[2])
        elif op[0] == "div":
            variables[op[1]] //= value(op[2])
        elif op[0] == "mod":
            variables[op[1]] %= value(op[2])
        elif op[0] == "eql":
            variables[op[1]] = 1 if value(op[1]) == value(op[2]) else 0
        IP += 1

    # print(variables)
    return value("z") == 0


for idx, num in enumerate(range(int("9" * 14), int("1" * 14) - 1, -1)):
    n = str(num)
    if "0" in n:
        continue

    if idx % 10000 == 0:
        print("progress", n)

    if is_valid(n):
        print(n)
        break

# print("13579246899999", is_valid("13579246899999"))
