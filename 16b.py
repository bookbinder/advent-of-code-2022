'''from a reddit user. both parts in 3s'''
import rctools as rc
import re

lines = [re.split('[ =,;]+', x) for x in rc.aoc_in(__file__)[1].splitlines()]
adjList = {x[1]: set(x[10:]) for x in lines}
flows = {x[1]: int(x[5]) for x in lines if int(x[5]) != 0}
I = {x: 1 << i for i, x in enumerate(flows)}
T = {x: {y: 1 if y in adjList[x] else float('+inf') for y in adjList}
     for x in adjList}

for k in T:
    for i in T:
        for j in T:
            T[i][j] = min(T[i][j], T[i][k] + T[k][j])

def visit(v1, time, opened, flow, answer):
    answer[opened] = max(answer.get(opened, 0), flow)
    for v2 in flows:
        newtime = time - T[v1][v2] - 1
        if I[v2] & opened or newtime <= 0: continue
        visit(v2, newtime, opened | I[v2], flow + newtime * flows[v2], answer)
    return answer

total1 = max(visit('AA', 30, 0, 0, {}).values())
visited2 = visit('AA', 26, 0, 0, {})
total2 = max(v1 + v2 for k1, v1 in visited2.items()
                     for k2, v2 in visited2.items() if not k1 & k2)

print("Part 1:", total1)
print("Part 2:", total2)
