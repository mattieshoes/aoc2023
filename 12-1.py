#!/usr/bin/python3

#given a drawing, makes the description (e.g. "1,1,3")
def make_description(drawing):
    tmp = drawing.split(".")
    desc = []
    for i in tmp: 
        if len(i) > 0:
            desc.append(str(len(i)))
    return(",".join(desc))

# recursive function -- given the drawing and the description, will find the
# next '?' and replace it with '.', then call itself... then replace it with
# '#' and call itself again.  Eventually returns the sum of all the sequences
# that match the given description
def recurse(drawing, description):
    # bail if done
    question_count = drawing.count('?')
    if question_count ==  0:
        if make_description(drawing) == description:
            return 1
        return 0
    
    # recursively call self with '.' and with '#'returning sum
    sum = 0
    sum += recurse(drawing.replace('?', '.', 1), description)
    sum += recurse(drawing.replace('?', '#', 1), description)
    return sum

with open("inputs/12") as f:
    lines = f.read().rstrip("\n").split("\n")

sum = 0
for line in lines:
    fields = line.split(" ") # fields[0] being the drawing, fields[1] being the description
    result = recurse(fields[0], fields[1])
    print(f"Drawing: {fields[0]} Description: {fields[1]} Ways: {result}")
    sum += result
print(f"Part 1: {sum}")
