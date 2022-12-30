import rctools as rc

input = map(rc.ints, rc.aoc_in(__file__)[0].split('\n\n'))
sums = tuple(map(sum, input))

print("Part 1:", max(sums))
print("Part 2:", sum(sorted(sums)[-3:]))
