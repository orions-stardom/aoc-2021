import numpy as np
import itertools as it
from collections import Counter
from pathlib import Path

rotation_matrices = [np.array([[int(c) for c in l.split()] for l in m.splitlines()]) for m in Path("rotation-matrices.txt").read_text().split("\n\n")]

class NoCalibration(ValueError):
    pass

class Scanner:
    def __init__(self, beacons):
        self.beacons = beacons
        self.location = None

    @property
    def rotations(self):
        for matrix in rotation_matrices:
            yield Scanner((matrix@self.beacons.T).T)

    def calibrate_to(self, other):
        # assume we overlap completely and go through each possible map of corresponding beacons. 
        # If we find at least 12 corresponding pairs are the same distance away from each other,
        # then that must be the true offset
        for order in it.permutations(range(len(self.beacons))):
            mode, freq = Counter(map(tuple, other.beacons - self.beacons[order, :])).most_common()[0]
            if freq >= 12:
                offset = mode
                break
        else:
            raise NoCalibration

        self.location = other.location + offset
        self.beacons += self.location

    @property
    def beaconset(self):
        return {tuple(b) for b in self.beacons}
    
def _parse(rawdata):
    scanners = []
    for scannerinfo in rawdata.split("\n\n"):
        beaconinfo = scannerinfo.splitlines()[1:]
        beacons = np.array([[int(n) for n in b.split(",")] for b in beaconinfo])
        scanners.append(Scanner(beacons))

    return scanners

def part_1(*scanners):
    r"""
    >>> part_1(*_parse('''\
    ... --- scanner 0 ---
    ... 404,-588,-901
    ... 528,-643,409
    ... -838,591,734
    ... 390,-675,-793
    ... -537,-823,-458
    ... -485,-357,347
    ... -345,-311,381
    ... -661,-816,-575
    ... -876,649,763
    ... -618,-824,-621
    ... 553,345,-567
    ... 474,580,667
    ... -447,-329,318
    ... -584,868,-557
    ... 544,-627,-890
    ... 564,392,-477
    ... 455,729,728
    ... -892,524,684
    ... -689,845,-530
    ... 423,-701,434
    ... 7,-33,-71
    ... 630,319,-379
    ... 443,580,662
    ... -789,900,-551
    ... 459,-707,401
    ... 
    ... --- scanner 1 ---
    ... 686,422,578
    ... 605,423,415
    ... 515,917,-361
    ... -336,658,858
    ... 95,138,22
    ... -476,619,847
    ... -340,-569,-846
    ... 567,-361,727
    ... -460,603,-452
    ... 669,-402,600
    ... 729,430,532
    ... -500,-761,534
    ... -322,571,750
    ... -466,-666,-811
    ... -429,-592,574
    ... -355,545,-477
    ... 703,-491,-529
    ... -328,-685,520
    ... 413,935,-424
    ... -391,539,-444
    ... 586,-435,557
    ... -364,-763,-893
    ... 807,-499,-711
    ... 755,-354,-619
    ... 553,889,-390
    ... 
    ... --- scanner 2 ---
    ... 649,640,665
    ... 682,-795,504
    ... -784,533,-524
    ... -644,584,-595
    ... -588,-843,648
    ... -30,6,44
    ... -674,560,763
    ... 500,723,-460
    ... 609,671,-379
    ... -555,-800,653
    ... -675,-892,-343
    ... 697,-426,-610
    ... 578,704,681
    ... 493,664,-388
    ... -671,-858,530
    ... -667,343,800
    ... 571,-461,-707
    ... -138,-166,112
    ... -889,563,-600
    ... 646,-828,498
    ... 640,759,510
    ... -630,509,768
    ... -681,-892,-333
    ... 673,-379,-804
    ... -742,-814,-386
    ... 577,-820,562
    ... 
    ... --- scanner 3 ---
    ... -589,542,597
    ... 605,-692,669
    ... -500,565,-823
    ... -660,373,557
    ... -458,-679,-417
    ... -488,449,543
    ... -626,468,-788
    ... 338,-750,-386
    ... 528,-832,-391
    ... 562,-778,733
    ... -938,-730,414
    ... 543,643,-506
    ... -524,371,-870
    ... 407,773,750
    ... -104,29,83
    ... 378,-903,-323
    ... -778,-728,485
    ... 426,699,580
    ... -438,-605,-362
    ... -469,-447,-387
    ... 509,732,623
    ... 647,635,-688
    ... -868,-804,481
    ... 614,-800,639
    ... 595,780,-596
    ... 
    ... --- scanner 4 ---
    ... 727,592,562
    ... -293,-554,779
    ... 441,611,-461
    ... -714,465,-776
    ... -743,427,-804
    ... -660,-479,-426
    ... 832,-632,460
    ... 927,-485,-438
    ... 408,393,-506
    ... 466,436,-512
    ... 110,16,151
    ... -258,-428,682
    ... -393,719,612
    ... -211,-452,876
    ... 808,-476,-593
    ... -575,615,604
    ... -485,667,467
    ... -680,325,-822
    ... -627,-443,-432
    ... 872,-547,-609
    ... 833,512,582
    ... 807,604,487
    ... 839,-516,451
    ... 891,-625,532
    ... -652,-548,-490
    ... 30,-46,-14
    ... '''))
    79
    """
    solved, unsolved = [scanners[0]], scanners[1:]

    while unsolved:
        for s, u in it.product(solved,unsolved):
            for ur in u.rotations:
                try:
                    ur.calibrate_to(s)
                except NoCalibration:
                    continue 
                else:
                    solved.append(ur)
                    unsolved.remove(u)
                    break
            else:
                # This rotation didnt calibrate
                continue
            break

    return len(set.union(s.beaconset for s in solved))
