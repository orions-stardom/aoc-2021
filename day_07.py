def _parse(rawdata):
    return [int(x) for x in rawdata.split(",")]

def part_1(*nums):
    r"""
    >>> part_1(*_parse('''\
    ... 16,1,2,0,4,2,7,1,2,14   
    ... '''))
    37
    """
    def fuel_used(cand):
        return sum(abs(num-cand) for num in nums)
  
    # return bisect(fuel_used, 0, max(nums)) 
    return min(fuel_used(cand) for cand in range(max(nums)+1))


def part_2(*nums):
    r"""
    >>> part_2(*_parse('''\
    ... 16,1,2,0,4,2,7,1,2,14   
    ... '''))
    168
    """
    def triangular(n):
        return (n*(n+1))//2

    def fuel_used(cand):
        return sum(triangular(abs(num-cand)) for num in nums)
 
    return min(fuel_used(cand) for cand in range(max(nums)+1))
