#!/usr/bin/python3

from dataclasses import dataclass

def hash(str):
    hv = 0
    for x in str:
        hv += ord(x)
        hv *= 17
        hv %= 256
    return hv

with open("inputs/15") as f:
    items = f.read().rstrip("\n").split(",")

part1 = 0
for item in items:
    part1 += hash(item)
print(f"Part 1: {part1}")

boxes = [list() for i in range(256)]

@dataclass
class Lens:
    label: str
    power: int

for item in items:
    if '=' in item:
        label, val = item.split('=')
        box = hash(label)
        found = False
        for n in range(len(boxes[box])):
            if boxes[box][n].label == label:
                boxes[box][n].power = int(val)
                found = True
                break
        if not found:
            boxes[box].append(Lens(label, int(val)))
    else:
        item = item.replace('-','')
        box = hash(item)
        for n in range(len(boxes[box])):
            if boxes[box][n].label == item:
                del boxes[box][n]
                break
part2 = 0
for b, box in enumerate(boxes):
    for l, lens in enumerate(box):
        part2 += (b+1) * (l+1) * lens.power

print(f"Part 2: {part2}")
