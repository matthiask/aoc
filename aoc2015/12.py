import json


IN = json.load(open("12.txt"))
print(IN)


def recursive_sum(obj):
    if isinstance(obj, dict):
        # Part 2
        if "red" in obj.values():
            return 0
        return sum(map(recursive_sum, obj.values()))
    elif isinstance(obj, list):
        return sum(map(recursive_sum, obj))
    elif isinstance(obj, int):
        return obj
    return 0


print(recursive_sum(IN))
