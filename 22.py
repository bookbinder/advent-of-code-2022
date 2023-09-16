'''see hyper-neutrino'''
import rctools as rc
import re

def part1(r, c, dr, dc, val):
    "Logic for a flat 2d traversal (in for-loop of run())"
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
    return r, c

def part2(r, c, dr, dc, val):
    "Logic for a cube traversal (in for-loop of run())"
    for _ in range(int(val)):
        cdr = dr
        cdc = dc
        nr = r + dr
        nc = c + dc
        if nr < 0 and 50 <= nc < 100 and dr == -1:
            dr, dc = 0, 1
            nr, nc = nc + 100, 0
        elif nc < 0 and 150 <= nr < 200 and dc == -1:
            dr, dc = 1, 0
            nr, nc = 0, nr - 100
        elif nr < 0 and 100 <= nc < 150 and dr == -1:
            nr, nc = 199, nc - 100
        elif nr >= 200 and 0 <= nc < 50 and dr == 1:
            nr, nc = 0, nc + 100
        elif nc >= 150 and 0 <= nr < 50 and dc == 1:
            dc = -1
            nr, nc = 149 - nr, 99
        elif nc == 100 and 100 <= nr < 150 and dc == 1:
            dc = -1
            nr, nc = 149 - nr, 149
        elif nr == 50 and 100 <= nc < 150 and dr == 1:
            dr, dc = 0, -1
            nr, nc = nc - 50, 99
        elif nc == 100 and 50 <= nr < 100 and dc == 1:
            dr, dc = -1, 0
            nr, nc = 49, nr + 50
        elif nr == 150 and 50 <= nc < 100 and dr == 1:
            dr, dc = 0, -1
            nr, nc = nc + 100, 49
        elif nc == 50 and 150 <= nr < 200 and dc == 1:
            dr, dc = -1, 0
            nr, nc = 149, nr - 100
        elif nr == 99 and 0 <= nc < 50 and dr == -1:
            dr, dc = 0, 1
            nr, nc = nc + 50, 50
        elif nc == 49 and 50 <= nr < 100 and dc == -1:
            dr, dc = 1, 0
            nr, nc = 100, nr - 50
        elif nc == 49 and 0 <= nr < 50 and dc == -1:
            dc = 1
            nr, nc = 149 - nr, 0
        elif nc < 0 and 100 <= nr < 150 and dc == -1:
            dc = 1
            nr, nc = 149 - nr, 50
        if grid[nr][nc] == "#":
            dr = cdr
            dc = cdc
            break
        r, c = nr, nc
    return r, c


def run(func=part1):
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
            r, c = func(r, c, dr, dc, val)
    k = ((0, 1), (1, 0), (0, -1), (-1, 0)).index((dr, dc))
    return 1000 * (r + 1) + 4 * (c + 1) + k

input = rc.aoc_in(__file__)[1]
grid, sequence = input.split('\n\n')
grid = grid.splitlines()
R, C = len(grid), max(map(len, grid))
grid = [line + " " * (C - len(line)) for line in grid]

print("Part 1:", run())
print("Part 1:", run(func=part2))
