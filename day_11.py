import numpy as np
from numpy import ma

import itertools as it

def _parse(rawdata):
    return [ma.array(np.fromiter(rawdata.replace("\n", "", 100), dtype=int).reshape((10,10)))]


def part_1(initialstate):
    r"""
    >>> part_1(*_parse('''\
    ... 5483143223
    ... 2745854711
    ... 5264556173
    ... 6141336146
    ... 6357385478
    ... 4167524645
    ... 2176841721
    ... 6882881134
    ... 4846848554
    ... 5283751526
    ... '''))
    1656
    """

    state = initialstate.copy()
    rows, cols = state.shape 
    
    def step():
        nonlocal state
        state += 1
        
        while len(ready_to_flash := (np.argwhere(state > 9))):
            for octopus in ready_to_flash:
                x,y = octopus
                neighbours = [(xi,yi) for (xi,yi) in ((x-1,y-1),(x-1,y),(x-1,y+1),(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1) )
                              if 0 <= xi < rows and 0 <= yi < cols]

                for neighbour in neighbours:
                    # Could do this in one go if fancy indexing wasnt updating the whole array for no reason..
                    state[neighbour] += 1
                
                state[x,y] = 0
                state.mask[x,y] = True # no more flashing this step


        flashes = np.count_nonzero(state.mask)
        state.mask = False
        return flashes

    return sum(step() for _ in range(100))


def part_2(initialstate):
    r"""
    >>> part_2(*_parse('''\
    ... 5483143223
    ... 2745854711
    ... 5264556173
    ... 6141336146
    ... 6357385478
    ... 4167524645
    ... 2176841721
    ... 6882881134
    ... 4846848554
    ... 5283751526
    ... '''))
    195
    """

    state = initialstate.copy()
    rows, cols = state.shape 
    
    def step():
        nonlocal state
        state += 1
        
        while len(ready_to_flash := (np.argwhere(state > 9))):
            for octopus in ready_to_flash:
                x,y = octopus
                neighbours = [(xi,yi) for (xi,yi) in ((x-1,y-1),(x-1,y),(x-1,y+1),(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1) )
                              if 0 <= xi < rows and 0 <= yi < cols]

                for neighbour in neighbours:
                    # Could do this in one go if fancy indexing wasnt updating the whole array for no reason..
                    state[neighbour] += 1
                
                state[x,y] = 0
                state.mask[x,y] = True # no more flashing this step


        flashes = np.count_nonzero(state.mask)
        state.mask = False

    for stepn in it.count(1):
        step()
        if np.all(state == 0):
            return stepn
