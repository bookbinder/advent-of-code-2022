import rctools as rc
from operator import add, sub, mul, truediv, gt, lt

def parse(line):
    ops = {'+': add, '-': sub, '*': mul, '/': truediv}
    k, v = line.split(': ')
    v = v.split()
    if v[0].isnumeric():
        return k, int(v[0])
    return k, [ops[v[1]], v[0], v[2]]

def dfs(node):
    match m[node]:
        case [op, a, b]: return op(dfs(a), dfs(b))
        case num: return num

def part2():
    "Binary search for correct value of m['humn']"
    op = gt if dfs(m['root'][1]) - dfs(m['root'][2]) > 0 else lt
    hi = int(1e15)
    lo = int(-1e15)
    while lo < hi:
        mid = m['humn'] = (lo + hi) // 2
        if op(dfs(m['root'][1]), dfs(m['root'][2])):
            lo = mid + 1
        else:
            hi = mid
    return lo

input = rc.aoc_in(__file__)[1].splitlines()
m = dict(map(parse, input))
print("Part 1:", int(dfs('root')))
print("Part 2:", part2())
