'''credit to user 0xdf'''
import re
import rctools as rc
from functools import cache

@cache
def dfs(pos, time, opened, part2=False):
    if time <= 0:
        return 0 if not part2 else dfs('AA', 26, opened)
    score = max(dfs(n, time - 1, opened, part2) for n in adjList[pos])
    if flows[pos] > 0 and not (m := bits[pos]) & opened:
        score = max(
            score,
            (time - 1) * flows[pos] + dfs(pos, time - 1, opened | m, part2)
        )
    return score

input   = rc.aoc_in(__file__)[1].splitlines()
parsed  = [re.split('[ =,;]+', line) for line in input]
flows   = {x[1]: int(x[5]) for x in parsed}
adjList = {x[1]: frozenset(x[10:]) for x in parsed}
# create bitset for opened valves:
bits  = {b: 1 << i for i, b in enumerate([z for z in flows if flows[z] > 0])}

print("Part 1:", dfs('AA', 30, 0))
print("Part 2:", dfs('AA', 26, 0, part2=True))  # takes over 5 min
