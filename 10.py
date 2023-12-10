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

sys.setrecursionlimit(10000) # fill function is not gentle
width = len(lines[0])
height = len(lines)
area_to_determine = width * height - len(visited)

# track left of path vs right of path as sets
left = set()
right = set()

# find the direction of movement for ease
def sub_point(n):
    return((n[1][0]-n[0][0], n[1][1]-n[0][1]))
direction = list(map(sub_point, zip(visited[:-1], visited[1:])))
direction.append( (visited[-1][0] - visited[0][0], visited[-1][1] - visited[0][1]) )

# ghetto fill function.  Should flatten but won't.
def fill(p, my_set):
    if p[0] < 0 or p[1] < 0 or p[0] >= width or p[1] >= height:
        return
    if(not (p in visited)):
        if(not (p in my_set)):
            my_set.add(p)
            offsets = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            for o in offsets:
                fill((p[0]+o[0], p[1]+o[1]), my_set)


#travel through loop from part 1, adding to left-hand and right-hand sets
for i in range(len(visited)):
    if direction[i] == (-1, 0): # moving left
        fill( (visited[i][0], visited[i][1] + 1), left) # down is left
        fill( (visited[i][0], visited[i][1] - 1), right) # up is right
        fill( (visited[i+1][0], visited[i+1][1] + 1), left) # down is left
        fill( (visited[i+1][0], visited[i+1][1] - 1), right) # up is right
    elif direction[i] == (0, -1): # moving up
        fill( (visited[i][0]-1, visited[i][1]), left) # left is left
        fill( (visited[i][0]+1, visited[i][1]), right) # right is right
        fill( (visited[i+1][0]-1, visited[i+1][1]), left) # left is left
        fill( (visited[i+1][0]+1, visited[i+1][1]), right) # right is right
    elif direction[i] == (1, 0): # moving right
        fill( (visited[i][0], visited[i][1] - 1), left) # up is left
        fill( (visited[i][0], visited[i][1] + 1), right) # down is right
        fill( (visited[i+1][0], visited[i+1][1] - 1), left) # up is left
        fill( (visited[i+1][0], visited[i+1][1] + 1), right) # down is right
    else: # moving down
        fill( (visited[i][0] + 1, visited[i][1]), left) # right is left
        fill( (visited[i][0] - 1, visited[i][1]), right) # left is right
        fill( (visited[i+1][0] + 1, visited[i+1][1]), left) # right is left
        fill( (visited[i+1][0] - 1, visited[i+1][1]), right) # left is right

    #when there's no more unallocated map, we can break out of loop
    if len(left)+len(right) == area_to_determine:
        break

# silly printing of map
# we're assuming there are more outside-bits than inside-bits because it's 
# obvious from the map.  I guess in theory, we could grow the map until there
# MUST be more outside than inside, but fill is already painful enough

ls = '.'
rs = 'o'
part2 = len(left)
if len(left) > len(right):
    ls = 'o'
    rs = '.'
    part2 = len(right)
for y in range(height):
    for x in range(width):
        if (x, y) in left:
            print(ls, end="")
        elif (x, y) in right:
            print(rs, end="")
        elif (x, y) in visited:
            print(" ", end="")
        else:
            print("#", end="")
    print()

print(f"Part 2: {part2}")
