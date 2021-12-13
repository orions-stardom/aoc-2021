from parse import parse
import more_itertools as mit

def _parse(rawdata):
    coord_lines, foldlines = mit.split_at(rawdata.splitlines(), lambda line: not line.strip())
    coord_data = [line.split(",") for line in coord_lines]
    coords = {(int(x), int(y)) for x,y in coord_data}

    folds = [parse("fold along {}={:n}", line) for line in foldlines]
    return State(coords), folds

class State:
    def __init__(self, coords):
        self.coords = coords
        self.rows = max(y for x,y in coords)
        self.cols = max(x for x,y in coords)

    @property
    def visible(self):
        return len(self.coords)

    def foldx(self, n):
       return State({(x if x < n else (2*n - x), y) for x,y in self.coords if x != n})
    
    def foldy(self, n):
        return State({(x, y if y < n else (2*n - y)) for x,y in self.coords if y != n})

    def __str__(self):
        return ("\n".join("".join("#" if (x,y) in self.coords else " " for x in range(self.cols+1)) for y in range(self.rows+1)))

def part_1(coords, folds):
    r"""
    >>> part_1(*_parse('''\
    ... 6,10
    ... 0,14
    ... 9,10
    ... 0,3
    ... 10,4
    ... 4,11
    ... 6,0
    ... 6,12
    ... 4,1
    ... 0,13
    ... 10,12
    ... 3,4
    ... 3,0
    ... 8,4
    ... 1,10
    ... 2,14
    ... 8,10
    ... 9,0
    ... 
    ... fold along y=7
    ... fold along x=5
    ... '''))
    17

    """
    axis, n = folds[0]

    if axis == "x":
        coords = coords.foldx(n)
    else:
        coords = coords.foldy(n)

    return coords.visible

def part_2(coords, folds):
    for axis, n in folds:
        if axis == "x":
            coords = coords.foldx(n)
        else:
            coords = coords.foldy(n)

    print(coords)
