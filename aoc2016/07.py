import re
from dataclasses import dataclass


@dataclass
class Record:
    line: str
    outside: list[str]
    inside: list[str]


def parse_line(line):
    parts = re.split(r"(\[\w+\])", line)
    outside = [part for part in parts if part[0] != "["]
    inside = [part[1:-1] for part in parts if part[0] == "["]
    return Record(line, outside, inside)


def supports_tls(record):
    return any(abba_re.search(p) for p in record.outside) and all(
        not abba_re.search(p) for p in record.inside
    )


IN = [parse_line(line.strip()) for line in open("07.txt")]
abba_re = re.compile(r"(\w)((?!\1)\w)\2\1")


# print(IN)
print(sum(1 for record in IN if supports_tls(record)))
