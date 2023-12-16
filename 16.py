#!/usr/bin/python3

import sys

# moves beam of light recursively
def recurse(r, c, d, e):
    if r>=height or c>=width or r<0 or c<0 or (r,c) in e[d]:
        return
    e[d].add((r,c))
    tile = lines[r][c]
    if tile == '.':
        recurse(r+d[0], c+d[1], d, e)
    elif tile == '\\':
        recurse(r+d[1], c+d[0], (d[1], d[0]), e)
    elif tile == '/':
        recurse(r-d[1], c-d[0], (-d[1], -d[0]), e)
    elif tile == '-':
        if d[1] != 0:
            recurse(r+d[0], c+d[1], d, e)
        else:
            recurse(r, c-1, (0, -1), e)
            recurse(r, c+1, (0, 1), e)
    elif tile == '|':
        if d[0] != 0:
            recurse(r+d[0], c+d[1], d, e)
        else:
            recurse(r-1, c, (-1, 0), e)
            recurse(r+1, c, (1, 0), e)

# gets the number of energized tiles
def calculate(row, col, direction):
    e = {(0,1): set(), (1,0): set(), (-1,0): set(), (0,-1): set()}
    recurse(row, col, direction, e)
    return len(e[(0,1)].union(e[(1,0)], e[(-1,0)], e[(0,-1)])) 

with open("inputs/16") as f:
    lines = f.read().rstrip("\n").split("\n")
height = len(lines)
width = len(lines[0])

sys.setrecursionlimit(10000)
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
