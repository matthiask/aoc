import re
from dataclasses import dataclass, field
from pprint import pprint


bot_re = re.compile(r"bot (\d+) .+? (bot|output) (\d+) .+? (bot|output) (\d+)")
value_re = re.compile(r"value (\d+) .+? bot (\d+)")
IN = [*open("10.txt")]
bots = {}
outputs = {}


@dataclass
class Bot:
    id: int
    low: tuple[str, int]
    high: tuple[str, int]
    chips: list[int] = field(default_factory=list)

    def accept(self, value: int):
        self.chips.append(value)

        if len(self.chips) == 2:
            low, high = sorted(self.chips)

            # part 1
            if low == 17 and high == 61:
                pprint(self.id)

            if self.low[0] == "bot":
                bots[self.low[1]].accept(low)
            elif self.low[0] == "output":
                outputs[self.low[1]] = low

            if self.high[0] == "bot":
                bots[self.high[1]].accept(high)
            elif self.high[0] == "output":
                outputs[self.high[1]] = high

            self.chips = []


for line in sorted(IN):
    if m := bot_re.match(line):
        bots[m[1]] = Bot(int(m[1]), (m[2], m[3]), (m[4], m[5]))
    elif m := value_re.match(line):
        bots[m[2]].accept(int(m[1]))
    else:
        1 / 0


# pprint(bots)
# pprint(outputs)

# part 2
pprint(outputs["0"] * outputs["1"] * outputs["2"])
