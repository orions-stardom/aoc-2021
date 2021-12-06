from collections import Counter

def _parse(rawdata):
    return [int(i) for i in rawdata.split(",")]

def part_1(*nums):
    r"""
    >>> part_1(*_parse('''\
    ... 3,4,3,1,2 
    ... '''))
    5934
    """
    for _ in range(80):
        nums = [n-1 if n else 6 for n in nums] + [8]*nums.count(0)

    return len(nums)


def part_2(*nums):
    r"""
    >>> part_2(*_parse('''\
    ... 3,4,3,1,2 
    ... '''))
    26984457539
    """
    state = Counter(nums)
    for _ in range(256):
        state = sum((Counter({n-1:c} if n else {6:c,8:c}) for n,c in state.items()), Counter())

    return state.total()

