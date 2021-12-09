import numpy as np
import itertools as it
import heapq
import math

def _parse(rawdata):
    return [np.array([[int(x) for x in line] for line in rawdata.splitlines()])]

def findneighbours(x,y,rows,cols):
    return ((xi,yi) for (xi,yi) in ((x-1, y),(x+1,y),(x,y-1),(x,y+1)) if 0 <= xi < rows and 0 <= yi < cols)

def part_1(heightmap):
    r"""
    >>> part_1(*_parse('''\
    ... 2199943210
    ... 3987894921
    ... 9856789892
    ... 8767896789
    ... 9899965678
    ... '''))
    15
    """
    
    rows,cols = heightmap.shape
    res = 0
    # breakpoint()
    for x,y in it.product(range(rows), range(cols)):
        height = heightmap[x,y]
        neighbours = [heightmap[xi,yi] for (xi,yi) in findneighbours(x,y,rows,cols)]

        if all(height < neighbour for neighbour in neighbours):
            res += height+1

    return res

def part_2(heightmap):
    r"""
    >>> part_2(*_parse('''\
    ... 2199943210
    ... 3987894921
    ... 9856789892
    ... 8767896789
    ... 9899965678
    ... '''))
    1134
    """
    
    rows,cols = heightmap.shape
    lowpoints = []
    for x,y in it.product(range(rows), range(cols)):
        height = heightmap[x,y]
        neighbours = [heightmap[xi,yi] for (xi,yi) in findneighbours(x,y,rows,cols)]

        if all(height < neighbour for neighbour in neighbours):
            lowpoints.append((x,y))

    basins = []
    
    for (x,y) in lowpoints:
        basin = [(x,y)]
        for (x,y) in basin: 
            for (x,y) in findneighbours(x,y,rows,cols):
                if heightmap[x,y] != 9 and (x,y) not in basin:
                    basin.append((x,y))
        
        basins.append(len(basin))
            
    return math.prod(heapq.nlargest(3,basins)) 
