import rctools as rc
from typing import List, Tuple

def move(crates: List[list], a: int, b: int, c: int):
    "Move one crate at a time, LIFO"
    for _ in range(a):
        crates[c].append(crates[b].pop())

def move2(crates: List[list], a: int, b: int, c: int):
    "Move a stack of crates at once"
    crates[c].extend(crates[b][-a:])
    crates[b] = crates[b][:-a]

def emulate(crates: List[list], moves: Tuple[tuple], func=move) -> str:
    "Run through `instructions` and return final element in each sublist"
    for m in moves:
        func(crates, *m)
    return ''.join(z[-1] for z in crates[1:])

def parse_input() -> Tuple[list]:
    crates, instructions = rc.aoc_in(__file__)[1].split('\n\n')
    crates = crates.splitlines()
    crates = [[]] + [[z[i] for z in crates if z[i] in rc.Uc][::-1]
                     for i in range(1, len(crates[0]), 4)]
    instructions = tuple(map(rc.ints, instructions.splitlines()))
    return crates, instructions

print("Part 1:", emulate(*parse_input()))
print("Part 2:", emulate(*parse_input(), func=move2))
