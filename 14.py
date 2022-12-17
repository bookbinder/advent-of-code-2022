import rctools as rc
import itertools as it
from copy import deepcopy

def falling(blocked, part2=False, r=0, c=500):
    if r > abyss or (0, 500) in blocked:
        return True
    while (r + 1, c) not in blocked and r < abyss:
        r += 1
    if part2 and r == abyss:
        blocked.add((r, c))
        return False
    if (r + 1, c - 1) not in blocked:
        return falling(blocked, part2, r + 1, c - 1)
    elif (r + 1, c + 1) not in blocked:
        return falling(blocked, part2, r + 1, c + 1)
    else:
        blocked.add((r, c))
        return False

# split the input and get max r value + 1 for abyss
input = rc.aoc_in(__file__)[1].splitlines()
input = [z.split(' -> ') for z in input]
input = [[z.split(',') for z in subl] for subl in input]
input = [[[int(z) for z in subla][::-1] for subla in sublb] for sublb in input]
abyss = max(int(z[0]) for subl in input for z in subl) + 1

# create set of all blocked coordinates and make a copy for both parts
blocked = set()
for line in input:
    for a, b in it.pairwise(line):
        #  now draw the line segment (delta r or delta c will be 0)
        for r in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            for c in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                blocked.add((r, c))
blockedB = deepcopy(blocked)

print("Part 1:", next(i for i in it.count() if falling(blocked)))
print("Part 2:", next(i for i in it.count() if falling(blockedB, part2=True)))
