#!/usr/bin/python3

from collections import namedtuple

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
    tile = lines[n.row][n.col]
    # return continuation nodes
    if tile == '.':
        return([Node(n.row + n.d[0], n.col + n.d[1], n.d)])
    elif tile == '\\':
        return([Node(n.row + n.d[1], n.col + n.d[0], (n.d[1], n.d[0]))])
    elif tile == '/':
        return([Node(n.row - n.d[1], n.col - n.d[0], (-n.d[1], -n.d[0]))])
    elif tile == '-':
        if n.d[1] != 0:
            return([Node(n.row + n.d[0], n.col + n.d[1], n.d)])
        else:
            return([Node(n.row, n.col-1, (0, -1)), Node(n.row, n.col+1, (0,1))])
    elif tile == '|':
        if n.d[0] != 0:
            return([Node(n.row + n.d[0], n.col + n.d[1], n.d)])
        else:
            return([Node(n.row-1, n.col, (-1, 0)), Node(n.row+1, n.col, (1,0))])

# gets the number of energized tiles given a start point
def calculate(row, col, direction):
    energized = set()
    visited = set()
    queue = [Node(row, col, direction)]
    # expand nodes from queue until queue is empty
    while len(queue) > 0:
        queue.extend(expand_node(queue[0], visited, energized))
        del queue[0]
    return(len(energized))

with open("inputs/16") as f:
    lines = f.read().rstrip("\n").split("\n")
height = len(lines)
width = len(lines[0])

part1 = calculate(0,0,(0,1))
print(f"Part 1: {part1}")

part2 = 0
for r in range(height):
    part2 = max(part2, calculate(r, 0, (0, 1)))
    part2 = max(part2, calculate(r, width-1, (0, -1)))
for c in range(width):
    part2 = max(part2, calculate(0, c, (1, 0)))
    part2 = max(part2, calculate(height-1, c, (-1, 0)))
print(f"Part 2: {part2}")
