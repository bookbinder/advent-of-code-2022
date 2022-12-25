'''from 0xdf'''
import rctools as rc
from math import ceil, prod
from collections import deque

blueprints = list(map(rc.ints, rc.aoc_in(__file__)[1].splitlines()))
BP = tuple([
    ((z[1], 0, 0, 0), (z[2], 0, 0, 0), (z[3], z[4], 0, 0), (z[5], 0, z[6], 0))
    for z in blueprints
])


def simulate(bp, t=24):
    q = deque()
    q.append((t, (0, 0, 0, 0), (1, 0, 0, 0)))
    seen = set()
    best = 0
    max_robots = [max(cost[i] for cost in bp) for i in range(3)] + [float('inf')]
    while q:
        t, stuff, robots = q.popleft()
        stuff = tuple([min(stuff[i], max_robots[i] * t) for i in range(4)])

        min_geodes_left = stuff[3] + (t * robots[3])
        if min_geodes_left > best:
            best = min_geodes_left

        if t == 0 or (t, stuff, robots) in seen:
            continue
        seen.add((t, stuff, robots))

        for resource in range(4):
            if resource != 3 and robots[resource] >= max_robots[resource]:
                continue
            if any([robots[rid] == 0 for rid, cost in enumerate(bp[resource])
                    if cost]):
                continue

            wait = max([ceil((cost - stuff[rid]) / robots[rid])
                        for rid, cost in enumerate(bp[resource]) if cost] + [0])

            if t - wait - 1 <= 0:
                continue

            next_stuff = [stuff[i] + (robots[i] * (wait + 1) - bp[resource][i]) for
                    i in range(4)]
            next_robots = list(robots)
            next_robots[resource] += 1

            q.append((t - wait - 1, tuple(next_stuff), tuple(next_robots)))

    return best

print("Part 1:", sum((i + 1) * simulate(BP[i], t=24) for i in range(len(BP))))
print("Part 2:", prod(simulate(BP[i], t=32) for i in range(3)))  # takes 90s
