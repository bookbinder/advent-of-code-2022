import rctools as rc

def is_visible(r: int, c: int):
    "Whether the top of a tree can be seen from any direction outside forest"
    val = grid[r][c]
    return any([
        all(z < val for z in grid[r][c + 1:]),
        all(z < val for z in grid[r][:c]),
        all(z < val for z in [grid[nr][c] for nr in range(0, r)]),
        all(z < val for z in [grid[nr][c] for nr in range(r + 1, len(grid))])
    ])

def viewing_dist(val: int, rr: range, cc: range) -> int:
    "Viewing distance along given axis"
    total = 0
    for r in rr:
        for c in cc:
            if grid[r][c] >= val:
                return total + 1
            else:
                total += 1
    return total

def scenic_score(r: int, c: int) -> int:
    "Mulitply viewing distances along 4 axes"
    val = grid[r][c]
    up    = viewing_dist(val, range(r - 1, -1, -1), range(c, c + 1))
    down  = viewing_dist(val, range(r + 1, R), range(c, c + 1))
    right = viewing_dist(val, range(r, r + 1), range(c + 1, C))
    left  = viewing_dist(val, range(r, r + 1), range(c - 1, -1, -1))
    return up * left * down * right

input = rc.aoc_in(__file__)[1].splitlines()
grid = tuple(tuple(map(int, r)) for r in input)
R, C = len(grid), len(grid[0])

print("Part 1:", sum(is_visible(r, c)
                     for r in range(R) for c in range(C)))
print("Part 2:", max(scenic_score(r, c)
                     for r in range(R) for c in range(C)))
