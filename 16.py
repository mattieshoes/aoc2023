#!/usr/bin/python3

# finds the next tile(s) the beam will travel to
def do_tile(r, c, d, e):
    if r>=height or c>=width or r<0 or c<0 or (r,c) in e[d]:
        return []
    e[d].add((r,c))
    tile = lines[r][c]
    if tile == '.':
        return([[r+d[0], c+d[1], d]])
    elif tile == '\\':
        return([[r+d[1], c+d[0], (d[1], d[0])]])
    elif tile == '/':
        return([[r-d[1], c-d[0], (-d[1], -d[0])]])
    elif tile == '-':
        if d[1] != 0:
            return([[r+d[0], c+d[1], d]])
        else:
            return([[r, c-1, (0, -1)],[r, c+1, (0, 1)]])
    elif tile == '|':
        if d[0] != 0:
            return([[r+d[0], c+d[1], d]])
        else:
            return([[r-1, c, (-1, 0)], [r+1, c, (1, 0)]])

# gets the number of energized tiles given a start point
def calculate(row, col, direction):
    e = {(0,1): set(), (1,0): set(), (-1,0): set(), (0,-1): set()}
    tbs = [[row, col, direction]]
    while len(tbs) > 0:
        tbs.extend(do_tile(tbs[0][0], tbs[0][1], tbs[0][2], e))
        del tbs[0]
    return len(e[(0,1)].union(e[(1,0)], e[(-1,0)], e[(0,-1)])) 

with open("inputs/16") as f:
    lines = f.read().rstrip("\n").split("\n")
height = len(lines)
width = len(lines[0])

part1 = calculate(0,0,(0,1))
print(f"Part 1: {part1}")

part2 = 0
for r in range(height):
    for c in range(width):
        if r == 0:
            part2 = max(part2, calculate(r, c, (1,0)))
        elif r == height-1:
            part2 = max(part2, calculate(r, c, (-1,0)))
        if c == 0:
            part2 = max(part2, calculate(r, c, (0,1)))
        elif c == width-1:
            part2 = max(part2, calculate(r, c, (0,-1)))
print(f"Part 2: {part2}")
