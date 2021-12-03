from collections import Counter
import itertools as it

def part_1(data):
    r"""
    >>> part_1('''\
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
    ... 01010''')
    198
    """

    data = data.splitlines()
    gamma = 0
    epsilon = 0

    for position, bits in enumerate(zip(*(num[::-1] for num in data))):
        count = Counter(bits)
       
        if count["1"] > count["0"]:
            gamma += 2**position 
        else:
            epsilon += 2**position
    
    return gamma*epsilon

def part_2(data):
    r"""
    >>> part_2('''\
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
    ... 01010''')
    230
    """
    # naive approach - just exactly as written
    oxy_candidates = data.splitlines()

    for pos in it.count():
        count = Counter(candidate[pos] for candidate in oxy_candidates)
        most_common = "1" if count["1"] >= count["0"] else "0"
        oxy_candidates = [cand for cand in oxy_candidates if cand[pos] == most_common]

        if len(oxy_candidates) == 1:
            oxy = int(oxy_candidates[0], 2)
            break


    co2_candidates = data.splitlines()
    
    for pos in it.count():
        count = Counter(candidate[pos] for candidate in co2_candidates)
        least_common = "0" if count["1"] >= count["0"] else "1"
        co2_candidates = [cand for cand in co2_candidates if cand[pos] == least_common]

        if len(co2_candidates) == 1:
            co2 = int(co2_candidates[0], 2)
            break

    return oxy * co2
