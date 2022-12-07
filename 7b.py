'''Credit to user 0xdf for the idea.'''

import rctools as rc
from collections import defaultdict

def parse_input(input):
    "Parse, manage stack, and add size to each dir in the stack"
    sizes = defaultdict(int)
    cwd = ['/']
    for line in input:
        match line.split():
            case ['$', 'cd', '/']:  cwd = ['/']
            case ['$', 'cd', '..']: cwd.pop()
            case ['$', 'cd', arg]:  cwd.append(arg)
            case ['$', 'ls']:       pass
            case ['dir', arg]:      pass
            case [a, b]:
                for i in range(len(cwd)):
                    sizes['/'.join(cwd[:i + 1])] += int(a)
    return sizes

input = rc.aoc_in(__file__)[1].splitlines()
sizes = parse_input(input)
DISK_SIZE = 70000000
SPACE_NEEDED = 30000000
current_free = DISK_SIZE - sizes['/']
to_free = SPACE_NEEDED - current_free

print("Part 1:", sum(v for v in sizes.values() if v <= 100000))
print("Part 2:", min(v for v in sizes.values() if v > to_free))
