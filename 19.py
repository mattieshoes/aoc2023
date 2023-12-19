#!/usr/bin/python3

# calculates the number of unique solutions given the constraints (part2)
def constraint_space(constraints):
    return((constraints['x'][1] - constraints['x'][0]) *
           (constraints['m'][1] - constraints['m'][0]) *
           (constraints['a'][1] - constraints['a'][0]) *
           (constraints['s'][1] - constraints['s'][0]))

# Rule description
# letter, cmp, val, target are straight from inputs
# test is just a boolean for whether it has a test or not
# rules without tests won't have letter, cmp, or val
class Rule():
    def __init__(self, desc):
        if ':' in desc:
            self.test = True
            r, t = desc.split(":")
            self.letter = r[0]
            self.cmp = r[1]
            self.target = t
            self.val = int(r[2:])
        else:
            self.test = False
            self.target = desc

    # applies a rule to a part
    # returns the target if it passes the rule
    # returns None if it fails the rule
    def apply(self, part):
        if self.test:
            if self.cmp == '>':
                if part[self.letter] > self.val:
                    return self.target
                return None
            else:
                if part[self.letter] < self.val:
                    return self.target
                return None
        else:
            return self.target

    # given constraints (min and max values for x, m, a, s)
    # returns the constraints that pass the rule and constraints that don't
    def accepts(self, constraints):
        if self.test:
            if self.cmp == '>':
                tgt = self.val + 1
                if tgt < constraints[self.letter][0]: # all pass
                    return([constraints, None])
                elif tgt >= constraints[self.letter][1]: # all fail
                    return([None, constraints])                
                else:
                    passing = constraints.copy()
                    failing = constraints.copy()
                    passing[self.letter] = (tgt, constraints[self.letter][1])
                    failing[self.letter] = (constraints[self.letter][0], tgt)
                    return([passing, failing])
            else: # self.cmp == '<'
                tgt = self.val
                if tgt >= constraints[self.letter][1]: # all pass
                    return([constraints, None])
                elif tgt < constraints[self.letter][0]: # all fail
                    return([None, constraints])                
                else:
                    passing = constraints.copy()
                    failing = constraints.copy()
                    passing[self.letter] = (constraints[self.letter][0], tgt)
                    failing[self.letter] = (tgt, constraints[self.letter][1])
                    return([passing, failing])
        else: # no test, all pass by default
            return([constraints, None])
        
# Workflow just contains a set of rules from the problem
class Workflow():
    def __init__(self, desc):
        self.rules = []
        name, rules = desc.split('{')
        rule_strings = rules[:-1].split(',')
        for rule in rule_strings:
            self.rules.append(Rule(rule))

    # apply() applies the rules sequentially, returns either 'A', 'R', or the name of the 
    # workflow it's passed to
    def apply(self, part):
        for rule in self.rules:
            result = rule.apply(part)
            if result is not None:
                return result

    # given constraints, applies rules sequentially and returns the number of eventually
    # accepted potential values
    # relies on global Workflow dict to recurse and solve nodes that get passed to 
    # other workflows
    def accepts(self, constraints):
        acc = 0
        for rule in self.rules:
            # split into passing and failing
            passing, failing = rule.accepts(constraints)
            if passing is not None:
                if rule.target == 'A':
                    acc += constraint_space(passing)
                elif rule.target == 'R':
                    acc += 0
                else:
                    acc += workflow[rule.target].accepts(passing)
            if failing is not None: # some failed, must run next rule
                constraints = failing
            else: # all have been accounted for
                return acc 
        
with open("inputs/19") as f:
    workflows, parts = f.read().rstrip("\n").split("\n\n")

workflows = workflows.split("\n")
parts = parts.split("\n")

# convert given workflows into a map of Workflow objects
# (which contain a list of Rule objects)
workflow = {}
for w in workflows:
    workflow[w[:w.index('{')]] = Workflow(w)

part1 = 0
for part in parts:
    p = {} # build part manually since it isn't quite json
    xmas_list = part[1:-1].split(',')
    for desc in xmas_list:
        letter, val = desc.split('=')
        p[letter] = int(val)

    result = "in"
    while(result != 'A' and result != 'R'):
        result = workflow[result].apply(p)
    if result == 'A':
        part1 += p['x'] + p['m'] + p['a'] + p['s']
print(f"Part 1: {part1}")

# just pass wide-open constraints to 'in' rule, and let it recurse through the rules
no_constraints = {'x': (1, 4001), 'm': (1, 4001), 'a': (1,4001), 's': (1, 4001)}
part2 = workflow['in'].accepts(no_constraints)
print(f"Part 2: {part2}")
