import rctools as rc
import itertools as it

def parse(blocked, line):
    for a, b in it.pairwise(line):
        for r in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            for c in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                blocked.add((r, c))

def falling(blocked, r, c, part2=False):
    if r > abyss or (0, 500) in blocked:
        return True
    while (r + 1, c) not in blocked and r < abyss:
        r += 1
    if part2 and r == abyss:
        blocked.add((r, c))
        return False
    if (r + 1, c - 1) not in blocked:
        return falling(blocked, r + 1, c - 1, part2)
    elif (r + 1, c + 1) not in blocked:
        return falling(blocked, r + 1, c + 1, part2)
    else:
        blocked.add((r, c))
        return False

def calc(part2=False):
    blocked = set()
    for line in input:
        parse(blocked, line)
    return next(i for i in it.count() if falling(blocked, 0, 500, part2))

input = rc.aoc_in(__file__)[1].splitlines()
input = [z.split(' -> ') for z in input]
input = [[z.split(',') for z in subl] for subl in input]
input = [[[int(z) for z in subla][::-1] for subla in sublb] for sublb in input]
abyss = max(int(z[0]) for subl in input for z in subl) + 1

print("Part 1:", calc())
print("Part 2:", calc(part2=True))
