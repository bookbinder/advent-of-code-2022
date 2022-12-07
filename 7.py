'''first attempt, not the best or most efficient'''

import rctools as rc
import itertools as it

def parse_input(input):
    "Return a nested dictionary of file and directory names/sizes"
    fs = {'/': {}}
    cwd = ['/']
    for line in input:
        match line.split():
            case ['$', 'cd', '/']:
                cwd = ['/']
                curr = fs['/']
            case ['$', 'cd', '..']:
                cwd.pop()
                curr = fs
                for dir in cwd:
                    curr = curr[dir]
            case ['$', 'cd', arg]:
                cwd.append(arg)
                curr = fs
                for dir in cwd:
                    curr = curr[dir]
            case ['$', 'ls']:
                pass
            case ['dir', arg]:
                curr[arg] = {}
            case [a, b]:
                curr[b] = int(a)
    return fs

def size_of_dir(node):
    "Total size of the given dir"
    total = 0
    def dfs(node):
        nonlocal total
        for k, v in node.items():
            if isinstance(v, int):
                total += v
            else:
                dfs(node[k])
    dfs(node)
    return total

sizes = {}
ctr = it.count(1)  # to ensure a unique name for each dir
def all_sizes(node):
    "Find all dirs and make dictionary of their sizes"
    for k, v in node.items():
        if isinstance(v, dict):
            sizes[k + str(next(ctr))] = size_of_dir(v)
            all_sizes(node[k])
    return sizes

input = rc.aoc_in(__file__)[1].splitlines()
fs = parse_input(input)
sizes = all_sizes(fs)
DISK_SIZE = 70000000
SPACE_NEEDED = 30000000
current_free = DISK_SIZE - sizes['/1']
to_free = SPACE_NEEDED - current_free
minDiff = float('inf')
for k, v in sizes.items():
    if v > to_free and v - to_free < minDiff:
        to_del = k
        minDiff = v - to_free

print("Part 1:", sum([v for k, v in sizes.items() if v <= 100000]))
print("Part 2:", sizes[to_del])
