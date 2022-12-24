import rctools as rc
from collections import deque

def adj(pt):
    a, b, c = pt
    return ((a + 1, b, c), (a - 1, b, c),
            (a, b + 1, c), (a, b - 1, c),
            (a, b, c + 1), (a, b, c - 1))

def outer_fill():
    "All points between outer bounds and object's edge"
    seen = set()
    q = deque([(xmin, ymin, zmin)])
    while q:
        x, y, z = pt = q.popleft()
        if pt in seen or pt in blocks:
            continue
        if any([x < xmin, x > xmax, y < ymin, y > ymax, z < zmin, z > zmax]):
            continue
        seen.add(pt)
        for neighbor in adj(pt):
            q.append(neighbor)
    return seen

blocks = frozenset(map(rc.ints, rc.aoc_in(__file__)[1].splitlines()))
xmin = min(z[0] for z in blocks) - 1
xmax = max(z[0] for z in blocks) + 1
ymin = min(z[1] for z in blocks) - 1
ymax = max(z[1] for z in blocks) + 1
zmin = min(z[2] for z in blocks) - 1
zmax = max(z[2] for z in blocks) + 1
outer = outer_fill()

print("Part 1:", sum(1 for pt in blocks for z in adj(pt) if z not in blocks))
print("Part 2:", sum(1 for pt in blocks for z in adj(pt) if z in outer))
