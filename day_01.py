import more_itertools as mit

def part_1(data):
    """
    part_1('''\
    ... 199
    ... 200
    ... 208
    ... 210
    ... 200
    ... 207
    ... 240
    ... 269
    ... 260
    ... 263''')
    7

    """
    data = [int(x) for x in data.splitlines()]
    return sum(b > a for a,b in mit.pairwise(data))

def part_2(data):
    """part_2('''\
    ... 199
    ... 200
    ... 208
    ... 210
    ... 200
    ... 207
    ... 240
    ... 269
    ... 260
    ... 263''')
    5
    """
    data = [int(x) for x in data.splitlines()]
    return sum(b > a for a,b in mit.pairwise(sum(w) for w in mit.windowed(data, 3)))
