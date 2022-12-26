import rctools as rc
from operator import add, sub, mul, truediv

def parse(line):
    ops = {'+': add, '-': sub, '*': mul, '/': truediv}
    k, v = line.split(': ')
    v = v.split()
    if v[0].isnumeric():
        return k, int(v[0])
    return k, [ops[v[1]], v[0], v[2]]

def dfs(node):
    if isinstance(m[node], int):
        return m[node]
    return m[node][0](dfs(m[node][1]), dfs(m[node][2]))

def part2():
    "Binary search for right value of m['humn']"
    hi = int(1e15)
    lo = int(-1e15)
    while lo < hi:
        mid = m['humn'] = (lo + hi) // 2
        if dfs(m['root'][1]) - dfs(m['root'][2]) > 0:
            lo = mid + 1
        else:
            hi = mid
    return lo

input = rc.aoc_in(__file__)[1].splitlines()
m = dict(map(parse, input))
print("Part 1:", int(dfs('root')))
print("Part 2:", part2())
