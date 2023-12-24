# https://github.com/AxlLind/AdventOfCode2023/blob/656dc57d614bc5f83bdd876cb9c943a082e1edd8/src/bin/24.py

from z3 import Real, Solver


# TODO: Port this to Rust somehow??

inp = open("24.txt").read().strip()
lines = []
for l in inp.splitlines():
    a, b = l.split(" @ ")
    pos = [int(w) for w in a.split(", ")]
    vel = [int(w) for w in b.split(", ")]
    lines.append((pos, vel))

fx, fy, fz = Real("fx"), Real("fy"), Real("fz")
fdx, fdy, fdz = Real("fdx"), Real("fdy"), Real("fdz")
s = Solver()
for i, ((x, y, z), (dx, dy, dz)) in enumerate(lines):
    t = Real(f"t{i}")
    s.add(t >= 0)
    s.add(x + dx * t == fx + fdx * t)
    s.add(y + dy * t == fy + fdy * t)
    s.add(z + dz * t == fz + fdz * t)
assert str(s.check()) == "sat"

print(s.model().eval(fx + fy + fz))
