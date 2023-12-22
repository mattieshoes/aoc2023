#!/usr/bin/python3

with open("inputs/21") as f:
    lines = f.read().rstrip("\n").split("\n")
height = len(lines)
width = len(lines[0])

# parse input
start = (0, 0)
for i in range(len(lines)):
    if "S" in lines[i]:
        start = (lines[i].index('S'), i)


visited = set()
visited.add(start)
for step in range(64):
    nv = set()
    for v in visited:
        l = [(v[0] + 1, v[1]), (v[0] - 1, v[1]), (v[0], v[1] + 1), (v[0], v[1] - 1)]
        for n in l:
            if n[0] < 0 or n[1] < 0 or n[0] >= width or n[1] >= height:
                continue
            if lines[n[1]][n[0]] == '#':
                continue
            nv.add(n)
    visited = nv


part1 = len(visited)
print(f"Part 1: {part1}")
