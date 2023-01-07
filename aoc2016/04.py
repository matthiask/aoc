import re
from collections import Counter


def parse_line(line):
    (*parts, sector_id, checksum) = re.split(r"[\[-]", line.rstrip("]"))
    return (parts, int(sector_id), checksum)


def is_real_room(room):
    c = Counter("".join(room[0]))
    calculated_checksum = "".join(
        pair[0]
        for pair in sorted(c.most_common(), key=lambda pair: (-pair[1], pair[0]))[:5]
    )
    return calculated_checksum == room[2]


def _rotate(part, places):
    base = ord("a")
    return "".join(chr(base + (ord(c) + places - base) % 26) for c in part)


def decrypt(room):
    """
    >>> decrypt(parse_line("qzmt-zixmtkozy-ivhz-343[blub]"))
    'very encrypted name'
    """
    return " ".join(_rotate(p, room[1]) for p in room[0])


def is_real_room_test(line):
    """
    >>> is_real_room_test("aaaaa-bbb-z-y-x-123[abxyz]")
    True
    >>> is_real_room_test("a-b-c-d-e-f-g-h-987[abcde]")
    True
    >>> is_real_room_test("not-a-real-room-404[oarel]")
    True
    >>> is_real_room_test("totally-real-room-200[decoy]")
    False
    """

    return is_real_room(parse_line(line))


rooms = [parse_line(line.strip()) for line in open("04.txt")]
real_rooms = [room for room in rooms if is_real_room(room)]
print(sum(room[1] for room in real_rooms))
print({decrypt(room): room[1] for room in real_rooms})
