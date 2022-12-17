import rctools as rc

def dist(pta, ptb):
    "Manhattan distance between two points"
    return sum(abs(a - b) for a, b in zip(pta, ptb))

def coords_in_row(pt, dist, row):
    "Endpoints in `row` that are manhatten `dist` from `pt`"
    m = pt[0] - row
    dist = dist - abs(m)
    return [pt[1] - dist, pt[1] + dist] if dist > 0 else []

def combine_ranges(ranges):
    "Combine overlapping ranges"
    res = [ranges[0]]
    for i in range(1, len(ranges)):
        if ranges[i][0] > res[-1][1]:
            res.append(ranges[i])
        if ranges[i][0] <= res[-1][1]:
            res[-1][1] = max(ranges[i][1], res[-1][1])
    return res

def part1():
    row = 2000000
    ar = filter(None,
                [coords_in_row(s, dist(s, sensors[s]), row) for s in sensors])
    combined = combine_ranges(sorted(ar))
    existing = sum(z[0] == row for z in set(sensors.values()))
    return sum(map(lambda x: x[1] - x[0] + 1, combined)) - existing

def part2():
    for i in range(4000001):
        ar = filter(None,
                    [coords_in_row(s, dist(s, sensors[s]), i) for s in sensors])
        combined = combine_ranges(sorted(ar))
        if len(combined) > 1:
            for j in range(1, len(combined)):
                if combined[j][0] - combined[j - 1][1] == 2:
                    return 4000000 * (combined[j][0] - 1) + i

input = rc.aoc_in(__file__)[1].splitlines()
sensors = {(b, a): (d, c) for a, b, c, d in map(rc.ints, input)}

print("Part 1:", part1())
print("Part 2:", part2())  # takes 90s
