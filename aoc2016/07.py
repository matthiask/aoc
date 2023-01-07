import re
from dataclasses import dataclass


@dataclass
class Record:
    line: str
    supernet: list[str]
    hypernet: list[str]


def parse_line(line):
    parts = re.split(r"(\[\w+\])", line)
    supernet = [part for part in parts if part[0] != "["]
    hypernet = [part[1:-1] for part in parts if part[0] == "["]
    return Record(line, supernet, hypernet)


def supports_tls(record):
    return any(abba_re.search(p) for p in record.supernet) and all(
        not abba_re.search(p) for p in record.hypernet
    )


def supports_ssl(record):
    for p in record.supernet:
        for aba in aba_re.findall(p):
            # print(aba)
            bab = aba[1] + aba[0] + aba[1]
            if any(bab in p2 for p2 in record.hypernet):
                print(aba, bab, record.line)
                return True
    return False


IN = [parse_line(line.strip()) for line in open("07.txt")]
abba_re = re.compile(r"(\w)((?!\1)\w)\2\1")
aba_re = re.compile(r"(?=(\w)((?!\1)\w)\1)")


# print(IN)
print(sum(1 for record in IN if supports_tls(record)))
print(sum(1 for record in IN if supports_ssl(record)))
