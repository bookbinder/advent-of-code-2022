import rctools as rc
from functools import partial
from typing import Tuple

def overlap(line: Tuple[int], part2=False) -> bool:
    """Accepts a tuple of 4 ints. Determines if ranges s1-e1 and
    s2-e2 overlap. Total overlap for part1. For part2, can be partial."""
    s1, e1, s2, e2 = line
    if part2:
        return (s1 <= s2 <= e1) or (s2 <= s1 <= e2)
    return (s1 <= s2 and e1 >= e2) or (s1 >= s2 and e1 <= e2)

input = tuple(map(rc.ints, rc.aoc_in(__file__)[1].splitlines()))
print("Part 1:", sum(map(overlap, input)))
print("Part 2:", sum(map(partial(overlap, part2=True), input)))
