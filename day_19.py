import numpy as np
import itertools as it

class NoCalibration(ValueError):
    pass

class Scanner:
    def __init__(self, beacons):
        self.beacons = beacons
        self.location = None

    @property
    def rotations(self):
        for matrix in rotation_matrices:
            yield Scanner(matrix@self.beacons)

    def calibrate_to(self, other):
        # find overlapping beacons
        # not sure how there's only one offset with at least 12 overlaps
        # but I guess there must be somehow?
        possible_offsets = ...
        for offset in possible_offsets:
            overlap = ...
            if len(overlap) >= 12:
                break
        else:
            raise NoCalibration

        self.location = other.location + offset
        self.beacons += self.location

    @property
    def beaconset(self):
        return {tuple(b) for b in self.beacons.T}
    
def _parse(rawdata):
    scanners = []
    for scannerinfo in rawdata.split("\n\n"):
        beaconinfo = scannerinfo.splitlines()[1:]
        beacons = np.array([[int(n) for n in b.split(",")] for b in beaconinfo])
        scanners.append(Scanner(beacons.T))

    return scanners

def part_1(*scanners):
    r"""
    >>> part_1(*_parse('''\
    ... --- scanner 0 ---
    ... -1,-1,1
    ... -2,-2,2
    ... -3,-3,3
    ... -2,-3,1
    ... 5,6,-4
    ... 8,0,7
    ... 
    ... --- scanner 0 ---
    ... 1,-1,1
    ... 2,-2,2
    ... 3,-3,3
    ... 2,-1,3
    ... -5,4,-6
    ... -8,-7,0
    ... 
    ... --- scanner 0 ---
    ... -1,-1,-1
    ... -2,-2,-2
    ... -3,-3,-3
    ... -1,-3,-2
    ... 4,6,5
    ... -7,0,8
    ... 
    ... --- scanner 0 ---
    ... 1,1,-1
    ... 2,2,-2
    ... 3,3,-3
    ... 1,3,-2
    ... -4,-6,5
    ... 7,0,8
    ... 
    ... --- scanner 0 ---
    ... 1,1,1
    ... 2,2,2
    ... 3,3,3
    ... 3,1,2
    ... -6,-4,-5
    ... 0,7,-8 
    ... '''))
    79
    """
    solved, unsolved = [scanners[0]], scanners[1:]

    while unsolved:
        for s, u in it.product(solved,unsolved):
            for ur in u.rotations:
                try:
                    ur.calibate(s)
                except NoCalibration:
                    continue 
                else:
                    solved.append(u)
                    unsolved.remove(u)
                    break
            else:
                # This rotation didnt calibrate
                continue
            break

    return len(set.union(s.beaconset for s in solved))
