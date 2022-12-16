import heapq
import re
from collections import defaultdict, namedtuple
from itertools import product


Valve = namedtuple("Valve", "name flow_rate tunnels_to")


def read(filename):
    with open(filename) as f:
        groups = (
            re.search(
                r"^Valve ([A-Z]{2}) .*? rate=(\d+); .*? valves? ((?:\w+)(?:, \w+)*)",
                line,
            ).groups()
            for line in f
        )
        return {
            name: Valve(name, int(flow_rate), tunnels_to.split(", "))
            for name, flow_rate, tunnels_to in groups
        }


def shortest_path_length(valves, start, end):
    seen = {start}
    heap = [(0, start)]
    while heap:
        cost, name = heapq.heappop(heap)
        if name == end:
            return cost
        for to in valves[name].tunnels_to:
            if to in seen:
                continue
            seen.add(to)
            heapq.heappush(heap, (cost + 1, to))


def determine_tunnel_costs(valves):
    paths = defaultdict(list)
    for start, end in product(valves.values(), valves.values()):
        if start == end or not end.flow_rate:
            continue
        paths[start.name].append(
            (end.name, shortest_path_length(valves, start.name, end.name))
        )
    return paths


def _valve(valves, tunnel_costs, name, open_valves, release, minutes):
    # print(name, open_valves, release, minutes)
    # Any action will take a minute; if we have only one minute left we can stop.
    if minutes <= 1:
        return

    next_open_valves = open_valves + (name,)
    next_release = release + minutes * valves[name].flow_rate
    # print(next_release, sorted(next_open_valves))
    yield next_release, set(next_open_valves)

    for to, costs in tunnel_costs[name]:
        if to not in open_valves:
            yield from _valve(
                valves,
                tunnel_costs,
                to,
                next_open_valves,
                next_release,
                minutes - costs - 1,
            )


def part1(valves):
    tunnel_costs = determine_tunnel_costs(valves)
    max_release = {
        release
        for release, open_valves in _valve(valves, tunnel_costs, "AA", (), 0, 30)
    }

    # pprint(max_release)
    return max(max_release)


def part2(valves):
    # from pprint import pprint

    tunnel_costs = determine_tunnel_costs(valves)
    max_releases = [
        res for res in _valve(valves, tunnel_costs, "AA", (), 0, 26) if res[0]
    ]

    # pprint(max_releases)

    disjoint_releases = []
    for res1, res2 in product(max_releases, max_releases):
        if (res1[1] - {"AA"}).isdisjoint(res2[1]):
            disjoint_releases.append(res1[0] + res2[0])

    return max(disjoint_releases)


if __name__ == "__main__":
    # from pprint import pprint
    # valves = read("16-test.txt")
    # pprint(valves)
    # pprint(determine_tunnel_costs(valves))
    # print()

    # print("part1 test", part1(read("16-test.txt")))
    # print("part2 test", part2(read("16-test.txt")))

    print("part1", part1(read("16.txt")))
    print("part2", part2(read("16.txt")))
