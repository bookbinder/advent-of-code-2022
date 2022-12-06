import rctools as rc

input = rc.aoc_in(__file__)[1].splitlines()
vals = dict(zip(rc.Lc + rc.Uc, range(1, 53)))

def common(s):
    "Return the first letter that is in both halves of the word"
    N = len(s) // 2
    return vals[next(z for z in s[:N] if z in s[N:])]

part2 = [next(z for z in input[i]
              if z in input[i + 1] and z in input[i + 2])
         for i in range(0, len(input), 3)]

print("Part 1:", sum(map(common, input)))
print("Part 2:", sum(map(vals.get, part2)))
