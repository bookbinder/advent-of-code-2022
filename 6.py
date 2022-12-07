import rctools as rc

def start_marker(s: str, n: int) -> int:
    "Returns index of s after cirst substring of unique chars of length n"
    for i in range(len(s) - (n - 1)):
        if len(set(s[i:i + n])) == n:
            return i + n

input = rc.aoc_in(__file__)[1]
print("Part 1:", start_marker(input, 4))
print("Part 2:", start_marker(input, 14))
