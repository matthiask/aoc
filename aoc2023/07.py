from collections import Counter
from pprint import pp

from tools import open_input


strengths = {
    card: strength + 2 for strength, card in enumerate(reversed("AKQJT98765432"))
}


def analyze(hand):
    counts = Counter(hand).most_common()
    groups = [c[1] for c in counts]

    if groups == [5]:
        return 10, "five", counts
    if groups == [4, 1]:
        return 8, "four", counts
    if groups == [3, 2]:
        return 6, "full house", counts
    if groups[0] == 3:
        return 5, "three of a kind", counts
    if groups == [2, 2, 1]:
        return 4, "two pair", counts
    if groups[0] == 2:
        return 3, "one pair", counts
    if groups == [1, 1, 1, 1, 1]:
        return 2, "high card", counts

    raise Exception()


def hand_to_strengths(hand):
    return tuple(strengths[h] for h in hand)


def one_beats_two(hand1, hand2):
    h1 = analyze(hand1)
    h2 = analyze(hand2)

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
        pp((hand, analyze(hand)))


def solve1():
    hands_and_bids = {}
    for line in open_input("07"):
        parts = line.strip().split()
        hand = parts[0]
        bid = int(parts[1])
        if hand in hands_and_bids:
            raise Exception()
        hands_and_bids[hand] = bid
    pp(hands_and_bids)

    hands = sorted(
        hands_and_bids.keys(),
        key=lambda hand: (analyze(hand)[0], hand_to_strengths(hand)),
    )
    pp(hands)

    pp({hand: (analyze(hand)[0], hand_to_strengths(hand)) for hand in hands})

    pp(
        (
            "part1",
            sum(hands_and_bids[hand] * (idx + 1) for idx, hand in enumerate(hands)),
        )
    )


solve1()
