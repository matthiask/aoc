g = [*open("24.txt")]
h, w = len(g) - 2, len(g[0].strip()) - 2

wrap = lambda p: complex(p.real % w, p.imag % h)

bliz = {
    c: {complex(x, y) for x in range(w) for y in range(h) if g[y + 1][x + 1] == c}
    for c in "<>^v"
}

home, goal = -1j, w - 1 + h * 1j
todo, time, trip = [home], 0, 0

while todo:
    bliz = {
        c: {wrap(p + d) for p in bliz[c]}
        for c, d in (("<", -1), (">", +1), ("^", -1j), ("v", +1j))
    }
    curr = {p + d for p in todo for d in (0, 1, -1, 1j, -1j)}
    todo, time = [], time + 1

    for p in curr:
        if (trip, p) in ((0, goal), (1, home), (2, goal)):
            if trip == 0:
                print(time)
            if trip == 2:
                print(time)
                exit()
            trip, todo = trip + 1, [p]
            break

        if not any([p in bliz[d] for d in bliz]) and p == wrap(p) or p in (home, goal):
            todo += [p]
