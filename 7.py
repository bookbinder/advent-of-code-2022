'''With credit to user 0xdf for the idea.'''

import rctools as rc
from typing import List
from collections import defaultdict
from pathlib import Path

def parse_input(input: List[str]) -> dict:
    "Parse; update stack; add size to each dir in the cwd"
    sizes = defaultdict(int)
    cwd = Path('/')
    for line in input:
        match line.split():
            case ['$', 'cd', '/']:  cwd = Path('/')
            case ['$', 'cd', '..']: cwd = cwd.parent
            case ['$', 'cd', arg]:  cwd = cwd / arg
            case ['$', 'ls']:       pass
            case ['dir', arg]:      sizes[str(cwd / arg)] += 0
            case [a, _]:
                temp = cwd
                for d in range(len(temp.parts)):
                    sizes[str(temp)] += int(a)
                    temp = temp.parent
    return sizes

input = rc.aoc_in(__file__)[1].splitlines()
sizes = parse_input(input)
DISK_SIZE = 70E6
SPACE_NEEDED = 30E6
current_free = DISK_SIZE - sizes['/']
to_free = SPACE_NEEDED - current_free

print("Part 1:", sum(v for v in sizes.values() if v <= 100000))
print("Part 2:", min(v for v in sizes.values() if v > to_free))
