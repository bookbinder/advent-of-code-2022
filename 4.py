import rctools as rc
from functools import partial
from typing import Tuple

def overlap(line: Tuple[int], part2=False) -> bool:
    """Creates 2 ranges from the tuple of 4 ints and checks for overlap: total
    overlap in part 1, and at least partial overlap in part 2"""
    a = range(line[0], line[1] + 1)
    b = range(line[2], line[3] + 1)
    if part2:
        return (a[0] in b) or (b[0] in a)
    return all([z in b for z in a]) or all([z in a for z in b])

input = tuple(map(rc.ints, rc.aoc_in(__file__)[1].splitlines()))
print("Part 1:", sum(map(overlap, input)))
print("Part 2:", sum(map(partial(overlap, part2=True), input)))
