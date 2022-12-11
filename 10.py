'''With credit to user hugues_hoppe'''
import rctools as rc

def run(s: str, x=1):
    "Process the instructions such that each yield represents a cycle"
    for line in s.splitlines():
        yield x
        if line != 'noop':
            yield x
            x += int(line.split()[1])

def part1(w=40) -> int:
    return sum(i * x for i, x in enumerate(run(input), 1) if i % w == 20)

def part2(w=40) -> list:
    "Each cycle, update a pixel based on overlap"
    G = [['?' for _ in range(w)] for _ in range(6)]
    for i, x in enumerate(run(input)):
        G[i // w][i % w] = '#' if abs(i % w - x) < 2 else ' '
    return G

input = rc.aoc_in(__file__)[1]
print("Part 1:", part1())
print("Part 2:")
p2 = part2()
for i in range(6):
    print(*p2[i])
