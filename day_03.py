from collections import Counter
import itertools as it

def _parse(rawdata):
    return rawdata.splitlines()

def part_1(*lines):
    r"""
    >>> part_1(*_parse('''\
    ... 00100
    ... 11110
    ... 10110
    ... 10111
    ... 10101
    ... 01111
    ... 00111
    ... 11100
    ... 10000
    ... 11001
    ... 00010
    ... 01010'''))
    198
    """
    
    scale = len(lines[0])
    cutoff = len(lines) / 2
    nums = [int(line, 2) for line in lines]
    
    gamma = sum(2**i for i in range(scale) if sum((num >> i) & 1 for num in nums) >= cutoff)
    epsilon = 2**(scale)-1 - gamma
    return gamma * epsilon

def part_2(*lines):
    r"""
    >>> part_2(*_parse('''\
    ... 00100
    ... 11110
    ... 10110
    ... 10111
    ... 10101
    ... 01111
    ... 00111
    ... 11100
    ... 10000
    ... 11001
    ... 00010
    ... 01010'''))
    230
    """
    # naive approach - just exactly as written
    oxy_candidates = lines

    for pos in it.count():
        count = Counter(candidate[pos] for candidate in oxy_candidates)
        most_common = "1" if count["1"] >= count["0"] else "0"
        oxy_candidates = [cand for cand in oxy_candidates if cand[pos] == most_common]

        if len(oxy_candidates) == 1:
            oxy = int(oxy_candidates[0], 2)
            break


    co2_candidates = lines

    for pos in it.count():
        count = Counter(candidate[pos] for candidate in co2_candidates)
        least_common = "0" if count["1"] >= count["0"] else "1"
        co2_candidates = [cand for cand in co2_candidates if cand[pos] == least_common]

        if len(co2_candidates) == 1:
            co2 = int(co2_candidates[0], 2)
            break

    return oxy * co2
