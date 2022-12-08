'''The idea for this came from user 0xdf.'''

import rctools as rc
from typing import List
from collections import defaultdict

def parse_input(input: List[str]) -> dict:
    "Parse; update stack; add size to each dir in the stack"
    sizes = defaultdict(int)
    cwd = ['']
    for line in input:
        match line.split():
            case ['$', 'cd', '/']:  cwd = ['']
            case ['$', 'cd', '..']: cwd.pop()
            case ['$', 'cd', arg]:  cwd.append(arg)
            case ['$', 'ls']:       pass
            case ['dir', arg]:      pass
            case [a, _]:
                for i in range(len(cwd)):
                    dirname = '/'.join(cwd[:i + 1]) or '/'
                    sizes[dirname] += int(a)
    return sizes

input = rc.aoc_in(__file__)[1].splitlines()
sizes = parse_input(input)
DISK_SIZE = 70000000
SPACE_NEEDED = 30000000
current_free = DISK_SIZE - sizes['/']
to_free = SPACE_NEEDED - current_free

print("Part 1:", sum(v for v in sizes.values() if v <= 100000))
print("Part 2:", min(v for v in sizes.values() if v > to_free))
