from dataclasses import dataclass
from pprint import pprint
from typing import Any


def read():
    with open("16.txt") as f:
        return "".join(hex_digit_to_4_binary_bits(c) for c in f.read().strip())


def hex_digit_to_4_binary_bits(hex):
    """
    >>> hex_digit_to_4_binary_bits("a")
    '1010'
    >>> hex_digit_to_4_binary_bits("f")
    '1111'
    >>> hex_digit_to_4_binary_bits("3")
    '0011'
    >>> hex_digit_to_4_binary_bits("0")
    '0000'
    """
    return "{:>04b}".format(int(hex, 16))


class EOF(Exception):
    pass


def create_reader(data):
    """
    >>> reader("abcdef")(3)
    'abc'
    >>> r = reader("abcdef"); _ignore = r(3); r(2)
    'de'
    """
    pos = 0

    def _read(bits):
        nonlocal pos
        ret = data[pos : pos + bits]
        pos += bits
        if bits and ret == "":
            raise EOF()
        return ret

    return _read


def read_int(reader, bits):
    """
    >>> read_int(reader("0101"), 4)
    5
    """
    return int(reader(bits), 2)


LITERAL = 4


@dataclass
class Literal:
    version: int
    type_id: int
    number: int


@dataclass
class Operator:
    version: int
    type_id: int
    subpackets: tuple = ()


def read_packet(reader):
    version = read_int(reader, 3)
    type_id = read_int(reader, 3)

    if type_id == 4:
        # Literal
        data = ""
        while True:
            more = read_int(reader, 1)
            data += reader(4)
            if not more:
                return Literal(version, type_id, int(data, 2))

    # Operator packet
    length_type_id = read_int(reader, 1)
    if length_type_id == 0:
        subreader = create_reader(reader(read_int(reader, 15)))
        return Operator(version, type_id, subpackets=parse(subreader))
    else:
        return Operator(
            version,
            type_id,
            subpackets=[read_packet(reader) for _i in range(read_int(reader, 11))],
        )


def parse(reader):
    packets = []
    while True:
        try:
            packets.append(read_packet(reader))
        except EOF:
            break
    return packets


def sum_up_versions(packets):
    version_sum = 0
    for packet in packets:
        match packet:
            case Literal():
                version_sum += packet.version
            case Operator():
                version_sum += packet.version + sum_up_versions(packet.subpackets)
    return version_sum


if __name__ == "__main__":
    data = read()
    reader = create_reader(data)
    # print(read_packet(
    # print(read())

    packets = read_packet(reader)
    pprint(packets)
    pprint(sum_up_versions([packets]))
