#!/usr/bin/python3

from collections import namedtuple
from multiprocessing import Pool
from functools import reduce

# Queue entry contains row, column, and a direction tuple
Node = namedtuple('Node', ['row', 'col', 'd'])

# adds to energized and visited, returns Nodes the beam will travel to
def expand_node(n, visited, energized):
    # bail if beam left grid
    if n.row >= height or n.col >= width or n.row < 0 or n.col < 0:
        return []
    # bail if we've already expanded an identical node
    if n in visited:
        return []
    # add to visited and energized 
    visited.add(n)
    energized.add((n.row, n.col))
    # return continuation nodes
    if lines[n.row][n.col] == '.': # continues straight
        return([Node(n.row + n.d[0], n.col + n.d[1], n.d)])
    elif lines[n.row][n.col] == '\\': # flips row and col directions
        return([Node(n.row + n.d[1], n.col + n.d[0], (n.d[1], n.d[0]))])
    elif lines[n.row][n.col] == '/': # flips and inverses row and col directions
        return([Node(n.row - n.d[1], n.col - n.d[0], (-n.d[1], -n.d[0]))])
    elif lines[n.row][n.col] == '-':
        if n.d[1] != 0: # no split if parallel 
            return([Node(n.row + n.d[0], n.col + n.d[1], n.d)])
        else: # splits to a right-hand and left-hand turn
            return([Node(n.row, n.col-1, (0, -1)), Node(n.row, n.col+1, (0,1))])
    elif lines[n.row][n.col] == '|':
        if n.d[0] != 0: # no split if parallel
            return([Node(n.row + n.d[0], n.col + n.d[1], n.d)])
        else: # splits into a right-hand and left-hand turn
            return([Node(n.row-1, n.col, (-1, 0)), Node(n.row+1, n.col, (1,0))])
    return [] # never reached, but for sanity...

# gets the number of energized tiles given a start point
def calculate(row, col, direction):
    energized = set()
    visited = set()
    queue = [Node(row, col, direction)]
    # expand nodes from queue until queue is empty
    while len(queue) > 0:
        queue.extend(expand_node(queue.pop(), visited, energized))
    return(len(energized))

with open("inputs/16") as f:
    lines = f.read().rstrip("\n").split("\n")
height = len(lines)
width = len(lines[0])

part1 = calculate(0,0,(0,1))
print(f"Part 1: {part1}")

part2 = 0
# generate list of arguments to calculate()
jobs = []
for r in range(height):
    jobs.append((r, 0, (0,1)))
    jobs.append((r, width-1, (0,-1)))
for c in range(width):
    jobs.append((0, c, (1,0)))
    jobs.append((height-1, c, (-1,0)))

# multiprocessing all the calculate jobs
part2 = 0
pool = Pool(processes=4)
results = pool.starmap(calculate, jobs)
part2 = max(results)
pool.close()
pool.join()

print(f"Part 2: {part2}")
