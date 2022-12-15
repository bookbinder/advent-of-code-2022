'''from hyper-neutrino'''

import rctools as rc
from functools import cmp_to_key
from ast import literal_eval

def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a - b  # all we care about is the sign or 0
    elif isinstance(a, int):
        a = [a]
    elif isinstance(b, int):
        b = [b]

    for x, y in zip(a, b):
        if v := compare(x, y):
            return v

    return len(a) - len(b)

input = rc.aoc_in(__file__)[1].split('\n\n')
input = map(str.splitlines, input)
input = [list(map(literal_eval, subl)) for subl in input]

print("Part 1:", sum(i for i, (a, b) in enumerate(input, 1)
                     if compare(a, b) < 0))

# get input by individual lines for second part
input2 = [a for subl in input for a in subl] + [[[2]]] + [[[6]]]

# # # Two approaches:
# # not the most efficient sort algorithm: bubble sort
# changed = True
# while changed:
#     changed = False
#     for i in range(len(input2) - 1):
#         if compare(input2[i], input2[i + 1]) > 0:
#             input2[i], input2[i + 1] = input2[i + 1], input2[i]
#             changed = True
# a = input2.index([[2]]) + 1
# b = input2.index([[6]]) + 1
# print("Part 2:", a * b)

# # or use functools comparator -> key:
input2.sort(key=cmp_to_key(compare))
a = input2.index([[2]]) + 1
b = input2.index([[6]]) + 1
print("Part 2:", a * b)
