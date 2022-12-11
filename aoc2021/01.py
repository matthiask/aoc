with open("01.txt") as f:
    nums = [int(line.strip()) for line in f]

prev = 1e100
larger = 0
for num in nums:
    if num > prev:
        larger += 1
    prev = num

print("part1:", larger)

print(
    "part2:",
    sum(
        1
        for idx in range(len(nums))
        if sum(nums[idx + 1 : idx + 4]) > sum(nums[idx + 0 : idx + 3])
    ),
)
