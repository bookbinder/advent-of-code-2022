'''With credit to user wooledge/greg'''
import rctools as rc

def run(n: int) -> int:
    "Run through the instructions with `n` number of knots"

    def move(hi: int, ti: int, dir=None):
        "Update knots[hi] and knots[ti]"
        hr, hc = knots[hi]
        tr, tc = knots[ti]

        # move head if dir is given
        hr += 1 if dir == 'D' else -1 if dir == 'U' else 0
        hc += 1 if dir == 'R' else -1 if dir == 'L' else 0

        # move tail if necessary
        if abs(tr - hr) <= 1 and abs(tc - hc) <= 1:
            pass
        elif hr == tr:
            tc += 1 if hc - tc > 1 else -1 if tc - hc > 1 else 0
        elif hc == tc:
            tr += 1 if hr - tr > 1 else -1 if tr - hr > 1 else 0
        elif abs(hr - tr) > 1 or abs(hc - tc) > 1:
            tr += 1 if hr - tr >= 1 else -1
            tc += 1 if hc - tc >= 1 else -1

        # update knots and remember position of tail
        knots[hi] = [hr, hc]
        knots[ti] = [tr, tc]
        seen.add(tuple(knots[-1]))

    seen = set()
    knots = [(0, 0) for _ in range(n)]
    for line in input:
        dir, amt = line.split()
        for i in range(int(amt)):
            move(0, 1, dir)
            for j in range(1, len(knots) - 1):
                move(j, j + 1)
    return len(seen)

input = rc.aoc_in(__file__)[1].splitlines()
print("Part 1:", run(2))
print("Part 2:", run(10))
