error_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

autocomplete_scores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

left = set(pairs.keys())
right = set(pairs.values())


with open("10.txt") as f:
    lines = [line.strip() for line in f]


def error_score():
    error_score = 0
    ac_scores = []
    for line in lines:
        nesting = []
        for index, char in enumerate(line):
            if char in left:
                nesting.insert(0, char)
            elif char in right and char == pairs[nesting[0]]:
                nesting.pop(0)
            elif char in right:
                # print(f"Expected {nesting[0]}, found {char} at position {index} instead.")
                # print(nesting)
                error_score += error_scores[char]
                break
            else:
                raise Exception(f"Unknown character {char} at position {index}.")
        # print(nesting)
        ac_score = 0
        for char in nesting:
            ac_score = ac_score * 5 + autocomplete_scores[pairs[char]]
        ac_scores.append(ac_score)

    print("Error score:", error_score)
    ac_scores = sorted(ac_scores)
    print("Autocomplete score:", ac_scores[len(ac_scores) // 2])


error_score()
