from collections import defaultdict

def _parse(rawdata):
    graph = defaultdict(list)
    for line in rawdata.splitlines():
        l, r = line.split("-")
        graph[l].append(r)
        graph[r].append(l)

    return [graph]


def part_1(graph):
    r"""
    >>> part_1(*_parse('''\
    ... start-A
    ... start-b
    ... A-c
    ... A-b
    ... b-d
    ... A-end
    ... b-end
    ... '''))
    10

    >>> part_1(*_parse('''\
    ... dc-end
    ... HN-start
    ... start-kj
    ... dc-start
    ... dc-HN
    ... LN-dc
    ... HN-end
    ... kj-sa
    ... kj-HN
    ... kj-dc
    ... '''))
    19

    >>> part_1(*_parse('''\
    ... fs-end
    ... he-DX
    ... fs-he
    ... start-DX
    ... pj-DX
    ... end-zg
    ... zg-sl
    ... zg-pj
    ... pj-he
    ... RW-he
    ... fs-DX
    ... pj-RW
    ... zg-RW
    ... start-pj
    ... he-WI
    ... zg-he
    ... pj-fs
    ... start-RW
    ... '''))
    226
    """

    search = [["start",]]
    total = 0

    for path in search:
        here = path[-1]

        for next_ in graph[here]:
            if next_.islower() and next_ in path:
                continue
            elif next_ == "end":
                total += 1
            else:
                search.append(path+[next_,])

    return total


def part_2(graph):
    r"""
    >>> part_2(*_parse('''\
    ... start-A
    ... start-b
    ... A-c
    ... A-b
    ... b-d
    ... A-end
    ... b-end
    ... '''))
    36

    >>> part_2(*_parse('''\
    ... dc-end
    ... HN-start
    ... start-kj
    ... dc-start
    ... dc-HN
    ... LN-dc
    ... HN-end
    ... kj-sa
    ... kj-HN
    ... kj-dc
    ... '''))
    103

    >>> part_2(*_parse('''\
    ... fs-end
    ... he-DX
    ... fs-he
    ... start-DX
    ... pj-DX
    ... end-zg
    ... zg-sl
    ... zg-pj
    ... pj-he
    ... RW-he
    ... fs-DX
    ... pj-RW
    ... zg-RW
    ... start-pj
    ... he-WI
    ... zg-he
    ... pj-fs
    ... start-RW
    ... '''))
    3509
    """

    search = [(["start",], False)]
    total = 0

    for path, small_cave_twice in search:
        here = path[-1]

        if here == "end":
            total += 1
            continue

        for next_ in graph[here]:
            if next_ == "start":
                continue

            if next_.islower() and next_ in path:
                if small_cave_twice:
                    continue
                
                search.append((path+[next_], True)) 
            else:
                search.append((path+[next_], small_cave_twice))
    
    return total
