import re
import itertools as it
import rctools as rc
import sys

def get_data(input):
    chart, path = input.split('\n\n')
    path = re.findall(r'\d+|L|R', path)
    chart = chart.splitlines()
    R = len(chart)
    C = max(len(chart[z]) for z in range(R))
    for i, r in enumerate(chart):
        chart[i] = r + " " * (C - len(r))  # pad right if necessary
    return chart, path, R, C

def get_range(r, c, facing):
    "Infinite iterator of valid pts going from r, c in given direction"
    if chart[r][c] in '#.':
        minc = next(z for z in range(C) if chart[r][z] in '#.')
        maxc = next(z for z in reversed(range(C)) if chart[r][z] in '#.')
        minr = next(z for z in range(R) if chart[z][c] in '#.')
        maxr = next(z for z in reversed(range(R)) if chart[z][c] in '#.')
        if facing == 0:
            rng = list(range(c + 1, maxc + 1)) + list(range(minc, c + 1))
            return it.cycle((r, z) for z in rng)
        elif facing == 2:
            rng = list(range(c - 1, minc - 1, -1)) + list(range(maxc, c - 1, -1))
            return it.cycle((r, z) for z in rng)
        elif facing == 1:
            rng = list(range(r + 1, maxr + 1)) + list(range(minr, r + 1))
            return it.cycle((z, c) for z in rng)
        elif facing == 3:
            rng = list(range(r - 1, minr - 1, -1)) + list(range(maxr, r - 1, -1))
            return it.cycle((z, c) for z in rng)

def get_range2():
    return 'hi'

def run(part2=False):
    func = get_range if not part2 else get_range2
    facing = 0
    # get the starting point
    r, c = (0, next(z for z in range(C) if chart[0][z] == '.'))
    for i, val in enumerate(path):
        if val == 'R':
            facing = (facing + 1) % 4
        elif val == 'L':
            facing = (facing - 1) % 4
        else:
            rng = func(r, c, facing)
            for _ in range(int(val)):
                nr, nc = next(rng)
                if chart[nr][nc] == '#':
                    break
                else:
                    r, c = nr, nc
    return 1000 * (r + 1) + 4 * (c + 1) + facing

input = rc.aoc_in(__file__)[1]
chart, path, R, C = get_data(input)
test = list(map(str.strip, [*open(0)]))[0]
print(test)
# print("Part 1:", run())
# print("Part 2:", run(part2=True))
