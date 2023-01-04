from collections import defaultdict


IN = [*open("09.txt")]

edges = defaultdict(dict)
nodes = set()

for line in IN:
    start, _, end, _, distance = line.strip().split()
    nodes.add(start)
    nodes.add(end)

    edges[start][end] = edges[end][start] = int(distance)

print(len(nodes), nodes)
print(len(edges), edges)


def select_distance(start, selector):
    todo = [
        [[start], 0],
    ]

    while True:
        next_todo = []
        for visited, distance in todo:
            # Since all nodes are connected to all other nodes that works fine.
            unvisited = nodes - set(visited)
            if not unvisited:
                # from pprint import pprint; pprint(todo)
                distances = [distance for visited, distance in todo]
                return selector(distances)
            next_todo.extend(
                [visited + [next], distance + edges[visited[-1]][next]]
                for next in unvisited
            )
        todo = next_todo


print(min(select_distance(start, min) for start in nodes))
print(max(select_distance(start, max) for start in nodes))
