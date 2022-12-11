'''With credit to user hugues_hoppe'''
import textwrap
import advent_of_code_ocr
import rctools as rc

def run(s: str, x=1):
    "Process the instructions, doing two yields for each non-noop"
    for line in s.splitlines():
        yield x
        if line != 'noop':
            yield x
            x += int(line.split()[1])

def part1(w: int) -> int:
    return sum(i * x for i, x in enumerate(run(input), 1) if i % w == 20)

def part2(w: int) -> str:
    t = ''.join('.#'[abs(i % w - x) < 2]
                for i, x in enumerate(run(input)))
    t = '\n'.join(textwrap.wrap(t, width=w))
    return advent_of_code_ocr.convert_6(t)

input = rc.aoc_in(__file__)[1]
print("Part 1:", part1(40))
print("Part 2:", part2(40))
