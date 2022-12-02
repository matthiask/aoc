# Rock A X
# Paper B Y
# Scissors C Z

from pprint import pprint

choice_scores = {
    "A": 1,
    "B": 2,
    "C": 3,
    "X": 1, 
    "Y": 2, 
    "Z": 3,
}
round_scores = {
    # Draws
    ("A", "X"): 3,
    ("B", "Y"): 3,
    ("C", "Z"): 3,
    # Second player loses
    ("A", "Z"): 0,
    ("B", "X"): 0,
    ("C", "Y"): 0,
    # Second player wins
    ("A", "Y"): 6,
    ("B", "Z"): 6,
    ("C", "X"): 6,
}


def read():
    with open("input.txt") as f:
        lines = f.readlines()
    return [tuple(line.strip().split(" ")) for line in lines]


def score_round_for_player_2(round):
    return choice_scores[round[1]] + round_scores[round]


def score_round_for_player_2_round_2(round):
    if round[1] == "X":  # lose
        piece = next((pair[1] for pair, score in round_scores.items() if score == 0 and pair[0] == round[0]))
    elif round[1] == "Y":  # draw
        piece = next((pair[1] for pair, score in round_scores.items() if score == 3 and pair[0] == round[0]))
    elif round[1] == "Z":  # win
        piece = next((pair[1] for pair, score in round_scores.items() if score == 6 and pair[0] == round[0]))

    return choice_scores[piece] + round_scores[(round[0], piece)]


if __name__ == "__main__":
    rounds = read()
    print(sum(score_round_for_player_2(round) for round in rounds))

    print(sum(score_round_for_player_2_round_2(round) for round in rounds))
