#!/usr/bin/python3

import sys

# given coords, gives the coords it connects to
def get_next(point):
    p = get_square(point)
    x = point[0]
    y = point[1]

    if p =='|':
        return([(x, y-1), (x, y+1)])
    elif p =='-':
        return([(x-1, y), (x+1, y)])
    elif p =='L':
        return([(x, y-1), (x+1, y)])
    elif p =='J':
        return([(x-1, y), (x, y-1)])
    elif p =='7':
        return([(x-1, y), (x, y+1)])
    elif p =='F':
        return([(x, y+1), (x+1, y)])
    elif p =='.':
        return []
    elif p =='S':
        dirs = []
        if (get_square((x-1, y)) in "F-L"):
            dirs.append((x-1, y))
        if (get_square((x+1, y)) in "7-J"):
            dirs.append((x+1, y))
        if (get_square((x, y-1)) in "7|F"):
            dirs.append((x, y-1))
        if (get_square((x, y+1)) in "J|L"):
            dirs.append((x, y+1))
        return dirs

# just returns the char at specified coordinates
def get_square(point):
    return(lines[point[1]][point[0]])

# sum tuple, for sanity
def tsum(a, b):
    return( (a[0]+b[0], a[1]+b[1]) )

with open("inputs/10") as f:
    lines = f.read().rstrip("\n").split("\n")

# find starting point
visited = []
for y in range(len(lines)):
    if 'S' in lines[y]:
        visited.append((lines[y].index('S'),y))
        break
visited.append(get_next(visited[0])[0])

# traverse the loop, answer will be length/2
while(True):
    result = get_next(visited[-1])
    if result[0] == visited[-2]:
        if result[1] == visited[0]:
            break
        visited.append(result[1])
    else:
        if result[0] == visited[0]:
            break
        visited.append(result[0])
print(f"Part 1: {len(visited) // 2}")

width = len(lines[0])
height = len(lines)
area_to_determine = width * height - len(visited)

# track left of path vs right of path as sets
lr = [set(), set()]
visited_set = set(visited)

print("\tCalculating directions of travel on main path")
def sub_point(n):
    return((n[1][0]-n[0][0], n[1][1]-n[0][1]))
direction = list(map(sub_point, zip(visited[:-1], visited[1:])))
direction.append( (visited[0][0] - visited[-1][0], visited[0][1] - visited[-1][1]) )

print("\tTraversing path marking left-hand and right-hand nodes")
for i in range(len(visited)):
    if direction[i] == (-1, 0): # moving left
        p = [[(visited[i][0], visited[i][1]+1), (visited[i][0]-1, visited[i][1]+1)],[(visited[i][0], visited[i][1]-1), (visited[i][0]-1, visited[i][1]-1)]]
    elif direction[i] == (0, -1): # moving up
        p = [[(visited[i][0]-1, visited[i][1]), (visited[i][0]-1, visited[i][1]-1)], [(visited[i][0]+1, visited[i][1]), (visited[i][0]+1, visited[i][1]-1)]]
    elif direction[i] == (1, 0): # moving right
        p = [[(visited[i][0], visited[i][1]-1), (visited[i][0]+1, visited[i][1]-1)],[(visited[i][0], visited[i][1]+1), (visited[i][0]+1, visited[i][1]+1)]]
    else: # moving down
        p = [[(visited[i][0]+1, visited[i][1]), (visited[i][0]+1, visited[i][1]+1)],[(visited[i][0]-1, visited[i][1]), (visited[i][0]-1, visited[i][1]+1)]]
    for i in range(2):
        for pi in range(2):
            if p[i][pi] not in visited_set:
                lr[i].add(p[i][pi])

# fill function -- find neigbors not part of the main path, add to set
def fill(my_set):
    offsets = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    list_set = list(my_set)
    for p in list_set:
        for o in offsets:
            neighbor = tsum(p, o)
            if neighbor[0] >= 0 and neighbor[1] >= 0 and \
                neighbor[0] < width and neighbor[1] < height and \
                neighbor not in visited:
                my_set.add(neighbor)
    if len(my_set) == len(list_set):
        return True
    return False


print("\tFlood filling until we can distinguish inside from outside")
part2 = 0
while part2 == 0:
    found = False
    for i in range(2):
        result = fill(lr[i])
        if result and (0,0) not in lr[i]:
            part2 = len(lr[i])
            break
print(f"Part 2: {part2}")
