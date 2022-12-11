'''Functions and variables made by me for AoC 2022.'''

from typing import Tuple

# some useful variables
Lc = "abcdefghijklmnopqrstuvwxyz"
Uc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# some useful functions
def ints(s: str) -> Tuple[int]:
    "Return nums in s. (Dash before num is neg unless preceded by digit)."
    import re
    return tuple(map(int, re.findall(r'(?<!\d)-?\d+', s)))

def aoc_in(day: str) -> Tuple[str]:
    "Get number from `day` filename and return corresponding data"
    from pathlib import Path
    day = ''.join(z for z in Path(day).stem if z.isdigit())
    p1 = Path(f'data/{day}ex.txt')
    p1 = p1.read_text() if p1.exists() else ""
    p2 = Path(f'data/{day}.txt')
    p2 = p2.read_text() if p2.exists() else ""
    return p1, p2

def flatten(items):
    from typing import Iterable
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x

