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
    seen = {}
    q = deque([[start, [start]]])
    while q:
        pt, path = q.popleft()
        r, c = pt
        if pt == E:
            return len(path) - 1
        if tuple(pt) in seen and seen[tuple(pt)] <= len(path):
            continue
        else:
            seen[tuple(pt)] = len(path)
        for child in rc.neighbors4(pt, R, C):
            nr, nc = child
            if ord(G[nr][nc]) <= ord(G[r][c]) + 1 and list(child) not in path:
                q.append((list(child), path + [list(child)]))
    return float('inf')

starts = [z for z in COR if G[z[0]][z[1]] == 'a']
print("Part 1:", bfs(S))
print("Part 2:", min(bfs(s) for s in starts))
