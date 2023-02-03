from collections import defaultdict

from utils import numbers, open_input


def parse():
    connections = defaultdict(set)
    for start, *ends in map(numbers, open_input("12")):
        for end in ends:
            connections[start].add(end)
            connections[end].add(start)
    return connections


def group(connections, start):
    todo = {start}
    while True:
        new_todo = set(todo)
        for node in todo:
            new_todo |= connections[node]
        if new_todo == todo:
            return todo
        todo = new_todo


def part1():
    return len(group(parse(), 0))


def part2():
    connections = parse()
    remaining = set(connections)
    groups = 0
    while remaining:
        # any random member, really.
        g = group(connections, min(remaining))
        remaining -= g
        groups += 1
    return groups


print(parse())
print("part1", part1())
print("part2", part2())
