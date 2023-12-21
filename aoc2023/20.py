import sys
from dataclasses import dataclass, field
from pprint import pp

from tools import open_input


sys.setrecursionlimit(20000)


LOW = False
HIGH = True
counters = {LOW: 0, HIGH: 0}


@dataclass
class FlipFlop:
    name: str
    destinations: list[str]
    type: bool = LOW

    def receive(self, modules, module, pulse):
        self.type = not pulse

    def broadcast(self):
        if self.type is LOW:
            return
        for destination in self.destinations:
            counters[self.type] += 1
            modules[destination].receive(modules, self.name, self.type)
        for destination in self.destinations:
            modules[destination].broadcast()


@dataclass
class Conjunction:
    name: str
    destinations: list[str]
    received: dict[str, bool] = field(default_factory=dict)

    def receive(self, modules, module, pulse):
        self.received[module] = pulse

    def broadcast(self):
        type = LOW if all(self.received.values()) else HIGH
        for destination in self.destinations:
            counters[type] += 1
            modules[destination].receive(modules, self.name, type)
        for destination in self.destinations:
            modules[destination].broadcast()


@dataclass
class Broadcaster:
    name: str
    destinations: list[str]
    pulse: bool = False

    def receive(self, modules, module, pulse):
        self.pulse = pulse

    def broadcast(self):
        for destination in self.destinations:
            counters[self.pulse] += 1
            modules[destination].receive(modules, self.name, self.pulse)
        for destination in self.destinations:
            modules[destination].broadcast()


@dataclass
class Output:
    def receive(self, modules, module, pulse):
        pass

    def broadcast(self):
        pass


def parse_module(line):
    type_name, destinations = line.split(" -> ")
    if type_name[0] == "%":
        return type_name[1:], FlipFlop(type_name[1:], destinations.split(", "))
    if type_name[0] == "&":
        return type_name[1:], Conjunction(type_name[1:], destinations.split(", "))
    if type_name == "broadcaster":
        return type_name, Broadcaster(type_name, destinations.split(", "))
    raise Exception


modules = dict(
    parse_module(line) for line in open_input("20").read().strip().split("\n")
)
for module in modules.values():
    for destination in module.destinations:
        if (dest := modules.get(destination)) and isinstance(dest, Conjunction):
            dest.received[module.name] = LOW
modules["output"] = Output()
pp(modules)


for _ in range(1000):
    counters[LOW] += 1
    modules["broadcaster"].receive(modules, "broadcaster", LOW)
    modules["broadcaster"].broadcast()
print(counters)
