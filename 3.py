import rctools as rc

def part1(s: str) -> int:
    "Find a letter common to both halves of string s and return its value"
    N = len(s) // 2
    letter = set(s[:N]) & set(s[N:])
    return vals[letter.pop()]

def part2(a: str, b: str, c: str) -> int:
    "Find a letter common to all three strings and return its value"
    letter = set(a) & set(b) & set(c)
    return vals[letter.pop()]

input = rc.aoc_in(__file__)[1].splitlines()
vals = dict(zip(rc.Lc + rc.Uc, range(1, 53)))
print("Part 1:", sum(map(part1, input)))
print("Part 2:", sum(map(part2, input[::3], input[1::3], input[2::3])))
