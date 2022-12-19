import re
from collections import deque
from itertools import zip_longest
from pprint import pprint


with open("19.txt") as f:
    real_input = f.read()
test_input = """\
Blueprint 1:\
 Each ore robot costs 4 ore.\
 Each clay robot costs 2 ore.\
 Each obsidian robot costs 3 ore and 14 clay.\
 Each geode robot costs 2 ore and 7 obsidian.\

Blueprint 2:\
 Each ore robot costs 2 ore.\
 Each clay robot costs 3 ore.\
 Each obsidian robot costs 3 ore and 8 clay.\
 Each geode robot costs 3 ore and 12 obsidian.\
"""


ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3


def parse_blueprints(input):
    blueprints = {}
    for line in filter(None, input.splitlines()):
        groups = [
            int(group)
            for group in re.match(
                r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
                line,
            ).groups()
        ]
        blueprints[groups[0]] = [
            # ORE
            (
                groups[1],  # Ore
                0,
                0,
            ),
            # CLAY
            (
                groups[2],  # Ore
                0,
                0,
            ),
            # OBSIDIAN:
            (
                groups[3],  # Ore
                groups[4],  # Clay
                0,
            ),
            # GEODE
            (
                groups[5],  # Ore
                0,
                groups[6],  # Obsidian
            ),
        ]
    return blueprints


INITIAL_ROBOTS = [1, 0, 0, 0]  # One Ore robot
INITIAL_RESOURCES = [0, 0, 0, 0]  # No resources


def collect(robots, resources):
    # print(robots, resources)
    return [a + b for a, b in zip(resources, robots)]


def maybe_build_robot(blueprint, robots, resources, type):
    new_resources = [
        resource - requirement
        for resource, requirement in zip_longest(
            resources, blueprint[type], fillvalue=0
        )
    ]
    if any(nr < 0 for nr in new_resources):
        return None
    new_robots = robots[:]
    new_robots[type] += 1
    return new_robots, collect(robots, new_resources)


def next_actions(blueprint, robots, resources):
    return [
        action
        for action in [
            # Just waiting is an option
            [robots, collect(robots, resources)],
            # Maybe build robots
            maybe_build_robot(blueprint, robots, resources, ORE),
            maybe_build_robot(blueprint, robots, resources, CLAY),
            maybe_build_robot(blueprint, robots, resources, OBSIDIAN),
            maybe_build_robot(blueprint, robots, resources, GEODE),
        ]
        if action
    ]


def run(blueprint):
    # print("blueprint", blueprint)
    robots = INITIAL_ROBOTS[:]
    resources = INITIAL_RESOURCES[:]

    geodes = set()
    options = deque()
    options.append([24, INITIAL_ROBOTS[:], INITIAL_RESOURCES[:]])

    while options:
        minutes, robots, resources = options.popleft()
        if minutes == 0:
            geodes.add(resources[GEODE])
            print(
                "found geode result",
                resources[GEODE],
                "current max",
                max(geodes),
                robots,
                resources,
            )
            continue

        na = next_actions(blueprint, robots, resources)
        # pprint(("next_actions", na))
        options.extendleft([minutes - 1, robots, resources] for robots, resources in na)

    print(geodes)
    return max(geodes)


# print(test_input)
pprint(parse_blueprints(test_input))
# pprint(parse_blueprints(real_input))

blueprints = parse_blueprints(test_input)
run(blueprints[1])
