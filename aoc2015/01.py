IN = open("01.txt").read()

print(IN.count("(") - IN.count(")"))

floor = 0
for idx, c in enumerate(IN):
    floor += {"(": 1, ")": -1}[c]
    if floor < 0:
        print(idx + 1)
        break
