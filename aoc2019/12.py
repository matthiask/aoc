import re
from dataclasses import dataclass


IN = [*open("12.txt")]


@dataclass
class Moon:
    position: list[int]
    velocity: list[int]

    def move(self):
        for i, v in enumerate(self.velocity):
            self.position[i] += v

    def potential_energy(self):
        return sum(map(abs, self.position))

    def kinetic_energy(self):
        return sum(map(abs, self.velocity))

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()


moons = [
    Moon(
        [int(n) for n in re.findall(r"[-\d]+", line)],
        [0, 0, 0],
    )
    for line in IN
]


def apply_gravity(moons):
    for i, m1 in enumerate(moons):
        for m2 in moons[i + 1 :]:
            # print(m1, m2)
            for i in range(3):
                c1 = m1.position[i]
                c2 = m2.position[i]
                if c1 == c2:
                    continue
                elif c1 < c2:
                    m1.velocity[i] += 1
                    m2.velocity[i] -= 1
                elif c1 > c2:
                    m1.velocity[i] -= 1
                    m2.velocity[i] += 1


def apply_velocity(moons):
    for moon in moons:
        moon.move()


def cycle(moons):
    apply_gravity(moons)
    apply_velocity(moons)


# print(moons)
# cycle(moons)
# print(moons)
# cycle(moons)
# print(moons)

for _ in range(1000):
    cycle(moons)
print(sum(moon.total_energy() for moon in moons))
