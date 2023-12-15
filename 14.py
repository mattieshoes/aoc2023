#!/usr/bin/python3

import random

# calculates load as specified by the problem
def calculate_load():
    load = 0
    for row in range(height):
        for col in range(width):
            if board[row][col] == 'O':
                load += height - row
    return load

# tilts board in direction specified
# should clean up, but won't
def tilt_board(direction="north"):
    if direction == 'north':
        for row in range(height):
            for col in range(width):
                if board[row][col] == '.': # scan south
                    for offset in range(1, height-row):
                        if board[row+offset][col] == '#':
                            break
                        if board[row+offset][col] == 'O':
                            board[row][col] = 'O'
                            board[row+offset][col] = '.'
                            break
    elif direction == 'south':
        for row in range(height-1, -1, -1):
            for col in range(width):
                if board[row][col] == '.': # scan north
                    for offset in range(-1, -row-1, -1):
                        if board[row+offset][col] == '#':
                            break
                        if board[row+offset][col] == 'O':
                            board[row][col] = 'O'
                            board[row+offset][col] = '.'
                            break
    elif direction == 'west':
        for col in range(width):
            for row in range(height):
                if board[row][col] == '.': # scan east
                    for offset in range(1, width-col):
                        if board[row][col+offset] == '#':
                            break
                        if board[row][col+offset] == 'O':
                            board[row][col] = 'O'
                            board[row][col+offset] = '.'
                            break
    elif direction == 'east':
        for col in range(width-1, -1, -1):
            for row in range(height):
                if board[row][col] == '.': # scan west
                    for offset in range(-1, -col-1, -1):
                        if board[row][col+offset] == '#':
                            break
                        if board[row][col+offset] == 'O':
                            board[row][col] = 'O'
                            board[row][col+offset] = '.'
                            break

with open("inputs/14") as f:
    lines = f.read().rstrip("\n").split("\n")
height, width = len(lines), len(lines[0])
board = [[x for x in line] for line in lines]

tilt_board()
part1 = calculate_load()
print(f"Part 1: {part1}")

part2 = 0
board = [[x for x in line] for line in lines] # reset board to initial state

# we're going to generate 64 bit hash keys describing the board in order to
# detect when we've fallen into a cycle
hash_map = {'.': 0, 'O': 1, '#': 2}
hv = [[[random.getrandbits(64) for x in line] for line in lines] for i in range(3)]

def get_hash_value():
    val = 0
    for r in range(height):
        for c in range(width):
            val ^= hv[hash_map[board[r][c]]][r][c]
    return val 

seen = dict() # seen[position_hash] -> cycle seen
loads = [] 

# iterate doing spin cycles, store hash in seen and load in loads
# when position repeats, do math and spit out answer
for i in range(1000000):
    tilt_board("north")
    tilt_board("west")
    tilt_board("south")
    tilt_board("east")
    
    position_hash = get_hash_value()
    if position_hash in seen:
        cycle_length = i - seen[position_hash]
        offset = seen[position_hash] + 1
        cycle_offset = (1000000000 - offset) % (cycle_length)
        print(f"Cycle found on {i+1}: Cycle length {cycle_length} with", \
              f"starting offset {offset}, meaning cycle_offset {cycle_offset}")
        part2 = loads[seen[position_hash]+cycle_offset]
        break
    seen[position_hash] = i
    loads.append(calculate_load())

print(f"Part 2: {part2}")
