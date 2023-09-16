import re
from functools import reduce

*grid, _, path = open('data/22.txt')
pos, dir = grid[0].index('.') + 199j, 1
grid = {((199 - y) * 1j + x): c
        for y, l in enumerate(grid) for x, c in enumerate(l) if c in '.#'}

def transform(pos, dir, src, dest, rotor):
    broadcast_min = lambda p0, p1: complex(min(p0.real, p1.real),
                                           min(p0.imag, p1.imag))
    bottom_left = reduce(broadcast_min,
                         [rotor * p for p in [0, 1, 1j, 1 + 1j]])
    return ((pos - 50 * src) * rotor + 50 * dest + bottom_left, dir * rotor)

def itransform(pos, dir, src, dest, rotor):
    return transform(pos, dir, dest, src, 1 / rotor)

def wrap(pos, dir):
    match (pos.real % 200) // 50, (pos.imag % 250) // 50, dir:
        case 0, 2, 1j:  return transform(pos, dir, 1 + 2j, 1 + 2j, -1j)
        case 0, 2, -1:  return itransform(pos, dir, 1 + 2j, 1 + 2j, -1j)
        case 2, 2, -1j: return transform(pos, dir, 2 + 3j, 2 + 3j, -1j)
        case 2, 2, 1:   return itransform(pos, dir, 2 + 3j, 2 + 3j, -1j)
        case 1, 0, -1j: return transform(pos, dir, 1 + 1j, 1 + 1j, -1j)
        case 1, 0, 1:   return itransform(pos, dir, 1 + 1j, 1 + 1j, -1j)
        case 3, 0, -1:  return transform(pos, dir, 1j, 1 + 4j, 1j)
        case 1, 4, 1j:  return itransform(pos, dir, 1j, 1 + 4j, 1j)
        case 3, 1, -1:  return transform(pos, dir, 2j, 1 + 3j, -1)
        case 0, 3, -1:  return itransform(pos, dir, 2j, 1 + 3j, -1)
        case 2, 1, 1:   return transform(pos, dir, 2 + 2j, 3 + 3j, -1)
        case 3, 3, 1:   return itransform(pos, dir, 2 + 2j, 3 + 3j, -1)
        case 0, 4, -1j: return transform(pos, dir, 1, 3 + 4j, 1)
        case 2, 4, 1j:  return itransform(pos, dir, 1, 3 + 4j, 1)

for move in re.findall(r'\d+|[RL]', path):
    match move:
        case 'L': dir *= +1j
        case 'R': dir *= -1j
        case _:
            for _ in range(int(move)):
                p, d = pos + dir, dir
                if p not in grid: p, d = wrap(p, d)
                if grid[p] == '.': pos, dir = p, d

k = [1, -1j, -1, 1j].index(dir)
print("Part 2:", int(1000 * (199 - pos.imag + 1) + 4 * (pos.real + 1) + k))
