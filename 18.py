#!/usr/bin/python3

from collections import namedtuple

Rule = namedtuple('Rule', ['p1dir', 'p1len', 'p2dir', 'p2len'])

with open("inputs/18") as f:
    lines = f.read().rstrip("\n").split("\n")

#convert input to rules
p2conv = [(1,0),(0,1),(-1,0),(0,-1)]
p1conv = {'R': (1,0), 'L': (-1,0), 'U': (0,-1), 'D': (0,1)}
rules = []
for line in lines:
    fields = line.split(" ")
    p2d = p2conv[int(fields[2][-2:-1])]
    p2l = int(fields[2][2:-2], 16)
    rules.append(Rule(p1conv[fields[0]], int(fields[1]), 
        p2conv[int(fields[2][-2:-1])], int(fields[2][2:-2], 16)))

perimeter = 0
new_loc = (0,0)
area = 0
for rule in rules:
    loc = new_loc
    perimeter += rule.p1len
    offset = (rule.p1dir[0]*rule.p1len, rule.p1dir[1]*rule.p1len)
    new_loc = (loc[0] + offset[0], loc[1] + offset[1])
    area += (loc[0] * new_loc[1] - loc[1] * new_loc[0]) / 2
area = int(area + perimeter / 2 + 1)
print(f"Part 1: {area}")

perimeter = 0
new_loc = (0,0)
area = 0
for rule in rules:
    loc = new_loc
    perimeter += rule.p2len
    offset = (rule.p2dir[0]*rule.p2len, rule.p2dir[1]*rule.p2len)
    new_loc = (loc[0] + offset[0], loc[1] + offset[1])
    area += (loc[0] * new_loc[1] - loc[1] * new_loc[0]) / 2
area = int(area + perimeter / 2 + 1)
print(f"Part 2: {area}")
