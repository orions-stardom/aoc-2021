from parse import parse
import itertools as it

def _parse(rawdata):
    return parse("target area: x={:n}..{:n}, y={:n}..{:n}", rawdata)

def part_1(xmin,xmax,ymin,ymax):
    r"""
    >>> part_1(*_parse("target area: x=20..30, y=-10..-5"))
    45
    """
    y = abs(ymin)
    return (y * (y-1))//2

def sign(x):
    return 0 if x == 0 else 1 if x > 0 else -1

def part_2(xmin,xmax,ymin,ymax):
    r"""
    >>> part_2(*_parse("target area: x=20..30, y=-10..-5"))
    112
    """
    # I really cant work out how to do this properly so just brute force with
    # ridiculous bounds
    def works(dx,dy):
        x, y = 0,0
        for _ in range(300):
            if xmin <= x <= xmax and ymin <= y <= ymax:
                return True

            # if dx == 0 and not xmin <= x <= xmax:
            #     return False

            # if y < ymin and dy < 0:
            #     return False

            x,y,dx,dy = (x+dx, 
                         y+dy,
                         dx-sign(dx),
                         dy - 1)

        return False

    return sum(works(dx,dy) for dx,dy in it.product(range(-1000, 1000), range(-1000, 1000)))
