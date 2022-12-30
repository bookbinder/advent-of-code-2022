'''from a reddit user'''
import rctools as rc

def solve(start, end, step):
    positions = set([start])

    while True:
        next_positions = set()
        for r, c in positions:
            for x, y in ((r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if (x, y) == end:
                    return step
                if 0 <= x < R and 0 <= y < C \
                  and grid[x][(y - step) % C] != ">" \
                  and grid[x][(y + step) % C] != "<" \
                  and grid[(x - step) % R][y] != "v" \
                  and grid[(x + step) % R][y] != "^":
                    next_positions.add((x, y))
        # update positions unless we waited at start and missed boundary check
        positions = next_positions or {start}
        step += 1

grid = [row[1:-1] for row in rc.aoc_in(__file__)[1].splitlines()[1:-1]]
R, C = len(grid), len(grid[0])
start, end = (-1, 0), (R, C - 1)

print("Part 1:", s1 := solve(start, end, 1))
print("Part 2:", solve(start, end, solve(end, start, s1)))
