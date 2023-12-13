#!/usr/bin/python3

# There's probably a fancy way to do this, but this works
def rotate(item):
    lines = item.split("\n")
    out = []
    for i in range(len(lines[0])):
        tmp = []
        for line in lines:
            tmp.append(line[i])
        out.append(''.join(tmp))
    return '\n'.join(out)

# now returns the number of differences
# for part 1, zero differences
# for part 2, exactly 1 differenc3
def test_split(item, spl):
    lines = item.split("\n")
    top = spl - 1
    bot = spl
    diff = 0
    while top >= 0 and bot < len(lines):
        zipped = zip(list(lines[top]), list(lines[bot]))
        for z in zipped:
            if z[0] != z[1]:
                diff += 1
        top -= 1
        bot += 1
    return diff

# iterates through possible splits
# score doesn't need to be adjusted for the zero offset because it's looking
# at the first reflected line rather than the last not-reflected line
def find_split(item, diff):
    lines = item.split("\n")
    for i in range(1,len(lines)):
        if(test_split(item, i) == diff):
            return 100 * i 
    rotated = rotate(item)
    lines = rotated.split("\n")
    for i in range(1,len(lines)):
        if(test_split(rotated, i) == diff):
            return i
    return 0

with open("inputs/13") as f:
    items = f.read().rstrip("\n").split("\n\n")

sum = 0
for item in items:
    sum += find_split(item, 0)
print(f"Part 1: {sum}")
sum = 0
for item in items:
    sum += find_split(item, 1)
print(f"Part 2: {sum}")
