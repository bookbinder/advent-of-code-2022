'''Functions and variables made by me for AoC 2022.'''

from typing import Tuple

# some useful variables
Lc = "abcdefghijklmnopqrstuvwxyz"
Uc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# some useful functions
def ints(s: str) -> Tuple[int]:
    """Return all numbers in s as a tuple of ints. A dash before a number
    indicates negative unless the dash is preceded by a number."""
    import re
    return tuple(map(int, re.findall(r'(?<!\d)-?\d+', s)))

def aoc_in(day: str) -> Tuple[str]:
    """Accepts file name `day` and converts it to just the digits in
    the stem of the filename. (4b.py == 4.py == 4) Returns tuple of two
    file strings: the first for example data (or empty string) and the
    second for the real data (or empty) for the corresponding day in
    data subdirectory."""
    from pathlib import Path
    day = ''.join(z for z in Path(day).stem if z.isdigit())
    p1 = Path(f'data/{day}ex.txt')
    p1 = p1.read_text() if p1.exists() else ""
    p2 = Path(f'data/{day}.txt')
    p2 = p2.read_text() if p2.exists() else ""
    return p1, p2
