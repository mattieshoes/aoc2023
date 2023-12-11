#!/usr/bin/python3

with open("inputs/11") as f:
    lines = f.read().rstrip("\n").split("\n")

# find blank rows and columns
expanded_rows = []
for i in range(len(lines)):
    if len(set(list(lines[i]))) == 1 and lines[i][0] == '.':
        expanded_rows.append(i)
expanded_cols = []
for i in range(len(lines[0])):
    found = False
    for j in range(len(lines)):
        if lines[j][i] == '#':
            found = True
            break
    if(not found):
        expanded_cols.append(i)

# build coordinate list for galaxies accounting for expansion
gal = []
def expanded_coordinates(x, y, factor):
    factor -= 1
    xoff = 0
    yoff = 0
    for col in expanded_cols:
        if x > col:
            xoff += 1
    for row in expanded_rows:
        if y > row:
            yoff += 1
    return( (x+xoff*factor, y+yoff*factor))

for y in range(len(lines)):
    for x in range(len(lines[0])):
        if lines[y][x] == '#':
            gal.append(expanded_coordinates(x, y, 2))

# part 1, sum list of distances
sum = 0
for i in range(len(gal)):
    for j in range(i+1, len(gal), 1):
        sum += abs(gal[i][0] - gal[j][0]) + abs(gal[i][1] - gal[j][1])
print(f"Part 1: {sum}")

# part 2, same except expansion factor is 1000000 instead of 2
gal = []
for y in range(len(lines)):
    for x in range(len(lines[0])):
        if lines[y][x] == '#':
            gal.append(expanded_coordinates(x, y, 1000000))
sum = 0
for i in range(len(gal)):
    for j in range(i+1, len(gal), 1):
        sum += abs(gal[i][0] - gal[j][0]) + abs(gal[i][1] - gal[j][1])
print(f"Part 2: {sum}")
