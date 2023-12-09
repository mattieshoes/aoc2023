#!/usr/bin/python3

import re

def recurse(sequence):
    if set(sequence) == set([0]):
        return [0, 0]
    new_sequence = [x - y for x, y in zip(sequence[1:], sequence[:-1])]
    val = recurse(new_sequence)
    return [sequence[0] - val[0], sequence[-1] + val[1]]

with open('inputs/9') as f:
    data = f.read().rstrip('\n').split('\n')
sums = [0,0]
for line in data:
    n = list(map(int, re.findall(r'[0-9\-]+', line)))
    sums = [x + y for x, y in zip(sums, recurse(n))]
print(f"Part 1: {sums[1]}\nPart 2: {sums[0]}")
