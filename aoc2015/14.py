IN = [*open("14.txt")]
reindeer = []


def reindeer_distance(speed, flight, rest):
    def distance(seconds):
        cycles, partial_cycle = divmod(seconds, flight + rest)
        return speed * flight * (cycles + min(1.0, partial_cycle / flight))

    return distance


for line in IN:
    parts = line.split()
    params = (int(parts[3]), int(parts[6]), int(parts[13]))
    # print(params)
    reindeer.append(reindeer_distance(*params))

print(max(r(2503) for r in reindeer))


points = [0 for _ in reindeer]
for elapsed in range(1, 2503 + 1):
    now = [r(elapsed) for r in reindeer]
    lead = max(now)
    for idx, d in enumerate(now):
        if lead == d:
            points[idx] += 1
print(max(points))
