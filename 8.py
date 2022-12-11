import rctools as rc
from typing import Tuple
from math import prod

def up(r, c):    return (GRID[nr][c] for nr in range(r - 1, -1, -1))
def down(r, c):  return (GRID[nr][c] for nr in range(r + 1, R))
def right(r, c): yield from GRID[r][c + 1:]
def left(r, c):  yield from reversed(GRID[r][:c])

def is_visible(pt: Tuple[int]):
    "Whether the treetop at r, c can be seen from any direction outside forest"
    r, c = pt
    for dir in DIRS:
        if all(z < GRID[r][c] for z in dir(r, c)):
            return True
    return False

def viewing_dist(pt: Tuple[int], dir) -> int:
    "Viewing distance along the dir"
    r, c = pt
    return next((i for i, v in enumerate(dir(r, c), 1) if v >= GRID[r][c]),
                len(list(dir(r, c))))

def scenic_score(pt: Tuple[int]) -> int:
    "Mulitply viewing distances along 4 axes"
    return prod(viewing_dist(pt, dir) for dir in DIRS)

input = rc.aoc_in(__file__)[1].splitlines()
GRID = tuple(tuple(map(int, r)) for r in input)
R, C = len(GRID), len(GRID[0])
COORDS = tuple((r, c) for r in range(R) for c in range(C))
DIRS = (up, down, right, left)

print("Part 1:", sum(map(is_visible, COORDS)))
print("Part 2:", max(map(scenic_score, COORDS)))
