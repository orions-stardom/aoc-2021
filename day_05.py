import numpy as np
from parse import parse
import itertools as it

def _parse(rawdata):
    lines = [tuple(parse("{:n},{:n} -> {:n},{:n}", line)) for line in rawdata.splitlines()]
    w = max(it.chain.from_iterable((x1,x2) for x1,_,x2,_ in lines)) +1
    h = max(it.chain.from_iterable((y1,y2) for y1,_,y2,_ in lines)) +1

    return lines,(w,h)

def part_1(lines, gridsize):
    r"""
    >>> part_1(*_parse('''\
    ... 0,9 -> 5,9
    ... 8,0 -> 0,8
    ... 9,4 -> 3,4
    ... 2,2 -> 2,1
    ... 7,0 -> 7,4
    ... 6,4 -> 2,0
    ... 0,9 -> 2,9
    ... 3,4 -> 1,4
    ... 0,0 -> 8,8
    ... 5,5 -> 8,2
    ... '''))
    5
    """
    grid = np.zeros(gridsize)
    for x1,y1,x2,y2 in lines:
        if y1 == y2:
            # horizontal
            start, end = sorted((x1,x2))
            grid[start:end+1, y1] += 1
        elif x1 == x2:
            start, end = sorted((y1,y2))
            grid[x1, start:end+1] += 1
   
    return np.count_nonzero(grid >= 2)
    
def part_2(lines, gridsize):
    r"""
    >>> part_2(*_parse('''\
    ... 0,9 -> 5,9
    ... 8,0 -> 0,8
    ... 9,4 -> 3,4
    ... 2,2 -> 2,1
    ... 7,0 -> 7,4
    ... 6,4 -> 2,0
    ... 0,9 -> 2,9
    ... 3,4 -> 1,4
    ... 0,0 -> 8,8
    ... 5,5 -> 8,2
    ... '''))
    12
    """
    grid = np.zeros(gridsize)
    for x1,y1,x2,y2 in lines:
        # Lets just be sensible about this now...
        xd, yd = np.sign(x2 - x1), np.sign(y2 - y1)  
        steps = abs(x1-x2) or abs(y1-y2) # Always equal unless one is zero

        for i in range(steps+1):
            grid[x1+i*xd, y1+i*yd] += 1

    return np.count_nonzero(grid >= 2)
