import rctools as rc

input = rc.aoc_in(__file__)[1].splitlines()

# input = """\
# .....
# ..##.
# ..#..
# .....
# ..##.
# .....""".splitlines()

elves = {c + r * 1j for r in range(len(input)) for c in range(len(input[0]))
         if input[r][c] == '#'}
scanmap = {
    -1j: [-1j - 1, -1j, -1j + 1],
    1j: [1j - 1, 1j, 1j + 1],
    1: [1, 1j + 1, -1j + 1],
    -1: [-1 - 1j, -1, -1 + 1j]
}
moves = [-1j, 1j, -1, 1]
N = [-1 - 1j, -1j, 1 - 1j, 1, 1 + 1j, 1j, -1 + 1j, -1]

i = 0
changed = True
while changed:
    changed = False
    once = set()
    twice = set()

    for elf in elves:
        if all(elf + x not in elves for x in N):
            continue
        for move in moves:
            if all(elf + x not in elves for x in scanmap[move]):
                prop = elf + move
                if prop in twice:
                    pass
                elif prop in once:
                    twice.add(prop)
                else:
                    once.add(prop)
                break

    ec = set(elves)

    for elf in ec:
        if all(elf + x not in ec for x in N):
            continue
        for move in moves:
            if all(elf + x not in ec for x in scanmap[move]):
                prop = elf + move
                if prop not in twice:
                    elves.remove(elf)
                    elves.add(prop)
                    changed = True
                break

    i += 1
    moves.append(moves.pop(0))

mx = min(x.real for x in elves)
Mx = max(x.real for x in elves)
my = min(x.imag for x in elves)
My = max(x.imag for x in elves)

# print(int((Mx - mx + 1) * (My - my + 1) - len(elves)))
print(i)
