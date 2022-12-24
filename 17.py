'''assisted by hyper-neutrino
Right answer for test data part 2, but wrong for real data'''
import rctools as rc
import itertools as it
from tqdm import tqdm

def emulate(part2=False):
    "Generator yielding height or state after each piece settles"
    solid = set(range(7))  # ground starts at 0 in imaginary numbers
    rockidx, rock = newrock(0)
    for jetidx, jet in jets:  # a perpetual cycle
        moved = {z + jet for z in rock}  # move right/left
        if all(0 <= z.real < 7 for z in moved) and not (moved & solid):
            rock = moved
        moved = {z - 1j for z in rock}  # move down
        if moved & solid:
            solid |= rock
            height = int(max(int(z.imag) for z in solid))
            if not part2:
                yield height
            else:
                yield frozenset(signature(solid)), height, jetidx, rockidx
            rockidx, rock = newrock(height)
        else:
            rock = moved

def newrock(height):
    "Starting coordinates of next rock given height of solid structure"
    rockidx, rock = next(rocks)
    return rockidx, {z + 2 + (height + 4) * 1j for z in rock}

def find_cycle():
    "Detects cycle and returns starting/ending rock and height"
    memo = {}
    period = emulate(part2=True)
    for rocknum in tqdm(it.count()):
        solid, height, jetidx, rockidx = next(period)
        if (solid, jetidx, rockidx) in memo:
            print(f"{rocknum-rockidx=}, {height=}, {jetidx=}, {rockidx=}")
            return *memo[(solid, jetidx, rockidx)], rocknum, height
        memo[(solid, jetidx, rockidx)] = rocknum, height

def signature(solid):
    "Only cache as many rows as the lowest a piece can go"
    res = []
    for i in range(7):
        res.append(max(int(z.imag) for z in solid if z.real == i))
    minRow = min(res)
    ans = [z - (minRow * 1j) for z in solid]
    return {z for z in ans if z.imag >= 0}

def trim(solid, n=30):
    maxY = max(int(z.imag) for z in solid)
    return {z - (maxY * 1j) + (n * 1j) for z in solid if z.imag > maxY - n}

input = rc.aoc_in(__file__)[1].strip()
jets = it.cycle(enumerate(1 if z == ">" else -1 for z in input))
rocks = it.cycle(enumerate((
    (0, 1, 2, 3),
    (1, 1j, 1 + 1j, 2 + 1j, 1 + 2j),
    (0, 1, 2, 2 + 1j, 2 + 2j),
    (0, 1j, 2j, 3j),
    (0, 1, 1j, 1 + 1j)
)))
simulation = emulate()
# print("Part 1:", next(it.islice(simulation, 2021, None)))
# print("Part 2:", next(it.islice(find_cycle, 2021, None)))

target = 1000000000000
# target = 2022
rock_a, height_a, rock_b, height_b = find_cycle()
print(f"{rock_a=}", f"{height_a=}", f"{rock_b=}", f"{height_b=}")
allCycles, rem = divmod(target - rock_a, rock_b - rock_a)
heightAllCycles = allCycles * (height_b - height_a)
heightRemainder = next(it.islice(simulation, rock_a + rem, None)) - height_a
print(heightAllCycles + height_a + heightRemainder)
