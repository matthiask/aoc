from functools import cache


IN = [*open("07.txt")]
wires = {}


@cache
def value(v):
    if v in wires:
        return wires[v]()
    return int(v)


# Part 2
IN.append("16076 -> b")


for line in IN:
    op, tg = line.strip().split(" -> ")

    match op.split():
        case (w1, "AND", w2):
            wires[tg] = lambda w1=w1, w2=w2: value(w1) & value(w2)
        case (w1, "OR", w2):
            wires[tg] = lambda w1=w1, w2=w2: value(w1) | value(w2)
        case (w1, "LSHIFT", w2):
            wires[tg] = lambda w1=w1, w2=w2: value(w1) << value(w2)
        case (w1, "RSHIFT", w2):
            wires[tg] = lambda w1=w1, w2=w2: value(w1) >> value(w2)
        case ("NOT", w1):
            wires[tg] = lambda w1=w1: ~value(w1)
        case (w1,):
            wires[tg] = lambda w1=w1: value(w1)


print(wires["a"]())
