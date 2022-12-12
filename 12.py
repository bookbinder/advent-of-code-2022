import rctools as rc
from collections import deque

G = list(map(list, rc.aoc_in(__file__)[1].splitlines()))
R, C = len(G), len(G[0])
COR = [[r, c] for r in range(R) for c in range(C)]
S = next(z for z in COR if G[z[0]][z[1]] == 'S')
E = next(z for z in COR if G[z[0]][z[1]] == 'E')
G[S[0]][S[1]] = 'a'
G[E[0]][E[1]] = 'z'

def bfs(start):
    seen = {tuple(S)}
    q = deque([[start, 0]])
    while q:
        pt, steps = q.popleft()
        r, c = pt
        if pt == E:
            return steps
        for child in rc.neighbors4(pt, R, C):
            nr, nc = child
            if ord(G[nr][nc]) <= ord(G[r][c]) + 1 and child not in seen:
                seen.add(child)
                q.append((list(child), steps + 1))
    return float('inf')

starts = [z for z in COR if G[z[0]][z[1]] == 'a']
print("Part 1:", bfs(S))
print("Part 2:", min(bfs(s) for s in starts))
