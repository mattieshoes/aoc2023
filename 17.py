#!/usr/bin/python3

from collections import namedtuple

# row, column, direction
Node = namedtuple('Node', ['r', 'c', 'd'])

def add_to_boundary(n, direction, squares, cost):
    # generate new node and calculate cost
    new_cost = cost
    if direction == 'E':
        if n.c + squares >= width:
            return
        new_node = Node(n.r, n.c + squares, 'E')
        for i in range(n.c+1, new_node.c+1, 1):
            new_cost += int(lines[n.r][i])
    elif direction == 'W':
        if n.c - squares < 0:
            return
        new_node = Node(n.r, n.c - squares, 'W')
        for i in range(n.c-1, new_node.c-1, -1):
            new_cost += int(lines[n.r][i])
    elif direction == 'N':
        if n.r - squares < 0:
            return
        new_node = Node(n.r - squares, n.c, 'N')
        for i in range(n.r-1, new_node.r-1, -1):
            new_cost += int(lines[i][n.c])
    else:
        if n.r + squares >= height:
            return
        new_node = Node(n.r + squares, n.c, 'S')
        for i in range(n.r+1, new_node.r+1, 1):
            new_cost += int(lines[i][n.c])
    
    # if it's in visited, bail
    if new_node in visited:
        return
    
    # add new node to boundary unless it already exists as a 
    # boundary node with a better cost
    if new_node not in boundary or boundary[new_node] > new_cost:
        boundary[new_node] = new_cost


def expand(n, cost, min_count=1, max_count=3):
    # if we've already been here, bail early
    if n in visited:
        del boundary[n]
        return

    # okay now we've been here
    visited[n] = boundary[n]
    del boundary[n]

    # generate moves.  since we generate all valid straight-line moves,
    # we only need to generate turns 
    if n.d in 'NSQ':
        for i in range(min_count, max_count+1):
            add_to_boundary(n, 'E', i, cost)
            add_to_boundary(n, 'W', i, cost)
    if n.d in 'EWQ':
        for i in range(min_count, max_count+1):
            add_to_boundary(n, 'N', i, cost)
            add_to_boundary(n, 'S', i, cost)


def dijkstra(min_count, max_count):
    target_row, target_col = height-1, width-1
    while(True):
        # find the lowest cost boundary and expand it
        min_cost = 999999999
        min_k = ''
        for k in boundary:
            if boundary[k] < min_cost:
                min_cost = boundary[k]
                min_k = k
        tmp = {}
        for k in boundary:
            if boundary[k] == min_cost:
                tmp[k] = min_cost

        for k in tmp:
            if k.r == target_row and k.c == target_col: 
                return min_cost
            expand(k, min_cost, min_count, max_count)

with open("inputs/17") as f:
    lines = f.read().rstrip("\n").split("\n")

height = len(lines)
width = len(lines[0])

visited = {}
boundary = {Node(0,0,'Q'): 0}
part1 = dijkstra(1, 3)
print(f"Part 1: {part1}")

visited = {}
boundary = {Node(0,0,'Q'): 0}
part2 = dijkstra(4, 10)
print(f"Part 2: {part2}")
