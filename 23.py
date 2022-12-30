import rctools as rc

input = rc.aoc_in(__file__)[0].splitlines()

# input = """\
# .....
# ..##.
# ..#..
# .....
# ..##.
# .....""".splitlines()

elves = [[r, c, r, c] for r in range(len(input)) for c in range(len(input[0]))
          if input[r][c] == '#']

def all_neighbors(i):
    r, c, *_ = elves[i]
    for er, ec, *_ in [z for j, z in enumerate(elves) if j != i]:
        if er - 1 <= r <= er + 1 and ec - 1 <= c <= ec + 1:
            return True
    return False

def n_neighbors(i):
    r, c, *_ = elves[i]
    for e in [z for j, z in enumerate(elves) if j != i]:
        if e[0] == r - 1 and e[1] - 1 <= c <= e[1] + 1:
            return True
    return False

def s_neighbors(i):
    r, c, *_ = elves[i]
    for e in [z for j, z in enumerate(elves) if j != i]:
        if e[0] == r + 1 and e[1] - 1 <= c <= e[1] + 1:
            return True
    return False

def w_neighbors(i):
    r, c, *_ = elves[i]
    for e in [z for j, z in enumerate(elves) if j != i]:
        if e[1] == c - 1 and e[0] - 1 <= r <= e[0] + 1:
            return True
    return False

def e_neighbors(i):
    r, c, *_ = elves[i]
    for e in [z for j, z in enumerate(elves) if j != i]:
        if e[1] == c + 1 and e[0] - 1 <= r <= e[0] + 1:
            return True
    return False


def rounds(n=10):
    for _ in range(n):
        turn = n % 4
        dirs = [(n_neighbors, -1, 0), (s_neighbors, 1, 0),
                (w_neighbors, 0, -1), (e_neighbors, 0, 1)]
        dirs = dirs[turn:] + dirs[:turn]

        # part 1 of the round
        for i, elf in enumerate(elves):
            if not all_neighbors(i):
                elves[i][2] = elves[i][0]
                elves[i][3] = elves[i][1]
                continue
            for dir in dirs:
                if not dir[0](i):
                    elves[i][2] = elves[i][0] + dir[1]
                    elves[i][3] = elves[i][1] + dir[2]
                    break

        # part 2 of the round
        for i, elf in enumerate(elves):
            for j, e in enumerate(elves):
                if i == j:
                    continue
                if elves[i][2] == elves[j][2] and elves[i][3] == elves[j][3]:
                    elves[i][2] = elves[i][0]
                    elves[i][3] = elves[i][1]
                    elves[j][2] = elves[j][0]
                    elves[j][3] = elves[j][1]

        for i, elf in enumerate(elves):
            elves[i][0] = elves[i][2]
            elves[i][1] = elves[i][3]
    return elves

pt1 = rounds(10)
minr = min(z[0] for z in elves)
maxr = max(z[0] for z in elves)
minc = min(z[1] for z in elves)
maxc = max(z[1] for z in elves)
print("Part 1:", (maxr - minr) * (maxc - minc) - len(elves))
