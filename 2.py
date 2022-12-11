import rctools as rc

input = rc.aoc_in(__file__)[1].splitlines()

def round_score(a, b):
    played = dict(X=1, Y=2, Z=3)
    return (3 if a + b in draw else 6 if a + b in win else 0) + played[b]

def choose(a, b):
    res = lose if b == 'X' else draw if b == 'Y' else win
    return next(z[1] for z in res if z[0] == a)

lose = ("AZ", "BX", "CY")
win  = ("AY", "BZ", "CX")
draw = ("AX", "BY", "CZ")

p1 = p2 = 0
for a, _, b in input:
    p1 += round_score(a, b)
    p2 += round_score(a, choose(a, b))

print("Part 1:", p1)
print("Part 2:", p2)
