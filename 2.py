import rctools as rc

input = rc.aoc_in(__file__)[1].splitlines()

def score(line): return res[line] + played[line[2]]
def part2(line): return score(f"{line[0]} {to_play[line]}")

res = {"A Z": 0, "B X": 0, "C Y": 0,
       "A Y": 6, "B Z": 6, "C X": 6,
       "A X": 3, "B Y": 3, "C Z": 3}
played = {"X": 1, "Y": 2, "Z": 3}
to_play = {"A Z": 'Y', "B X": 'X', "C Y": 'Z',
           "A Y": 'X', "B Z": 'Z', "C X": 'Y',
           "A X": 'Z', "B Y": 'Y', "C Z": 'X'}

print("Part 1:", sum(map(score, input)))
print("Part 2:", sum(map(part2, input)))
