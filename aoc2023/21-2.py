G = {
    i + j * 1j: c
    for i, r in enumerate(open("21.txt"))
    for j, c in enumerate(r)
    if c in ".S"
}

done = []
todo = {x for x in G if G[x] == "S"}
cmod = lambda x: complex(x.real % 131, x.imag % 131)

for s in range(3 * 131):
    if s == 64:
        print(len(todo))
    if s % 131 == 65:
        done.append(len(todo))

    todo = {p + d for d in {1, -1, 1j, -1j} for p in todo if cmod(p + d) in G}

# Polynomial fitting
f = lambda n, a, b, c: a + n * (b - a + (n - 1) * (c - b - b + a) // 2)
print(f(26501365 // 131, *done))
