from itertools import combinations


IN = [*open("17.txt")]
containers = [int(n) for n in IN]


options = []
for r in range(len(containers)):
    options.extend(c for c in combinations(containers, r + 1) if sum(c) == 150)
print(len(options))

counts = [len(c) for c in options]
print(counts.count(min(counts)))
