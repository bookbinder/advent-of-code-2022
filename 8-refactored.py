"""Refactored, less repetitive, probably less memory, but takes slower"""

import rctools as rc
from math import prod

def up(r, c):    yield from (grid[nr][c] for nr in range(r - 1, -1, -1))
def down(r, c):  yield from (grid[nr][c] for nr in range(r + 1, R))
def right(r, c): yield from (grid[r][nc] for nc in range(c + 1, C))
def left(r, c):  yield from (grid[r][nc] for nc in range(c - 1, -1, -1))

def is_visible(r: int, c: int):
    "Whether the treetop at r, c can be seen from any direction outside forest"
    for f in dirs:
        if all(z < grid[r][c] for z in f(r, c)):
            return True
    return False

def viewing_dist(r: int, c: int, dir) -> int:
    "Viewing distance along the dir"
    return next((i + 1
                 for i, v in enumerate(dir(r, c)) if v >= grid[r][c]),
                 len(list(dir(r, c))))

def scenic_score(r: int, c: int) -> int:
    "Mulitply viewing distances along 4 axes"
    return prod(viewing_dist(r, c, dir) for dir in dirs)

input = rc.aoc_in(__file__)[1].splitlines()
grid = tuple(tuple(map(int, r)) for r in input)
R, C = len(grid), len(grid[0])
dirs = (up, down, right, left)

print("Part 1:", sum(is_visible(r, c)
                     for r in range(R) for c in range(C)))
print("Part 2:", max(scenic_score(r, c)
                     for r in range(R) for c in range(C)))
