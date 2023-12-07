from collections import Counter
from pprint import pp

from tools import open_input


part2 = True

if part2:  # noqa: SIM108
    # Part2
    cards = "AKQT98765432J"
else:
    # Part1
    cards = "AKQJT98765432"

strengths = {card: strength + 2 for strength, card in enumerate(reversed(cards))}


def type_with_jokers(counts, groups):
    # pp(counts)
    if "J" not in counts:
        return None

    jokers = counts.pop("J")
    groups = [c[1] for c in counts.most_common()]

    if not groups:
        return 10, "five"
    if groups[0] == 5 - jokers:
        return 10, "five"
    if groups[0] == 4 - jokers:
        return 8, "four"
    if set(groups) == {3 - jokers, 2}:
        return 6, "full house"
    if groups[0] == 3 - jokers:
        return 5, "three of a kind"
    if set(groups[:2]) == {2, 2 - jokers}:
        return 4, "two pair"
    return 3, "one pair"
    print(jokers, counts)


def type(hand):
    counts = Counter(hand)
    groups = [c[1] for c in counts.most_common()]

    if part2 and (with_jokers := type_with_jokers(counts, groups)):
        return with_jokers

    if groups == [5]:
        return 10, "five"
    if groups == [4, 1]:
        return 8, "four"
    if groups == [3, 2]:
        return 6, "full house"
    if groups[0] == 3:
        return 5, "three of a kind"
    if groups == [2, 2, 1]:
        return 4, "two pair"
    if groups[0] == 2:
        return 3, "one pair"
    if groups == [1, 1, 1, 1, 1]:
        return 2, "high card"

    raise Exception()


def hand_to_strengths(hand):
    return tuple(strengths[h] for h in hand)


def one_beats_two(hand1, hand2):
    h1 = type(hand1)
    h2 = type(hand2)

    # Different type
    if h1[0] != h2[0]:
        return h1[0] > h2[0]

    # Consider card by card in order
    for i in range(5):
        s1 = strengths[hand1[i]]
        s2 = strengths[hand2[i]]
        if s1 != s2:
            return s1 > s2

    raise Exception()


def test():
    pp(strengths)
    for hand in ("AAAAA", "AA8AA", "23332", "TTT98", "23432", "A23A4", "23456"):
        pp((hand, type(hand)))


def parse_hands_and_pids():
    hands_and_bids = {}
    for line in open_input("07"):
        parts = line.strip().split()
        hand = parts[0]
        bid = int(parts[1])
        if hand in hands_and_bids:
            raise Exception()
        hands_and_bids[hand] = bid
    return hands_and_bids


def solve1():
    hands_and_bids = parse_hands_and_pids()
    pp(hands_and_bids)

    hands = sorted(
        hands_and_bids.keys(),
        key=lambda hand: (type(hand)[0], hand_to_strengths(hand)),
    )
    pp(hands)

    pp({hand: (type(hand)[0], hand_to_strengths(hand)) for hand in hands})

    pp(
        (
            "part1",
            sum(hands_and_bids[hand] * (idx + 1) for idx, hand in enumerate(hands)),
        )
    )


def solve2():
    hands_and_bids = parse_hands_and_pids()
    # pp(hands_and_bids)
    pp({hand: type(hand) for hand in hands_and_bids})
    hands = sorted(
        hands_and_bids.keys(),
        key=lambda hand: (type(hand)[0], hand_to_strengths(hand)),
    )
    pp(
        (
            "part2",
            sum(hands_and_bids[hand] * (idx + 1) for idx, hand in enumerate(hands)),
        )
    )


if part2:
    solve2()
else:
    solve1()
