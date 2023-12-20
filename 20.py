#!/usr/bin/python3

from functools import reduce

class Module():
    def __init__(self, desc):
        if desc[0] == 'b':
            self.type = 'broadcaster'
            self.name = 'broadcaster'
        elif desc[0] == '%':
            self.name = desc[1:desc.index(' ')]
            self.type = 'flipflop'
            self.state = 0
        elif desc[0] == '&':
            self.name = desc[1:desc.index(' ')]
            self.type = 'conjunction'
        elif desc[0] == '0':
            self.name = desc[1:]
            self.type = 'none'
        self.inputs = {}
        self.outputs = []

    def reset(self):
        if self.type == 'flipflop':
            self.state = 0
        elif self.type == 'conjunction':
            for k in self.inputs:
                self.inputs[k] = 0

    def send_pulse(self, val, source):
        result = []
        if self.type == 'none':
            return []
        elif self.type == 'flipflop':
            if val == 0: # low pulse
                self.state ^= 1
                if self.state == 0:
                    for o in self.outputs:
                        result.append((o, 0, self.name))
                else:
                    for o in self.outputs:
                        result.append((o, 1, self.name))
            else: # high pulse
                return []
        elif self.type == 'conjunction':
            self.inputs[source] = val # update memory
            found = False
            for k in self.inputs:
                if self.inputs[k] == 0:
                    found = True
                    break
            if found: # low found
                for o in self.outputs:
                    result.append((o, 1, self.name)) # send high
            else: # all highs
                for o in self.outputs:
                    result.append((o, 0, self.name)) # send low
        elif self.type == 'broadcaster':
            for o in self.outputs:
                result.append((o, val, self.name))
        return result

with open("inputs/20") as f:
    lines = f.read().rstrip("\n").split("\n")

# first pass, create modules
modules = {}
for line in lines:
    if line[0] == 'b':
        modules["broadcaster"] = Module(line)
    else:
        modules[line[1:line.index(' ')]] = Module(line)

# second pass, link outputs and add input names
# I was linking actual modules to outputs so it could just stream
# depth-first, but they have to be done sequentially so that turned 
# out to be irrelevant
for line in lines:
    if line[0] == 'b':
        name = "broadcaster"
    else:
        name = line[1:line.index(' ')]
    fields = line.split(' -> ')
    outputs = fields[1].split(', ')
    outs = []
    for o in outputs:
        if o not in modules:
            modules[o] = Module("0"+o)
        modules[o].inputs[name] = 0 
        modules[name].outputs.append(modules[o])

# just iterate 1000 button presses
count = [0,0]
for i in range(1000):
    results = modules['broadcaster'].send_pulse(0, "button")
    count[0] += 1
    while len(results) > 0:
        new_results = []
        for r in results:
            new_results.extend(r[0].send_pulse(r[1], r[2]))
            count[r[1]] += 1
        results = new_results
part1 = count[0] * count[1]
print(f"Part 1: {part1}")


# rx is connected to a conjunction which is connected to four conjunctions.
# the four conjunctions have different cycle lengths before sending a high
# lcm of the four cycle lengths should result in them all sending a high
# they all looked prime though so I just multiplied

part2 = 0
for k in modules:
    modules[k].reset()
prev = list(modules['rx'].inputs.keys())[0]
targets = list(modules[prev].inputs.keys())
cycles = [0 for x in targets]
found = False
while(not found):
    results = modules['broadcaster'].send_pulse(0, "button")
    part2 += 1
    while len(results) > 0:
        new_results = []
        for r in results:
            new_results.extend(r[0].send_pulse(r[1], r[2]))
        results = new_results
        for r in results:
            for i in range(len(targets)):
                if r[2] == targets[i] and r[1] == 1 and cycles[i] == 0:
                    cycles[i] = part2
                    if 0 not in set(cycles) :
                        found = True
                        break
part2 = reduce(lambda a,b: a * b, cycles)
print(f"Part 2: {part2}")
