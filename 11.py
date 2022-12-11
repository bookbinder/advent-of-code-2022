import rctools as rc
from operator import add, mul
from math import prod
from collections import deque

class Monkey:
    def __init__(self, id, items, op, test):
        self.id = id
        self.items = deque(items)
        self.op = op
        self.test = test

def run(part2=False):
    def parse(monkey):
        lines = monkey.splitlines()
        id = rc.ints(lines[0])[0]
        items = rc.ints(lines[1])
        op = lines[2].split()[-2:]
        test = rc.ints(' '.join(lines[3:]))
        return Monkey(id, items, op, test)

    def turn(m):
        func = {"+": add, "*": mul}[m.op[0]]
        while m.items:
            counts[m.id] += 1
            item = m.items.popleft()
            val = item if m.op[1] == 'old' else int(m.op[1])
            if part2:
                item = func(item, val) % prod(z.test[0] for z in monkeys)
            else:
                item = func(item, val) // 3
            if item % m.test[0] == 0:
                monkeys[m.test[1]].items.append(item)
            else:
                monkeys[m.test[2]].items.append(item)

    input = rc.aoc_in(__file__)[1].split('\n\n')
    monkeys = list(map(parse, input))
    counts = {m.id: 0 for m in monkeys}

    for _ in range(10000 if part2 else 20):
        for m in monkeys:
            turn(m)
    return prod(sorted(counts.values())[-2:])

print("Part 1:", run())
print("Part 2:", run(part2=True))
