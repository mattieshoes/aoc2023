#!/usr/bin/python3

from functools import cache, reduce
from multiprocessing import Pool

def make_description(drawing):
    tmp = drawing.split(".")
    desc = []
    for i in tmp:
        if len(i) > 0:
            desc.append(str(len(i)))
    return(",".join(desc))

@cache
def recurse(drawing, description, springs_to_place):
    # bail if done
    question_count = drawing.count('?')
    if question_count ==  0:
        if make_description(drawing) == description:
            return 1
        return 0
    
    # if there are more springs to place than ? remaining, we've already failed
    if question_count < springs_to_place:
        return 0

    # if springs_to_place is 0, remaining ? must be . so we can skip ahead
    if springs_to_place == 0:
        if make_description(drawing.replace('?', '.')) == description:
            return 1
        return 0

    # if question_count is equal to springs to place, we must place all #
    if question_count == springs_to_place:
        if make_description(drawing.replace('?', '#')) == description:
            return 1
        return 0

    # validate the starting portion of our match
    partial = drawing[:drawing.find('?')]
    # go back to the last . so we don't wreck a sequence of # that may continue on
    while len(partial) > 0 and partial[-1] == '#':
        partial = partial[:-1]
    # generate a partial description for that amount
    partial_description = make_description(partial)
    # validate it against the existing description
    if len(partial_description) == 0 or description.startswith(partial_description):
        # hacky fix for 1,1 matching 1,10
        if (len(description) > len(partial_description) and description[len(partial_description)] == ',') or len(partial_description) == len(description):
            # remove the already validated part from both the drawing and description
            # for better cache hits
            drawing = drawing[len(partial):]
            description = description[len(partial_description):]
            if len(description) > 0 and description[0] == ',':
                description = description[1:]
    else:
        return 0

    # recurse, returning sum
    sum = 0
    sum += recurse(drawing.replace('?', '.', 1), description, springs_to_place)
    sum += recurse(drawing.replace('?', '#', 1), description, springs_to_place - 1)
    return sum

with open("inputs/12") as f:
    lines = f.read().rstrip("\n").split("\n")

part1 = 0
for line in lines:
    fields = line.split(" ")
    springs_required = reduce(lambda a, b: a+b, map(int, fields[1].split(",")))
    springs_already = fields[0].count('#')
    part1 += recurse(fields[0], fields[1], springs_required - springs_already)

print(f"Part 1: {part1}")

jobs = []
for line in lines:
    fields = line.split(" ")
    drawing = fields[0]
    desc = fields[1]
    for i in range(4):
        drawing += '?' + fields[0]
        desc += ',' + fields[1]
    springs_required = reduce(lambda a, b: a+b, map(int, desc.split(","))) - drawing.count('#')
    jobs.append( (drawing, desc, springs_required) )
pool = Pool(processes=4)
results = pool.starmap(recurse, jobs)
part2 = sum(results)
pool.close()
pool.join()
print(f"Part 2: {part2}")
