import more_itertools as mit

def _parse(rawdata):
    return [int(x) for x in rawdata.splitlines()]

def part_1(*nums):
    r"""
    >>> part_1(*_parse('''\
    ... 199
    ... 200
    ... 208
    ... 210
    ... 200
    ... 207
    ... 240
    ... 269
    ... 260
    ... 263'''))
    7

    """
    return sum(b > a for a,b in mit.pairwise(nums))

def part_2(*nums):
    r"""
    >>> part_2(*_parse('''\
    ... 199
    ... 200
    ... 208
    ... 210
    ... 200
    ... 207
    ... 240
    ... 269
    ... 260
    ... 263'''))
    5
    """
    return sum(b > a for a,b in mit.pairwise(sum(w) for w in mit.windowed(nums, 3)))
