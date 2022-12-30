'''see hyper-neutrino'''
import rctools as rc
import re

input = rc.aoc_in(__file__)[1]
grid, sequence = input.split('\n\n')
grid = grid.splitlines()
R, C = len(grid), max(map(len, grid))
grid = [line + " " * (C - len(line)) for line in grid]

r = 0
c = next(z for z in range(len(grid[0])) if grid[r][z] == '.')
dr = 0
dc = 1

for val in re.findall(r"\d+|R|L", sequence):
    if val == "R":
        dr, dc = dc, -dr
    elif val == "L":
        dr, dc = -dc, dr
    else:
        for _ in range(int(val)):
            nr, nc = r, c
            while True:
                nr = (nr + dr) % R
                nc = (nc + dc) % C
                if grid[nr][nc] != " ":
                    break
            if grid[nr][nc] == "#":
                break
            r, c = nr, nc

k = ((0, 1), (1, 0), (0, -1), (-1, 0)).index((dr, dc))
print("Part 1:", 1000 * (r + 1) + 4 * (c + 1) + k)
