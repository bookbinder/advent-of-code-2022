import re
import rctools as rc

chart, path = rc.aoc_in(__file__)[0].split('\n\n')
path = [int(z) if z.isnumeric() else z for z in re.findall(r'\d+|L|R', path)]
chart = chart.splitlines()

dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
curr = 0
r, c = (0, next(i for i in range(len(chart[0])) if chart[0][i] == '.'))

for i, val in enumerate(path):
    if val == 'R':
        curr = (curr + 1) % 4
    elif val == 'L':
        curr = (curr - 1) % 4
    else:
        while chart[r][c] != '#' and val > 0:
            nr = r + dirs[curr][0]
            nc = c + dirs[curr][1]
