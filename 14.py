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
def tilt_board(direction="north"):
    global position_hash
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
                            position_hash ^= hv[row][col] ^ hv[row+offset][col]
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
                            position_hash ^= hv[row][col] ^ hv[row+offset][col]
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
                            position_hash ^= hv[row][col] ^ hv[row][col+offset]
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
                            position_hash ^= hv[row][col] ^ hv[row][col+offset]
                            break

with open("inputs/14") as f:
    lines = f.read().rstrip("\n").split("\n")

height, width = len(lines), len(lines[0])
board = [[x for x in line] for line in lines]
position_hash = 0
hv = [[random.getrandbits(64) for x in line] for line in lines]

tilt_board()
part1 = calculate_load()
print(f"Part 1: {part1}")

part2 = 0
board = [[x for x in line] for line in lines] # reset board to initial state

seen = dict() # seen[position_hash] -> cycle seen
loads = [] 

# iterate doing spin cycles, store hash in seen and load in loads
# when position repeats:
# offset -> how many times until it starts repeating
# cycle_length -> how long the cycle is
# cycle_offset -> which part of the cycle hits on the 1 billionth spin cycle
# pull the load for that bit of the cycle
for i in range(1000000):
    tilt_board("north")
    tilt_board("west")
    tilt_board("south")
    tilt_board("east")
    
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
