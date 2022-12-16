import re
from collections import namedtuple
from pprint import pprint


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
        return [
            Valve(name, int(flow_rate), tunnels_to.split(", "))
            for name, flow_rate, tunnels_to in groups
        ]


if __name__ == "__main__":
    pprint(read("16-test.txt"))
