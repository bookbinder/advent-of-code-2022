import rctools as rc

def from_snafu(s):
    vals = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
    return sum(vals[c] * 5 ** i for i, c in enumerate(reversed(s)))

def to_snafu(num):
    total = ""
    while num:
        a = "012=-"[num % 5]
        num = num // 5 + (a in '-=')
        total = a + total
    return total

input = rc.aoc_in(__file__)[1].splitlines()
print("Part 1:", to_snafu(sum(map(from_snafu, input))))
