import more_itertools as mit
import math
from copy import deepcopy
import itertools as it

class SnailfishNum:
    def __init__(self, val):
        self.val = val
        self.reduce()

    def __add__(self, other):
        return SnailfishNum([deepcopy(self.val), deepcopy(other.val)])

    def __radd__(self, other):
        # Just needed to make sum() work
        if other == 0:
            return self

    def reduce(self):
        while True:
            try:
                explode_at = mit.first(c for c in self.coords if len(c) > 4)[:-1]
            except ValueError:
                pass
            else:
                l, r = self[explode_at]
                
                left_coord_index = mit.first(mit.locate(self.coords, lambda c: c[:-1] == explode_at)) - 1
                right_coord_index = mit.first(mit.rlocate(self.coords, lambda c: c[:-1] == explode_at)) + 1

                if left_coord_index >= 0:
                    self[self.coords[left_coord_index]] += l
                if right_coord_index < len(self.coords):
                    self[self.coords[right_coord_index]] += r

                self[explode_at] = 0
                continue

            try:
                split_at = mit.first(c for c in self.coords if self[c] >= 10)
            except ValueError:
                break
            else:
                val = self[split_at]
                self[split_at] = [math.floor(val/2), math.ceil(val/2)]

    @property
    def coords(self):
        def list_coords(lst):
            if not isinstance(lst, list):
                yield None
                return

            for i, item in enumerate(lst):
                yield from ((i, n) for n in list_coords(item))

        return [list(mit.collapse(c))[:-1] for c in list_coords(self.val)]# Remove the sentinal None 

    def __getitem__(self, coord):
        val = self.val
        for i in coord:
            val = val[i]

        return val

    def __setitem__(self, coord, value):
        *ns, m = coord
        val = self.val
        for n in ns:
            val = val[n]

        val[m] = value

    def __delitem__(self, coord):
        *ns, m = coord
        val = self.val
        for n in ns:
            val = val[n]

        del val[m]

    @property
    def magnitude(self):
        def mag(val):
            if isinstance(val, int):
                return val
            else:
                return 3*mag(val[0]) + 2*mag(val[1])

        return mag(self.val)


def _parse(rawdata):
    return [SnailfishNum(eval(line)) for line in rawdata.splitlines()]

def part_1(*nums):
    r"""
    >>> part_1(*_parse('''\
    ... [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    ... [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    ... [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    ... [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    ... [7,[5,[[3,8],[1,4]]]]
    ... [[2,[2,2]],[8,[8,1]]]
    ... [2,9]
    ... [1,[[[9,3],9],[[9,0],[0,7]]]]
    ... [[[5,[7,4]],7],1]
    ... [[[[4,2],2],6],[8,7]]
    ... '''))
    3488

    >>> part_1(*_parse('''\
    ... [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    ... [[[5,[2,8]],4],[5,[[9,9],0]]]
    ... [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    ... [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    ... [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    ... [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    ... [[[[5,4],[7,7]],8],[[8,3],8]]
    ... [[9,3],[[9,9],[6,[4,9]]]]
    ... [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    ... [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    ... '''))
    4140
    """
    result = sum(nums)
    return result.magnitude

def part_2(*nums):
    r"""
    >>> part_2(*_parse('''\
    ... [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    ... [[[5,[2,8]],4],[5,[[9,9],0]]]
    ... [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    ... [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    ... [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    ... [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    ... [[[[5,4],[7,7]],8],[[8,3],8]]
    ... [[9,3],[[9,9],[6,[4,9]]]]
    ... [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    ... [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    ... '''))
    3993
    """

    return max((a+b).magnitude for a,b in it.permutations(nums, r=2))
