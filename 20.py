'''from a reddit user'''
import rctools as rc

def mix(key=1, count=1):
    x = [int(x) * key for x in rc.aoc_in(__file__)[1].splitlines()]
    j = list(range(len(x)))  # new idx positions for corresponding idx in x
    for _ in range(count):
        for i in range(len(x)):
            c = j.index(i)
            j.pop(c)
            j.insert((c + x[i]) % len(j), i)
    z = j.index(x.index(0))
    return sum(x[j[(z + i) % len(j)]] for i in [1000, 2000, 3000])

print("Part 1:", mix())
print("Part 2:", mix(key=811589153, count=10))
